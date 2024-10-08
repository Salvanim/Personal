from PIL import Image, ImageDraw, ImageFont

# Setting the size of the image
size = (400, 300)

# Create an image with a blue background
image_with_background = Image.new('RGB', size, 'blue')

draw = ImageDraw.Draw(image_with_background)

draw.rectangle(
    [(50, 50), (100, 100)], 
    fill='yellow', 
    outline='black'
)

draw.text(
    (150, 75), 
    'Hello World!', 
    fill='white', 
    font=ImageFont.truetype('arial.ttf', size=20)
)

# Save the customized image
image_with_background.save('custom_image.png')