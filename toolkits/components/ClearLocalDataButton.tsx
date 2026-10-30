'use client';

import React, { useState } from 'react';
import { Trash2, CheckCircle2, AlertTriangle } from 'lucide-react';

export default function ClearLocalDataButton() {
  const [cleared, setCleared] = useState(false);

  const handleClear = () => {
    try {
      if (typeof window !== 'undefined') {
        localStorage.clear();
        sessionStorage.clear();
        
        // Clear cookies
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          const eqPos = cookie.indexOf('=');
          const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
          document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
        }
        setCleared(true);
      }
    } catch (e) {
      console.error('Failed to clear storage:', e);
    }
  };

  return (
    <div className="bg-red-50 border border-red-200 rounded-xl p-5 space-y-3">
      <div className="flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <h3 className="text-sm font-bold text-red-900">
            Instant Client-Side Storage Purge
          </h3>
          <p className="text-xs text-red-800/90 leading-relaxed">
            Clicking below will immediately purge all cached draft invoices, saved customer names, and cookie preferences stored in this browser.
          </p>
        </div>
      </div>

      <div className="pt-1">
        {cleared ? (
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-600 text-white text-xs font-semibold">
            <CheckCircle2 className="w-4 h-4" />
            <span>Browser Data &amp; Drafts Purged Successfully</span>
          </div>
        ) : (
          <button
            type="button"
            onClick={handleClear}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-white text-xs font-semibold transition shadow-sm"
          >
            <Trash2 className="w-4 h-4" />
            <span>Clear My Browser Data Now</span>
          </button>
        )}
      </div>
    </div>
  );
}
