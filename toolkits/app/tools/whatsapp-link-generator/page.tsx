'use client';

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import {
  MessageSquare,
  ArrowLeft,
  Copy,
  ExternalLink,
  Check,
  QrCode,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';
import { normalizePhoneNumber, buildWhatsAppLink } from '@/lib/phone';
import ServiceCTA from '@/components/ServiceCTA';

const MESSAGE_TEMPLATES = [
  {
    title: 'Product Inquiry',
    text: 'Hello! I saw your catalog and would like to inquire about pricing and product availability.',
  },
  {
    title: 'Order Placement',
    text: 'Hi there, I would like to place an order for delivery. Please share your catalog and payment details.',
  },
  {
    title: 'Customer Support',
    text: 'Hello Support team, I have a question regarding my recent order.',
  },
  {
    title: 'Service Booking',
    text: 'Good day! I would like to schedule a consultation/appointment for your services.',
  },
];

export default function WhatsAppLinkGeneratorPage() {
  const [phoneNumber, setPhoneNumber] = useState('08100015498');
  const [countryCode, setCountryCode] = useState('234');
  const [customMessage, setCustomMessage] = useState('Hi! I saw your business online and would like to make an inquiry.');
  const [copied, setCopied] = useState(false);

  const phoneValidation = useMemo(() => {
    return normalizePhoneNumber(phoneNumber, countryCode);
  }, [phoneNumber, countryCode]);

  const generatedLink = useMemo(() => {
    if (!phoneValidation.isValid) return '';
    return buildWhatsAppLink(phoneNumber, customMessage);
  }, [phoneValidation, phoneNumber, customMessage]);

  const copyToClipboard = async () => {
    if (!generatedLink) return;
    try {
      await navigator.clipboard.writeText(generatedLink);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch (err) {
      alert('Could not copy automatically. You can highlight the link and copy.');
    }
  };

  const qrCodeUrl = useMemo(() => {
    if (!generatedLink) return '';
    // Standard public QR Code generation service via quickchart / api
    return `https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=${encodeURIComponent(
      generatedLink
    )}`;
  }, [generatedLink]);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
      {/* Breadcrumb & Intro */}
      <div className="space-y-3">
        <Link
          href="/tools"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-purple-700 hover:text-purple-900 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to All Tools</span>
        </Link>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
              WhatsApp Link Generator
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              Create instant click-to-chat WhatsApp links with customized greetings for your social media bios, cards, and ads.
            </p>
          </div>
        </div>
      </div>

      {/* Main Form & Link Preview Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left: Input Configurations */}
        <div className="lg:col-span-7 bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-4">
            <MessageSquare className="w-5 h-5 text-emerald-600" />
            <h2 className="font-bold text-slate-900 text-base">Configure Your Link</h2>
          </div>

          <div className="space-y-4">
            {/* Phone Number Input */}
            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-700">
                WhatsApp Phone Number *
              </label>
              <div className="flex gap-2">
                <select
                  value={countryCode}
                  onChange={(e) => setCountryCode(e.target.value)}
                  className="w-32 text-xs font-semibold border border-slate-300 rounded-xl px-3 py-2.5 bg-slate-50"
                >
                  <option value="234">Nigeria (+234)</option>
                  <option value="1">US/Canada (+1)</option>
                  <option value="44">UK (+44)</option>
                  <option value="233">Ghana (+233)</option>
                  <option value="254">Kenya (+254)</option>
                  <option value="27">South Africa (+27)</option>
                </select>

                <input
                  type="text"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  placeholder="e.g. 08100015498"
                  className="flex-1 text-sm rounded-xl border border-slate-300 p-2.5 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none transition"
                />
              </div>

              {!phoneValidation.isValid && (
                <p className="text-xs text-red-600 pt-1">
                  {phoneValidation.errorMessage || 'Please check your phone number.'}
                </p>
              )}
              {phoneValidation.isValid && (
                <p className="text-[11px] text-emerald-600 font-medium pt-1">
                  ✓ Formatted international number: +{phoneValidation.normalizedNumber}
                </p>
              )}
            </div>

            {/* Prefilled Message */}
            <div className="space-y-1">
              <div className="flex justify-between items-center">
                <label className="text-xs font-bold text-slate-700">
                  Default Greeting / Prefilled Message
                </label>
                <span className="text-[11px] text-slate-600">Optional</span>
              </div>
              <textarea
                rows={4}
                value={customMessage}
                onChange={(e) => setCustomMessage(e.target.value)}
                placeholder="Type the message customers will send when they click your link..."
                className="w-full text-sm rounded-xl border border-slate-300 p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none transition"
              />
            </div>

            {/* Quick Templates */}
            <div className="space-y-2 pt-2">
              <span className="text-xs font-bold text-slate-600 flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5 text-purple-600" />
                Quick Message Ideas (Click to use)
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {MESSAGE_TEMPLATES.map((tmpl, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => setCustomMessage(tmpl.text)}
                    className="p-2.5 text-left rounded-xl border border-slate-200 bg-slate-50/60 hover:bg-purple-50 hover:border-purple-200 transition text-xs space-y-0.5"
                  >
                    <span className="font-semibold text-slate-800 block">{tmpl.title}</span>
                    <span className="text-slate-500 line-clamp-1 text-[11px]">{tmpl.text}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right: Generated Output & QR Code */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <h3 className="font-bold text-slate-900 text-base">Your Generated Link</h3>
              {generatedLink && (
                <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                  Ready to Share
                </span>
              )}
            </div>

            {generatedLink ? (
              <div className="space-y-4">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs font-mono break-all text-slate-700 select-all">
                  {generatedLink}
                </div>

                <div className="flex flex-col sm:flex-row gap-2">
                  <button
                    onClick={copyToClipboard}
                    className="flex-1 inline-flex items-center justify-center gap-2 px-4 py-3 rounded-xl font-semibold text-sm bg-purple-600 hover:bg-purple-700 text-white shadow-sm transition"
                  >
                    {copied ? (
                      <>
                        <Check className="w-4 h-4 text-emerald-300" />
                        <span>Copied to Clipboard!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4" />
                        <span>Copy WhatsApp Link</span>
                      </>
                    )}
                  </button>

                  <a
                    href={generatedLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center gap-2 px-4 py-3 rounded-xl font-semibold text-sm bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm transition"
                  >
                    <ExternalLink className="w-4 h-4" />
                    <span>Test Chat</span>
                  </a>
                </div>

                {/* QR Code Section */}
                <div className="pt-4 border-t border-slate-100 text-center space-y-3">
                  <div className="flex items-center justify-center gap-1.5 text-xs font-bold text-slate-700">
                    <QrCode className="w-4 h-4 text-purple-600" />
                    <span>Printable QR Code</span>
                  </div>
                  <p className="text-[11px] text-slate-600 max-w-xs mx-auto">
                    Customers can scan this directly using their phone camera or WhatsApp scanner.
                  </p>
                  <div className="w-48 h-48 mx-auto p-2 bg-white rounded-2xl border border-slate-200 shadow-sm flex items-center justify-center">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src={qrCodeUrl}
                      alt="WhatsApp QR Code"
                      className="w-full h-full object-contain"
                    />
                  </div>
                  <a
                    href={qrCodeUrl}
                    download="whatsapp-qr-code.png"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block text-xs font-semibold text-purple-700 hover:underline"
                  >
                    Open full-size QR image ↗
                  </a>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-sm text-slate-400">
                Enter a valid phone number on the left to generate your WhatsApp link and QR code.
              </div>
            )}
          </div>

          <div className="flex items-center gap-2 p-3 bg-slate-100 rounded-xl text-xs text-slate-500">
            <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>We never store your phone number or prefilled messages.</span>
          </div>
        </div>
      </div>

      {/* Contextual Ameetech CTA */}
      <ServiceCTA
        headline="Want to turn more WhatsApp clicks into paying customers?"
        description="Amee Technology Ltd creates automated WhatsApp chatbots, CRM integrations, and high-converting marketing campaigns that capture and convert qualified leads automatically."
        buttonText="Explore Digital Marketing Services"
        url="https://ameetechnology.com.ng/#services"
      />
    </div>
  );
}
