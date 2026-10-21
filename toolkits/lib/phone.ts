/**
 * Normalizes phone numbers for WhatsApp click-to-chat links.
 * Handles Nigerian local prefixes (080, 070, 090, 081, 091) and international formats.
 */
export function normalizePhoneNumber(rawNumber: string, defaultCountryCode: string = '234'): {
  isValid: boolean;
  normalizedNumber: string;
  errorMessage?: string;
} {
  if (!rawNumber || !rawNumber.trim()) {
    return { isValid: false, normalizedNumber: '', errorMessage: 'Phone number is required.' };
  }

  // Remove spaces, hyphens, plus signs, brackets, parentheses, and other non-digits
  let digits = rawNumber.replace(/\D/g, '');

  if (!digits) {
    return { isValid: false, normalizedNumber: '', errorMessage: 'Please enter a valid numeric phone number.' };
  }

  // If starts with 0 and length is 11 (typical Nigerian format like 08012345678)
  if (digits.startsWith('0') && digits.length === 11 && defaultCountryCode === '234') {
    digits = '234' + digits.substring(1);
  } else if (digits.startsWith('00')) {
    // E.164 international access prefix like 00234...
    digits = digits.substring(2);
  } else if (!digits.startsWith(defaultCountryCode) && digits.length <= 10) {
    // Missing country code, append default
    digits = defaultCountryCode + digits;
  }

  // E.164 phone numbers typically have 8 to 15 digits
  if (digits.length < 8 || digits.length > 15) {
    return {
      isValid: false,
      normalizedNumber: digits,
      errorMessage: `Phone number length (${digits.length} digits) appears invalid for international WhatsApp standards.`,
    };
  }

  return {
    isValid: true,
    normalizedNumber: digits,
  };
}

/**
 * Builds standard wa.me link with URL-encoded message.
 */
export function buildWhatsAppLink(phone: string, message?: string): string {
  const norm = normalizePhoneNumber(phone);
  if (!norm.isValid) return '';

  const baseUrl = `https://wa.me/${norm.normalizedNumber}`;
  if (message && message.trim()) {
    const encoded = encodeURIComponent(message.trim());
    return `${baseUrl}?text=${encoded}`;
  }
  return baseUrl;
}
