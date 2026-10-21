'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Calculator,
  ArrowLeft,
  TrendingUp,
  TrendingDown,
  Info,
  DollarSign,
  PieChart,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
} from 'lucide-react';
import { calculateProfitAndMarkup, formatNumber } from '@/lib/calculations';
import { SUPPORTED_CURRENCIES, formatMoney } from '@/lib/currency';
import ServiceCTA from '@/components/ServiceCTA';

export default function ProfitCalculatorPage() {
  const [currency, setCurrency] = useState('NGN');
  const [costPrice, setCostPrice] = useState<number>(15000);
  const [sellingPrice, setSellingPrice] = useState<number>(22500);
  const [quantity, setQuantity] = useState<number>(1);
  const [additionalCosts, setAdditionalCosts] = useState<number>(500);

  const calc = calculateProfitAndMarkup(costPrice, sellingPrice, quantity, additionalCosts);

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
              Profit and Markup Calculator
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              Accurately calculate your gross profit, markup percentage, and profit margin to avoid underpricing your products.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-xs font-medium text-slate-500">Currency:</label>
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="text-xs font-semibold border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white shadow-xs focus:ring-1 focus:ring-purple-600"
            >
              {SUPPORTED_CURRENCIES.map((c) => (
                <option key={c.code} value={c.code}>
                  {c.code} ({c.symbol})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Main Grid: Inputs vs Realtime Results */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left: Inputs */}
        <div className="lg:col-span-6 bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-4">
            <Calculator className="w-5 h-5 text-purple-600" />
            <h2 className="font-bold text-slate-900 text-base">Pricing Inputs</h2>
          </div>

          <div className="space-y-4">
            {/* Cost Price */}
            <div className="space-y-1">
              <div className="flex justify-between items-center">
                <label className="text-xs font-bold text-slate-700">
                  Cost Price per Unit ({currency}) *
                </label>
                <span className="text-[11px] text-slate-600">What you bought it for</span>
              </div>
              <input
                type="number"
                min="0"
                step="any"
                value={costPrice}
                onChange={(e) => setCostPrice(Math.max(0, Number(e.target.value)))}
                className="w-full text-base font-semibold rounded-xl border border-slate-300 p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none transition"
              />
            </div>

            {/* Selling Price */}
            <div className="space-y-1">
              <div className="flex justify-between items-center">
                <label className="text-xs font-bold text-slate-700">
                  Selling Price per Unit ({currency}) *
                </label>
                <span className="text-[11px] text-slate-600">What customers pay</span>
              </div>
              <input
                type="number"
                min="0"
                step="any"
                value={sellingPrice}
                onChange={(e) => setSellingPrice(Math.max(0, Number(e.target.value)))}
                className="w-full text-base font-semibold rounded-xl border border-slate-300 p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none transition"
              />
            </div>

            {/* Additional Costs per Unit */}
            <div className="space-y-1">
              <div className="flex justify-between items-center">
                <label className="text-xs font-bold text-slate-700">
                  Additional Unit Costs ({currency})
                </label>
                <span className="text-[11px] text-slate-600">Packaging, waybill, card fee</span>
              </div>
              <input
                type="number"
                min="0"
                step="any"
                value={additionalCosts}
                onChange={(e) => setAdditionalCosts(Math.max(0, Number(e.target.value)))}
                className="w-full text-sm rounded-xl border border-slate-300 p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none transition"
              />
            </div>

            {/* Units Quantity */}
            <div className="space-y-1">
              <div className="flex justify-between items-center">
                <label className="text-xs font-bold text-slate-700">
                  Number of Units Sold (Batch Size)
                </label>
                <span className="text-[11px] text-slate-600">Default: 1 unit</span>
              </div>
              <input
                type="number"
                min="1"
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, Number(e.target.value)))}
                className="w-full text-sm rounded-xl border border-slate-300 p-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-purple-600 focus:outline-none transition"
              />
            </div>
          </div>

          <div className="bg-purple-50 p-4 rounded-xl text-xs text-purple-900 leading-relaxed flex items-start gap-2">
            <Info className="w-4 h-4 shrink-0 text-purple-600 mt-0.5" />
            <span>
              <strong>Gross Profit vs Net Profit:</strong> This calculation determines your gross commercial profit based on product unit cost. Rent, staff salaries, and general company overheads are not included.
            </span>
          </div>
        </div>

        {/* Right: Results Dashboard */}
        <div className="lg:col-span-6 space-y-6">
          {/* Status Badge */}
          <div
            className={`p-4 rounded-2xl border flex items-center gap-3 ${
              calc.isProfit
                ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
                : calc.isBreakEven
                ? 'bg-amber-50 border-amber-200 text-amber-800'
                : 'bg-red-50 border-red-200 text-red-800'
            }`}
          >
            {calc.isProfit ? (
              <CheckCircle2 className="w-5 h-5 shrink-0 text-emerald-600" />
            ) : calc.isBreakEven ? (
              <AlertCircle className="w-5 h-5 shrink-0 text-amber-600" />
            ) : (
              <AlertCircle className="w-5 h-5 shrink-0 text-red-600" />
            )}
            <span className="text-xs sm:text-sm font-semibold">{calc.statusMessage}</span>
          </div>

          {/* Cards for Margin and Markup */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
              <span className="text-xs font-semibold text-slate-500 block uppercase tracking-wider">
                Gross Profit Margin
              </span>
              <div className="text-2xl sm:text-3xl font-extrabold text-purple-700">
                {calc.grossMarginPercent !== null ? `${calc.grossMarginPercent}%` : 'N/A'}
              </div>
              <p className="text-[11px] text-slate-600 leading-tight">
                Percentage of selling price that is profit.
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
              <span className="text-xs font-semibold text-slate-500 block uppercase tracking-wider">
                Markup Percentage
              </span>
              <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                {calc.markupPercent !== null ? `${calc.markupPercent}%` : 'N/A'}
              </div>
              <p className="text-[11px] text-slate-600 leading-tight">
                Percentage added on top of your total cost.
              </p>
            </div>
          </div>

          {/* Breakdown Table */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <h3 className="font-bold text-slate-900 text-sm border-b border-slate-100 pb-3">
              Financial Breakdown ({quantity} {quantity === 1 ? 'Unit' : 'Units'})
            </h3>

            <div className="space-y-3 text-sm">
              <div className="flex justify-between items-center text-slate-600">
                <span>Total Expected Revenue:</span>
                <span className="font-bold text-slate-900">{formatMoney(calc.revenue, currency)}</span>
              </div>

              <div className="flex justify-between items-center text-slate-600">
                <span>Total Cost of Goods (inc. extras):</span>
                <span className="font-semibold text-slate-800">
                  {formatMoney(calc.totalCost, currency)}
                </span>
              </div>

              <div className="border-t border-slate-100 pt-3 flex justify-between items-center">
                <span className="font-bold text-slate-900">Gross Commercial Profit:</span>
                <span
                  className={`text-lg font-black ${
                    calc.grossProfit >= 0 ? 'text-emerald-700' : 'text-red-600'
                  }`}
                >
                  {formatMoney(calc.grossProfit, currency)}
                </span>
              </div>
            </div>
          </div>

          {/* Formula Reference */}
          <div className="bg-slate-50 rounded-2xl p-5 border border-slate-200/80 space-y-2 text-xs text-slate-600">
            <div className="font-bold text-slate-800 flex items-center gap-1.5">
              <HelpCircle className="w-4 h-4 text-purple-600" />
              <span>Formulas Used:</span>
            </div>
            <ul className="list-disc list-inside space-y-1 text-[11px] text-slate-500">
              <li><strong>Gross Profit</strong> = Selling Price − Total Unit Cost</li>
              <li><strong>Markup %</strong> = (Profit ÷ Total Cost) × 100</li>
              <li><strong>Gross Margin %</strong> = (Profit ÷ Selling Price) × 100</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Contextual Ameetech CTA */}
      <ServiceCTA
        headline="Ready to launch an e-commerce website to sell at scale?"
        description="Amee Technology Ltd creates high-converting e-commerce web applications with Paystack/Flutterwave integrations, real-time inventory management, and automated profit analytics."
        buttonText="Explore E-Commerce Development"
        url="https://ameetechnology.com.ng/#services"
      />
    </div>
  );
}
