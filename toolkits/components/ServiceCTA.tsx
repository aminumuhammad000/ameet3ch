import React from 'react';
import { ArrowUpRight, CheckCircle2, PhoneCall } from 'lucide-react';

interface ServiceCTAProps {
  headline?: string;
  description?: string;
  buttonText?: string;
  url?: string;
  badge?: string;
}

export default function ServiceCTA({
  headline = 'Need a Professional Online Presence for Your Business?',
  description = 'Amee Technology Ltd designs custom responsive websites, e-commerce stores, and digital tools tailored for ambitious Nigerian businesses.',
  buttonText = 'Explore Web Development Services',
  url = 'https://ameetechnology.com.ng/#services',
  badge = 'Ameetech Digital Solutions',
}: ServiceCTAProps) {
  return (
    <aside className="my-10 rounded-2xl bg-gradient-to-br from-purple-900 via-purple-950 to-slate-950 text-white p-6 sm:p-8 shadow-xl border border-purple-800/60 relative overflow-hidden">
      {/* Subtle decorative glow */}
      <div className="absolute top-0 right-0 w-72 h-72 bg-purple-600/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20" />
      <div className="absolute bottom-0 left-0 w-60 h-60 bg-pink-500/10 rounded-full blur-2xl pointer-events-none -ml-20 -mb-20" />

      <div className="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
        <div className="space-y-3 max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-purple-500/20 text-purple-200 border border-purple-500/30">
            <CheckCircle2 className="w-3.5 h-3.5 text-purple-300" />
            <span>{badge}</span>
          </div>
          <h3 className="text-xl sm:text-2xl font-bold tracking-tight text-white leading-snug">
            {headline}
          </h3>
          <p className="text-sm text-purple-200/90 leading-relaxed">
            {description}
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full lg:w-auto shrink-0">
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-sm bg-white text-purple-900 hover:bg-purple-50 shadow-md hover:shadow-lg transition-all"
          >
            <span>{buttonText}</span>
            <ArrowUpRight className="w-4 h-4 text-purple-800" />
          </a>

          <a
            href="https://wa.me/2348100015498?text=Hello%20Ameetech%2C%20I%20would%20like%20to%20discuss%20a%20digital%20service%20project."
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center gap-2 px-5 py-3.5 rounded-xl font-medium text-sm bg-purple-800/60 hover:bg-purple-800 text-purple-100 border border-purple-700/60 transition"
          >
            <PhoneCall className="w-4 h-4" />
            <span>Talk to Us</span>
          </a>
        </div>
      </div>
    </aside>
  );
}
