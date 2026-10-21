import React from 'react';
import { Metadata } from 'next';
import Link from 'next/link';
import { ArrowLeft, FileText, AlertTriangle } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Terms of Use & Disclaimers',
  description:
    'Terms of use and operational disclaimers for Ameetech Toolkits. Understand tool usage terms, calculation limitations, and legal boundaries.',
};

export default function TermsOfUsePage() {
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
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Terms of Use & Disclaimers
        </h1>
        <p className="text-sm text-slate-500">
          Last Updated: October 2026 · Ameetech Toolkits
        </p>
      </div>

      <div className="bg-white rounded-2xl p-6 sm:p-10 border border-slate-200 shadow-sm space-y-8 text-sm text-slate-700 leading-relaxed">
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <h2 className="font-bold text-sm text-amber-950">Important Professional Disclaimer</h2>
            <p className="text-xs text-amber-900/90 leading-relaxed">
              Ameetech Toolkits is a free digital productivity platform provided for administrative convenience. The platform and its tools (including calculators and document templates) do not provide licensed tax, legal, or chartered financial auditing services.
            </p>
          </div>
        </div>

        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">1. Acceptance of Terms</h2>
          <p>
            By accessing or using Ameetech Toolkits (available at{' '}
            <code className="text-purple-700 font-mono text-xs">toolkits.ameetechnology.com.ng</code>),
            you agree to these Terms of Use. If you do not agree, you should discontinue using the platform.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">2. Free Use & Fair Access</h2>
          <p>
            All standard tools are provided free of charge for legitimate commercial and individual productivity purposes. Users agree not to abuse the tools via automated scraping, denial of service attacks, or deceptive generation of fraudulent documents.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">3. Document Accuracy & User Responsibility</h2>
          <p>
            Users are solely responsible for ensuring the accuracy of values, names, tax rates, and prices entered into invoices, receipts, and quotations. Ameetech does not verify transactions, certify bank payments, or guarantee tax compliance for individual business jurisdictions.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">4. Intellectual Property</h2>
          <p>
            The interface, branding, code, and design of Ameetech Toolkits are the proprietary property of AMEE TECHNOLOGY LTD. Generated business documents created with your own business data remain your property.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-bold text-slate-900">5. Limitation of Liability</h2>
          <p>
            AMEE TECHNOLOGY LTD and its team shall not be held liable for any indirect, incidental, or consequential damages resulting from business decisions made using our tools, formula interpretations, or browser-based document generation failures.
          </p>
        </section>
      </div>
    </div>
  );
}
