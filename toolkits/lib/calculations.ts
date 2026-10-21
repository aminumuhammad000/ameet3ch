export interface LineItem {
  id: string;
  description: string;
  quantity: number;
  unitPrice: number;
  discount: number; // fixed discount per line
}

export interface InvoiceCalculations {
  subtotal: number;
  discountAmount: number;
  taxAmount: number;
  grandTotal: number;
}

/**
 * Calculates line total for a single item.
 * Line total = (Quantity * Unit Price) - Discount
 */
export function calculateLineTotal(quantity: number, unitPrice: number, discount: number = 0): number {
  const safeQty = Math.max(0, Number(quantity) || 0);
  const safePrice = Math.max(0, Number(unitPrice) || 0);
  const safeDiscount = Math.max(0, Number(discount) || 0);
  const rawTotal = safeQty * safePrice - safeDiscount;
  return Math.max(0, Math.round(rawTotal * 100) / 100);
}

/**
 * Calculates subtotal, overall discount, tax and grand total for an invoice.
 */
export function calculateInvoiceTotals(
  items: LineItem[],
  discountType: 'fixed' | 'percentage',
  discountValue: number,
  taxRatePercent: number
): InvoiceCalculations {
  const subtotal = items.reduce((acc, item) => {
    return acc + calculateLineTotal(item.quantity, item.unitPrice, item.discount);
  }, 0);

  const safeDiscountVal = Math.max(0, Number(discountValue) || 0);
  let discountAmount = 0;

  if (discountType === 'percentage') {
    const safePercent = Math.min(100, safeDiscountVal);
    discountAmount = (subtotal * safePercent) / 100;
  } else {
    discountAmount = Math.min(subtotal, safeDiscountVal);
  }
  discountAmount = Math.round(discountAmount * 100) / 100;

  const taxableAmount = Math.max(0, subtotal - discountAmount);
  const safeTaxRate = Math.max(0, Number(taxRatePercent) || 0);
  const taxAmount = Math.round(((taxableAmount * safeTaxRate) / 100) * 100) / 100;

  const grandTotal = Math.round((taxableAmount + taxAmount) * 100) / 100;

  return {
    subtotal: Math.round(subtotal * 100) / 100,
    discountAmount,
    taxAmount,
    grandTotal,
  };
}

export interface ProfitCalculations {
  revenue: number;
  totalCost: number;
  grossProfit: number;
  markupPercent: number | null; // null if cost is zero
  grossMarginPercent: number | null; // null if selling price is zero
  isProfit: boolean;
  isBreakEven: boolean;
  statusMessage: string;
}

/**
 * Calculates profit, markup %, and gross margin % with safe zero-denominator handling.
 */
export function calculateProfitAndMarkup(
  costPrice: number,
  sellingPrice: number,
  quantity: number = 1,
  additionalCosts: number = 0
): ProfitCalculations {
  const safeCost = Math.max(0, Number(costPrice) || 0);
  const safeSelling = Math.max(0, Number(sellingPrice) || 0);
  const safeQty = Math.max(1, Number(quantity) || 1);
  const safeAddl = Math.max(0, Number(additionalCosts) || 0);

  const unitCostTotal = safeCost + safeAddl;
  const revenue = Math.round(safeSelling * safeQty * 100) / 100;
  const totalCost = Math.round(unitCostTotal * safeQty * 100) / 100;
  const grossProfit = Math.round((revenue - totalCost) * 100) / 100;

  let markupPercent: number | null = null;
  if (totalCost > 0) {
    markupPercent = Math.round(((grossProfit / totalCost) * 100) * 100) / 100;
  }

  let grossMarginPercent: number | null = null;
  if (revenue > 0) {
    grossMarginPercent = Math.round(((grossProfit / revenue) * 100) * 100) / 100;
  }

  const isProfit = grossProfit > 0;
  const isBreakEven = grossProfit === 0;

  let statusMessage = 'Break-even: Selling price matches your total cost.';
  if (grossProfit > 0) {
    statusMessage = `Profitable: You earn ${formatNumber(grossProfit)} gross profit on this sale.`;
  } else if (grossProfit < 0) {
    statusMessage = `Loss alert: Your selling price is lower than costs by ${formatNumber(Math.abs(grossProfit))}.`;
  }

  return {
    revenue,
    totalCost,
    grossProfit,
    markupPercent,
    grossMarginPercent,
    isProfit,
    isBreakEven,
    statusMessage,
  };
}

export function formatNumber(val: number): string {
  return new Intl.NumberFormat('en-NG', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(val);
}
