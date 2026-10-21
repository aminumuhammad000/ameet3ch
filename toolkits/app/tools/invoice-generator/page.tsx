'use client';

import React, { useState, useId } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import {
  FileText,
  Plus,
  Trash2,
  Printer,
  Download,
  RotateCcw,
  Eye,
  ArrowLeft,
  Building,
  User,
  CreditCard,
  CheckCircle,
  HelpCircle,
} from 'lucide-react';
import {
  LineItem,
  calculateInvoiceTotals,
  calculateLineTotal,
} from '@/lib/calculations';
import { SUPPORTED_CURRENCIES, formatMoney } from '@/lib/currency';
import ServiceCTA from '@/components/ServiceCTA';

export default function InvoiceGeneratorPage() {
  const [currency, setCurrency] = useState('NGN');
  const [logoUrl, setLogoUrl] = useState<string | null>(null);

  // Business Details
  const [businessName, setBusinessName] = useState('My Business Ltd');
  const [businessEmail, setBusinessEmail] = useState('');
  const [businessPhone, setBusinessPhone] = useState('');
  const [businessAddress, setBusinessAddress] = useState('');
  const [businessRegNo, setBusinessRegNo] = useState('');

  // Customer Details
  const [customerName, setCustomerName] = useState('Valued Client');
  const [customerEmail, setCustomerEmail] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [customerAddress, setCustomerAddress] = useState('');

  // Invoice Details
  const [invoiceNumber, setInvoiceNumber] = useState('INV-001');
  const [issueDate, setIssueDate] = useState('2026-10-21');
  const [dueDate, setDueDate] = useState('');
  const [paymentTerms, setPaymentTerms] = useState('Payment due within 14 days of issue.');
  const [bankDetails, setBankDetails] = useState('Bank: First Bank Nigeria\nAccount: 1234567890\nName: My Business Ltd');
  const [notes, setNotes] = useState('Thank you for your business!');

  // Discount & Tax
  const [discountType, setDiscountType] = useState<'fixed' | 'percentage'>('fixed');
  const [discountValue, setDiscountValue] = useState<number>(0);
  const [taxRate, setTaxRate] = useState<number>(0);

  // Line items
  const [items, setItems] = useState<LineItem[]>([
    {
      id: '1',
      description: 'Professional Service / Product Delivery',
      quantity: 1,
      unitPrice: 50000,
      discount: 0,
    },
  ]);

  // Preview Mode
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [isExporting, setIsExporting] = useState(false);

  // File upload handler for logo
  const handleLogoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 2 * 1024 * 1024) {
        alert('Logo file size must be less than 2MB.');
        return;
      }
      const reader = new FileReader();
      reader.onload = () => {
        setLogoUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const addItem = () => {
    const newItem: LineItem = {
      id: Date.now().toString(),
      description: '',
      quantity: 1,
      unitPrice: 0,
      discount: 0,
    };
    setItems([...items, newItem]);
  };

  const removeItem = (id: string) => {
    if (items.length <= 1) {
      alert('Invoice must contain at least one line item.');
      return;
    }
    setItems(items.filter((item) => item.id !== id));
  };

  const updateItem = (id: string, field: keyof LineItem, value: any) => {
    setItems(
      items.map((item) => {
        if (item.id === id) {
          return { ...item, [field]: value };
        }
        return item;
      })
    );
  };

  const totals = calculateInvoiceTotals(items, discountType, discountValue, taxRate);

  const resetForm = () => {
    if (confirm('Are you sure you want to start a new invoice? Unsaved data will be reset.')) {
      setInvoiceNumber(`INV-${Math.floor(100 + Math.random() * 900)}`);
      setItems([
        {
          id: Date.now().toString(),
          description: '',
          quantity: 1,
          unitPrice: 0,
          discount: 0,
        },
      ]);
      setCustomerName('');
      setCustomerEmail('');
      setCustomerPhone('');
      setCustomerAddress('');
      setDiscountValue(0);
      setTaxRate(0);
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

      const invoiceElement = document.getElementById('invoice-preview-sheet');
      if (!invoiceElement) {
        alert('Could not find invoice sheet for export.');
        return;
      }

      const canvas = await html2canvas(invoiceElement, {
        scale: 2,
        useCORS: true,
        logging: false,
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4',
      });

      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`${invoiceNumber.trim() || 'invoice'}.pdf`);
    } catch (err) {
      console.error('PDF export failed:', err);
      alert('Unable to generate PDF automatically. You can use the "Print Invoice" option and save as PDF.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
      {/* Breadcrumb & Intro */}
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
              Free Invoice Generator
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              Create professional, branded PDF invoices with customized line items, discounts, and banking details.
            </p>
          </div>

          {/* Action Bar */}
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setIsPreviewOpen(!isPreviewOpen)}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-purple-50 text-purple-700 hover:bg-purple-100 border border-purple-200 transition"
            >
              <Eye className="w-4 h-4" />
              <span>{isPreviewOpen ? 'Edit Invoice' : 'Preview Invoice'}</span>
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
            <button
              onClick={resetForm}
              title="Reset invoice form"
              className="p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Workspace: Form & Interactive Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Editor Form */}
        <div className={`space-y-8 ${isPreviewOpen ? 'hidden lg:block lg:col-span-6' : 'lg:col-span-7'}`}>
          {/* Card 1: Business Details & Invoice Meta */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2">
                <Building className="w-5 h-5 text-purple-600" />
                <h2 className="font-bold text-slate-900 text-base">Your Business Details</h2>
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
                <label className="text-xs font-semibold text-slate-700">Business Name *</label>
                <input
                  type="text"
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="e.g. Zenith Global Enterprises"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Registration / Tax ID (Optional)</label>
                <input
                  type="text"
                  value={businessRegNo}
                  onChange={(e) => setBusinessRegNo(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="e.g. RC 1234567 or TIN"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Email Address</label>
                <input
                  type="email"
                  value={businessEmail}
                  onChange={(e) => setBusinessEmail(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="info@business.com"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Phone Number</label>
                <input
                  type="text"
                  value={businessPhone}
                  onChange={(e) => setBusinessPhone(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="+234 810 000 0000"
                />
              </div>

              <div className="sm:col-span-2 space-y-1">
                <label className="text-xs font-semibold text-slate-700">Business Address</label>
                <input
                  type="text"
                  value={businessAddress}
                  onChange={(e) => setBusinessAddress(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="Office address, City, State"
                />
              </div>

              <div className="sm:col-span-2 pt-2">
                <label className="text-xs font-semibold text-slate-700 block mb-1">
                  Business Logo (Optional, Max 2MB)
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

          {/* Card 2: Customer & Invoice Timing */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-6">
            <div className="flex items-center gap-2 border-b border-slate-100 pb-4">
              <User className="w-5 h-5 text-purple-600" />
              <h2 className="font-bold text-slate-900 text-base">Client & Invoice Details</h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Invoice Number *</label>
                <input
                  type="text"
                  value={invoiceNumber}
                  onChange={(e) => setInvoiceNumber(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Issue Date *</label>
                <input
                  type="date"
                  value={issueDate}
                  onChange={(e) => setIssueDate(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Due Date (Optional)</label>
                <input
                  type="date"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Client / Customer Name *</label>
                <input
                  type="text"
                  value={customerName}
                  onChange={(e) => setCustomerName(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="Client or Company Name"
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Client Email / Phone</label>
                <input
                  type="text"
                  value={customerEmail}
                  onChange={(e) => setCustomerEmail(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="client@gmail.com or 080..."
                />
              </div>
              <div className="sm:col-span-2 space-y-1">
                <label className="text-xs font-semibold text-slate-700">Client Billing Address (Optional)</label>
                <input
                  type="text"
                  value={customerAddress}
                  onChange={(e) => setCustomerAddress(e.target.value)}
                  className="w-full text-sm rounded-lg border border-slate-300 p-2.5 focus:ring-2 focus:ring-purple-600 focus:outline-none"
                  placeholder="Street, City, Country"
                />
              </div>
            </div>
          </div>

          {/* Card 3: Line Items */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <h2 className="font-bold text-slate-900 text-base">Line Items</h2>
              <button
                type="button"
                onClick={addItem}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-purple-600 hover:bg-purple-700 text-white transition"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add Item</span>
              </button>
            </div>

            <div className="space-y-4">
              {items.map((item, index) => {
                const lineTotal = calculateLineTotal(item.quantity, item.unitPrice, item.discount);
                return (
                  <div
                    key={item.id}
                    className="p-4 rounded-xl border border-slate-200/90 bg-slate-50/50 space-y-3 relative group"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                        Item #{index + 1}
                      </span>
                      {items.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeItem(item.id)}
                          className="text-red-500 hover:text-red-700 p-1 rounded-md transition"
                          title="Remove item"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-12 gap-3">
                      <div className="sm:col-span-6 space-y-1">
                        <label className="text-[11px] font-semibold text-slate-600">
                          Description *
                        </label>
                        <input
                          type="text"
                          value={item.description}
                          onChange={(e) => updateItem(item.id, 'description', e.target.value)}
                          placeholder="Product or service delivered"
                          className="w-full text-sm rounded-lg border border-slate-300 p-2 bg-white focus:ring-1 focus:ring-purple-600"
                        />
                      </div>
                      <div className="sm:col-span-2 space-y-1">
                        <label className="text-[11px] font-semibold text-slate-600">Qty</label>
                        <input
                          type="number"
                          min="1"
                          value={item.quantity}
                          onChange={(e) => updateItem(item.id, 'quantity', Number(e.target.value))}
                          className="w-full text-sm rounded-lg border border-slate-300 p-2 bg-white focus:ring-1 focus:ring-purple-600"
                        />
                      </div>
                      <div className="sm:col-span-4 space-y-1">
                        <label className="text-[11px] font-semibold text-slate-600">
                          Price ({currency})
                        </label>
                        <input
                          type="number"
                          min="0"
                          step="any"
                          value={item.unitPrice}
                          onChange={(e) => updateItem(item.id, 'unitPrice', Number(e.target.value))}
                          className="w-full text-sm rounded-lg border border-slate-300 p-2 bg-white focus:ring-1 focus:ring-purple-600"
                        />
                      </div>
                    </div>

                    <div className="flex items-center justify-between pt-2 border-t border-slate-200/60 text-xs">
                      <span className="text-slate-500">
                        Line Total: <strong>{formatMoney(lineTotal, currency)}</strong>
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Calculations Breakdown */}
            <div className="pt-4 border-t border-slate-200 space-y-3 bg-slate-50 p-4 rounded-xl">
              <div className="flex justify-between text-sm text-slate-600">
                <span>Subtotal:</span>
                <span className="font-semibold text-slate-900">
                  {formatMoney(totals.subtotal, currency)}
                </span>
              </div>

              {/* Discount Options */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                <div className="space-y-1">
                  <label className="text-xs font-semibold text-slate-700">Discount Type</label>
                  <select
                    value={discountType}
                    onChange={(e) => setDiscountType(e.target.value as any)}
                    className="w-full text-xs rounded-lg border border-slate-300 p-2 bg-white"
                  >
                    <option value="fixed">Fixed Amount ({currency})</option>
                    <option value="percentage">Percentage (%)</option>
                  </select>
                </div>
                <div className="space-y-1">
                  <label className="text-xs font-semibold text-slate-700">
                    Discount {discountType === 'percentage' ? '(%)' : `(${currency})`}
                  </label>
                  <input
                    type="number"
                    min="0"
                    value={discountValue}
                    onChange={(e) => setDiscountValue(Number(e.target.value))}
                    className="w-full text-xs rounded-lg border border-slate-300 p-2 bg-white"
                  />
                </div>
              </div>

              {/* Tax Rate */}
              <div className="space-y-1 pt-2">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-semibold text-slate-700">
                    Applicable Tax Rate (% VAT / Sales Tax)
                  </label>
                  <span className="text-[11px] text-slate-600">Optional</span>
                </div>
                <input
                  type="number"
                  min="0"
                  max="100"
                  step="0.1"
                  value={taxRate}
                  onChange={(e) => setTaxRate(Number(e.target.value))}
                  placeholder="e.g. 7.5"
                  className="w-full text-xs rounded-lg border border-slate-300 p-2 bg-white"
                />
              </div>

              {totals.taxAmount > 0 && (
                <div className="flex justify-between text-xs text-slate-600 pt-1">
                  <span>Tax Amount ({taxRate}%):</span>
                  <span>+{formatMoney(totals.taxAmount, currency)}</span>
                </div>
              )}

              {totals.discountAmount > 0 && (
                <div className="flex justify-between text-xs text-emerald-700 pt-1">
                  <span>Discount Applied:</span>
                  <span>-{formatMoney(totals.discountAmount, currency)}</span>
                </div>
              )}

              <div className="flex justify-between text-base font-bold text-slate-900 border-t border-slate-200 pt-3">
                <span>Grand Total:</span>
                <span className="text-purple-700">{formatMoney(totals.grandTotal, currency)}</span>
              </div>
            </div>
          </div>

          {/* Card 4: Payment Info & Notes */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
              <CreditCard className="w-5 h-5 text-purple-600" />
              <h2 className="font-bold text-slate-900 text-base">Payment Details & Terms</h2>
            </div>

            <div className="space-y-3">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">
                  Bank Account / Payment Instructions
                </label>
                <textarea
                  rows={3}
                  value={bankDetails}
                  onChange={(e) => setBankDetails(e.target.value)}
                  className="w-full text-xs rounded-lg border border-slate-300 p-2.5 focus:ring-1 focus:ring-purple-600 focus:outline-none"
                  placeholder="Bank Name, Account Number, Account Name..."
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-700">Notes & Terms</label>
                <textarea
                  rows={2}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className="w-full text-xs rounded-lg border border-slate-300 p-2.5 focus:ring-1 focus:ring-purple-600 focus:outline-none"
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
                A4 Document Live Preview
              </span>
              <span className="text-[11px] text-emerald-600 font-medium">Ready to print or download</span>
            </div>

            {/* Printable & Exportable Canvas Sheet */}
            <div
              id="invoice-preview-sheet"
              className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-md text-slate-900 text-xs sm:text-sm font-sans space-y-6"
            >
              {/* Header */}
              <div className="flex items-start justify-between gap-4 border-b border-slate-100 pb-6">
                <div className="space-y-1">
                  {logoUrl ? (
                    <div className="relative w-24 h-12 mb-2">
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img
                        src={logoUrl}
                        alt="Logo"
                        className="object-contain max-h-12 max-w-24"
                      />
                    </div>
                  ) : null}
                  <h3 className="font-extrabold text-lg sm:text-xl text-slate-900">
                    {businessName || 'Business Name'}
                  </h3>
                  {businessRegNo && (
                    <p className="text-[11px] text-slate-500">Reg: {businessRegNo}</p>
                  )}
                  {businessAddress && (
                    <p className="text-[11px] text-slate-600">{businessAddress}</p>
                  )}
                  {businessEmail && (
                    <p className="text-[11px] text-slate-600">{businessEmail}</p>
                  )}
                  {businessPhone && (
                    <p className="text-[11px] text-slate-600">{businessPhone}</p>
                  )}
                </div>

                <div className="text-right space-y-1">
                  <span className="inline-block text-xl sm:text-2xl font-black uppercase tracking-wider text-purple-700">
                    INVOICE
                  </span>
                  <p className="text-xs font-bold text-slate-800">#{invoiceNumber}</p>
                  <p className="text-[11px] text-slate-500">Date: {issueDate}</p>
                  {dueDate && <p className="text-[11px] text-red-600 font-medium">Due: {dueDate}</p>}
                </div>
              </div>

              {/* Billed To */}
              <div className="bg-slate-50 p-3.5 rounded-xl space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  Billed To:
                </span>
                <p className="font-bold text-slate-900 text-sm">
                  {customerName || 'Customer / Client Name'}
                </p>
                {customerAddress && (
                  <p className="text-xs text-slate-600">{customerAddress}</p>
                )}
                {customerEmail && (
                  <p className="text-xs text-slate-600">{customerEmail}</p>
                )}
              </div>

              {/* Items Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-slate-200 text-slate-500 uppercase tracking-wider text-[10px]">
                      <th className="py-2">Item Description</th>
                      <th className="py-2 text-center">Qty</th>
                      <th className="py-2 text-right">Price</th>
                      <th className="py-2 text-right">Total</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {items.map((item) => (
                      <tr key={item.id}>
                        <td className="py-2.5 font-medium text-slate-800">
                          {item.description || 'Service/Product item'}
                        </td>
                        <td className="py-2.5 text-center text-slate-600">{item.quantity}</td>
                        <td className="py-2.5 text-right text-slate-600">
                          {formatMoney(item.unitPrice, currency)}
                        </td>
                        <td className="py-2.5 text-right font-semibold text-slate-900">
                          {formatMoney(
                            calculateLineTotal(item.quantity, item.unitPrice, item.discount),
                            currency
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Totals Summary */}
              <div className="border-t border-slate-200 pt-4 space-y-1.5 text-xs text-slate-600">
                <div className="flex justify-between">
                  <span>Subtotal:</span>
                  <span className="font-semibold text-slate-900">
                    {formatMoney(totals.subtotal, currency)}
                  </span>
                </div>
                {totals.discountAmount > 0 && (
                  <div className="flex justify-between text-emerald-700">
                    <span>Discount:</span>
                    <span>-{formatMoney(totals.discountAmount, currency)}</span>
                  </div>
                )}
                {totals.taxAmount > 0 && (
                  <div className="flex justify-between">
                    <span>Tax ({taxRate}%):</span>
                    <span>+{formatMoney(totals.taxAmount, currency)}</span>
                  </div>
                )}
                <div className="flex justify-between text-sm sm:text-base font-bold text-slate-900 border-t border-slate-200 pt-2 text-purple-700">
                  <span>Grand Total:</span>
                  <span>{formatMoney(totals.grandTotal, currency)}</span>
                </div>
              </div>

              {/* Payment Details in preview */}
              {bankDetails && (
                <div className="border-t border-slate-100 pt-4 space-y-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                    Payment Instructions:
                  </span>
                  <p className="text-[11px] text-slate-700 whitespace-pre-line leading-relaxed">
                    {bankDetails}
                  </p>
                </div>
              )}

              {/* Notes */}
              {notes && (
                <div className="border-t border-slate-100 pt-3">
                  <p className="text-[11px] text-slate-500 italic">{notes}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Contextual Ameetech Service CTA */}
      <ServiceCTA
        headline="Need a custom client billing or e-commerce portal?"
        description="Amee Technology Ltd develops custom enterprise websites, client portals with automated billing, and secure online payment integrations for businesses across Nigeria."
        buttonText="Explore Web Development Services"
        url="https://ameetechnology.com.ng/#services"
      />
    </div>
  );
}
