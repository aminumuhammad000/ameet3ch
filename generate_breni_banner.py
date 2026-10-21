from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

w, h = 1200, 550
img = Image.new('RGB', (w, h), color=(15, 23, 42))
draw = ImageDraw.Draw(img)

# 1. Base Gradient: Deep indigo to navy slate
for y in range(h):
    ratio = y / h
    r = int(30 * (1 - ratio) + 15 * ratio)
    g = int(27 * (1 - ratio) + 23 * ratio)
    b = int(75 * (1 - ratio) + 42 * ratio)
    draw.line([(0, y), (w, y)], fill=(r, g, b))

# 2. Ambient glows (cyan/blue on right, warm amber/purple on left)
glow_overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_overlay)

# Top right edtech cyan glow
glow_draw.ellipse([700, -120, 1300, 420], fill=(14, 165, 233, 45))
# Center bottom violet/amber glow
glow_draw.ellipse([80, 180, 680, 720], fill=(168, 85, 247, 45))
glow_draw.ellipse([900, 250, 1250, 550], fill=(245, 158, 11, 35))

glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(70))
img.paste(glow_overlay, (0, 0), glow_overlay)
draw = ImageDraw.Draw(img)

# Load fonts
font_path_bold = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
font_path_reg = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

font_title = ImageFont.truetype(font_path_bold, 40)
font_subtitle = ImageFont.truetype(font_path_reg, 19)
font_badge = ImageFont.truetype(font_path_bold, 13)
font_pill = ImageFont.truetype(font_path_bold, 14)
font_card_head = ImageFont.truetype(font_path_bold, 17)
font_card_sub = ImageFont.truetype(font_path_reg, 13)
font_metric = ImageFont.truetype(font_path_bold, 26)

# 3. Left Content Column:
# Badge Pill
badge_text = "AMEETECH  •  FOUNDER STORY & EDTECH INNOVATION"
draw.rounded_rectangle([70, 55, 490, 88], radius=16, fill=(59, 130, 246, 200), outline=(147, 197, 253))
draw.text((95, 64), badge_text, font=font_badge, fill=(255, 255, 255))

# Main Title (wrapped)
title_line1 = "Rethinking Education:"
title_line2 = "Building BRENi & Founder Lessons"
draw.text((70, 110), title_line1, font=font_title, fill=(255, 255, 255))
draw.text((70, 158), title_line2, font=font_title, fill=(56, 189, 248))

# Subtitle
sub_line1 = "Abubakar Sadik Umar on Cognitive Science, Personalised"
sub_line2 = "Learning, Startup Resilience, and Choosing Co-Founders."
draw.text((70, 230), sub_line1, font=font_subtitle, fill=(226, 232, 240))
draw.text((70, 258), sub_line2, font=font_subtitle, fill=(148, 163, 184))

# 3 Feature Pills
pills = [
    ("★ Beyond One-Size-Fits-All Education", 70, 315, 385, 351),
    ("★ Cognitive Science & Learner Avatars", 70, 368, 395, 404),
    ("★ Choosing Co-Founders & Managing Risk", 70, 421, 395, 457),
    ("★ Exclusive Fagen Hikima Interview", 70, 474, 370, 510)
]

for label, x1, y1, x2, y2 in pills:
    draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=(30, 41, 59, 170), outline=(51, 65, 85))
    draw.text((x1 + 14, y1 + 8), label, font=font_pill, fill=(241, 245, 249))

# 4. Right Visual Mockup (Founder Insight Card & Tech Framework)
mock_bg_x, mock_bg_y, mock_bg_w, mock_bg_h = 710, 55, 430, 440
draw.rounded_rectangle([mock_bg_x, mock_bg_y, mock_bg_x + mock_bg_w, mock_bg_y + mock_bg_h],
                       radius=20, fill=(15, 23, 42, 230), outline=(56, 189, 248), width=2)

# Card Header
draw.rounded_rectangle([mock_bg_x, mock_bg_y, mock_bg_x + mock_bg_w, mock_bg_y + 68],
                       radius=20, fill=(30, 41, 59, 240))
draw.rectangle([mock_bg_x, mock_bg_y + 40, mock_bg_x + mock_bg_w, mock_bg_y + 68], fill=(30, 41, 59, 240))

# Try pasting Ameetech logo
try:
    amee_icon = Image.open('images/ameelogo.png').convert('RGBA')
    amee_icon = amee_icon.resize((42, 42), Image.Resampling.LANCZOS)
    img.paste(amee_icon, (mock_bg_x + 18, mock_bg_y + 13), amee_icon)
except Exception as e:
    print('amee_icon error:', e)

draw.text((mock_bg_x + 72, mock_bg_y + 15), "BRENi Founder Spotlight", font=font_card_head, fill=(255, 255, 255))
draw.text((mock_bg_x + 72, mock_bg_y + 38), "Featuring Abubakar Sadik Umar", font=font_card_sub, fill=(56, 189, 248))

# Sub-block 1: Cognitive Science in Education
box1_y = mock_bg_y + 85
draw.rounded_rectangle([mock_bg_x + 18, box1_y, mock_bg_x + 412, box1_y + 90],
                       radius=12, fill=(30, 41, 59, 180), outline=(71, 85, 105))
draw.text((mock_bg_x + 32, box1_y + 12), "EdTech Vision: Beyond Static Video", font=font_card_head, fill=(251, 191, 36))
draw.text((mock_bg_x + 32, box1_y + 38), "• Cognitive Science vs One-Size-Fits-All", font=font_card_sub, fill=(226, 232, 240))
draw.text((mock_bg_x + 32, box1_y + 60), "• Individual Learner Avatar Concept", font=font_card_sub, fill=(148, 163, 184))

# Sub-block 2: Startup Realities & Resilience
box2_y = box1_y + 105
draw.rounded_rectangle([mock_bg_x + 18, box2_y, mock_bg_x + 412, box2_y + 90],
                       radius=12, fill=(30, 41, 59, 180), outline=(71, 85, 105))
draw.text((mock_bg_x + 32, box2_y + 12), "Startup Journey: The Roller Coaster", font=font_card_head, fill=(52, 211, 153))
draw.text((mock_bg_x + 32, box2_y + 38), "• Going all-in with personal resources", font=font_card_sub, fill=(226, 232, 240))
draw.text((mock_bg_x + 32, box2_y + 60), "• Facing convention & sustaining conviction", font=font_card_sub, fill=(148, 163, 184))

# Sub-block 3: Co-founder & Relationships Quote
box3_y = box2_y + 105
draw.rounded_rectangle([mock_bg_x + 18, box3_y, mock_bg_x + 412, box3_y + 90],
                       radius=12, fill=(30, 41, 59, 180), outline=(71, 85, 105))
draw.text((mock_bg_x + 32, box3_y + 12), "Core Founder Principles", font=font_card_head, fill=(244, 114, 182))
draw.text((mock_bg_x + 32, box3_y + 38), "• Character over pure capability in co-founders", font=font_card_sub, fill=(226, 232, 240))
draw.text((mock_bg_x + 32, box3_y + 60), "• Supportive relationships as bedrock for growth", font=font_card_sub, fill=(148, 163, 184))

# Save output
os.makedirs('images/blog', exist_ok=True)
output_path = 'images/blog/abubakar_sadik_umar_breni_banner.png'
img.save(output_path, 'PNG', optimize=True)
print(f"Successfully generated {output_path} ({w}x{h})")
