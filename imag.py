from PIL import Image, ImageDraw, ImageFont

class imageDraw():
    def __init__(self, size, backgroundColor):
        self.size = size
        self.image = Image.new('RGB', size, backgroundColor)
        self.draw = ImageDraw.Draw(self.image)

    def rect(self, startX, startY, endX, endY, fill='white', outline='black',rectwidth=1):
        self.draw.rectangle([(startX, startY), (endX, endY)], fill=fill, outline=outline, width=rectwidth)
    
    def circle(self, x, y, radius, fill='white', outline='black', width=1):
        self.draw.circle((x,y), radius, fill, outline=outline, width=width)
    
    def text(self, x, y, content, fill, fontName='arial.ttf', fontsize=20):
        self.draw.text((x, y), content, fill=fill, font=ImageFont.truetype(fontName, size=fontsize))
    
    def ellipse(self, x, y, fill, outline, width=1):
        self.draw.ellipse((x,y), fill=fill, outline=outline, width=width)
    
    def colorPixel(self, x, y, color):
        self.rect(x, y, x, y, color, color, 1)

    def convertArray(self, locationArray, colorArray):
        for i in range(min(len(locationArray), len(colorArray))):
            self.colorPixel(locationArray[i][0],locationArray[i][1], colorArray[i])

    def getPixel(self, x, y):
        return self.image.getpixel((x, y))
    
    def toArrays(self):
        locationArray = []
        colorArray = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                colorArray.append(self.getPixel(x, y))
                locationArray.append((x,y))
        return locationArray, colorArray

    def Ellipse(self, rx, ry, xc, yc, color):
        for rxi in range(rx):
            rx = rxi
            for ryi in range(ry):
                ry = ryi
                x = 0; 
                y = ry; 
            
                # Initial decision parameter of region 1 
                d1 = ((ry * ry) - (rx * rx * ry) +
                                (0.25 * rx * rx)); 
                dx = 2 * ry * ry * x; 
                dy = 2 * rx * rx * y; 
            
                # For region 1 
                while (dx < dy): 
            
                    # Adding points based on 4-way symmetry
                    self.colorPixel(x + xc,  y + yc, color)
                    self.colorPixel(-x + xc,  y + yc, color)
                    self.colorPixel(x + xc,  -y + yc, color)
                    self.colorPixel(-x + xc,  -y + yc, color)
            
                    # Checking and updating value of 
                    # decision parameter based on algorithm 
                    if (d1 < 0): 
                        x += 1; 
                        dx = dx + (2 * ry * ry); 
                        d1 = d1 + dx + (ry * ry); 
                    else:
                        x += 1; 
                        y -= 1; 
                        dx = dx + (2 * ry * ry); 
                        dy = dy - (2 * rx * rx); 
                        d1 = d1 + dx - dy + (ry * ry); 
            
                # Decision parameter of region 2 
                d2 = (((ry * ry) * ((x + 0.5) * (x + 0.5))) +
                    ((rx * rx) * ((y - 1) * (y - 1))) -
                    (rx * rx * ry * ry)); 
            
                # Plotting points of region 2 
                while (y >= 0):
            
                    # Adding points to point array based on 4-way symmetry
                    self.colorPixel(x + xc,  y + yc, color)
                    self.colorPixel(-x + xc,  y + yc, color)
                    self.colorPixel(x + xc,  -y + yc, color)
                    self.colorPixel(-x + xc,  -y + yc, color)
            
                    # Checking and updating parameter 
                    # value based on algorithm 
                    if (d2 > 0):
                        y -= 1; 
                        dy = dy - (2 * rx * rx); 
                        d2 = d2 + (rx * rx) - dy; 
                    else:
                        y -= 1; 
                        x += 1; 
                        dx = dx + (2 * ry * ry); 
                        dy = dy - (2 * rx * rx); 
                        d2 = d2 + dx - dy + (rx * rx); 

    def save(self, name):
        self.image.save(name)

# Setting the size of the image
size = (400, 300)

image = imageDraw(size, 'blue')
image.ellipse(10, 15, 200, 150, 'red')
image.save('custom_image.png')

# # Create an image with a blue background
# image_with_background = Image.new('RGB', size, 'blue')

# draw = ImageDraw.Draw(image_with_background)

# draw.rectangle(
#     [(50, 50), (100, 100)], 
#     fill='yellow', 
#     outline='black'
# )

# draw.text(
#     (150, 75), 
#     'Hello World!', 
#     fill='white', 
#     font=ImageFont.truetype('arial.ttf', size=20)
# )

# # Save the customized image
# image_with_background.save('custom_image.png')