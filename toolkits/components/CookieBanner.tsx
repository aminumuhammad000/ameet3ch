'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { ShieldCheck, Cookie, X, Sliders, Check } from 'lucide-react';

const STORAGE_KEY = 'amee_cookie_consent';

export default function CookieBanner() {
  const [showBanner, setShowBanner] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [analyticsEnabled, setAnalyticsEnabled] = useState(false);
  const [functionalEnabled, setFunctionalEnabled] = useState(true);

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (!stored) {
        setShowBanner(true);
      } else {
        const parsed = JSON.parse(stored);
        setAnalyticsEnabled(Boolean(parsed.analytics));
        setFunctionalEnabled(Boolean(parsed.functional));
      }
    } catch {
      // ignore
    }

    const handleOpenSettings = () => {
      setShowModal(true);
    };

    window.addEventListener('openAmeeCookieSettings', handleOpenSettings);
    return () => {
      window.removeEventListener('openAmeeCookieSettings', handleOpenSettings);
    };
  }, []);

  const savePreferences = (analytics: boolean, functional: boolean) => {
    try {
      const payload = {
        necessary: true,
        analytics,
        functional,
        timestamp: Date.now(),
        version: '1.0',
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
      setAnalyticsEnabled(analytics);
      setFunctionalEnabled(functional);
      setShowBanner(false);
      setShowModal(false);

      // Notify gtag if present
      if (typeof window !== 'undefined' && (window as any).gtag) {
        (window as any).gtag('consent', 'update', {
          analytics_storage: analytics ? 'granted' : 'denied',
        });
      }
    } catch {
      // ignore
    }
  };

  return (
    <>
      {/* Floating Cookie Consent Banner */}
      {showBanner && !showModal && (
        <aside
          role="dialog"
          aria-label="Cookie consent banner"
          className="fixed bottom-4 left-4 right-4 sm:left-auto sm:right-6 sm:max-w-xl z-50 bg-slate-900/95 backdrop-blur-md text-white border border-slate-800 rounded-2xl p-4 sm:p-5 shadow-2xl space-y-3.5 animate-in fade-in slide-in-from-bottom-4 duration-300"
        >
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-xl bg-purple-900/50 text-purple-400 border border-purple-700/50 shrink-0 mt-0.5">
              <Cookie className="w-5 h-5" />
            </div>
            <div className="space-y-1">
              <h2 className="text-sm font-bold text-white flex items-center gap-1.5">
                <span>We Value Your Privacy</span>
              </h2>
              <p className="text-xs text-slate-300 leading-relaxed">
                We use cookies and client browser storage to secure our services, preserve your draft documents locally, and analyze traffic under the <strong>Nigeria Data Protection Act (NDPA 2023)</strong>.
              </p>
              <div className="flex items-center gap-2 pt-0.5 text-xs">
                <Link href="/privacy" className="text-purple-400 hover:text-purple-300 underline font-medium">
                  Privacy Policy
                </Link>
                <span className="text-slate-600">&middot;</span>
                <Link href="/cookies" className="text-purple-400 hover:text-purple-300 underline font-medium">
                  Cookie Policy
                </Link>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 pt-1 sm:justify-end">
            <button
              type="button"
              onClick={() => savePreferences(true, true)}
              className="px-3.5 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold transition"
            >
              Accept All
            </button>
            <button
              type="button"
              onClick={() => savePreferences(false, true)}
              className="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition"
            >
              Reject Non-Essential
            </button>
            <button
              type="button"
              onClick={() => setShowModal(true)}
              className="px-2.5 py-1.5 text-xs text-slate-400 hover:text-white transition font-medium"
            >
              Preferences
            </button>
          </div>
        </aside>
      )}

      {/* Preferences Modal */}
      {showModal && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200"
        >
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 space-y-5 text-slate-800">
            <div className="flex items-start justify-between border-b border-slate-100 pb-3">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Cookie &amp; Storage Preferences
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Manage how Ameetech Toolkits handles cookies on your browser.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setShowModal(false)}
                className="text-slate-400 hover:text-slate-600 p-1 rounded-lg"
                aria-label="Close"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Necessary */}
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-900">Strictly Necessary</span>
                <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-purple-100 text-purple-700">
                  Always Active
                </span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Required for site security, CSRF protection, and remembering your consent state. Cannot be deactivated.
              </p>
            </div>

            {/* Analytics */}
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-900">Analytics &amp; Performance</span>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={analyticsEnabled}
                    onChange={(e) => setAnalyticsEnabled(e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-9 h-5 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-purple-600"></div>
                </label>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Aggregated, anonymous usage metrics to help us understand which tools are popular and fix loading bottlenecks.
              </p>
            </div>

            {/* Functional */}
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-900">Local Browser Storage</span>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={functionalEnabled}
                    onChange={(e) => setFunctionalEnabled(e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-9 h-5 bg-slate-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-purple-600"></div>
                </label>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Stores your unfinished draft invoices and receipts locally on this device so you don&apos;t lose work if you refresh the browser.
              </p>
            </div>

            <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
              <button
                type="button"
                onClick={() => savePreferences(false, false)}
                className="px-3 py-1.5 rounded-lg border border-slate-300 hover:bg-slate-100 text-slate-700 text-xs font-semibold transition"
              >
                Reject Non-Essential
              </button>
              <button
                type="button"
                onClick={() => savePreferences(analyticsEnabled, functionalEnabled)}
                className="px-4 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-700 text-white text-xs font-semibold transition"
              >
                Save Preferences
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
