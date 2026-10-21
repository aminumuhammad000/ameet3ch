# Ameetech Toolkits (Free Digital Tools for Nigerian Businesses)

A modern, mobile-first business productivity web application engineered by **AMEE TECHNOLOGY LTD**.

- **Production Domain:** `https://toolkits.ameetechnology.com.ng`
- **Parent Website:** `https://ameetechnology.com.ng`
- **Privacy Standard:** 100% Client-side document processing (Compliant with Nigeria Data Protection Act 2023 - NDPA).

---

## 🚀 Features & Tools Included

### P0 Core Utilities
1. **Invoice Generator (`/tools/invoice-generator`)**
   - Professional PDF invoice export with client-side canvas rendering.
   - Line items with auto arithmetic, fixed or percentage discounts, optional VAT/tax, custom currency selection (NGN `₦`, USD `$`, GBP `£`, EUR `€`), payment terms, bank details, and business logo upload.
2. **Receipt Generator (`/tools/receipt-generator`)**
   - Verified proof-of-payment receipts for completed transactions (Bank Transfer, Cash, POS / Card, USSD, Cheque).
   - High-resolution PDF export and print formatting.
3. **Profit & Markup Calculator (`/tools/profit-calculator`)**
   - Precise financial calculations for Gross Profit, Markup %, and Gross Margin %.
   - Zero-denominator protection and visual health indicators.
4. **WhatsApp Link Generator (`/tools/whatsapp-link-generator`)**
   - `wa.me` click-to-chat links formatted for Nigerian numbers (`+234`) and international formats.
   - URL-encoded prefilled message templates, instant copy-to-clipboard, and printable QR codes.

### P1 Value-Add Utilities
5. **Marketing Caption Generator (`/tools/marketing-caption-generator`)**
   - Promotional social media copy for WhatsApp Status, Instagram, and TikTok.
6. **Business Name Generator (`/tools/business-name-generator`)**
   - Creative brand name ideation with modern taglines and CAC clearance disclaimers.
7. **Quotation Generator (`/tools/quotation-generator`)**
   - Project scope estimates with validity dates and contract milestones for freelancers.

### Shell, SEO & Compliance
- **Homepage (`/`) & Catalog (`/tools`):** Interactive search and category filters.
- **Privacy Policy (`/privacy`):** NDPA 2023 data minimization compliance.
- **Terms of Use (`/terms`):** Professional disclaimers & terms.
- **Resources (`/resources`):** Practical guides on invoicing and pricing.
- **Contact (`/contact`):** Lead-generation desk connected to WhatsApp.
- **Technical SEO:** Auto-generated `sitemap.xml` and `robots.txt`.

---

## 🛠️ Local Development & Testing

```bash
# Enter directory
cd toolkits

# Run development server
npm run dev

# Run arithmetic and utility unit test suite
npm test

# Build for production
npm run build
```

---

## 🌐 Deployment to `toolkits.ameetechnology.com.ng`

The toolkit is designed to deploy independently without disrupting `ameetechnology.com.ng`:

1. **Vercel / Cloudflare Pages / Netlify Deployment:**
   - **Root Directory:** `toolkits`
   - **Build Command:** `npm run build`
   - **Output Directory:** `.next`
2. **DNS Configuration:**
   - In your domain DNS manager for `ameetechnology.com.ng`, add a CNAME record:
     - **Host / Subdomain:** `toolkits`
     - **Target:** Point to your deployment target (e.g., `cname.vercel-dns.com` or custom server).
