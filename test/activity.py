from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import locale

# Set locale ke Indonesia (hanya berhasil jika locale tersedia di sistem)
try:
    locale.setlocale(locale.LC_TIME, 'id_ID.utf8')  # Linux biasanya
except:
    try:
        locale.setlocale(locale.LC_TIME, 'indonesian')  # Windows
    except:
        pass  # fallback ke default (bahasa Inggris)



lead = env['crm.lead'].search([], limit=15)


# Set up image
width = 800
height = 170 + 20  * len(lead)
background_color = (255, 255, 255)
text_color = (0, 0, 0)

# Create a blank image
img = Image.new('RGB', (width, height), color=background_color)
draw = ImageDraw.Draw(img)


# Print each lead
# for l in lead:
#     print('{:<30} {:<15} Rp.{:>15}'.format(
#         l.name or '',
#         str(l.activity_date_deadline or ''),
#         str(str(f"{l.planned_revenue:,.0f}".replace(',', '.') or '') or '')
#     ))
    
# Load a font (default if no TTF available)
try:
    #font = ImageFont.truetype("arial.ttf", 20)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
    font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 14)
except:
    font = ImageFont.load_default()


# Header
x = 50
y = 30
tanggal_sekarang = datetime.today()
tanggal_str = tanggal_sekarang.strftime('%A, %d-%b-%Y')

judul= 'Laporan Lead PT Azka Mulia International'
print(judul)
draw.text((x, y),judul, fill=text_color, font=font_header)
y += 20
subjudul='Hari/Tanggal :{}'.format(tanggal_str)
print(subjudul)
draw.text((x, y), subjudul, fill=text_color, font=font)
y += 20
garis= '-' * 70
print(garis)
draw.text((x, y),garis, fill=text_color, font=font)
y += 14
header='{:>3} {:<30} {:<15} {:>15}'.format('No','Nama Lead', 'Customer', 'Exp.Revenue')
print(header)
draw.text((x, y),header , fill=text_color, font=font)
y += 15
print(garis)
draw.text((x, y), garis, fill=text_color, font=font)
y += 20

# Draw each lead
subtotal=0
urut=0
for l in lead:
    name = l.name or ''
    partner = str(l.partner_id.name or '')
    revenue = str(f"{l.planned_revenue:,.0f}".replace(',', '.') or '')
    urut+=1
    subtotal+=l.planned_revenue
    line = "{:>3} {:<30} {:<15} Rp.{:>15}".format(str(urut),name, partner, revenue)
    print(line)
    draw.text((x, y), line, fill=text_color, font=font)
    y += 20
print(garis)
draw.text((x, y), garis, fill=text_color, font=font)
y += 15
footer='{:>3} {:<30} {:<15} Rp.{:>15}'.format('','Total :', '', str(f"{subtotal:,.0f}".replace(',', '.') or ''))
print(footer)
draw.text((x, y), footer, fill=text_color, font=font)
y += 15

# Save as image
img.save("report.jpg")