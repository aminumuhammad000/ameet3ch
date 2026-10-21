import React from 'react';
import { Metadata } from 'next';
import Link from 'next/link';
import { BookOpen, ArrowLeft, ArrowRight, FileText, Calculator, MessageSquare, Globe } from 'lucide-react';
import ServiceCTA from '@/components/ServiceCTA';

export const metadata: Metadata = {
  title: 'Practical Business Guides & Resources for Nigerian MSMEs',
  description:
    'Free practical guides on invoicing, markup calculations, product pricing, WhatsApp marketing, and setting up an online business presence in Nigeria.',
};

const GUIDES = [
  {
    slug: 'how-to-create-an-invoice-nigeria',
    title: 'How to Create a Professional Invoice for Your Nigerian Small Business',
    category: 'Billing & Accounting',
    readTime: '4 min read',
    summary:
      'Learn what essential fields must be included in a commercial invoice in Nigeria (CAC business details, bank instructions, payment terms, and VAT rates).',
    actionText: 'Use Invoice Tool',
    actionUrl: '/tools/invoice-generator',
  },
  {
    slug: 'how-to-calculate-profit-and-markup',
    title: 'The Real Difference Between Markup and Gross Profit Margin',
    category: 'Financial Management',
    readTime: '5 min read',
    summary:
      'Why mixing up markup percentage with profit margin causes Nigerian business owners to lose money on sales, and how to price correctly for healthy margins.',
    actionText: 'Open Profit Calculator',
    actionUrl: '/tools/profit-calculator',
  },
  {
    slug: 'how-to-create-whatsapp-business-link',
    title: 'How to Generate & Use WhatsApp Direct Click-to-Chat Links for Sales',
    category: 'Sales & Marketing',
    readTime: '3 min read',
    summary:
      'Turn social media followers into direct WhatsApp conversations. How to format +234 phone numbers and prefill greetings to eliminate customer friction.',
    actionText: 'Create WhatsApp Link',
    actionUrl: '/tools/whatsapp-link-generator',
  },
  {
    slug: 'when-does-small-business-need-website',
    title: 'When Does a Nigerian Small Business Truly Need a Dedicated Website?',
    category: 'Digital Transformation',
    readTime: '6 min read',
    summary:
      'Is relying solely on Instagram and WhatsApp enough? Signs your enterprise is ready for a professional dot-ng domain, automated e-commerce store, and Google Search presence.',
    actionText: 'Explore Web Design',
    actionUrl: 'https://ameetechnology.com.ng/#services',
  },
  {
    slug: 'how-to-issue-valid-business-receipts',
    title: 'How to Issue Legally Sound Payment Receipts for Cash and Bank Transfers',
    category: 'Operations',
    readTime: '4 min read',
    summary:
      'Best practices for documenting transactions, logging NIP session IDs, issuing receipts promptly, and preventing financial disputes with clients.',
    actionText: 'Use Receipt Maker',
    actionUrl: '/tools/receipt-generator',
  },
];

export default function ResourcesPage() {
  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-12">
      <div className="space-y-3 max-w-3xl">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-purple-700 hover:text-purple-900 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Home</span>
        </Link>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-800">
          <BookOpen className="w-3.5 h-3.5 text-purple-600" />
          <span>Educational Guides</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Practical Guides for Nigerian Entrepreneurs
        </h1>
        <p className="text-base text-slate-600 leading-relaxed">
          Actionable advice, step-by-step walk-throughs, and strategies to help you manage your business numbers, create professional documents, and market with higher returns.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {GUIDES.map((guide, idx) => (
          <div
            key={idx}
            className="flex flex-col justify-between bg-white rounded-2xl p-6 border border-slate-200 shadow-xs hover:shadow-md transition space-y-4"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between text-xs text-slate-500">
                <span className="font-semibold text-purple-700 bg-purple-50 px-2.5 py-0.5 rounded-md">
                  {guide.category}
                </span>
                <span>{guide.readTime}</span>
              </div>
              <h2 className="text-base font-bold text-slate-900 leading-snug">
                {guide.title}
              </h2>
              <p className="text-xs text-slate-600 leading-relaxed">
                {guide.summary}
              </p>
            </div>

            <div className="pt-4 border-t border-slate-100">
              <Link
                href={guide.actionUrl}
                className="inline-flex items-center gap-1.5 text-xs font-bold text-purple-700 hover:text-purple-900 transition"
              >
                <span>{guide.actionText}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>

      <ServiceCTA
        headline="Looking to grow your business brand online?"
        description="Amee Technology Ltd helps businesses build custom websites, e-commerce stores, and digital marketing strategies that bring measurable growth."
        buttonText="Explore Ameetech Services"
        url="https://ameetechnology.com.ng/#services"
      />
    </div>
  );
}
