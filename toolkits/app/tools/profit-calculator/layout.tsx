import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Free Profit Margin & Selling Price Calculator Nigeria',
  description:
    'Calculate gross profit, net margin, markup percentage, and suggested retail price including delivery and overheads. Essential pricing tool for Nigerian traders.',
  alternates: {
    canonical: 'https://toolkits.ameetechnology.com.ng/tools/profit-calculator',
  },
  openGraph: {
    title: 'Free Profit Margin & Selling Price Calculator | Ameetech Toolkits',
    description:
      'Calculate gross profit, net margin, markup percentage, and suggested retail price including delivery and overheads for Nigerian businesses.',
    url: 'https://toolkits.ameetechnology.com.ng/tools/profit-calculator',
  },
};

export default function ProfitCalculatorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
