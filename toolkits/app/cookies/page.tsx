import React from 'react';
import { Metadata } from 'next';
import Link from 'next/link';
import { Cookie, ArrowLeft, ShieldCheck, Database, Sliders, ExternalLink } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Cookie Policy & Storage Disclosures',
  description:
    'Detailed disclosure of cookies, local storage, and telemetry used across Ameetech Toolkits in compliance with NDPA 2023 and GDPR.',
};

export default function CookiePolicyPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-10">
      <div className="space-y-3">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-purple-700 hover:text-purple-900 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Home</span>
        </Link>
        <div className="flex flex-wrap items-center gap-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            <span>NDPA 2023 Aligned</span>
          </div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-purple-50 text-purple-700 border border-purple-200">
            <Cookie className="w-3.5 h-3.5 text-purple-600" />
            <span>Consent Mode v2</span>
          </div>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Cookie Policy &amp; Storage Disclosures
        </h1>
        <p className="text-sm text-slate-500">
          Last Updated: October 30, 2026 &middot; Ameetech Toolkits (Amee Technology Ltd)
        </p>
      </div>

      <div className="bg-white rounded-2xl p-6 sm:p-10 border border-slate-200 shadow-sm space-y-8 text-sm text-slate-700 leading-relaxed">
        <div className="p-4 rounded-xl bg-purple-50 border border-purple-200/80 flex items-start gap-3">
          <Sliders className="w-5 h-5 text-purple-700 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <h2 className="font-bold text-purple-900 text-sm">
              Your Privacy, Your Control
            </h2>
            <p className="text-xs text-purple-900/90 leading-relaxed">
              We believe in total transparency. Ameetech Toolkits uses minimal, privacy-preserving browser storage. We do not track your financial figures, customer names, or line items.
            </p>
          </div>
        </div>

        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">1. What Are Cookies and Local Storage?</h2>
          <p>
            Cookies are small text files stored on your browser to facilitate navigation and remember preferences. HTML5 Local Storage allows web applications to temporarily preserve data on your device locally without sending it to our servers.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">2. Cookies &amp; Storage Used on Toolkits</h2>
          <div className="overflow-x-auto border border-slate-200 rounded-xl">
            <table className="min-w-full text-xs text-left text-slate-600">
              <thead className="bg-slate-50 text-slate-900 font-semibold border-b border-slate-200">
                <tr>
                  <th className="p-3">Key / Cookie</th>
                  <th className="p-3">Type</th>
                  <th className="p-3">Purpose</th>
                  <th className="p-3">Lifespan</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                <tr>
                  <td className="p-3 font-mono font-medium text-slate-800">amee_cookie_consent</td>
                  <td className="p-3">Strictly Necessary</td>
                  <td className="p-3">Records your consent choices for analytics and cookies.</td>
                  <td className="p-3">12 Months (LocalStorage)</td>
                </tr>
                <tr>
                  <td className="p-3 font-mono font-medium text-slate-800">_ga, _ga_*</td>
                  <td className="p-3">Analytics</td>
                  <td className="p-3">Aggregated telemetry to measure tool visits and optimize speed. Disabled by default.</td>
                  <td className="p-3">Up to 14 months</td>
                </tr>
                <tr>
                  <td className="p-3 font-mono font-medium text-slate-800">Local Tool Drafts</td>
                  <td className="p-3">Functional Storage</td>
                  <td className="p-3">Keeps your current draft invoice or receipt from erasing if you refresh. Stored only in browser memory.</td>
                  <td className="p-3">Until cleared by user</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">3. How to Manage or Clear Cookies</h2>
          <p>
            You can manage or delete cookies via your browser settings (Chrome, Firefox, Safari, Edge). To immediately delete all draft invoices and local storage created by Ameetech Toolkits on your device, visit our{' '}
            <Link href="/data-deletion" className="text-purple-700 font-semibold hover:underline">
              Data Deletion Page
            </Link>.
          </p>
        </section>

        <section className="space-y-3 border-t border-slate-100 pt-6 text-xs text-slate-500">
          <p>
            Questions regarding our cookie practices? Contact us at{' '}
            <a href="mailto:support@ameetechnology.com.ng" className="text-purple-700 hover:underline">
              support@ameetechnology.com.ng
            </a>.
          </p>
        </section>
      </div>
    </div>
  );
}
