'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Lightbulb,
  ArrowLeft,
  Copy,
  Check,
  Sparkles,
  ShieldAlert,
  ArrowRight,
} from 'lucide-react';
import ServiceCTA from '@/components/ServiceCTA';

export default function BusinessNameGeneratorPage() {
  const [keyword, setKeyword] = useState('Tech');
  const [industry, setIndustry] = useState('Technology & Digital Services');
  const [vibe, setVibe] = useState('Modern & Innovative');
  const [copiedName, setCopiedName] = useState<string | null>(null);

  const generateNames = () => {
    const cleanWord = keyword.trim() || 'Venture';
    return [
      { name: `Nova${cleanWord}`, tagline: 'Empowering tomorrow with reliable solutions.' },
      { name: `Apex ${cleanWord}`, tagline: 'The pinnacle of quality and performance.' },
      { name: `${cleanWord}Core Nigeria`, tagline: 'Building resilient foundations for African commerce.' },
      { name: `Zenith ${cleanWord}`, tagline: 'Elevating standards through thoughtful design.' },
      { name: `Aura${cleanWord}`, tagline: 'Distinctive excellence that sets you apart.' },
      { name: `Prime${cleanWord} Solutions`, tagline: 'Delivering trusted results every single time.' },
      { name: `${cleanWord}Nest`, tagline: 'Your trusted hub for growth and innovation.' },
      { name: `Kano${cleanWord} / Naija${cleanWord}`, tagline: 'Locally rooted, globally minded.' },
    ];
  };

  const nameList = generateNames();

  const handleCopy = async (name: string) => {
    await navigator.clipboard.writeText(name);
    setCopiedName(name);
    setTimeout(() => setCopiedName(null), 2500);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
      <div className="space-y-3">
        <Link
          href="/tools"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-purple-700 hover:text-purple-900 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to All Tools</span>
        </Link>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Business Name Idea Generator
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Brainstorm creative, modern brand name concepts and taglines for your new enterprise.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Inputs */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">Core Keyword or Seed Word *</label>
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="e.g. Solar, Cloth, Logistics, Glow"
              className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">Industry / Niche</label>
            <select
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-white"
            >
              <option value="Technology & Digital Services">Technology & Software</option>
              <option value="Fashion & Lifestyle">Fashion & Apparel</option>
              <option value="Food, Catering & Restaurant">Food & Culinary</option>
              <option value="Real Estate & Construction">Real Estate & Property</option>
              <option value="Consulting & Agency">Professional Consulting</option>
              <option value="Retail & General Merchandise">Retail & E-commerce</option>
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">Brand Personality / Style</label>
            <select
              value={vibe}
              onChange={(e) => setVibe(e.target.value)}
              className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-white"
            >
              <option value="Modern & Innovative">Modern & Tech-forward</option>
              <option value="Prestigious & Premium">Prestigious & Luxury</option>
              <option value="Friendly & Approachable">Friendly & Community</option>
              <option value="Afrocentric & Indigenous">Afrocentric & Indigenous</option>
            </select>
          </div>

          <div className="p-4 rounded-xl bg-amber-50 border border-amber-200/80 text-xs text-amber-900 flex items-start gap-2">
            <ShieldAlert className="w-4 h-4 shrink-0 text-amber-700 mt-0.5" />
            <span>
              <strong>Legal Notice:</strong> Generated names are creative suggestions. Please verify trademark and CAC business registration availability on the official Corporate Affairs Commission (CAC) portal before printing branding assets.
            </span>
          </div>
        </div>

        {/* Right Output Grid */}
        <div className="lg:col-span-7 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Generated Name Ideas ({nameList.length})
            </span>
            <span className="text-xs text-purple-700 font-semibold flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5" />
              Click any name to copy
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {nameList.map((item, idx) => (
              <div
                key={idx}
                onClick={() => handleCopy(item.name)}
                className="cursor-pointer group bg-white rounded-2xl p-4 border border-slate-200 hover:border-purple-300 shadow-xs hover:shadow-md transition space-y-1 relative"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-slate-900 group-hover:text-purple-700 text-sm transition">
                    {item.name}
                  </h3>
                  {copiedName === item.name ? (
                    <span className="text-[10px] font-bold text-emerald-600 flex items-center gap-0.5">
                      <Check className="w-3 h-3" /> Copied!
                    </span>
                  ) : (
                    <Copy className="w-3.5 h-3.5 text-slate-400 group-hover:text-purple-600 transition" />
                  )}
                </div>
                <p className="text-[11px] text-slate-500 italic leading-snug">
                  &ldquo;{item.tagline}&rdquo;
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <ServiceCTA
        headline="Ready to build your logo, brand identity, and corporate website?"
        description="Amee Technology Ltd helps new and established businesses create corporate identities, brand books, websites, and high-impact digital presence."
        buttonText="Explore Branding & Web Design"
        url="https://ameetechnology.com.ng/#services"
      />
    </div>
  );
}
