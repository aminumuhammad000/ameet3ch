import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Free Invoice Generator for Nigerian Businesses',
  description:
    'Generate professional PDF invoices with Naira (₦) formatting, custom logo, itemized rows, discount, and VAT calculations. 100% free with no registration required.',
  alternates: {
    canonical: 'https://toolkits.ameetechnology.com.ng/tools/invoice-generator',
  },
  openGraph: {
    title: 'Free Invoice Generator for Nigerian Businesses | Ameetech Toolkits',
    description:
      'Generate professional PDF invoices with Naira (₦) formatting, custom logo, itemized rows, discount, and VAT calculations. 100% free.',
    url: 'https://toolkits.ameetechnology.com.ng/tools/invoice-generator',
  },
};

export default function InvoiceGeneratorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
