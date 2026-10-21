import type { Metadata } from 'next';
import './globals.css';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  metadataBase: new URL('https://toolkits.ameetechnology.com.ng'),
  title: {
    default: 'Ameetech Toolkits — Free Digital Tools for Nigerian Businesses',
    template: '%s | Ameetech Toolkits',
  },
  description:
    'Free online business productivity tools for Nigerian entrepreneurs, MSMEs, and freelancers. Create professional invoices, receipts, calculate profit margins, and generate WhatsApp links instantly.',
  keywords: [
    'free invoice generator Nigeria',
    'free receipt generator',
    'profit calculator Nigeria',
    'WhatsApp link generator',
    'business tools Nigerian entrepreneurs',
    'Ameetech toolkits',
    'Amee Technology Ltd',
  ],
  authors: [{ name: 'Amee Technology Ltd', url: 'https://ameetechnology.com.ng' }],
  creator: 'Amee Technology Ltd',
  publisher: 'Amee Technology Ltd',
  icons: {
    icon: '/brand/ameelogo2.png',
    apple: '/brand/ameelogo2.png',
  },
  openGraph: {
    type: 'website',
    locale: 'en_NG',
    url: 'https://toolkits.ameetechnology.com.ng',
    siteName: 'Ameetech Toolkits',
    title: 'Ameetech Toolkits — Free Digital Tools for Nigerian Businesses',
    description:
      'Free business utilities to help Nigerian business owners manage invoicing, receipts, financial pricing, and customer communication directly in the browser.',
    images: [
      {
        url: '/brand/ameelogo.png',
        width: 800,
        height: 600,
        alt: 'Ameetech Toolkits',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Ameetech Toolkits — Free Digital Tools for Nigerian Businesses',
    description: 'Free invoices, receipts, profit calculator, and WhatsApp link generator for Nigerian businesses.',
    images: ['/brand/ameelogo.png'],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full scroll-smooth">
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-800 font-sans selection:bg-purple-100 selection:text-purple-900">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
