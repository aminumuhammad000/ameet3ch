'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Menu, X, ArrowUpRight, Sparkles, MessageCircle } from 'lucide-react';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20">
          {/* Logo & Brand Identity */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="relative w-9 h-9 sm:w-10 sm:h-10 rounded-lg overflow-hidden flex items-center justify-center bg-purple-50 border border-purple-200 shadow-sm">
              <Image
                src="/brand/ameelogo2.png"
                alt="Amee Technology Ltd"
                width={40}
                height={40}
                className="object-contain"
                priority
              />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-lg sm:text-xl tracking-tight text-slate-900 group-hover:text-purple-700 transition">
                Ameetech <span className="text-purple-600">Toolkits</span>
              </span>
              <span className="text-[10px] text-slate-500 font-medium tracking-wider uppercase -mt-1 hidden sm:block">
                Free Digital Tools for Businesses
              </span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-7 text-sm font-medium text-slate-600">
            <Link href="/tools" className="hover:text-purple-700 transition">
              All Tools
            </Link>
            <Link href="/tools/invoice-generator" className="hover:text-purple-700 transition">
              Invoice
            </Link>
            <Link href="/tools/receipt-generator" className="hover:text-purple-700 transition">
              Receipt
            </Link>
            <Link href="/tools/profit-calculator" className="hover:text-purple-700 transition">
              Profit Calculator
            </Link>
            <Link href="/tools/whatsapp-link-generator" className="hover:text-purple-700 transition">
              WhatsApp Link
            </Link>
            <Link href="/resources" className="hover:text-purple-700 transition">
              Guides
            </Link>
            <Link href="/about" className="hover:text-purple-700 transition">
              About
            </Link>
          </nav>

          {/* Desktop Right CTAs */}
          <div className="hidden lg:flex items-center gap-3">
            <a
              href="https://wa.me/2348100015498?text=Hi%20Ameetech%2C%20I%20am%20using%20the%20business%20toolkits%20and%20would%20like%20to%20learn%20more."
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 transition"
              title="Chat with Ameetech on WhatsApp"
            >
              <MessageCircle className="w-3.5 h-3.5" />
              <span>WhatsApp Support</span>
            </a>

            <a
              href="https://ameetechnology.com.ng"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold text-white bg-purple-600 hover:bg-purple-700 shadow-sm transition"
            >
              <span>Ameetech Services</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </a>
          </div>

          {/* Mobile menu trigger */}
          <div className="flex md:hidden items-center gap-2">
            <a
              href="https://wa.me/2348100015498?text=Hi%20Ameetech!"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 text-emerald-600 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition"
              aria-label="WhatsApp"
            >
              <MessageCircle className="w-5 h-5" />
            </a>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-slate-700 hover:bg-slate-100 rounded-lg transition"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-200 bg-white px-4 pt-3 pb-6 space-y-3">
          <div className="grid grid-cols-2 gap-2 pb-3 border-b border-slate-100">
            <Link
              href="/tools/invoice-generator"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 p-2 rounded-lg bg-slate-50 text-xs font-medium text-slate-700 hover:bg-purple-50 hover:text-purple-700"
            >
              <Sparkles className="w-3.5 h-3.5 text-purple-600" />
              Invoice Maker
            </Link>
            <Link
              href="/tools/receipt-generator"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 p-2 rounded-lg bg-slate-50 text-xs font-medium text-slate-700 hover:bg-purple-50 hover:text-purple-700"
            >
              <Sparkles className="w-3.5 h-3.5 text-purple-600" />
              Receipt Maker
            </Link>
            <Link
              href="/tools/profit-calculator"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 p-2 rounded-lg bg-slate-50 text-xs font-medium text-slate-700 hover:bg-purple-50 hover:text-purple-700"
            >
              <Sparkles className="w-3.5 h-3.5 text-purple-600" />
              Profit Calculator
            </Link>
            <Link
              href="/tools/whatsapp-link-generator"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 p-2 rounded-lg bg-slate-50 text-xs font-medium text-slate-700 hover:bg-purple-50 hover:text-purple-700"
            >
              <Sparkles className="w-3.5 h-3.5 text-purple-600" />
              WhatsApp Link
            </Link>
          </div>

          <div className="space-y-1">
            <Link
              href="/tools"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-50 hover:text-purple-700"
            >
              Browse All Tools
            </Link>
            <Link
              href="/resources"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-50 hover:text-purple-700"
            >
              Business Guides & Articles
            </Link>
            <Link
              href="/about"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-50 hover:text-purple-700"
            >
              About Ameetech Toolkits
            </Link>
            <Link
              href="/contact"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-50 hover:text-purple-700"
            >
              Contact & Inquiries
            </Link>
          </div>

          <div className="pt-2">
            <a
              href="https://ameetechnology.com.ng"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-semibold text-white bg-purple-600 hover:bg-purple-700 transition"
            >
              <span>Visit Ameetech Parent Website</span>
              <ArrowUpRight className="w-4 h-4" />
            </a>
          </div>
        </div>
      )}
    </header>
  );
}
