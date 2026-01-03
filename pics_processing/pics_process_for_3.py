from PIL import Image, ImageDraw

number = 11

book1 = "/new_thing.jpg"
book2 = "/magicien.jpg"
book3 = "/briser_les_os.jpg"

# Paths to your two images
image1_path = "C:/Users/devos/carnetslunaires/content/posts/26-en-2026" + book1
image2_path = "C:/Users/devos/carnetslunaires/content/posts/26-en-2026" + book2
image3_path = "C:/Users/devos/carnetslunaires/content/posts/26-en-2026" + book3


# Load images
img1 = Image.open(image1_path).convert("RGBA")
img2 = Image.open(image2_path).convert("RGBA")
img3 = Image.open(image3_path).convert("RGBA")


# Get widths
width1, height1 = img1.size
width2, height2 = img2.size
width3, height3 = img3.size

# Determine which is larger horizontally
if width1 > width2:
    # Resize img1 to width2
    new_height = int((width2 / width1) * height1)
    img1 = img1.resize((width2, new_height), Image.Resampling.LANCZOS)

    width_temp = width2
else:
    # Resize img2 to width1
    new_height = int((width1 / width2) * height2)
    img2 = img2.resize((width1, new_height), Image.Resampling.LANCZOS)

    width_temp = width1

if width3 > width_temp:
    # Resize img3 to width_temp
    new_height = int((width_temp / width3) * height3)
    img3 = img3.resize((width_temp, new_height), Image.Resampling.LANCZOS)
else:
    new_height = int((width3 / width_temp) * new_height)
    img1 = img1.resize((width3, new_height), Image.Resampling.LANCZOS)
    img2 = img2.resize((width3, new_height), Image.Resampling.LANCZOS)

# Resize heights to match (optional, but helps for merging)
min_height = min(img1.height, img2.height)
img1 = img1.resize((img1.width, min_height), Image.Resampling.LANCZOS)
img2 = img2.resize((img2.width, min_height), Image.Resampling.LANCZOS)

img3 = img3.resize((img3.width, min_height), Image.Resampling.LANCZOS)


# --- Step 2: Create diagonal masks ---
w, h = img1.size
mask1 = Image.new("L", (w, h), 0)
mask2 = Image.new("L", (w, h), 0)
mask3 = Image.new("L", (w, h), 0)

draw1 = ImageDraw.Draw(mask1)
draw2 = ImageDraw.Draw(mask2)
draw3 = ImageDraw.Draw(mask3)

# # First mask: keep top-left triangle
# draw1.polygon([(0, 0), (w, 0), (0, h)], fill=255)
# # Second mask: keep bottom-right triangle
# draw2.polygon([(w, h), (w, 0), (0, h)], fill=255)

# # First mask: keep top-right triangle
# draw1.polygon([(0, 0), (w, 0), (w, h)], fill=255)
# # Second mask: keep bottom-left triangle
# draw2.polygon([(0, 0), (0, h), (w, h)], fill=255)

# First mask: left rectangle
draw1.polygon([(0, 0), (w/3, 0), (w/3, h), (0, h)], fill=255)
# Second mask: right rectangle
draw2.polygon([(w*2/3, h), (w/3, h), (w/3, 0), (w*2/3, 0)], fill=255)

draw3.polygon([(w, h), (w*2/3, h), (w*2/3, 0), (w, 0)], fill=255)


# --- Step 3: Apply masks ---
part1 = Image.composite(img1, Image.new("RGBA", (w, h)), mask1)
part2 = Image.composite(img2, Image.new("RGBA", (w, h)), mask2)
part3 = Image.composite(img3, Image.new("RGBA", (w, h)), mask3)


# --- Step 4: Merge ---
final_img = Image.alpha_composite(part1, part2)

final_img = Image.alpha_composite(final_img, part3)


# --- Save result ---
final_img.convert("RGB").save("./pics_processing/multicouv.jpg")

print("✅ Done! Created 'multicouv.jpg'")