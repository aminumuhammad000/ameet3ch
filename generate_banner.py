from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

w, h = 1200, 550
img = Image.new('RGB', (w, h), color=(30, 27, 75))
draw = ImageDraw.Draw(img)

# 1. Base Gradient (Deep purple to dark navy)
for y in range(h):
    ratio = y / h
    r = int(76 * (1 - ratio) + 20 * ratio)
    g = int(29 * (1 - ratio) + 15 * ratio)
    b = int(149 * (1 - ratio) + 55 * ratio)
    draw.line([(0, y), (w, y)], fill=(r, g, b))

# 2. Add subtle radial ambient glows (emerald & cyan highlights)
glow_overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_overlay)

# Top right emerald glow for WhatsApp theme
glow_draw.ellipse([750, -100, 1350, 450], fill=(16, 185, 129, 45))
# Center bottom purple glow
glow_draw.ellipse([100, 200, 700, 700], fill=(147, 51, 234, 50))
glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(60))
img.paste(glow_overlay, (0, 0), glow_overlay)

draw = ImageDraw.Draw(img)

# Load fonts
font_path_bold = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
font_path_reg = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

font_title = ImageFont.truetype(font_path_bold, 44)
font_subtitle = ImageFont.truetype(font_path_reg, 20)
font_badge = ImageFont.truetype(font_path_bold, 13)
font_pill = ImageFont.truetype(font_path_bold, 15)
font_card_head = ImageFont.truetype(font_path_bold, 16)
font_card_sub = ImageFont.truetype(font_path_reg, 13)

# 3. Left Content Column:
# Badge Pill
badge_text = "AMEETECH  •  2026 DIGITAL PLAYBOOK"
draw.rounded_rectangle([70, 60, 390, 92], radius=16, fill=(108, 43, 217, 180), outline=(192, 132, 252))
draw.text((95, 68), badge_text, font=font_badge, fill=(245, 235, 255))

# Main Title (wrapped)
title_line1 = "WhatsApp Business"
title_line2 = "for Nigerian SMEs"
draw.text((70, 115), title_line1, font=font_title, fill=(255, 255, 255))
draw.text((70, 168), title_line2, font=font_title, fill=(52, 211, 153))

# Subtitle
sub_line1 = "Turn casual chats into confirmed bank payments."
sub_line2 = "Catalogues • Quick Replies • wa.me Links • Sales Workflow"
draw.text((70, 245), sub_line1, font=font_subtitle, fill=(226, 232, 240))
draw.text((70, 275), sub_line2, font=font_subtitle, fill=(167, 139, 250))

# 3 Feature Pills
pills = [
    ("✓ Official Setup & Catalogues", 70, 340, 320, 376),
    ("✓ wa.me Direct Chat Links", 70, 395, 305, 431),
    ("✓ 7-Day Status Content Strategy", 70, 450, 345, 486),
]

for label, x1, y1, x2, y2 in pills:
    draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=(30, 41, 59, 160), outline=(71, 85, 105))
    draw.text((x1 + 14, y1 + 9), label, font=font_pill, fill=(241, 245, 249))

# 4. Right Visual Mockup (Mobile Card & Floating WhatsApp Pills):
mock_bg_x, mock_bg_y, mock_bg_w, mock_bg_h = 720, 60, 420, 430
draw.rounded_rectangle([mock_bg_x, mock_bg_y, mock_bg_x + mock_bg_w, mock_bg_y + mock_bg_h],
                       radius=24, fill=(15, 23, 42, 220), outline=(51, 65, 85), width=2)

# Header in mockup
draw.rounded_rectangle([mock_bg_x, mock_bg_y, mock_bg_x + mock_bg_w, mock_bg_y + 70],
                       radius=24, fill=(30, 41, 59, 240))
# Flatten bottom corners of mockup header
draw.rectangle([mock_bg_x, mock_bg_y + 40, mock_bg_x + mock_bg_w, mock_bg_y + 70], fill=(30, 41, 59, 240))

# Load & paste WhatsApp icon
try:
    wa_icon = Image.open('images/whatsapp.png').convert('RGBA')
    wa_icon = wa_icon.resize((44, 44), Image.Resampling.LANCZOS)
    img.paste(wa_icon, (mock_bg_x + 20, mock_bg_y + 13), wa_icon)
except Exception as e:
    print('wa_icon error:', e)

draw.text((mock_bg_x + 75, mock_bg_y + 16), "Ameetech Store (Kano)", font=font_card_head, fill=(255, 255, 255))
draw.text((mock_bg_x + 75, mock_bg_y + 38), "Official Business Account • Online", font=font_card_sub, fill=(52, 211, 153))

# Chat bubbles inside mockup
# Bubble 1: Incoming customer
draw.rounded_rectangle([mock_bg_x + 20, mock_bg_y + 90, mock_bg_x + 320, mock_bg_y + 155],
                       radius=14, fill=(51, 65, 85))
draw.text((mock_bg_x + 35, mock_bg_y + 100), "Hello! How much is the 1kVA Solar", font=font_card_sub, fill=(241, 245, 249))
draw.text((mock_bg_x + 35, mock_bg_y + 124), "generator? Need it delivered to Abuja.", font=font_card_sub, fill=(241, 245, 249))

# Bubble 2: Business Response
draw.rounded_rectangle([mock_bg_x + 100, mock_bg_y + 175, mock_bg_x + 400, mock_bg_y + 255],
                       radius=14, fill=(5, 150, 105))
draw.text((mock_bg_x + 115, mock_bg_y + 185), "Hello! It is ₦385,000 complete.", font=font_card_sub, fill=(255, 255, 255))
draw.text((mock_bg_x + 115, mock_bg_y + 208), "Same-day Abuja dispatch available.", font=font_card_sub, fill=(255, 255, 255))
draw.text((mock_bg_x + 115, mock_bg_y + 230), "Invoice & account details sent! ✓✓", font=font_card_sub, fill=(209, 250, 229))

# Floating Stat Card: Bank Transfer Confirmed
draw.rounded_rectangle([mock_bg_x - 35, mock_bg_y + 280, mock_bg_x + 280, mock_bg_y + 360],
                       radius=16, fill=(17, 24, 39, 245), outline=(52, 211, 153), width=2)
draw.text((mock_bg_x - 15, mock_bg_y + 295), "✓ ₦385,000 Paid via Transfer", font=font_card_head, fill=(52, 211, 153))
draw.text((mock_bg_x - 15, mock_bg_y + 325), "NIP Ref: 000014299831 • Dispatched", font=font_card_sub, fill=(148, 163, 184))

# Floating Conversion Pill
draw.rounded_rectangle([mock_bg_x + 140, mock_bg_y + 375, mock_bg_x + 395, mock_bg_y + 420],
                       radius=14, fill=(108, 43, 217, 240), outline=(192, 132, 252))
draw.text((mock_bg_x + 155, mock_bg_y + 387), "⚡ 30% Enquiry Conversion", font=font_badge, fill=(255, 255, 255))

# Save image
output_path = 'images/blog/whatsapp_business_guide_banner.png'
img.save(output_path, quality=95)
print(f'Banner successfully generated and saved to {output_path}')
