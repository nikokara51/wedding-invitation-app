import csv
import os
from urllib.parse import quote_plus
import qrcode
from PIL import Image, ImageDraw, ImageFont

# Base URL for invitations
BASE = os.environ.get('BASE_URL', 'http://localhost:8000') + '/invite/'

# Ensure output folder exists
os.makedirs('output_qr', exist_ok=True)

# Optional: font for text
try:
    FONT_PATH = "arial.ttf"  # replace with a nicer font if available
    font = ImageFont.truetype(FONT_PATH, 28)
except:
    font = ImageFont.load_default()

# Read CSV and generate QR codes
with open('data/guests.csv', newline='', encoding='utf-8') as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        slug = row['slug']
        url = BASE + quote_plus(slug)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="#C84B31", back_color=None).convert("RGBA")  # warm color

        # Create invitation-style background
        bg = Image.new("RGBA", (qr_img.size[0]+60, qr_img.size[1]+120), (255, 244, 230, 255))  # cream background
        draw = ImageDraw.Draw(bg)

        # Title text
        text = "Scan Me!"
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((bg.width-w)//2, 20), text, font=font, fill="#6B4226")

        # Paste QR code in center
        qr_x = (bg.width - qr_img.width) // 2
        qr_y = 60
        bg.paste(qr_img, (qr_x, qr_y), qr_img)

        # Footer text
        footer = "Our Wedding Invitation"
        bbox = draw.textbbox((0, 0), footer, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((bg.width-w)//2, qr_y + qr_img.height + 10), footer, font=font, fill="#C84B31")

        # Save PNG
        output_path = f'output_qr/{slug}.png'
        bg.save(output_path)
        print(f"✅ Generated fancy QR for {slug}: {url}")
