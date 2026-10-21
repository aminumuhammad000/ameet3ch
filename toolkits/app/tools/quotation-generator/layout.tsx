import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Free Price Quotation Generator for Nigerian Contractors & SMEs',
  description:
    'Create clean, professional business price quotations and estimates in Naira (₦). Download ready-to-send PDF proposals instantly.',
  alternates: {
    canonical: 'https://toolkits.ameetechnology.com.ng/tools/quotation-generator',
  },
  openGraph: {
    title: 'Free Price Quotation Generator | Ameetech Toolkits',
    description:
      'Create clean, professional business price quotations and estimates in Naira (₦). Download PDF quotations free.',
    url: 'https://toolkits.ameetechnology.com.ng/tools/quotation-generator',
  },
};

export default function QuotationGeneratorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
