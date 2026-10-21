'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  FileSpreadsheet,
  Plus,
  Trash2,
  Printer,
  Download,
  RotateCcw,
  Eye,
  ArrowLeft,
  Building,
  User,
  Calendar,
} from 'lucide-react';
import { LineItem, calculateInvoiceTotals, calculateLineTotal } from '@/lib/calculations';
import { SUPPORTED_CURRENCIES, formatMoney } from '@/lib/currency';
import ServiceCTA from '@/components/ServiceCTA';

export default function QuotationGeneratorPage() {
  const [currency, setCurrency] = useState('NGN');
  const [logoUrl, setLogoUrl] = useState<string | null>(null);

  // Business Details
  const [businessName, setBusinessName] = useState('My Studio / Agency');
  const [businessEmail, setBusinessEmail] = useState('');
  const [businessPhone, setBusinessPhone] = useState('');
  const [businessAddress, setBusinessAddress] = useState('');

  // Customer Details
  const [clientName, setClientName] = useState('Prospective Client Ltd');
  const [clientEmail, setClientEmail] = useState('');

  // Quote Specifics
  const [quoteNumber, setQuoteNumber] = useState('QT-2026-01');
  const [quoteDate, setQuoteDate] = useState('2026-10-21');
  const [validUntil, setValidUntil] = useState('2026-11-20');
  const [scopeTerms, setScopeTerms] = useState(
    '1. 50% mobilization fee required upon contract signing.\n2. Project timeline begins upon receipt of deposit.\n3. Quote valid for 30 calendar days from issue date.'
  );

  // Line items
  const [items, setItems] = useState<LineItem[]>([
    {
      id: '1',
      description: 'Project Scope Milestone 1: Discovery & System Design',
      quantity: 1,
      unitPrice: 150000,
      discount: 0,
    },
    {
      id: '2',
      description: 'Project Scope Milestone 2: Implementation & Delivery',
      quantity: 1,
      unitPrice: 250000,
      discount: 0,
    },
  ]);

  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [isExporting, setIsExporting] = useState(false);

  const addItem = () => {
    setItems([
      ...items,
      { id: Date.now().toString(), description: '', quantity: 1, unitPrice: 0, discount: 0 },
    ]);
  };

  const removeItem = (id: string) => {
    if (items.length <= 1) return;
    setItems(items.filter((item) => item.id !== id));
  };

  const updateItem = (id: string, field: keyof LineItem, value: any) => {
    setItems(
      items.map((item) => (item.id === id ? { ...item, [field]: value } : item))
    );
  };

  const totals = calculateInvoiceTotals(items, 'fixed', 0, 0);

  const handlePrint = () => window.print();

  const handleDownloadPDF = async () => {
    try {
      setIsExporting(true);
      const html2canvas = (await import('html2canvas')).default;
      const { jsPDF } = await import('jspdf');

      const el = document.getElementById('quotation-preview-sheet');
      if (!el) return;

      const canvas = await html2canvas(el, { scale: 2, useCORS: true, logging: false });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`${quoteNumber.trim() || 'quotation'}.pdf`);
    } catch (err) {
      alert('Unable to generate PDF automatically. Use Print to PDF.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
      <div className="space-y-3">
        <Link
          href="/tools"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-purple-700 hover:text-purple-900 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to All Tools</span>
        </Link>

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
              Free Quotation & Estimate Generator
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              Create professional price quotes and scope estimates with validity dates and contract milestones.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setIsPreviewOpen(!isPreviewOpen)}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-purple-50 text-purple-700 hover:bg-purple-100 border border-purple-200 transition"
            >
              <Eye className="w-4 h-4" />
              <span>{isPreviewOpen ? 'Edit Quote' : 'Preview Quote'}</span>
            </button>
            <button
              onClick={handlePrint}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-white text-slate-700 hover:bg-slate-50 border border-slate-300 transition"
            >
              <Printer className="w-4 h-4" />
              <span>Print</span>
            </button>
            <button
              onClick={handleDownloadPDF}
              disabled={isExporting}
              className="inline-flex items-center gap-2 px-5 py-2 rounded-xl text-xs font-semibold bg-purple-600 hover:bg-purple-700 text-white shadow-sm transition disabled:opacity-50"
            >
              <Download className="w-4 h-4" />
              <span>{isExporting ? 'Generating PDF...' : 'Download PDF'}</span>
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Form Inputs */}
        <div className={`space-y-6 ${isPreviewOpen ? 'hidden lg:block lg:col-span-6' : 'lg:col-span-7'}`}>
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h2 className="font-bold text-slate-900 text-base">Issuer & Client Details</h2>
              <div className="flex items-center gap-2">
                <label className="text-xs font-medium text-slate-500">Currency:</label>
                <select
                  value={currency}
                  onChange={(e) => setCurrency(e.target.value)}
                  className="text-xs font-semibold border border-slate-300 rounded-lg px-2.5 py-1.5 bg-slate-50"
                >
                  {SUPPORTED_CURRENCIES.map((c) => (
                    <option key={c.code} value={c.code}>
                      {c.code} ({c.symbol})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Your Business Name *</label>
                <input
                  type="text"
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5"
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Client / Company Name *</label>
                <input
                  type="text"
                  value={clientName}
                  onChange={(e) => setClientName(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5"
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Quote Reference Number *</label>
                <input
                  type="text"
                  value={quoteNumber}
                  onChange={(e) => setQuoteNumber(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5"
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Valid Until Date *</label>
                <input
                  type="date"
                  value={validUntil}
                  onChange={(e) => setValidUntil(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5"
                />
              </div>
            </div>
          </div>

          {/* Items */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h2 className="font-bold text-slate-900 text-base">Proposed Deliverables / Scope</h2>
              <button
                type="button"
                onClick={addItem}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-purple-600 text-white"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add Item</span>
              </button>
            </div>

            <div className="space-y-3">
              {items.map((item, idx) => (
                <div key={item.id} className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-bold text-slate-500">Deliverable #{idx + 1}</span>
                    {items.length > 1 && (
                      <button onClick={() => removeItem(item.id)} className="text-red-500">
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-12 gap-2">
                    <input
                      type="text"
                      placeholder="Scope description"
                      value={item.description}
                      onChange={(e) => updateItem(item.id, 'description', e.target.value)}
                      className="sm:col-span-8 text-sm p-2 bg-white border border-slate-300 rounded-lg"
                    />
                    <input
                      type="number"
                      placeholder="Qty"
                      min="1"
                      value={item.quantity}
                      onChange={(e) => updateItem(item.id, 'quantity', Number(e.target.value))}
                      className="sm:col-span-2 text-sm p-2 bg-white border border-slate-300 rounded-lg"
                    />
                    <input
                      type="number"
                      placeholder="Price"
                      min="0"
                      value={item.unitPrice}
                      onChange={(e) => updateItem(item.id, 'unitPrice', Number(e.target.value))}
                      className="sm:col-span-2 text-sm p-2 bg-white border border-slate-300 rounded-lg"
                    />
                  </div>
                </div>
              ))}
            </div>

            <div className="space-y-1 pt-3">
              <label className="text-xs font-semibold text-slate-700">Terms & Conditions of Quote</label>
              <textarea
                rows={3}
                value={scopeTerms}
                onChange={(e) => setScopeTerms(e.target.value)}
                className="w-full text-xs p-2.5 border border-slate-300 rounded-lg"
              />
            </div>
          </div>
        </div>

        {/* Live Sheet */}
        <div className={`lg:col-span-5 ${!isPreviewOpen ? 'hidden lg:block' : 'col-span-12'}`}>
          <div className="sticky top-24 space-y-4">
            <div
              id="quotation-preview-sheet"
              className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-md text-xs sm:text-sm space-y-5"
            >
              <div className="flex justify-between items-start border-b border-slate-100 pb-4">
                <div>
                  <h3 className="font-extrabold text-base sm:text-lg text-slate-900">{businessName}</h3>
                  <p className="text-[11px] text-slate-500">Official Cost Estimate</p>
                </div>
                <div className="text-right">
                  <span className="text-lg font-black text-purple-700 uppercase">QUOTATION</span>
                  <p className="text-xs font-bold text-slate-800">#{quoteNumber}</p>
                  <p className="text-[11px] text-slate-500">Date: {quoteDate}</p>
                  <p className="text-[11px] text-purple-600 font-semibold">Valid Until: {validUntil}</p>
                </div>
              </div>

              <div className="bg-slate-50 p-3 rounded-xl">
                <span className="text-[10px] font-bold uppercase text-slate-400">Prepared For:</span>
                <p className="font-bold text-slate-900">{clientName}</p>
              </div>

              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b text-[10px] uppercase text-slate-500">
                    <th className="py-1.5">Scope Item</th>
                    <th className="py-1.5 text-center">Qty</th>
                    <th className="py-1.5 text-right">Estimate</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {items.map((item) => (
                    <tr key={item.id}>
                      <td className="py-2">{item.description || 'Deliverable'}</td>
                      <td className="py-2 text-center">{item.quantity}</td>
                      <td className="py-2 text-right font-medium">
                        {formatMoney(item.quantity * item.unitPrice, currency)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="border-t border-slate-200 pt-3 flex justify-between text-base font-bold text-slate-900">
                <span>Total Estimated Project Cost:</span>
                <span className="text-purple-700">{formatMoney(totals.subtotal, currency)}</span>
              </div>

              {scopeTerms && (
                <div className="border-t border-slate-100 pt-3">
                  <span className="text-[10px] font-bold uppercase text-slate-400">Quote Terms:</span>
                  <p className="text-[11px] text-slate-600 whitespace-pre-line leading-relaxed mt-1">
                    {scopeTerms}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <ServiceCTA
        headline="Need complex proposal systems or enterprise web apps?"
        description="Amee Technology Ltd partners with agencies and enterprises to deliver modern software systems, APIs, and digital platforms."
        buttonText="Schedule a Consultation"
        url="https://ameetechnology.com.ng/#contact"
      />
    </div>
  );
}
