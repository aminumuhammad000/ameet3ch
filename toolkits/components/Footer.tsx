'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { ArrowUpRight, ShieldCheck, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-slate-950 text-slate-300 pt-16 pb-12 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 pb-12 border-b border-slate-800">
          {/* Brand Info */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="relative w-9 h-9 rounded-lg overflow-hidden flex items-center justify-center bg-white/10 border border-white/20">
                <Image
                  src="/brand/ameelogo2.png"
                  alt="Amee Technology Ltd"
                  width={36}
                  height={36}
                  className="object-contain"
                />
              </div>
              <span className="font-bold text-xl text-white tracking-tight">
                Ameetech <span className="text-purple-400">Toolkits</span>
              </span>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed max-w-sm">
              Free digital business productivity tools engineered for Nigerian entrepreneurs, micro-enterprises, and freelancers. Run your operations smarter without forced subscriptions.
            </p>
            <div className="flex items-center gap-2 text-xs text-slate-400 bg-slate-900 border border-slate-800 px-3 py-2 rounded-lg w-fit">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Compliant with NDPA 2023 · 100% Client-Side Privacy</span>
            </div>
          </div>

          {/* Quick Tools */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-200 mb-4">
              Free Business Tools
            </h3>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link href="/tools/invoice-generator" className="hover:text-purple-400 transition">
                  Invoice Generator
                </Link>
              </li>
              <li>
                <Link href="/tools/receipt-generator" className="hover:text-purple-400 transition">
                  Receipt Generator
                </Link>
              </li>
              <li>
                <Link href="/tools/profit-calculator" className="hover:text-purple-400 transition">
                  Profit & Markup Calculator
                </Link>
              </li>
              <li>
                <Link href="/tools/whatsapp-link-generator" className="hover:text-purple-400 transition">
                  WhatsApp Link Generator
                </Link>
              </li>
              <li>
                <Link href="/tools/marketing-caption-generator" className="hover:text-purple-400 transition">
                  Marketing Caption Generator
                </Link>
              </li>
              <li>
                <Link href="/tools" className="text-purple-400 hover:text-purple-300 font-medium transition inline-flex items-center gap-1">
                  View all tools →
                </Link>
              </li>
            </ul>
          </div>

          {/* Ameetech Services */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-200 mb-4">
              Ameetech Services
            </h3>
            <ul className="space-y-2.5 text-sm">
              <li>
                <a
                  href="https://ameetechnology.com.ng/#services"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-purple-400 transition inline-flex items-center gap-1"
                >
                  Web & App Development <ArrowUpRight className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a
                  href="https://ameetechnology.com.ng/#services"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-purple-400 transition inline-flex items-center gap-1"
                >
                  E-Commerce Systems <ArrowUpRight className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a
                  href="https://ameetechnology.com.ng/#services"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-purple-400 transition inline-flex items-center gap-1"
                >
                  SEO & Organic Search <ArrowUpRight className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a
                  href="https://ameetechnology.com.ng/#services"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-purple-400 transition inline-flex items-center gap-1"
                >
                  UI/UX & Brand Identity <ArrowUpRight className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a
                  href="https://ameetechnology.com.ng/#services"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-purple-400 transition inline-flex items-center gap-1"
                >
                  Digital Marketing & Ads <ArrowUpRight className="w-3 h-3 text-slate-500" />
                </a>
              </li>
            </ul>
          </div>

          {/* Legal & Company */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-200 mb-4">
              Company &amp; Legal
            </h3>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link href="/about" className="hover:text-purple-400 transition">
                  About the Toolkit
                </Link>
              </li>
              <li>
                <Link href="/resources" className="hover:text-purple-400 transition">
                  Business Guides
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="hover:text-purple-400 transition">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="hover:text-purple-400 transition">
                  Terms of Use &amp; Disclaimers
                </Link>
              </li>
              <li>
                <Link href="/cookies" className="hover:text-purple-400 transition">
                  Cookie Policy
                </Link>
              </li>
              <li>
                <Link href="/data-deletion" className="hover:text-purple-400 transition">
                  Data Deletion
                </Link>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => {
                    if (typeof window !== 'undefined') {
                      window.dispatchEvent(new Event('openAmeeCookieSettings'));
                    }
                  }}
                  className="hover:text-purple-400 transition text-left text-sm text-slate-300 flex items-center gap-1.5"
                >
                  Cookie Settings
                </button>
              </li>
              <li>
                <Link href="/contact" className="hover:text-purple-400 transition">
                  Contact &amp; Support
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Legal Disclaimer & Copyright */}
        <div className="pt-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-xs text-slate-500">
          <p className="max-w-2xl leading-relaxed">
            <strong>Disclaimer:</strong> Ameetech Toolkits is an initiative by{' '}
            <a
              href="https://ameetechnology.com.ng"
              target="_blank"
              rel="noopener noreferrer"
              className="text-purple-400 hover:underline"
            >
              AMEE TECHNOLOGY LTD
            </a>{' '}
            (Nigeria). Tool outputs, calculations, and documents are provided for general operational and productivity purposes and should not be construed as formal tax, audit, or legal counsel.
          </p>
          <div className="flex items-center gap-1 text-slate-400 shrink-0">
            <span>Built with</span>
            <Heart className="w-3.5 h-3.5 text-pink-500 fill-pink-500" />
            <span>for Nigerian Businesses · © 2026</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
