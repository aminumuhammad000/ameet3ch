export interface ToolItem {
  id: string;
  name: string;
  slug: string;
  category: 'Documents' | 'Finance and Calculators' | 'Communication' | 'Marketing' | 'Business Setup';
  description: string;
  priority: 'P0' | 'P1' | 'P2';
  icon: string;
  isReady: boolean;
  metaTitle: string;
  metaDescription: string;
  ctaHeadline: string;
  ctaDescription: string;
  ctaButtonText: string;
  ctaUrl: string;
}

export const TOOLS_DATA: ToolItem[] = [
  {
    id: 'invoice-generator',
    name: 'Invoice Generator',
    slug: '/tools/invoice-generator',
    category: 'Documents',
    description: 'Create professional, branded PDF invoices with custom line items, discounts, and optional tax in seconds.',
    priority: 'P0',
    icon: 'FileText',
    isReady: true,
    metaTitle: 'Free Invoice Generator for Nigerian Businesses | Ameetech Toolkits',
    metaDescription: 'Generate professional business invoices with custom items, discounts, and instant PDF download. Completely free with no signup required.',
    ctaHeadline: 'Ready for a Custom Website or Invoicing Portal?',
    ctaDescription: 'Ameetech builds custom web platforms, automated invoicing, and digital business systems to help your enterprise scale.',
    ctaButtonText: 'Explore Web Development Services',
    ctaUrl: 'https://ameetechnology.com.ng/#services',
  },
  {
    id: 'receipt-generator',
    name: 'Receipt Generator',
    slug: '/tools/receipt-generator',
    category: 'Documents',
    description: 'Issue clean, verified proof-of-payment receipts for completed sales, bank transfers, POS, and cash transactions.',
    priority: 'P0',
    icon: 'Receipt',
    isReady: true,
    metaTitle: 'Free Receipt Generator | Issue Payment Receipts Online',
    metaDescription: 'Create clean, professional payment receipts online. Add business details, payment methods, transaction reference and download PDF for free.',
    ctaHeadline: 'Upgrade Your Business Financial Systems',
    ctaDescription: 'Need custom software, POS integration, or accounting dashboards? Partner with Amee Technology Ltd.',
    ctaButtonText: 'Consult Our Software Engineers',
    ctaUrl: 'https://ameetechnology.com.ng/#contact',
  },
  {
    id: 'profit-calculator',
    name: 'Profit and Markup Calculator',
    slug: '/tools/profit-calculator',
    category: 'Finance and Calculators',
    description: 'Calculate your exact profit, markup percentage, and gross profit margin to ensure your products are priced profitably.',
    priority: 'P0',
    icon: 'Calculator',
    isReady: true,
    metaTitle: 'Free Profit & Markup Calculator | Accurate Business Pricing',
    metaDescription: 'Accurately calculate gross profit, markup %, and margin % for your products. Avoid underpricing and make data-driven pricing decisions.',
    ctaHeadline: 'Ready to Sell Products Online at Scale?',
    ctaDescription: 'Let Ameetech design high-converting e-commerce web stores with integrated payment gateways and inventory tracking.',
    ctaButtonText: 'Explore E-commerce Development',
    ctaUrl: 'https://ameetechnology.com.ng/#services',
  },
  {
    id: 'whatsapp-link-generator',
    name: 'WhatsApp Link Generator',
    slug: '/tools/whatsapp-link-generator',
    category: 'Communication',
    description: 'Generate instant click-to-chat WhatsApp links with customized greetings for your social media bios, cards, and ads.',
    priority: 'P0',
    icon: 'MessageSquare',
    isReady: true,
    metaTitle: 'Free WhatsApp Link Generator | Create Click-to-Chat wa.me Links',
    metaDescription: 'Create free WhatsApp direct chat links with prefilled messages for Nigerian business numbers. One-click copy and instant QR code.',
    ctaHeadline: 'Turn WhatsApp Chats into Paying Customers',
    ctaDescription: 'Ameetech helps Nigerian brands run profitable social media ads, lead funnels, and marketing campaigns.',
    ctaButtonText: 'Explore Digital Marketing Services',
    ctaUrl: 'https://ameetechnology.com.ng/#services',
  },
  {
    id: 'marketing-caption-generator',
    name: 'Marketing Caption Generator',
    slug: '/tools/marketing-caption-generator',
    category: 'Marketing',
    description: 'Draft engaging promotional captions, hashtags, and social post copies for WhatsApp, Instagram, and TikTok.',
    priority: 'P1',
    icon: 'Sparkles',
    isReady: true,
    metaTitle: 'Marketing Caption Generator | Social Media Captions for Small Business',
    metaDescription: 'Create compelling promotional captions, sales announcements, and product descriptions tailored for Nigerian audiences.',
    ctaHeadline: 'Need Hands-Off Social Media Management?',
    ctaDescription: 'Let our creative team handle content creation, video reels, and brand growth for your business.',
    ctaButtonText: 'Discover Brand & Content Services',
    ctaUrl: 'https://ameetechnology.com.ng/#services',
  },
  {
    id: 'business-name-generator',
    name: 'Business Name Generator',
    slug: '/tools/business-name-generator',
    category: 'Business Setup',
    description: 'Brainstorm creative, modern brand name ideas and tagline concepts for your new Nigerian startup or venture.',
    priority: 'P1',
    icon: 'Lightbulb',
    isReady: true,
    metaTitle: 'Free Business Name Idea Generator | Ameetech Toolkits',
    metaDescription: 'Generate catchy, modern brand and business name suggestions for your new enterprise. Fast, free ideation.',
    ctaHeadline: 'Bring Your Brand Identity to Life',
    ctaDescription: 'From CAC compliance advice to brand guidelines, logos, and UI/UX design, Ameetech sets up your venture for growth.',
    ctaButtonText: 'Explore Brand Design Services',
    ctaUrl: 'https://ameetechnology.com.ng/#services',
  },
  {
    id: 'quotation-generator',
    name: 'Quotation Generator',
    slug: '/tools/quotation-generator',
    category: 'Documents',
    description: 'Issue formal price quotes and project estimates with validity periods and terms for freelancers and contractors.',
    priority: 'P1',
    icon: 'FileSpreadsheet',
    isReady: true,
    metaTitle: 'Free Quotation Generator | Professional Price Estimates & Quotes',
    metaDescription: 'Create professional business quotations and formal cost estimates for clients. Download clean PDF quotes with validity dates.',
    ctaHeadline: 'Win More High-Value Enterprise Projects',
    ctaDescription: 'Boost your credibility with a high-end corporate website and technical proposals engineered by Ameetech.',
    ctaButtonText: 'Schedule a Tech Consultation',
    ctaUrl: 'https://ameetechnology.com.ng/#contact',
  },
];

export const TOOL_CATEGORIES = [
  'All',
  'Documents',
  'Finance and Calculators',
  'Communication',
  'Marketing',
  'Business Setup',
] as const;
