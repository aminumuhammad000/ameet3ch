import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Free Marketing Caption Generator for Social Media Nigeria',
  description:
    'Generate engaging, high-converting social media captions for Instagram, WhatsApp Status, Facebook, and TikTok tailored for Nigerian shoppers.',
  alternates: {
    canonical: 'https://toolkits.ameetechnology.com.ng/tools/marketing-caption-generator',
  },
  openGraph: {
    title: 'Free Marketing Caption Generator | Ameetech Toolkits',
    description:
      'Generate engaging social media captions for Instagram, WhatsApp Status, Facebook, and TikTok tailored for Nigerian businesses.',
    url: 'https://toolkits.ameetechnology.com.ng/tools/marketing-caption-generator',
  },
};

export default function MarketingCaptionGeneratorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
