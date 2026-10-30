import React from 'react';
import { Metadata } from 'next';
import Link from 'next/link';
import { ShieldCheck, ArrowLeft, Lock, Database, FileText, Trash2, Cookie, Building, Mail, Phone, ExternalLink } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Privacy Policy & NDPA 2023 Compliance',
  description:
    'Our commitment to privacy, data minimization, and compliance with the Nigeria Data Protection Act (NDPA 2023). Zero remote data retention for free business tools.',
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
        <div className="flex flex-wrap items-center gap-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            <span>NDPA 2023 Compliant</span>
          </div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-purple-50 text-purple-700 border border-purple-200">
            <Database className="w-3.5 h-3.5 text-purple-600" />
            <span>Zero Remote Storage Architecture</span>
          </div>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Privacy Policy
        </h1>
        <p className="text-sm text-slate-500">
          Effective Date: October 30, 2026 &middot; Ameetech Toolkits (Amee Technology Ltd, Kano, Nigeria)
        </p>
      </div>

      <div className="bg-white rounded-2xl p-6 sm:p-10 border border-slate-200 shadow-sm space-y-8 text-sm text-slate-700 leading-relaxed">
        {/* Core Guarantee */}
        <div className="p-5 rounded-xl bg-purple-50 border border-purple-200/80 flex items-start gap-3.5">
          <Lock className="w-5 h-5 text-purple-700 shrink-0 mt-0.5" />
          <div className="space-y-1.5">
            <h2 className="font-bold text-purple-900 text-sm">
              Our Zero-Retention Privacy Promise
            </h2>
            <p className="text-xs text-purple-900/90 leading-relaxed">
              Ameetech Toolkits operates on a client-first privacy model. We do not require accounts, logins, or user registration to access our free productivity utilities. All customer names, bank details, itemized line items, and financial calculations remain exclusively in your local browser session and are never transmitted to, archived on, or processed by our remote servers.
            </p>
          </div>
        </div>

        {/* Section 1 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Database className="w-4 h-4 text-purple-700" /> 1. Information We Do Not Collect
          </h2>
          <p>
            When you use our free productivity utilities (Invoice Generator, Receipt Generator, Quotation Generator, WhatsApp Link Generator, Profit and Markup Calculator), we:
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
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Mail className="w-4 h-4 text-purple-700" /> 2. Information Collected Only With Voluntary Consent
          </h2>
          <p>
            The only times we collect personal information are when you voluntarily choose to contact us or inquire about Amee Technology paid custom software engineering or consulting services:
          </p>
          <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-600">
            <li><strong>Service Inquiries:</strong> When you submit a project inquiry or contact form, we collect your name, email, phone number, and project requirements to provide quotes and support.</li>
            <li><strong>Direct WhatsApp Communication:</strong> When you initiate a chat with our customer support, your WhatsApp profile and messages are processed via WhatsApp under Meta privacy guidelines.</li>
          </ul>
        </section>

        {/* Section 3 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-purple-700" /> 3. Nigeria Data Protection Act (NDPA 2023) Compliance
          </h2>
          <p>
            As a registered Nigerian entity (Amee Technology Ltd), we handle data in accordance with the provisions of the <strong>Nigeria Data Protection Act 2023</strong> and the Nigeria Data Protection Commission (NDPC) guidelines.
          </p>
          <p>
            You possess full statutory data subject rights:
          </p>
          <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-600">
            <li><strong>Right of Access:</strong> Request confirmation and copies of any personal data we hold about you.</li>
            <li><strong>Right to Rectification:</strong> Have incomplete or inaccurate contact records corrected.</li>
            <li><strong>Right to Erasure (Deletion):</strong> Request that your personal contact details be expunged from our inquiry logs.</li>
            <li><strong>Right to Object &amp; Restrict Processing:</strong> Limit how we process your information.</li>
          </ul>
        </section>

        {/* Section 4 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Trash2 className="w-4 h-4 text-purple-700" /> 4. Information Required for Data Deletion
          </h2>
          <p>
            To request permanent deletion of your contact records or inquiry logs, email our Data Protection Desk at{' '}
            <a href="mailto:support@ameetechnology.com.ng" className="text-purple-700 font-semibold hover:underline">
              support@ameetechnology.com.ng
            </a>.
          </p>
          <p>
            To prevent unauthorized or fraudulent deletion requests, please provide:
          </p>
          <ol className="list-decimal list-inside space-y-1.5 pl-2 text-slate-600 text-xs sm:text-sm">
            <li>Your full legal name;</li>
            <li>The registered email address used when contacting us;</li>
            <li>Your phone number / WhatsApp contact (if previously provided);</li>
            <li>Scope of deletion (e.g. inquiry history or marketing correspondence).</li>
          </ol>
          <p className="text-xs text-slate-500">
            Requests are processed within 30 calendar days free of charge. For full details, review our{' '}
            <Link href="/data-deletion" className="text-purple-700 font-semibold hover:underline">
              Data Deletion Instructions Page
            </Link>.
          </p>
        </section>

        {/* Section 5 */}
        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Cookie className="w-4 h-4 text-purple-700" /> 5. Cookies &amp; Browser Storage
          </h2>
          <p>
            We use strictly necessary cookies to maintain security and record your cookie preferences. Optional analytical metrics (Google Analytics 4) are aggregated and privacy-preserving. Review our{' '}
            <Link href="/cookies" className="text-purple-700 font-semibold hover:underline">
              Cookie Policy
            </Link>{' '}
            for a full breakdown of storage keys.
          </p>
        </section>

        {/* Section 6 */}
        <section className="space-y-3 border-t border-slate-100 pt-6">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Building className="w-4 h-4 text-purple-700" /> 6. Contact Our Data Protection Desk
          </h2>
          <p>
            If you have questions about this policy or our data practices, please contact us at:
          </p>
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs space-y-1.5">
            <p><strong>Entity:</strong> Amee Technology Ltd</p>
            <p><strong>Location:</strong> Kano State, Nigeria</p>
            <p><strong>Email:</strong> support@ameetechnology.com.ng</p>
            <p><strong>Phone / WhatsApp:</strong> +234 810 001 5498</p>
            <p>
              <strong>Corporate Website:</strong>{' '}
              <a
                href="https://ameetechnology.com.ng"
                target="_blank"
                rel="noopener noreferrer"
                className="text-purple-700 hover:underline inline-flex items-center gap-1"
              >
                https://ameetechnology.com.ng <ExternalLink className="w-3 h-3" />
              </a>
            </p>
            <p>
              <strong>Supervisory Authority:</strong> Nigeria Data Protection Commission (NDPC), Abuja, Nigeria (
              <a href="https://ndpc.gov.ng" target="_blank" rel="noopener noreferrer" className="text-purple-700 hover:underline">
                https://ndpc.gov.ng
              </a>)
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
