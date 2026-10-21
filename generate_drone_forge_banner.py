from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

w, h = 1200, 550
img = Image.new('RGB', (w, h), color=(11, 19, 43))
draw = ImageDraw.Draw(img)

# 1. Base Gradient: Deep slate-navy to dark emerald tint
for y in range(h):
    ratio = y / h
    r = int(15 * (1 - ratio) + 8 * ratio)
    g = int(23 * (1 - ratio) + 38 * ratio)
    b = int(42 * (1 - ratio) + 59 * ratio)
    draw.line([(0, y), (w, y)], fill=(r, g, b))

# 2. Ambient Glows
glow_overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_overlay)

# Top right emerald/cyan glow for Drone/Robotics theme
glow_draw.ellipse([720, -100, 1320, 450], fill=(16, 185, 129, 45))
# Center bottom sky blue glow
glow_draw.ellipse([100, 200, 700, 700], fill=(14, 165, 233, 40))
glow_draw.ellipse([850, 260, 1220, 560], fill=(245, 158, 11, 30))

glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(65))
img.paste(glow_overlay, (0, 0), glow_overlay)
draw = ImageDraw.Draw(img)

# Load fonts
font_path_bold = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
font_path_reg = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

font_title = ImageFont.truetype(font_path_bold, 38)
font_subtitle = ImageFont.truetype(font_path_reg, 18)
font_badge = ImageFont.truetype(font_path_bold, 13)
font_pill = ImageFont.truetype(font_path_bold, 14)
font_card_head = ImageFont.truetype(font_path_bold, 17)
font_card_sub = ImageFont.truetype(font_path_reg, 13)

# 3. Left Content Column:
# Badge Pill
badge_text = "AMEETECH  •  FOUNDER PROFILE & EMERGING TECH"
draw.rounded_rectangle([70, 55, 490, 88], radius=16, fill=(16, 185, 129, 200), outline=(110, 231, 183))
draw.text((95, 64), badge_text, font=font_badge, fill=(255, 255, 255))

# Main Title (wrapped)
title_line1 = "From Importing to Innovating:"
title_line2 = "Drone Forge Africa & Founder Story"
draw.text((70, 110), title_line1, font=font_title, fill=(255, 255, 255))
draw.text((70, 156), title_line2, font=font_title, fill=(52, 211, 153))

# Subtitle
sub_line1 = "Nasir Muhammad Auwal on UAV Technology, STEM Education,"
sub_line2 = "Precision Agriculture, and Building Robotics in Nigeria."
draw.text((70, 226), sub_line1, font=font_subtitle, fill=(226, 232, 240))
draw.text((70, 254), sub_line2, font=font_subtitle, fill=(148, 163, 184))

# 4 Feature Pills
pills = [
    ("★ UAV Engineering & Local Capabilities", 70, 310, 400, 346),
    ("★ Hands-on Workshops in Kano & Kaduna", 70, 362, 405, 398),
    ("★ Precision Agriculture & Aerial Mapping", 70, 414, 405, 450),
    ("★ Exclusive Fagen Hikima Interview", 70, 466, 375, 502)
]

for label, x1, y1, x2, y2 in pills:
    draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=(30, 41, 59, 180), outline=(51, 65, 85))
    draw.text((x1 + 14, y1 + 8), label, font=font_pill, fill=(241, 245, 249))

# 4. Right Visual Mockup (Founder Insight Card & Tech Framework)
mock_bg_x, mock_bg_y, mock_bg_w, mock_bg_h = 710, 55, 430, 440
draw.rounded_rectangle([mock_bg_x, mock_bg_y, mock_bg_x + mock_bg_w, mock_bg_y + mock_bg_h],
                       radius=20, fill=(15, 23, 42, 230), outline=(16, 185, 129), width=2)

# Card Header
draw.rounded_rectangle([mock_bg_x, mock_bg_y, mock_bg_x + mock_bg_w, mock_bg_y + 68],
                       radius=20, fill=(30, 41, 59, 240))
draw.rectangle([mock_bg_x, mock_bg_y + 40, mock_bg_x + mock_bg_w, mock_bg_y + 68], fill=(30, 41, 59, 240))

# Paste Ameetech logo
try:
    amee_icon = Image.open('images/ameelogo.png').convert('RGBA')
    amee_icon = amee_icon.resize((42, 42), Image.Resampling.LANCZOS)
    img.paste(amee_icon, (mock_bg_x + 18, mock_bg_y + 13), amee_icon)
except Exception as e:
    print('amee_icon error:', e)

draw.text((mock_bg_x + 72, mock_bg_y + 15), "Drone Forge Africa Spotlight", font=font_card_head, fill=(255, 255, 255))
draw.text((mock_bg_x + 72, mock_bg_y + 38), "Featuring Nasir Muhammad Auwal", font=font_card_sub, fill=(52, 211, 153))

# Sub-block 1: Mission
box1_y = mock_bg_y + 85
draw.rounded_rectangle([mock_bg_x + 18, box1_y, mock_bg_x + 412, box1_y + 90],
                       radius=12, fill=(30, 41, 59, 180), outline=(71, 85, 105))
draw.text((mock_bg_x + 32, box1_y + 12), "Vision: Developing Local UAV Capacity", font=font_card_head, fill=(56, 189, 248))
draw.text((mock_bg_x + 32, box1_y + 38), "• Transition from consumer to tech creator", font=font_card_sub, fill=(226, 232, 240))
draw.text((mock_bg_x + 32, box1_y + 60), "• Drone simulation, calibration & repair", font=font_card_sub, fill=(148, 163, 184))

# Sub-block 2: Core Focus Areas
box2_y = box1_y + 105
draw.rounded_rectangle([mock_bg_x + 18, box2_y, mock_bg_x + 412, box2_y + 90],
                       radius=12, fill=(30, 41, 59, 180), outline=(71, 85, 105))
draw.text((mock_bg_x + 32, box2_y + 12), "Sectors & Applications", font=font_card_head, fill=(251, 191, 36))
draw.text((mock_bg_x + 32, box2_y + 38), "• Precision Agriculture & Crop Health Mapping", font=font_card_sub, fill=(226, 232, 240))
draw.text((mock_bg_x + 32, box2_y + 60), "• Aerial Topography, IoT & STEM Bootcamps", font=font_card_sub, fill=(148, 163, 184))

# Sub-block 3: Founder Principle
box3_y = box2_y + 105
draw.rounded_rectangle([mock_bg_x + 18, box3_y, mock_bg_x + 412, box3_y + 90],
                       radius=12, fill=(30, 41, 59, 180), outline=(71, 85, 105))
draw.text((mock_bg_x + 32, box3_y + 12), "Founder Takeaway", font=font_card_head, fill=(244, 114, 182))
draw.text((mock_bg_x + 32, box3_y + 38), "• Understand community problems before building", font=font_card_sub, fill=(226, 232, 240))
draw.text((mock_bg_x + 32, box3_y + 60), "• Build partnerships to de-risk hard tech", font=font_card_sub, fill=(148, 163, 184))

# Save output
os.makedirs('images/blog', exist_ok=True)
output_path = 'images/blog/drone_forge_africa_founder_banner.png'
img.save(output_path, 'PNG', optimize=True)
print(f"Successfully generated {output_path} ({w}x{h})")
