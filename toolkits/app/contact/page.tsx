'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Mail,
  Phone,
  MessageCircle,
  ArrowLeft,
  Send,
  CheckCircle2,
  Building,
} from 'lucide-react';

export default function ContactPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [service, setService] = useState('Website Design & Development');
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !phone) {
      alert('Please provide your name and phone number.');
      return;
    }

    // Direct inquiry to WhatsApp with prefilled message
    const inquiryText = `Hello Ameetech! My name is ${name}. I am inquiring about *${service}*.\nPhone: ${phone}\nEmail: ${email || 'N/A'}\nProject Details: ${message || 'I would like to request a quote/consultation.'}`;
    const waUrl = `https://wa.me/2348100015498?text=${encodeURIComponent(inquiryText)}`;

    setSubmitted(true);
    window.open(waUrl, '_blank');
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-12">
      <div className="space-y-3">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-purple-700 hover:text-purple-900 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Home</span>
        </Link>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Contact Ameetech
        </h1>
        <p className="text-base text-slate-600 leading-relaxed max-w-2xl">
          Have feedback on our free tools, or ready to discuss a custom website, software, or digital marketing project? Reach out to our team.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left: Contact Info */}
        <div className="lg:col-span-5 bg-gradient-to-br from-purple-900 to-slate-900 text-white p-6 sm:p-8 rounded-3xl space-y-6 shadow-md">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-purple-300">
              Direct Channels
            </span>
            <h2 className="text-xl font-bold text-white mt-1">
              AMEE TECHNOLOGY LTD
            </h2>
            <p className="text-xs text-purple-200/80 mt-1">
              RC: 7083049 · Registered Technology Provider in Nigeria
            </p>
          </div>

          <div className="space-y-4 text-sm">
            <a
              href="https://wa.me/2348100015498?text=Hello%20Ameetech%2C%20I%20have%20an%20inquiry%20regarding%20your%20services."
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-3 p-3.5 rounded-2xl bg-white/10 hover:bg-white/20 transition border border-white/10"
            >
              <div className="w-9 h-9 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0">
                <MessageCircle className="w-5 h-5" />
              </div>
              <div>
                <span className="text-xs text-purple-200 block">WhatsApp Chat</span>
                <span className="font-semibold text-white">+234 810 001 5498</span>
              </div>
            </a>

            <a
              href="tel:+2348100015498"
              className="flex items-center gap-3 p-3.5 rounded-2xl bg-white/10 hover:bg-white/20 transition border border-white/10"
            >
              <div className="w-9 h-9 rounded-xl bg-purple-500/20 text-purple-300 flex items-center justify-center shrink-0">
                <Phone className="w-5 h-5" />
              </div>
              <div>
                <span className="text-xs text-purple-200 block">Call Helpline</span>
                <span className="font-semibold text-white">+234 810 001 5498</span>
              </div>
            </a>

            <a
              href="mailto:support@ameetechnology.com.ng"
              className="flex items-center gap-3 p-3.5 rounded-2xl bg-white/10 hover:bg-white/20 transition border border-white/10"
            >
              <div className="w-9 h-9 rounded-xl bg-pink-500/20 text-pink-300 flex items-center justify-center shrink-0">
                <Mail className="w-5 h-5" />
              </div>
              <div>
                <span className="text-xs text-purple-200 block">Email Inquiries</span>
                <span className="font-semibold text-white">support@ameetechnology.com.ng</span>
              </div>
            </a>
          </div>

          <div className="pt-4 border-t border-white/10 text-xs text-purple-200/70 space-y-1">
            <p><strong>Parent Website:</strong> https://ameetechnology.com.ng</p>
            <p><strong>Response Time:</strong> Typically within 1 to 3 hours during Nigerian business hours (Mon – Sat).</p>
          </div>
        </div>

        {/* Right: Lead & Project Inquiry Form */}
        <div className="lg:col-span-7 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
          <h2 className="text-xl font-bold text-slate-900 border-b border-slate-100 pb-3">
            Send a Project or Service Inquiry
          </h2>

          {submitted ? (
            <div className="p-6 rounded-2xl bg-emerald-50 border border-emerald-200 text-center space-y-3">
              <CheckCircle2 className="w-10 h-10 text-emerald-600 mx-auto" />
              <h3 className="text-lg font-bold text-emerald-900">Inquiry Prepared!</h3>
              <p className="text-xs text-emerald-800 leading-relaxed max-w-sm mx-auto">
                Your project inquiry has been formatted and opened in WhatsApp for instant conversation with our team.
              </p>
              <button
                onClick={() => setSubmitted(false)}
                className="text-xs font-semibold text-purple-700 hover:underline pt-2 block mx-auto"
              >
                Send another inquiry
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700">Your Full Name *</label>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Aminu Muhammad"
                    className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700">Phone / WhatsApp Number *</label>
                  <input
                    type="text"
                    required
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="e.g. 08100015498"
                    className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700">Email Address (Optional)</label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700">Interested Service</label>
                  <select
                    value={service}
                    onChange={(e) => setService(e.target.value)}
                    className="w-full text-sm rounded-xl border border-slate-300 p-2.5 bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  >
                    <option value="Website Design & Development">Website Design & Development</option>
                    <option value="E-commerce Store Development">E-commerce Store Development</option>
                    <option value="Custom Software & Dashboards">Custom Software & Dashboards</option>
                    <option value="SEO & Search Engine Ranking">SEO & Search Optimization</option>
                    <option value="UI/UX & Brand Identity Design">UI/UX & Brand Design</option>
                    <option value="Digital Marketing & Social Ads">Digital Marketing & Social Ads</option>
                  </select>
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-700">
                  Project Description or Questions
                </label>
                <textarea
                  rows={4}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Tell us about your business, target timeline, or what you need built..."
                  className="w-full text-sm rounded-xl border border-slate-300 p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none"
                />
              </div>

              <button
                type="submit"
                className="w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl font-bold text-sm bg-purple-600 hover:bg-purple-700 text-white shadow-md hover:shadow-lg transition"
              >
                <Send className="w-4 h-4" />
                <span>Submit Inquiry via WhatsApp / Direct Desk</span>
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
