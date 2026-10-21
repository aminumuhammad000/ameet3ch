import React from 'react';
import { Metadata } from 'next';
import Link from 'next/link';
import { ShieldCheck, ArrowLeft, Lock, Database, EyeOff } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Privacy Policy & NDPA 2023 Compliance',
  description:
    'Our commitment to privacy, data minimization, and compliance with the Nigeria Data Protection Act (NDPA 2023). Zero mandatory data retention for free business tools.',
};

export default function PrivacyPolicyPage() {
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
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          <span>NDPA 2023 Compliant</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Privacy Policy
        </h1>
        <p className="text-sm text-slate-500">
          Effective Date: October 2026 · Ameetech Toolkits (AMEE TECHNOLOGY LTD)
        </p>
      </div>

      <div className="bg-white rounded-2xl p-6 sm:p-10 border border-slate-200 shadow-sm space-y-8 text-sm text-slate-700 leading-relaxed">
        {/* Core Guarantee */}
        <div className="p-4 rounded-xl bg-purple-50 border border-purple-200/60 flex items-start gap-3">
          <Lock className="w-5 h-5 text-purple-700 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <h2 className="font-bold text-purple-900 text-sm">
              Our Core Data Minimization Promise
            </h2>
            <p className="text-xs text-purple-800/90 leading-relaxed">
              Ameetech Toolkits operates on a client-first privacy model. We do not require accounts or user registration to access our core free tools. All invoices, receipts, financial calculations, and phone numbers remain exclusively in your local browser session and are not transmitted to or stored on our servers.
            </p>
          </div>
        </div>

        {/* Section 1 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">
            1. Information We Do Not Collect
          </h2>
          <p>
            When you use our free productivity utilities (Invoice Generator, Receipt Generator, Profit and Markup Calculator, WhatsApp Link Generator), we:
          </p>
          <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-600">
            <li>Do <strong>not</strong> save your customer names, addresses, or phone numbers.</li>
            <li>Do <strong>not</strong> record your invoice line items, product pricing, or financial figures.</li>
            <li>Do <strong>not</strong> upload your generated PDF documents to remote databases.</li>
            <li>Do <strong>not</strong> access your device contacts, camera, or banking credentials.</li>
            <li>Do <strong>not</strong> sell, rent, or trade your personal or commercial data to third-party data brokers.</li>
          </ul>
        </section>

        {/* Section 2 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">
            2. Information Collected Only With Voluntary Consent
          </h2>
          <p>
            The only times we collect personal information are when you voluntarily choose to contact us or inquire about Ameetech paid services:
          </p>
          <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-600">
            <li><strong>Service Inquiries:</strong> When you submit a project inquiry or contact form, we collect your name, email, phone number, and project requirements to provide quotes and support.</li>
            <li><strong>Direct WhatsApp Communication:</strong> When you initiate a chat with our customer support, your WhatsApp profile and messages are processed via WhatsApp under Meta privacy guidelines.</li>
          </ul>
        </section>

        {/* Section 3 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">
            3. Nigeria Data Protection Act (NDPA 2023) Compliance
          </h2>
          <p>
            As a registered Nigerian entity (AMEE TECHNOLOGY LTD), we handle data in accordance with the provisions of the Nigeria Data Protection Act 2023. You have the right to request access, rectification, or deletion of any voluntarily submitted contact information at any time.
          </p>
        </section>

        {/* Section 4 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">
            4. Cookies & Anonymous Telemetry
          </h2>
          <p>
            We may use privacy-preserving, aggregated operational analytics (e.g. counting total visits and page views) to identify which tools are most useful and optimize mobile performance. These analytics never correlate with or include user document contents or personal financial inputs.
          </p>
        </section>

        {/* Section 5 */}
        <section className="space-y-3 border-t border-slate-100 pt-6">
          <h2 className="text-base font-bold text-slate-900">5. Contact Our Privacy Officer</h2>
          <p>
            If you have questions about this policy or our data practices, please contact us at:
          </p>
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs space-y-1">
            <p><strong>Entity:</strong> AMEE TECHNOLOGY LTD</p>
            <p><strong>Email:</strong> support@ameetechnology.com.ng</p>
            <p><strong>Phone:</strong> +234 810 001 5498</p>
            <p><strong>Website:</strong> <a href="https://ameetechnology.com.ng" target="_blank" rel="noopener noreferrer" className="text-purple-700 hover:underline">https://ameetechnology.com.ng</a></p>
          </div>
        </section>
      </div>
    </div>
  );
}
