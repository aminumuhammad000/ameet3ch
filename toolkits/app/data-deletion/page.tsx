import React from 'react';
import { Metadata } from 'next';
import Link from 'next/link';
import { Trash2, ArrowLeft, ShieldCheck, Mail, FileText, CheckCircle } from 'lucide-react';
import ClearLocalDataButton from '@/components/ClearLocalDataButton';

export const metadata: Metadata = {
  title: 'Data Deletion Policy & Request Instructions',
  description:
    'Information required to delete personal data under the Nigeria Data Protection Act (NDPA 2023) and GDPR. Instant browser storage purge tool.',
};

export default function DataDeletionPage() {
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
            <span>Right to Erasure (NDPA Sec. 34)</span>
          </div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-purple-50 text-purple-700 border border-purple-200">
            <Trash2 className="w-3.5 h-3.5 text-purple-600" />
            <span>GDPR Art. 17 Compliant</span>
          </div>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Data Deletion Policy &amp; Instructions
        </h1>
        <p className="text-sm text-slate-500">
          Last Updated: October 30, 2026 &middot; Ameetech Toolkits (Amee Technology Ltd)
        </p>
      </div>

      <div className="bg-white rounded-2xl p-6 sm:p-10 border border-slate-200 shadow-sm space-y-8 text-sm text-slate-700 leading-relaxed">
        {/* Local storage purge button */}
        <ClearLocalDataButton />

        {/* Section 1 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">
            1. Zero Server Retention on Ameetech Toolkits
          </h2>
          <p>
            Please note that <strong>Ameetech Toolkits does not store your invoice, receipt, or calculator data on our servers</strong>. All calculations, business names, and document line items remain exclusively inside your local browser. If you wish to delete your documents, clicking the red button above or clearing your browser cache immediately wipes all records.
          </p>
        </section>

        {/* Section 2 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">
            2. Information Required to Delete Server-Side Records
          </h2>
          <p>
            If you previously submitted a project inquiry, contact form, or requested custom software development from our parent entity <strong>Amee Technology Ltd</strong>, you can request that all records be permanently deleted from our active databases and CRM systems.
          </p>
          <p>
            To prevent fraudulent or unauthorized deletion, your request must contain the following verification details:
          </p>
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2 text-xs">
            <div className="flex items-start gap-2">
              <CheckCircle className="w-4 h-4 text-purple-700 shrink-0 mt-0.5" />
              <span><strong>Full Legal Name:</strong> The name associated with your correspondence or business contract.</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="w-4 h-4 text-purple-700 shrink-0 mt-0.5" />
              <span><strong>Primary Email Address:</strong> The exact email used during your interactions. Your deletion request must originate from this email.</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="w-4 h-4 text-purple-700 shrink-0 mt-0.5" />
              <span><strong>Phone Number / WhatsApp:</strong> (If previously provided) to verify identity.</span>
            </div>
            <div className="flex items-start gap-2">
              <CheckCircle className="w-4 h-4 text-purple-700 shrink-0 mt-0.5" />
              <span><strong>Scope of Deletion:</strong> Specify whether you want complete erasure or removal from specific email lists.</span>
            </div>
          </div>
        </section>

        {/* Section 3 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">
            3. How to Submit Your Deletion Request
          </h2>
          <p>
            Email our Data Protection Desk at:
          </p>
          <div className="p-4 rounded-xl bg-purple-50 border border-purple-200/80 text-xs space-y-1">
            <p><strong>Email:</strong> support@ameetechnology.com.ng</p>
            <p><strong>Subject Line:</strong> <code>Data Deletion Request - [Your Full Name]</code></p>
            <p><strong>Processing Window:</strong> Completed within 30 calendar days free of charge.</p>
          </div>
        </section>

        {/* Section 4 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">
            4. Statutory Retention Exceptions
          </h2>
          <p>
            Under Nigerian commercial and tax laws (Companies and Allied Matters Act 2020 &amp; FIRS), signed software contracts, VAT records, and commercial invoices must be retained for <strong>6 years</strong> for audit compliance before being securely shredded or purged.
          </p>
        </section>
      </div>
    </div>
  );
}
