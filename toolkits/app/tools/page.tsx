import React from 'react';
import { Metadata } from 'next';
import Link from 'next/link';
import { TOOLS_DATA, TOOL_CATEGORIES } from '@/lib/tools-data';
import ToolCard from '@/components/ToolCard';
import ServiceCTA from '@/components/ServiceCTA';
import { Layers, ArrowLeft } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Directory of Free Digital Business Tools',
  description:
    'Browse our comprehensive catalog of free digital productivity tools for Nigerian businesses: invoice generator, receipt maker, profit calculator, WhatsApp link maker, and marketing generators.',
};

export default function ToolsDirectoryPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-16 space-y-12">
      {/* Header */}
      <div className="space-y-4 max-w-3xl">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-purple-700 hover:text-purple-900 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Home</span>
        </Link>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-800">
          <Layers className="w-3.5 h-3.5 text-purple-600" />
          <span>Full Tool Catalog</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          All Free Business Utilities
        </h1>
        <p className="text-base text-slate-600 leading-relaxed">
          Select any of the free tools below to handle invoices, receipts, pricing analysis, or WhatsApp customer links directly in your browser. No registration or software installation required.
        </p>
      </div>

      {/* Grouped by Category */}
      {TOOL_CATEGORIES.filter((c) => c !== 'All').map((category) => {
        const categoryTools = TOOLS_DATA.filter((t) => t.category === category);
        if (categoryTools.length === 0) return null;

        return (
          <section key={category} className="space-y-6 pt-6 border-t border-slate-200">
            <div>
              <h2 className="text-xl sm:text-2xl font-bold text-slate-900">
                {category}
              </h2>
              <p className="text-xs sm:text-sm text-slate-500 mt-1">
                {category === 'Documents' && 'Create and download business documents, invoices, receipts, and quotations.'}
                {category === 'Finance and Calculators' && 'Calculate pricing, gross margins, and markups with accurate arithmetic.'}
                {category === 'Communication' && 'Generate direct customer chat links for WhatsApp and social media.'}
                {category === 'Marketing' && 'Boost promotional outreach and social media captions.'}
                {category === 'Business Setup' && 'Tools to brainstorm and structure new business ventures.'}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {categoryTools.map((tool) => (
                <ToolCard key={tool.id} tool={tool} />
              ))}
            </div>
          </section>
        );
      })}

      {/* Service CTA */}
      <ServiceCTA
        headline="Need custom business software or automation?"
        description="Ameetech builds dedicated enterprise portals, CRM integrations, and mobile solutions for growing businesses in Nigeria."
        buttonText="Discuss Your Custom Project"
        url="https://ameetechnology.com.ng/#contact"
      />
    </div>
  );
}
