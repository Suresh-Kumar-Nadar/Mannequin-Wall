from PIL import Image

# Load the resized image and the resized cut
image = Image.open("input_1000.jpg")
cut = Image.open("suresh.jpeg")

# Scaled-down coordinates
x1, y1 = 377, 0
x2, y2 = 634, 1000

# Create a white rectangle where the cut was
white_box = Image.new("RGB", (x2 - x1, y2 - y1), color=(255, 255, 255))
image.paste(white_box, (x1, y1))

# Paste the cut image back into the original
image.paste(cut, (x1, y1))
image.save("suresh_output.jpg")

print("Final image saved as final_combined_resized.jpg")
