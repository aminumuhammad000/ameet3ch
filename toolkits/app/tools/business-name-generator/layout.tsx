import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Free Nigerian Business Name Generator',
  description:
    'Discover creative, brandable, and CAC-ready business names for Nigerian startups, retail shops, tech firms, fashion brands, and food ventures.',
  alternates: {
    canonical: 'https://toolkits.ameetechnology.com.ng/tools/business-name-generator',
  },
  openGraph: {
    title: 'Free Nigerian Business Name Generator | Ameetech Toolkits',
    description:
      'Discover creative, brandable, and CAC-ready business names for Nigerian startups and businesses.',
    url: 'https://toolkits.ameetechnology.com.ng/tools/business-name-generator',
  },
};

export default function BusinessNameGeneratorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
