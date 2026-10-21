'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Receipt,
  Printer,
  Download,
  RotateCcw,
  Eye,
  ArrowLeft,
  Building,
  CheckCircle,
  CreditCard,
  ShieldAlert,
} from 'lucide-react';
import { SUPPORTED_CURRENCIES, formatMoney } from '@/lib/currency';
import ServiceCTA from '@/components/ServiceCTA';

export default function ReceiptGeneratorPage() {
  const [currency, setCurrency] = useState('NGN');
  const [logoUrl, setLogoUrl] = useState<string | null>(null);

  // Business Details
  const [businessName, setBusinessName] = useState('My Business Ltd');
  const [businessPhone, setBusinessPhone] = useState('');
  const [businessEmail, setBusinessEmail] = useState('');
  const [businessAddress, setBusinessAddress] = useState('');

  // Receipt Meta
  const [receiptNumber, setReceiptNumber] = useState('REC-1001');
  const [paymentDate, setPaymentDate] = useState('2026-10-21');
  const [customerName, setCustomerName] = useState('Customer / Payer Name');
  const [paymentMethod, setPaymentMethod] = useState('Bank Transfer');
  const [transactionRef, setTransactionRef] = useState('');

  // Transaction Description & Amount
  const [description, setDescription] = useState('Payment for products / consulting services rendered');
  const [amountPaid, setAmountPaid] = useState<number>(25000);
  const [balanceDue, setBalanceDue] = useState<number>(0);
  const [notes, setNotes] = useState('Payment received with thanks.');

  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [isExporting, setIsExporting] = useState(false);

  const handleLogoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 2 * 1024 * 1024) {
        alert('File size must be under 2MB.');
        return;
      }
      const reader = new FileReader();
      reader.onload = () => setLogoUrl(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const resetForm = () => {
    if (confirm('Are you sure you want to start a new receipt?')) {
      setReceiptNumber(`REC-${Math.floor(1000 + Math.random() * 9000)}`);
      setCustomerName('');
      setDescription('');
      setAmountPaid(0);
      setBalanceDue(0);
      setTransactionRef('');
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadPDF = async () => {
    try {
      setIsExporting(true);
      const html2canvas = (await import('html2canvas')).default;
      const { jsPDF } = await import('jspdf');

      const receiptElement = document.getElementById('receipt-preview-sheet');
      if (!receiptElement) {
        alert('Could not find receipt sheet for export.');
        return;
      }

      const canvas = await html2canvas(receiptElement, {
        scale: 2,
        useCORS: true,
        logging: false,
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a5',
      });

      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`${receiptNumber.trim() || 'receipt'}.pdf`);
    } catch (err) {
      console.error('PDF export failed:', err);
      alert('Unable to generate PDF automatically. You can use the "Print Receipt" option and save as PDF.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
      {/* Breadcrumb */}
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
              Free Receipt Generator
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              Issue professional, verified proof-of-payment receipts for bank transfers, cash, or POS transactions.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setIsPreviewOpen(!isPreviewOpen)}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-purple-50 text-purple-700 hover:bg-purple-100 border border-purple-200 transition"
            >
              <Eye className="w-4 h-4" />
              <span>{isPreviewOpen ? 'Edit Receipt' : 'Preview Receipt'}</span>
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
              className="inline-flex items-center gap-2 px-5 py-2 rounded-xl text-xs font-semibold bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm transition disabled:opacity-50"
            >
              <Download className="w-4 h-4" />
              <span>{isExporting ? 'Generating PDF...' : 'Download PDF'}</span>
            </button>
            <button
              onClick={resetForm}
              title="Reset receipt form"
              className="p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Editor Form */}
        <div className={`space-y-6 ${isPreviewOpen ? 'hidden lg:block lg:col-span-6' : 'lg:col-span-7'}`}>
          {/* Card: Issuer & Currency */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <Building className="w-5 h-5 text-purple-600" />
                <h2 className="font-bold text-slate-900 text-base">Issuer Information</h2>
              </div>
              <div className="flex items-center gap-2">
                <label className="text-xs font-medium text-slate-500">Currency:</label>
                <select
                  value={currency}
                  onChange={(e) => setCurrency(e.target.value)}
                  className="text-xs font-semibold border border-slate-300 rounded-lg px-2.5 py-1.5 bg-slate-50 focus:ring-1 focus:ring-purple-600"
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
                <label className="text-xs font-semibold text-slate-700">Business / Issuer Name *</label>
                <input
                  type="text"
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="Business Name"
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Phone Number</label>
                <input
                  type="text"
                  value={businessPhone}
                  onChange={(e) => setBusinessPhone(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="+234..."
                />
              </div>
              <div className="sm:col-span-2 space-y-1">
                <label className="text-xs font-semibold text-slate-700">Address / Location</label>
                <input
                  type="text"
                  value={businessAddress}
                  onChange={(e) => setBusinessAddress(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="Address or market stall"
                />
              </div>
              <div className="sm:col-span-2 pt-1">
                <label className="text-xs font-semibold text-slate-700 block mb-1">
                  Business Logo (Optional)
                </label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleLogoUpload}
                  className="text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
                />
              </div>
            </div>
          </div>

          {/* Card: Payment Specifics */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
              <CreditCard className="w-5 h-5 text-purple-600" />
              <h2 className="font-bold text-slate-900 text-base">Payment Details</h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Receipt Number *</label>
                <input
                  type="text"
                  value={receiptNumber}
                  onChange={(e) => setReceiptNumber(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Payment Date *</label>
                <input
                  type="date"
                  value={paymentDate}
                  onChange={(e) => setPaymentDate(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Received From (Customer Name)</label>
                <input
                  type="text"
                  value={customerName}
                  onChange={(e) => setCustomerName(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="Customer Name"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Payment Method *</label>
                <select
                  value={paymentMethod}
                  onChange={(e) => setPaymentMethod(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none"
                >
                  <option value="Bank Transfer">Bank Transfer</option>
                  <option value="Cash">Cash</option>
                  <option value="POS / Debit Card">POS / Debit Card</option>
                  <option value="USSD">USSD</option>
                  <option value="Online Payment Gateway">Online Gateway / Card</option>
                  <option value="Cheque">Cheque</option>
                </select>
              </div>

              <div className="sm:col-span-2 space-y-1">
                <label className="text-xs font-semibold text-slate-700">
                  Transaction Reference / Session ID (Optional)
                </label>
                <input
                  type="text"
                  value={transactionRef}
                  onChange={(e) => setTransactionRef(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="e.g. NIP session ID, POS Ref #, or Cheque #"
                />
              </div>

              <div className="sm:col-span-2 space-y-1">
                <label className="text-xs font-semibold text-slate-700">
                  Payment Description / Purpose *
                </label>
                <textarea
                  rows={2}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="Goods purchased or services provided..."
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">
                  Total Amount Received ({currency}) *
                </label>
                <input
                  type="number"
                  min="0"
                  step="any"
                  value={amountPaid}
                  onChange={(e) => setAmountPaid(Number(e.target.value))}
                  className="w-full text-base font-bold text-slate-900 rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">
                  Remaining Balance Due ({currency})
                </label>
                <input
                  type="number"
                  min="0"
                  step="any"
                  value={balanceDue}
                  onChange={(e) => setBalanceDue(Number(e.target.value))}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="0.00"
                />
              </div>

              <div className="sm:col-span-2 space-y-1">
                <label className="text-xs font-semibold text-slate-700">Additional Remarks / Notes</label>
                <input
                  type="text"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Live Document Preview Sheet */}
        <div className={`lg:col-span-5 ${!isPreviewOpen ? 'hidden lg:block' : 'col-span-12'}`}>
          <div className="sticky top-24 space-y-4">
            <div className="flex items-center justify-between px-1">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Official Receipt Preview
              </span>
              <span className="text-[11px] text-emerald-700 font-medium bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                Proof of Payment
              </span>
            </div>

            {/* Printable Sheet */}
            <div
              id="receipt-preview-sheet"
              className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-md text-slate-900 text-xs sm:text-sm font-sans space-y-6"
            >
              {/* Header */}
              <div className="flex items-start justify-between gap-4 border-b border-slate-100 pb-5">
                <div className="space-y-1">
                  {logoUrl && (
                    <div className="relative w-24 h-12 mb-2">
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img
                        src={logoUrl}
                        alt="Logo"
                        className="object-contain max-h-12 max-w-24"
                      />
                    </div>
                  )}
                  <h3 className="font-extrabold text-base sm:text-lg text-slate-900">
                    {businessName || 'Business Name'}
                  </h3>
                  {businessAddress && (
                    <p className="text-[11px] text-slate-600">{businessAddress}</p>
                  )}
                  {businessPhone && (
                    <p className="text-[11px] text-slate-600">{businessPhone}</p>
                  )}
                </div>

                <div className="text-right space-y-1">
                  <div className="inline-block px-3 py-1 bg-emerald-600 text-white rounded-lg text-xs font-black uppercase tracking-wider">
                    PAYMENT RECEIPT
                  </div>
                  <p className="text-xs font-bold text-slate-800">#{receiptNumber}</p>
                  <p className="text-[11px] text-slate-500">Date: {paymentDate}</p>
                </div>
              </div>

              {/* Main Receipt Details Box */}
              <div className="space-y-3 bg-slate-50 p-4 rounded-xl border border-slate-100">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-500 font-medium">Received From:</span>
                  <span className="font-bold text-slate-900 text-sm">{customerName || 'Customer'}</span>
                </div>

                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-500 font-medium">Payment Method:</span>
                  <span className="font-semibold text-slate-800">{paymentMethod}</span>
                </div>

                {transactionRef && (
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-slate-500 font-medium">Transaction Ref:</span>
                    <span className="font-mono text-slate-700 text-[11px]">{transactionRef}</span>
                  </div>
                )}
              </div>

              {/* Description */}
              <div className="space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  Payment For:
                </span>
                <p className="text-xs text-slate-800 leading-relaxed font-medium bg-slate-50/50 p-3 rounded-lg border border-slate-100">
                  {description || 'Goods / Services'}
                </p>
              </div>

              {/* Amount Paid Callout */}
              <div className="bg-emerald-50 border border-emerald-200/80 rounded-xl p-4 flex items-center justify-between">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 block">
                    Amount Received
                  </span>
                  <span className="text-xl sm:text-2xl font-black text-emerald-700">
                    {formatMoney(amountPaid, currency)}
                  </span>
                </div>
                <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-700">
                  <CheckCircle className="w-6 h-6" />
                </div>
              </div>

              {balanceDue > 0 && (
                <div className="flex justify-between items-center text-xs text-red-600 font-semibold px-1">
                  <span>Outstanding Balance:</span>
                  <span>{formatMoney(balanceDue, currency)}</span>
                </div>
              )}

              {/* Notes */}
              {notes && (
                <div className="border-t border-slate-100 pt-3">
                  <p className="text-[11px] text-slate-500 italic">{notes}</p>
                </div>
              )}

              {/* Legal Verification Disclaimer */}
              <div className="pt-3 border-t border-slate-100 flex items-start gap-1.5 text-[9px] text-slate-600 leading-tight">
                <ShieldAlert className="w-3.5 h-3.5 shrink-0 text-slate-600 mt-0.5" />
                <span>
                  Notice: This document records payment details submitted by the issuer. Ameetech Toolkits is a document generator and does not independently audit or verify banking transactions.
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Contextual Ameetech CTA */}
      <ServiceCTA
        headline="Need custom POS, billing software, or financial dashboards?"
        description="Amee Technology Ltd builds custom inventory management, retail billing, and fintech software tailored to your specific operations."
        buttonText="Consult Our Engineering Team"
        url="https://ameetechnology.com.ng/#contact"
      />
    </div>
  );
}
