'use client';

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import {
  Search,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Zap,
  CheckCircle,
  HelpCircle,
  ChevronDown,
  Building2,
  FileCheck2,
  TrendingUp,
} from 'lucide-react';
import { TOOLS_DATA, TOOL_CATEGORIES } from '@/lib/tools-data';
import ToolCard from '@/components/ToolCard';
import ServiceCTA from '@/components/ServiceCTA';

export default function HomePage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  // Filter tools based on search and category
  const filteredTools = useMemo(() => {
    return TOOLS_DATA.filter((tool) => {
      const matchesCategory =
        selectedCategory === 'All' || tool.category === selectedCategory;
      const matchesSearch =
        tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tool.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tool.category.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    });
  }, [searchQuery, selectedCategory]);

  const p0Tools = useMemo(() => {
    return TOOLS_DATA.filter((t) => t.priority === 'P0');
  }, []);

  const faqs = [
    {
      q: 'Are these tools really 100% free to use?',
      a: 'Yes. All core tools (including the Invoice Generator, Receipt Generator, Profit Calculator, and WhatsApp Link Maker) are completely free to use without requiring any payment or mandatory subscription.',
    },
    {
      q: 'Do I need to create an account or provide my email to use the tools?',
      a: 'No. You can generate invoices, download receipts, calculate margins, or create WhatsApp links immediately without creating an account or signing up.',
    },
    {
      q: 'Is my business and customer data kept private?',
      a: 'Absolutely. We comply with the Nigeria Data Protection Act (NDPA 2023). All document generation and calculations run client-side directly within your browser session. We do not store your client names, prices, or documents on any remote database without your explicit action.',
    },
    {
      q: 'Can I download and print the invoices and receipts on mobile devices?',
      a: 'Yes! The generated documents are designed to be mobile-responsive and support instant high-resolution PDF download and native browser printing on Android, iOS, tablets, and desktop computers.',
    },
    {
      q: 'Who built Ameetech Toolkits?',
      a: 'Ameetech Toolkits is developed and maintained by AMEE TECHNOLOGY LTD, an indigenous Nigerian digital technology company offering web development, custom software engineering, e-commerce, SEO, and digital marketing services.',
    },
    {
      q: 'Can Ameetech help build a custom website or software for my business?',
      a: 'Yes! If your business is ready for a dedicated website, e-commerce store, mobile application, or automated software system, our engineering team can build it for you. You can explore our services or reach out directly on WhatsApp.',
    },
  ];

  return (
    <div className="space-y-16 sm:space-y-24 pb-20">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 sm:pt-20 pb-16 bg-gradient-to-b from-purple-50/70 via-white to-slate-50 border-b border-slate-200/60">
        <div className="absolute inset-0 bg-[radial-gradient(#6C2BD9_1px,transparent_1px)] [background-size:24px_24px] opacity-[0.04] pointer-events-none" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            {/* Pill Badge */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-purple-100 text-purple-800 border border-purple-200 shadow-xs">
              <Sparkles className="w-3.5 h-3.5 text-purple-600" />
              <span>Built for Nigerian MSMEs & Entrepreneurs</span>
            </div>

            {/* Main Headline */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.15]">
              Run your business smarter with{' '}
              <span className="text-purple-700 underline decoration-purple-300 decoration-wavy decoration-2">
                free online tools
              </span>
              .
            </h1>

            {/* Subtitle */}
            <p className="text-base sm:text-lg text-slate-600 leading-relaxed max-w-2xl mx-auto">
              Create invoices, calculate profit margins, generate WhatsApp links, and market your products using practical tools built specifically for businesses that want to grow.
            </p>

            {/* Actions */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
              <a
                href="#tools"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-white bg-purple-600 hover:bg-purple-700 shadow-md shadow-purple-600/20 hover:shadow-lg transition"
              >
                <span>Explore Free Tools</span>
                <ArrowRight className="w-4 h-4" />
              </a>

              <a
                href="https://ameetechnology.com.ng/#services"
                target="_blank"
                rel="noopener noreferrer"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 shadow-xs transition"
              >
                <span>Get Help Growing Your Business</span>
              </a>
            </div>

            {/* Trust Badges */}
            <div className="pt-6 flex flex-wrap items-center justify-center gap-6 text-xs font-medium text-slate-500">
              <div className="flex items-center gap-1.5">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>100% Free Forever</span>
              </div>
              <div className="flex items-center gap-1.5">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>No Registration Required</span>
              </div>
              <div className="flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-500" />
                <span>No Data Stored Privately</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Core Tools (P0) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
          <div>
            <div className="text-xs font-bold text-purple-700 uppercase tracking-widest mb-1">
              Essential Utilities
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Featured Business Tools
            </h2>
          </div>
          <p className="text-sm text-slate-500 max-w-md">
            The most used tools by shop owners, contractors, and service providers to automate their daily admin.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {p0Tools.map((tool) => (
            <ToolCard key={tool.id} tool={tool} />
          ))}
        </div>
      </section>

      {/* Complete Tools Directory & Interactive Search */}
      <section id="tools" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 scroll-mt-24">
        <div className="bg-white rounded-3xl p-6 sm:p-10 border border-slate-200/80 shadow-sm space-y-8">
          <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 pb-6 border-b border-slate-100">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
                All Digital Tools
              </h2>
              <p className="text-sm text-slate-500 mt-1">
                Filter by category or type keywords to quickly find the exact utility you need.
              </p>
            </div>

            {/* Search Input */}
            <div className="relative w-full lg:w-80">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search tools (e.g. invoice, profit, WhatsApp)..."
                className="w-full pl-10 pr-4 py-2.5 text-sm rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400 hover:text-slate-600"
                >
                  Clear
                </button>
              )}
            </div>
          </div>

          {/* Category Tabs */}
          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
            {TOOL_CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition ${
                  selectedCategory === cat
                    ? 'bg-purple-600 text-white shadow-xs'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Filtered Tools Grid */}
          {filteredTools.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-2">
              {filteredTools.map((tool) => (
                <ToolCard key={tool.id} tool={tool} />
              ))}
            </div>
          ) : (
            <div className="text-center py-16 space-y-3">
              <div className="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
                <Search className="w-6 h-6" />
              </div>
              <h3 className="text-base font-semibold text-slate-800">No matching tools found</h3>
              <p className="text-sm text-slate-500 max-w-sm mx-auto">
                We could not find any tools matching &ldquo;{searchQuery}&rdquo;. Try another search term or reset category filters.
              </p>
              <button
                onClick={() => {
                  setSearchQuery('');
                  setSelectedCategory('All');
                }}
                className="text-xs font-semibold text-purple-600 hover:underline pt-2"
              >
                Reset search filters
              </button>
            </div>
          )}
        </div>
      </section>

      {/* Contextual Ameetech Parent Promotion */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <ServiceCTA
          headline="Ready to build an online identity or e-commerce shop?"
          description="Amee Technology Ltd helps Nigerian entrepreneurs transition from informal setups to custom high-performance websites, e-commerce stores, and digital marketing systems that bring real revenue."
          buttonText="View Ameetech Services"
          url="https://ameetechnology.com.ng/#services"
          badge="Ameetech Engineering"
        />
      </section>

      {/* Why Choose Ameetech Toolkits */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12 space-y-3">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Designed for Practical Daily Use
          </h2>
          <p className="text-sm text-slate-600">
            Everything you need to handle routine business administration quickly, accurately, and professionally.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center font-bold">
              <Zap className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900">Immediate Utility</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              No mandatory signup or paywalls. Open the tool in your browser, enter your data, and export your professional document in under 60 seconds.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900">Strict Data Privacy</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Your financial figures, customer names, and pricing stay in your browser. We adhere strictly to the Nigeria Data Protection Act (NDPA 2023).
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-pink-100 text-pink-700 flex items-center justify-center font-bold">
              <Building2 className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900">Supported by Tech Experts</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Backed by Amee Technology Ltd, a recognized tech partner providing software development, SEO, and digital transformation for Nigerian businesses.
            </p>
          </div>
        </div>
      </section>

      {/* Frequently Asked Questions */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-10 space-y-3">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">
            <HelpCircle className="w-3.5 h-3.5 text-purple-600" />
            <span>Answers to Common Questions</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Frequently Asked Questions
          </h2>
        </div>

        <div className="space-y-3">
          {faqs.map((faq, idx) => {
            const isOpen = openFaq === idx;
            return (
              <div
                key={idx}
                className="bg-white rounded-2xl border border-slate-200 overflow-hidden transition"
              >
                <button
                  onClick={() => setOpenFaq(isOpen ? null : idx)}
                  className="w-full flex items-center justify-between p-5 text-left font-semibold text-slate-900 hover:text-purple-700 transition"
                >
                  <span className="text-base">{faq.q}</span>
                  <ChevronDown
                    className={`w-5 h-5 text-slate-400 transition-transform ${
                      isOpen ? 'rotate-180 text-purple-600' : ''
                    }`}
                  />
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 text-sm text-slate-600 leading-relaxed border-t border-slate-100 pt-3">
                    {faq.a}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
