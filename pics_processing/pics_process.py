from PIL import Image, ImageDraw

number = 12

book1 = "/jewish_gangsta.jpg"
book2 = "/scholomance.jpg"

# Paths to your two images
image1_path = "C:/Users/devos/carnetslunaires/content/posts/notules-" + str(number) + book1
image2_path = "C:/Users/devos/carnetslunaires/content/posts/notules-" + str(number) + book2

# Load images
img1 = Image.open(image1_path).convert("RGBA")
img2 = Image.open(image2_path).convert("RGBA")

# Get widths
width1, height1 = img1.size
width2, height2 = img2.size

# Determine which is larger horizontally
if width1 > width2:
    # Resize img1 to width2
    new_height = int((width2 / width1) * height1)
    img1 = img1.resize((width2, new_height), Image.Resampling.LANCZOS)
else:
    # Resize img2 to width1
    new_height = int((width1 / width2) * height2)
    img2 = img2.resize((width1, new_height), Image.Resampling.LANCZOS)

# Resize heights to match (optional, but helps for merging)
min_height = min(img1.height, img2.height)
img1 = img1.resize((img1.width, min_height), Image.Resampling.LANCZOS)
img2 = img2.resize((img2.width, min_height), Image.Resampling.LANCZOS)

# --- Step 2: Create diagonal masks ---
w, h = img1.size
mask1 = Image.new("L", (w, h), 0)
mask2 = Image.new("L", (w, h), 0)

draw1 = ImageDraw.Draw(mask1)
draw2 = ImageDraw.Draw(mask2)

# First mask: keep top-left triangle
draw1.polygon([(0, 0), (w, 0), (0, h)], fill=255)
# Second mask: keep bottom-right triangle
draw2.polygon([(w, h), (w, 0), (0, h)], fill=255)

# # First mask: keep top-right triangle
# draw1.polygon([(0, 0), (w, 0), (w, h)], fill=255)
# # Second mask: keep bottom-left triangle
# draw2.polygon([(0, 0), (0, h), (w, h)], fill=255)

# # First mask: left rectangle
# draw1.polygon([(0, 0), (w/2, 0), (w/2, h), (0, h)], fill=255)
# # Second mask: right rectangle
# draw2.polygon([(w, h), (w/2, h), (w/2, 0), (w, 0)], fill=255)

# --- Step 3: Apply masks ---
part1 = Image.composite(img1, Image.new("RGBA", (w, h)), mask1)
part2 = Image.composite(img2, Image.new("RGBA", (w, h)), mask2)

# --- Step 4: Merge ---
final_img = Image.alpha_composite(part1, part2)

# --- Save result ---
final_img.convert("RGB").save("./pics_processing/multicouv.jpg")

print("✅ Done! Created 'multicouv.jpg'")