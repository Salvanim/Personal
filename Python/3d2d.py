import json
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# Load the model data and texture image
with open("Python\katana.json") as f:
    model_json = json.load(f)

texture_image = Image.open("Python\katanatexture.png")

# Function to convert 3D coordinates to 2D
def project_3d_to_2d(x, y, z):
    # Simplistic orthographic projection
    return x, y  # Disregard z for 2D projection

# Create an image to draw the 2D projection
canvas = Image.new("RGBA", texture_image.size, (255, 255, 255, 0))
draw = ImageDraw.Draw(canvas)

# Parse and draw each element
for element in model_json["elements"]:
    from_coord = element["from"]
    to_coord = element["to"]
    faces = element["faces"]

    # Define the vertices for each face in 3D space
    vertices = {
        "north": [(from_coord[0], from_coord[1], to_coord[2]), (to_coord[0], from_coord[1], to_coord[2]),
                  (to_coord[0], to_coord[1], to_coord[2]), (from_coord[0], to_coord[1], to_coord[2])],
        "east": [(to_coord[0], from_coord[1], from_coord[2]), (to_coord[0], from_coord[1], to_coord[2]),
                 (to_coord[0], to_coord[1], to_coord[2]), (to_coord[0], to_coord[1], from_coord[2])],
        "south": [(from_coord[0], from_coord[1], from_coord[2]), (to_coord[0], from_coord[1], from_coord[2]),
                  (to_coord[0], to_coord[1], from_coord[2]), (from_coord[0], to_coord[1], from_coord[2])],
        "west": [(from_coord[0], from_coord[1], from_coord[2]), (from_coord[0], from_coord[1], to_coord[2]),
                 (from_coord[0], to_coord[1], to_coord[2]), (from_coord[0], to_coord[1], from_coord[2])],
        "up": [(from_coord[0], to_coord[1], from_coord[2]), (to_coord[0], to_coord[1], from_coord[2]),
               (to_coord[0], to_coord[1], to_coord[2]), (from_coord[0], to_coord[1], to_coord[2])],
        "down": [(from_coord[0], from_coord[1], from_coord[2]), (to_coord[0], from_coord[1], from_coord[2]),
                 (to_coord[0], from_coord[1], to_coord[2]), (from_coord[0], from_coord[1], to_coord[2])]
    }

    # Updated portion of the code for resizing and pasting face textures
    for face_name, face_vertices in vertices.items():
        face = faces[face_name]
        uv_coords = face["uv"]

        # Ensure UV coordinates are in the correct order
        left = min(uv_coords[0], uv_coords[2])
        right = max(uv_coords[0], uv_coords[2])
        top = min(uv_coords[1], uv_coords[3])
        bottom = max(uv_coords[1], uv_coords[3])

        # Map UV coordinates from texture
        face_texture = texture_image.crop((left, top, right, bottom))

        # Project vertices to 2D
        face_2d_vertices = [project_3d_to_2d(*v) for v in face_vertices]

        # Prepare polygon coordinates and paste face texture onto the canvas
        polygon = [tuple(face_2d_vertices[i]) for i in range(4)]
        min_x = min(p[0] for p in polygon)
        min_y = min(p[1] for p in polygon)

        # Calculate face width and height
        face_width = int(max(p[0] for p in polygon) - min_x)
        face_height = int(max(p[1] for p in polygon) - min_y)

        # Ensure non-zero dimensions
        face_width = max(1, face_width)
        face_height = max(1, face_height)

        # Resize texture to fit the face size
        face_texture = face_texture.resize((face_width, face_height))

        # Create a mask for pasting
        mask = Image.new("L", face_texture.size, 255)
        canvas.paste(face_texture, (int(min_x), int(min_y)), mask)

output_filename = "projection.png"
canvas.save(output_filename, format="PNG")
print(f"Saved 2D projection as {output_filename}")
