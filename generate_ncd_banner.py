from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

w, h = 1200, 630  # Standard 1200x630 OpenGraph / featured banner
img = Image.new('RGB', (w, h), color=(13, 5, 32))
draw = ImageDraw.Draw(img)

# 1. Base Gradient: Deep purple-navy to dark slate
for y in range(h):
    ratio = y / h
    r = int(24 * (1 - ratio) + 10 * ratio)
    g = int(10 * (1 - ratio) + 8 * ratio)
    b = int(58 * (1 - ratio) + 28 * ratio)
    draw.line([(0, y), (w, y)], fill=(r, g, b))

# 2. Ambient glows
glow_overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_overlay)

# Purple glow on left
glow_draw.ellipse([-50, -50, 600, 500], fill=(108, 43, 217, 75))
# Emerald glow on right (Arewa / NCD accent)
glow_draw.ellipse([700, 50, 1300, 650], fill=(0, 204, 103, 55))
# Soft amber in center
glow_draw.ellipse([450, 300, 850, 650], fill=(168, 85, 247, 40))

glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(80))
img.paste(glow_overlay, (0, 0), glow_overlay)
draw = ImageDraw.Draw(img)

# Fonts
font_path_bold = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
font_path_reg = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

font_title = ImageFont.truetype(font_path_bold, 38)
font_subtitle = ImageFont.truetype(font_path_reg, 18)
font_badge = ImageFont.truetype(font_path_bold, 13)
font_card_head = ImageFont.truetype(font_path_bold, 16)
font_card_sub = ImageFont.truetype(font_path_reg, 13)

# 3. Badge Pill
badge_text = "OFFICIAL PARTNERSHIP  •  KANO 2026"
draw.rounded_rectangle([70, 55, 410, 90], radius=16, fill=(108, 43, 217, 220), outline=(168, 85, 247))
draw.text((95, 65), badge_text, font=font_badge, fill=(255, 255, 255))

# 4. Main Title
title_line1 = "AMEE TECHNOLOGY Named"
title_line2 = "Official Software Partner"
draw.text((70, 115), title_line1, font=font_title, fill=(255, 255, 255))
draw.text((70, 165), title_line2, font=font_title, fill=(168, 85, 247))

# 5. Subtitle
sub_line1 = "Northern Creative Designers Summit 2.0 (Roots & Vectors)"
sub_line2 = "19 December 2026  •  Kano, Nigeria  •  9:00 PM"
draw.text((70, 235), sub_line1, font=font_subtitle, fill=(243, 232, 255))
draw.text((70, 265), sub_line2, font=font_subtitle, fill=(0, 204, 103))

# 6. Logos Partnership Container (Right Side)
container_box = [670, 110, 1130, 480]
draw.rounded_rectangle(container_box, radius=24, fill=(15, 23, 42, 230), outline=(108, 43, 217, 120))

# Inner Header in Container
draw.text((705, 140), "OFFICIAL PARTNERSHIP DESIGNATION", font=font_badge, fill=(148, 163, 184))

# Paste Ameetech Logo
amee_logo_path = "images/ameelogo.png"
if os.path.exists(amee_logo_path):
    amee_logo = Image.open(amee_logo_path).convert("RGBA")
    amee_logo.thumbnail((90, 90), Image.Resampling.LANCZOS)
    img.paste(amee_logo, (715, 180), amee_logo)

# "X" Partnership Symbol
font_x = ImageFont.truetype(font_path_bold, 32)
draw.text((835, 205), "×", font=font_x, fill=(168, 85, 247))

# Paste North C Designers Logo
ncd_logo_path = "images/northcdesigners.png"
if os.path.exists(ncd_logo_path):
    ncd_logo = Image.open(ncd_logo_path).convert("RGBA")
    ncd_logo.thumbnail((200, 80), Image.Resampling.LANCZOS)
    img.paste(ncd_logo, (890, 190), ncd_logo)

# Event Details Card Box inside container
draw.rounded_rectangle([705, 295, 1095, 445], radius=16, fill=(30, 41, 59, 220), outline=(51, 65, 85))
draw.text((725, 315), "Northern Creative Designers Summit 2.0", font=font_card_head, fill=(255, 255, 255))
draw.text((725, 342), "Theme: Roots & Vectors — Shaping the Future of Arewa Design", font=font_card_sub, fill=(203, 213, 225))
draw.text((725, 372), "• Date: 19 December 2026   • Time: 9:00 PM", font=font_card_sub, fill=(0, 204, 103))
draw.text((725, 398), "• Location: Kano, Nigeria    • Role: Official Software Partner", font=font_card_sub, fill=(168, 85, 247))

# 7. Bottom Left Summary Callout Box
draw.rounded_rectangle([70, 340, 610, 480], radius=18, fill=(18, 12, 45, 220), outline=(108, 43, 217, 90))
draw.text((95, 360), "Advancing Creativity & Software in Northern Nigeria", font=font_card_head, fill=(255, 255, 255))
callout_p1 = "Uniting software engineering with Arewa's creative design"
callout_p2 = "ecosystem to foster digital growth and regional innovation."
draw.text((95, 392), callout_p1, font=font_card_sub, fill=(226, 232, 240))
draw.text((95, 415), callout_p2, font=font_card_sub, fill=(148, 163, 184))

# Footer watermark line
draw.text((70, 560), "Amee Technology Ltd  •  ameetechnology.com.ng", font=font_card_sub, fill=(148, 163, 184))

os.makedirs("images/blog", exist_ok=True)
webp_path = "images/blog/amee-technology-ncd-summit-2026-software-partner.webp"
png_path = "images/blog/amee-technology-ncd-summit-2026-software-partner.png"
img.save(webp_path, "WEBP", quality=90)
img.save(png_path, "PNG")
print(f"Saved banner to {webp_path} and {png_path}")
