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
    icon: [
      { url: '/favicon.ico' },
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
      { url: '/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
  },
  alternates: {
    canonical: 'https://toolkits.ameetechnology.com.ng',
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
        width: 500,
        height: 500,
        alt: 'Ameetech Toolkits Logo',
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
  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebSite',
        '@id': 'https://toolkits.ameetechnology.com.ng/#website',
        url: 'https://toolkits.ameetechnology.com.ng',
        name: 'Ameetech Toolkits',
        description: 'Free Digital Tools for Nigerian Businesses',
        publisher: {
          '@type': 'Organization',
          '@id': 'https://ameetechnology.com.ng/#organization',
          name: 'Amee Technology Ltd',
          url: 'https://ameetechnology.com.ng',
          logo: 'https://toolkits.ameetechnology.com.ng/brand/ameelogo.png',
        },
      },
      {
        '@type': 'Organization',
        '@id': 'https://ameetechnology.com.ng/#organization',
        name: 'Amee Technology Ltd',
        url: 'https://ameetechnology.com.ng',
        logo: 'https://toolkits.ameetechnology.com.ng/brand/ameelogo.png',
        contactPoint: {
          '@type': 'ContactPoint',
          telephone: '+2348100015498',
          contactType: 'customer service',
          areaServed: 'NG',
        },
      },
    ],
  };

  return (
    <html lang="en" className="h-full scroll-smooth">
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-800 font-sans selection:bg-purple-100 selection:text-purple-900">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
