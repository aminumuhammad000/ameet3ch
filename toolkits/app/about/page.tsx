import React from 'react';
import { Metadata } from 'next';
import Link from 'next/link';
import Image from 'next/image';
import { ArrowLeft, CheckCircle2, ShieldCheck, Zap, ArrowUpRight } from 'lucide-react';
import ServiceCTA from '@/components/ServiceCTA';

export const metadata: Metadata = {
  title: 'About Ameetech Toolkits',
  description:
    'Learn about Ameetech Toolkits, an indigenous Nigerian initiative by Amee Technology Ltd providing free digital productivity tools for MSMEs and freelancers.',
};

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-12">
      <div className="space-y-3">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-purple-700 hover:text-purple-900 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Home</span>
        </Link>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          About Ameetech Toolkits
        </h1>
        <p className="text-base text-slate-600 leading-relaxed">
          Empowering Nigerian micro, small, and medium enterprises with practical, accessible, and completely free digital tools.
        </p>
      </div>

      <div className="bg-white rounded-3xl p-6 sm:p-10 border border-slate-200 shadow-sm space-y-8 text-sm text-slate-700 leading-relaxed">
        <div className="flex items-center gap-4 border-b border-slate-100 pb-6">
          <div className="w-14 h-14 rounded-2xl bg-purple-50 flex items-center justify-center p-2 border border-purple-200">
            <Image
              src="/brand/ameelogo2.png"
              alt="Amee Technology Ltd"
              width={48}
              height={48}
              className="object-contain"
            />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">Amee Technology Ltd</h2>
            <p className="text-xs text-slate-500">
              Technology Partner & Digital Transformation Specialists (Nigeria)
            </p>
          </div>
        </div>

        <section className="space-y-3">
          <h2 className="text-lg font-bold text-slate-900">Why We Built Ameetech Toolkits</h2>
          <p>
            Millions of Nigerian small business owners, market vendors, and freelancers manage their daily operations manually using notebooks, unformatted text messages, or spreadsheets. Many cannot afford expensive monthly software subscriptions just to send an invoice or calculate their profit margin accurately.
          </p>
          <p>
            Ameetech Toolkits was created to bridge this digital divide. By providing free, fast, browser-based utilities that work on any mobile device without mandatory signups or hidden charges, we help entrepreneurs run their businesses with greater confidence and professionalism.
          </p>
        </section>

        <section className="space-y-4 pt-4 border-t border-slate-100">
          <h2 className="text-lg font-bold text-slate-900">Our Core Principles</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Free Forever Core Tools
              </span>
              <p className="text-xs text-slate-600">
                Essential utilities like invoices, receipts, and WhatsApp links will always remain free.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-600" /> Privacy First (NDPA 2023)
              </span>
              <p className="text-xs text-slate-600">
                Your customer names, pricing, and business documents never leave your browser session.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                <Zap className="w-4 h-4 text-purple-600" /> Mobile Speed & Simplicity
              </span>
              <p className="text-xs text-slate-600">
                Optimized for fast mobile loading across Nigeria, even on modest network connections.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-purple-600" /> Backed by Real Engineers
              </span>
              <p className="text-xs text-slate-600">
                Need more than free tools? Ameetech’s software engineering team is available to build custom systems.
              </p>
            </div>
          </div>
        </section>
      </div>

      <ServiceCTA
        headline="Partner with Ameetech for your digital growth"
        description="Whether you need a custom e-commerce store, a bespoke enterprise portal, or targeted digital marketing to acquire more customers, our team is ready to collaborate."
        buttonText="Explore Ameetech Services"
        url="https://ameetechnology.com.ng/#services"
      />
    </div>
  );
}
