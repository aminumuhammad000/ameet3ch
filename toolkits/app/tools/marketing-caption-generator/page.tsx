'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Sparkles,
  ArrowLeft,
  Copy,
  Check,
  RefreshCw,
  Share2,
} from 'lucide-react';
import ServiceCTA from '@/components/ServiceCTA';

export default function MarketingCaptionGeneratorPage() {
  const [productName, setProductName] = useState('Premium Quality Fabric');
  const [description, setDescription] = useState('Breathable, vibrant colors, durable material suitable for traditional attire and corporate wear.');
  const [targetAudience, setTargetAudience] = useState('Men and women who love fashion');
  const [platform, setPlatform] = useState('WhatsApp');
  const [tone, setTone] = useState('Engaging & Friendly');
  const [language, setLanguage] = useState('English');
  const [discountOffer, setDiscountOffer] = useState('10% off for the first 10 orders');

  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  // Generate template-based variations
  const generateCaptions = () => {
    const isWhatsApp = platform === 'WhatsApp';
    const isInsta = platform === 'Instagram';

    return [
      {
        title: 'Direct Sales & Urgency',
        text: `✨ Looking for the best ${productName}? We've got you covered!\n\n${description}\n\n🎯 Perfect for: ${targetAudience}.\n🔥 Special Deal: ${discountOffer || 'Limited stock available!'}\n\n👉 Send a DM or click our WhatsApp link to place your order now before it sells out! 📦🚚`,
      },
      {
        title: 'Storytelling & Lifestyle',
        text: `Upgrade your style and comfort with ${productName}! ✨\n\nEvery piece is crafted to give you premium satisfaction. Whether it's for a special occasion or daily use, you deserve the best.\n\n✅ Premium Quality Guaranteed\n✅ Fast Nationwide Delivery across Nigeria\n\n💬 Tap the link in bio or WhatsApp us to order yours today!`,
      },
      {
        title: 'Short & Punchy (Status / Reels)',
        text: `Quality you can trust! 😍 Grab your ${productName} today.\n\n${discountOffer ? `⚡ Offer: ${discountOffer}` : '⚡ Limited pieces remaining in stock.'}\n\n📩 DM to secure yours now!`,
      },
    ];
  };

  const captions = generateCaptions();

  const handleCopy = async (text: string, index: number) => {
    await navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2500);
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
          Marketing Caption Generator
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Generate persuasive promotional copy, sales announcements, and post captions for your business social media channels.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Input Form */}
        <div className="lg:col-span-6 bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">Product / Service Name *</label>
            <input
              type="text"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">Product Key Benefits / Features *</label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-700">Target Audience</label>
              <input
                type="text"
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
                className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-slate-50 focus:bg-white"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-700">Platform</label>
              <select
                value={platform}
                onChange={(e) => setPlatform(e.target.value)}
                className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-white"
              >
                <option value="WhatsApp">WhatsApp (Status & Broadcast)</option>
                <option value="Instagram">Instagram (Feed & Reels)</option>
                <option value="Facebook">Facebook</option>
                <option value="TikTok">TikTok Caption</option>
              </select>
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-700">Special Promo / Discount Offer (Optional)</label>
            <input
              type="text"
              value={discountOffer}
              onChange={(e) => setDiscountOffer(e.target.value)}
              placeholder="e.g. Free delivery within Kano / Abuja / Lagos"
              className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-slate-50 focus:bg-white"
            />
          </div>
        </div>

        {/* Results */}
        <div className="lg:col-span-6 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Suggested Captions
            </span>
            <span className="text-xs text-purple-700 font-semibold flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5" />
              Editable output
            </span>
          </div>

          {captions.map((cap, idx) => (
            <div
              key={idx}
              className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-3"
            >
              <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                <span className="text-xs font-bold text-purple-700">{cap.title}</span>
                <button
                  onClick={() => handleCopy(cap.text, idx)}
                  className="inline-flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-semibold bg-slate-100 hover:bg-purple-100 text-slate-700 hover:text-purple-800 transition"
                >
                  {copiedIndex === idx ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-600" />
                      <span>Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5" />
                      <span>Copy</span>
                    </>
                  )}
                </button>
              </div>

              <p className="text-xs sm:text-sm text-slate-700 whitespace-pre-line leading-relaxed">
                {cap.text}
              </p>
            </div>
          ))}
        </div>
      </div>

      <ServiceCTA
        headline="Need hands-free digital marketing & content creation?"
        description="Amee Technology Ltd creates complete social media content strategies, video production, graphic design, and targeted lead campaigns for Nigerian businesses."
        buttonText="Explore Digital Marketing Services"
        url="https://ameetechnology.com.ng/#services"
      />
    </div>
  );
}
