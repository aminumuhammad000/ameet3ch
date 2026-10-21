import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Free Receipt Generator for Nigerian Businesses',
  description:
    'Issue instant payment receipts for bank transfers, POS, cash, and online sales with Naira (₦) formatting. Download cleanly formatted PDF receipts instantly.',
  alternates: {
    canonical: 'https://toolkits.ameetechnology.com.ng/tools/receipt-generator',
  },
  openGraph: {
    title: 'Free Receipt Generator for Nigerian Businesses | Ameetech Toolkits',
    description:
      'Issue instant payment receipts for bank transfers, POS, cash, and online sales with Naira (₦) formatting. Download PDF receipts free.',
    url: 'https://toolkits.ameetechnology.com.ng/tools/receipt-generator',
  },
};

export default function ReceiptGeneratorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
