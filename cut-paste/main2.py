from PIL import Image

# Load the original image and the cut image
image = Image.open("input_12000.jpg")
cut = Image.open("suresh.jpg")

# Coordinates
x1, y1 = 4527, 0
x2, y2 = 7616, 12000

# Create a white rectangle where the cut was
white_box = Image.new("RGB", (x2 - x1, y2 - y1), color=(255, 255, 255))
image.paste(white_box, (x1, y1))

# Now paste the cut image back into that region
image.paste(cut, (x1, y1))
image.save("output_suresh.jpg")

print("Final image saved as final_combined.jpeg")
