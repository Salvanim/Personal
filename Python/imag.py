from PIL import Image, ImageDraw, ImageFont, ImageColor

class imageDraw():
    def __init__(self, size, backgroundColor, imageType='RGBA'):
        self.size = size
        self.image = Image.new(imageType, size, backgroundColor)
        self.draw = ImageDraw.Draw(self.image)

    def rect(self, startX, startY, endX, endY, fill='white', outline='black',rectwidth=1):
        self.draw.rectangle([(startX, startY), (endX, endY)], fill=fill, outline=outline, width=rectwidth)

    def text(self, x, y, content, fill, fontName='arial.ttf', fontsize=20):
        self.draw.text((x, y), content, fill=fill, font=ImageFont.truetype(fontName, size=fontsize))

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

    def line(self, startX, startY, endX, endY, color):
        dx = abs(endX - startX)
        dy = abs(endY - startY)
        sx = 1 if startX < endX else -1
        sy = 1 if startY < endY else -1
        err = dx - dy

        x = startX
        y = startY

        while True:
            self.colorPixel(x, y, color)

            if x == endX and y == endY:
                break

            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x += sx

            if e2 < dx:
                err += dx
                y += sy

    def ellipse(self, rx, ry, xc, yc, color='red', fill='red', lineThickness=1):
        def plot_ellipse(rx, ry, xc, yc, color):
            x = 0
            y = ry

            # Initial decision parameter of region 1
            d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
            dx = 2 * ry * ry * x
            dy = 2 * rx * rx * y

            # Region 1
            while dx < dy:
                # 4-way symmetry
                self.colorPixel(x + xc, y + yc, color)
                self.colorPixel(-x + xc, y + yc, color)
                self.colorPixel(x + xc, -y + yc, color)
                self.colorPixel(-x + xc, -y + yc, color)

                if d1 < 0:
                    x += 1
                    dx += 2 * ry * ry
                    d1 += dx + ry * ry
                else:
                    x += 1
                    y -= 1
                    dx += 2 * ry * ry
                    dy -= 2 * rx * rx
                    d1 += dx - dy + ry * ry

            # Decision parameter for region 2
            d2 = ((ry * ry * (x + 0.5) ** 2) + (rx * rx * (y - 1) ** 2) - (rx * rx * ry * ry))

            # Region 2
            while y >= 0:
                # 4-way symmetry
                self.colorPixel(x + xc, y + yc, color)
                self.colorPixel(-x + xc, y + yc, color)
                self.colorPixel(x + xc, -y + yc, color)
                self.colorPixel(-x + xc, -y + yc, color)

                if d2 > 0:
                    y -= 1
                    dy -= 2 * rx * rx
                    d2 += rx * rx - dy
                else:
                    y -= 1
                    x += 1
                    dx += 2 * ry * ry
                    dy -= 2 * rx * rx
                    d2 += dx - dy + rx * rx

        savedRx, savedRy = rx, ry

        # Fill the ellipse from the outer to the inner layer
        for rxi in range(savedRx-lineThickness):
            for ryi in range(savedRy-lineThickness):
                plot_ellipse(rxi, ryi, xc, yc, fill)

        # Draw the outermost ellipse (outline)
        for rxi in range(lineThickness+1):
            for ryi in range(lineThickness+1):
                plot_ellipse(rx-rxi, ry-ryi, xc, yc, color)

    def shape(self, color, fill, *points):
        points = list(points)
        points.append(points[0])
        points = tuple(points)
        self.draw.polygon(points, fill=fill, outline=color)

    def generate_gradient(self, start_color, end_color, steps):
        start_rgb = ImageColor.getrgb(start_color)
        end_rgb = ImageColor.getrgb(end_color)
        gradient = []

        for step in range(steps):
            ratio = step / (steps - 1)
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            gradient.append((r, g, b))

        return gradient

    def grad_rect(self, startX, startY, endX, endY, start_color='white', end_color='black', rectwidth=1):
        width = endX - startX
        height = endY - startY
        gradient = self.generate_gradient(start_color, end_color, height)

        for y in range(height):
            current_color = gradient[y]
            self.rect(startX, startY + y, endX, startY + y, fill=current_color, outline=current_color, rectwidth=rectwidth)

    def grad_line(self, startX, startY, endX, endY, start_color='red', end_color='blue'):
        dx = abs(endX - startX)
        dy = abs(endY - startY)
        sx = 1 if startX < endX else -1
        sy = 1 if startY < endY else -1
        err = dx - dy

        gradient = self.generate_gradient(start_color, end_color, max(dx, dy) + 1)

        x = startX
        y = startY
        color_idx = 0

        while True:
            self.colorPixel(x, y, gradient[color_idx])

            if x == endX and y == endY:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx

            if e2 < dx:
                err += dx
                y += sy

            color_idx = min(color_idx + 1, len(gradient) - 1)  # Ensure color_idx stays within bounds

    def grad_ellipse(self, rx, ry, xc, yc, start_color='red', end_color='blue', lineThickness=1):
        def plot_ellipse(rx, ry, xc, yc, color):
            x = 0
            y = ry
            d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
            dx = 2 * ry * ry * x
            dy = 2 * rx * rx * y

            while dx < dy:
                self.colorPixel(x + xc, y + yc, color)
                self.colorPixel(-x + xc, y + yc, color)
                self.colorPixel(x + xc, -y + yc, color)
                self.colorPixel(-x + xc, -y + yc, color)

                if d1 < 0:
                    x += 1
                    dx += 2 * ry * ry
                    d1 += dx + ry * ry
                else:
                    x += 1
                    y -= 1
                    dx += 2 * ry * ry
                    dy -= 2 * rx * rx
                    d1 += dx - dy + ry * ry

            d2 = (ry * ry * (x + 0.5) ** 2) + (rx * rx * (y - 1) ** 2) - (rx * rx * ry * ry)

            while y >= 0:
                self.colorPixel(x + xc, y + yc, color)
                self.colorPixel(-x + xc, y + yc, color)
                self.colorPixel(x + xc, -y + yc, color)
                self.colorPixel(-x + xc, -y + yc, color)

                if d2 > 0:
                    y -= 1
                    dy -= 2 * rx * rx
                    d2 += rx * rx - dy
                else:
                    y -= 1
                    x += 1
                    dx += 2 * ry * ry
                    dy -= 2 * rx * rx
                    d2 += dx - dy + rx * rx

        savedRx, savedRy = rx, ry
        gradient = self.generate_gradient(start_color, end_color, savedRy + 1)

        for rxi in range(savedRx - lineThickness):
            for ryi in range(savedRy - lineThickness):
                color = gradient[min(ryi, len(gradient) - 1)]
                plot_ellipse(rxi, ryi, xc, yc, color)

        for rxi in range(lineThickness + 1):
            for ryi in range(lineThickness + 1):
                plot_ellipse(rx - rxi, ry - ryi, xc, yc, start_color)

    def grad_shape(self, start_color, end_color, *points):
        points = list(points)
        points.append(points[0])
        gradient = self.generate_gradient(start_color, end_color, len(points) - 1)

        for i in range(len(points) - 1):
            self.line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], gradient[i])

    def grad_text(self, x, y, content, start_color, end_color, fontName='arial.ttf', fontsize=20):
        gradient = self.generate_gradient(start_color, end_color, len(content))

        for i, char in enumerate(content):
            self.text(x + i * fontsize, y, char, fill=gradient[i], fontName=fontName, fontsize=fontsize)

    def fill_shape_with_image(self, imagePath, *points):

        # Load the image
        shape_image = Image.open(imagePath)
        shape_image = shape_image.convert('RGBA')  # Ensure it has an alpha channel for transparency

        # Create a mask to use the image only within the shape
        mask_image = Image.new('L', self.size, 0)  # Mask is the same size as the canvas (black)
        mask_draw = ImageDraw.Draw(mask_image)

        # If the shape is a polygon
        if len(points) > 2:
            points = list(points)
            mask_draw.polygon(points, outline=255, fill=255)
        else:
            # If it's a rectangle
            mask_draw.rectangle(points, outline=255, fill=255)

        # Create the final shape by pasting the image onto it
        final_shape = Image.new('RGBA', self.size, (0, 0, 0, 0))
        final_shape.paste(shape_image, (0, 0), mask_image)

        # Clip the image to the mask (only keep pixels within the shape)
        self.image.paste(final_shape, (0, 0), mask_image)

    def fill_rect_with_image(self, startX, startY, endX, endY, imagePath):
        # Load the image
        image_to_fill = Image.open(imagePath)
        image_to_fill = image_to_fill.convert('RGBA')  # Ensure it has an alpha channel for transparency

        # Resize the image to fit within the bounds of the rectangle
        rect_width = endX - startX
        rect_height = endY - startY
        image_to_fill = image_to_fill.resize((rect_width, rect_height))

        # Paste the resized image into the rectangle
        self.image.paste(image_to_fill, (startX, startY), image_to_fill)

    def fill_ellipse_with_image(self, rx, ry, xc, yc, imagePath):
        # Load the image
        ellipse_image = Image.open(imagePath)
        ellipse_image = ellipse_image.convert('RGBA')

        # Create an empty image with the size of the ellipse
        ellipse_size = (rx * 2, ry * 2)
        filled_ellipse = Image.new('RGBA', ellipse_size, (0, 0, 0, 0))

        # Resize the image to fit the ellipse bounds
        ellipse_image = ellipse_image.resize(ellipse_size)

        # Create a mask for the ellipse shape (white where the ellipse is, black elsewhere)
        mask = Image.new('L', ellipse_size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([(0, 0), ellipse_size], fill=255)

        # Paste the image inside the ellipse using the mask
        filled_ellipse.paste(ellipse_image, (0, 0), mask)

        # Paste the filled ellipse back to the main image
        self.image.paste(filled_ellipse, (xc - rx, yc - ry), mask)

    def fill_polygon_with_image(self, imagePath, *points):
        # Load the image
        polygon_image = Image.open(imagePath)
        polygon_image = polygon_image.convert('RGBA')  # Ensure it has an alpha channel

        # Create a mask for the polygon shape
        mask = Image.new('L', self.size, 0)  # Black mask (invisible)
        mask_draw = ImageDraw.Draw(mask)

        # Draw the polygon on the mask (white where the polygon is)
        points = list(points)
        mask_draw.polygon(points, fill=255)

        # Resize the image to fit within the bounding box of the polygon
        min_x = min([pt[0] for pt in points])
        max_x = max([pt[0] for pt in points])
        min_y = min([pt[1] for pt in points])
        max_y = max([pt[1] for pt in points])
        polygon_image = polygon_image.resize((max_x - min_x, max_y - min_y))

        # Create the final image by pasting the resized image into the polygon shape
        final_image = Image.new('RGBA', self.size, (0, 0, 0, 0))
        final_image.paste(polygon_image, (min_x, min_y), mask)

        # Paste the final image onto the main canvas using the polygon mask
        self.image.paste(final_image, (0, 0), mask)

    def save(self, name):
        self.image.save(name)

image = imageDraw((500, 500), 'white')

# 1. Draw a gradient rectangle
image.grad_rect(50, 50, 300, 150, start_color='blue', end_color='green')

# 2. Draw a gradient line
image.grad_line(100, 200, 400, 400, start_color='red', end_color='yellow')

# 3. Draw a gradient ellipse
image.grad_ellipse(80, 40, 300, 300, start_color='purple', end_color='orange', lineThickness=3)

# 4. Draw a gradient polygon (triangle)
image.grad_shape('black', 'cyan', (350, 100), (400, 50), (450, 100))

# 5. Draw gradient text
image.grad_text(50, 400, "Hello Gradient!", start_color='pink', end_color='lightblue', fontsize=40)

# Save the image
image.save('Created/gradient_image.png')

# Assuming `imageDraw` class is instantiated as `img_draw`
img_draw = imageDraw((5000, 5000), 'blue')

# Fill a rectangle with an image
img_draw.fill_rect_with_image(50, 50, 300, 200, 'Created/gradient_image.png')

# Fill an ellipse with an image
img_draw.fill_ellipse_with_image(80, 50, 250, 250, 'Created/gradient_image.png')

# Fill a polygon with an image
img_draw.fill_polygon_with_image('Created/gradient_image.png', (100, 100), (400, 50), (450, 300), (50, 350))

# Save the image with filled shapes
img_draw.save('filled_shapes_image.png')

