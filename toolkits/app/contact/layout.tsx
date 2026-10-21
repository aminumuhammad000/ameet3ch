import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Contact Ameetech Toolkits & Support',
  description:
    'Need help with any tool or looking to develop custom business software? Get in touch with the Ameetech team directly.',
  alternates: {
    canonical: 'https://toolkits.ameetechnology.com.ng/contact',
  },
  openGraph: {
    title: 'Contact Ameetech Toolkits & Support',
    description:
      'Need help with any tool or looking to develop custom business software? Get in touch with Ameetech.',
    url: 'https://toolkits.ameetechnology.com.ng/contact',
  },
};

export default function ContactLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
