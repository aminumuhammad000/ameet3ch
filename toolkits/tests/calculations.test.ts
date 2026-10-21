import assert from 'node:assert/strict';
import {
  calculateLineTotal,
  calculateInvoiceTotals,
  calculateProfitAndMarkup,
  LineItem,
} from '../lib/calculations';
import { normalizePhoneNumber, buildWhatsAppLink } from '../lib/phone';
import { formatMoney } from '../lib/currency';

console.log('🧪 Running Ameetech Toolkits Core Arithmetic & Utility Tests...\n');

// 1. Line Total
{
  const total = calculateLineTotal(3, 5000, 500);
  assert.equal(total, 14500, 'Line total should be qty * price - discount');

  const zeroTotal = calculateLineTotal(-2, 5000, 0);
  assert.equal(zeroTotal, 0, 'Negative quantity should be safely coerced to 0');
  console.log('✅ calculateLineTotal tests passed');
}

// 2. Invoice Totals - Percentage Discount
{
  const items: LineItem[] = [
    { id: '1', description: 'Web Dev', quantity: 1, unitPrice: 100000, discount: 0 },
    { id: '2', description: 'Hosting', quantity: 2, unitPrice: 25000, discount: 0 },
  ]; // Subtotal = 150,000

  // 10% discount, 7.5% tax
  const res = calculateInvoiceTotals(items, 'percentage', 10, 7.5);
  assert.equal(res.subtotal, 150000);
  assert.equal(res.discountAmount, 15000); // 10% of 150,000
  // Taxable = 135,000. 7.5% of 135,000 = 10,125
  assert.equal(res.taxAmount, 10125);
  // Grand total = 135,000 + 10,125 = 145,125
  assert.equal(res.grandTotal, 145125);
  console.log('✅ calculateInvoiceTotals (percentage discount & tax) tests passed');
}

// 3. Invoice Totals - Fixed Discount
{
  const items: LineItem[] = [
    { id: '1', description: 'Service', quantity: 1, unitPrice: 50000, discount: 0 },
  ];
  // 5,000 fixed discount, 0 tax
  const res = calculateInvoiceTotals(items, 'fixed', 5000, 0);
  assert.equal(res.subtotal, 50000);
  assert.equal(res.discountAmount, 5000);
  assert.equal(res.taxAmount, 0);
  assert.equal(res.grandTotal, 45000);
  console.log('✅ calculateInvoiceTotals (fixed discount) tests passed');
}

// 4. Profit & Markup - Normal Profitable
{
  // Cost: 10,000, Selling: 15,000, Qty: 2, Addl: 1,000
  // Unit cost = 11,000. Total cost for 2 = 22,000
  // Revenue for 2 = 30,000
  // Gross Profit = 8,000
  // Markup % = 8,000 / 22,000 * 100 = 36.36%
  // Margin % = 8,000 / 30,000 * 100 = 26.67%
  const res = calculateProfitAndMarkup(10000, 15000, 2, 1000);
  assert.equal(res.revenue, 30000);
  assert.equal(res.totalCost, 22000);
  assert.equal(res.grossProfit, 8000);
  assert.equal(res.markupPercent, 36.36);
  assert.equal(res.grossMarginPercent, 26.67);
  assert.equal(res.isProfit, true);
  console.log('✅ calculateProfitAndMarkup (profitable case) tests passed');
}

// 5. Profit & Markup - Zero Cost & Zero Selling (Denominator Edge Cases)
{
  const zeroCost = calculateProfitAndMarkup(0, 5000, 1, 0);
  assert.equal(zeroCost.markupPercent, null, 'Markup should be null when total cost is 0');
  assert.equal(zeroCost.grossMarginPercent, 100);

  const zeroSelling = calculateProfitAndMarkup(5000, 0, 1, 0);
  assert.equal(zeroSelling.grossMarginPercent, null, 'Margin should be null when revenue is 0');
  assert.equal(zeroSelling.isProfit, false);
  console.log('✅ calculateProfitAndMarkup (safe zero-denominator handling) tests passed');
}

// 6. WhatsApp Phone Number Normalization
{
  // Local Nigerian 11 digits format
  const local = normalizePhoneNumber('08100015498', '234');
  assert.equal(local.isValid, true);
  assert.equal(local.normalizedNumber, '2348100015498');

  // Spaces, hyphens, and brackets
  const messy = normalizePhoneNumber('+234 (810) 001-5498', '234');
  assert.equal(messy.isValid, true);
  assert.equal(messy.normalizedNumber, '2348100015498');

  // Missing code (10 digits)
  const shortNum = normalizePhoneNumber('8100015498', '234');
  assert.equal(shortNum.isValid, true);
  assert.equal(shortNum.normalizedNumber, '2348100015498');

  // Empty or invalid string
  const empty = normalizePhoneNumber('');
  assert.equal(empty.isValid, false);
  console.log('✅ normalizePhoneNumber tests passed');
}

// 7. WhatsApp Link Builder
{
  const link = buildWhatsAppLink('08100015498', 'Hello Ameetech & Partners!');
  assert.ok(link.startsWith('https://wa.me/2348100015498?text='));
  assert.ok(link.includes('Hello%20Ameetech%20%26%20Partners!'));
  console.log('✅ buildWhatsAppLink tests passed');
}

// 8. Currency Formatter
{
  const formatted = formatMoney(25000, 'NGN');
  assert.ok(formatted.includes('₦') && formatted.includes('25,000.00'));
  console.log('✅ formatMoney tests passed');
}

console.log('\n🎉 ALL 8 TEST SUITES PASSED CLEANLY!\n');
