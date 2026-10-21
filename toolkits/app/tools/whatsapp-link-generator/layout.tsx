import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Free WhatsApp Link Generator with Pre-filled Message',
  description:
    'Create custom WhatsApp direct chat links (wa.me) and downloadable QR codes with customized pre-filled messages for Nigerian business numbers (+234).',
  alternates: {
    canonical: 'https://toolkits.ameetechnology.com.ng/tools/whatsapp-link-generator',
  },
  openGraph: {
    title: 'Free WhatsApp Link Generator | Ameetech Toolkits',
    description:
      'Create custom WhatsApp direct chat links (wa.me) and downloadable QR codes with pre-filled messages for Nigerian business numbers.',
    url: 'https://toolkits.ameetechnology.com.ng/tools/whatsapp-link-generator',
  },
};

export default function WhatsAppLinkGeneratorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
