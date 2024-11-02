import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Shape:
    def __init__(self, vertices, edges, faces, colors, position=(0, 0, 0), size=1, rotation=(0, 0, 0)):
        self.vertices = np.array(vertices) * size  # Scale vertices based on size
        self.edges = edges
        self.faces = faces
        self.colors = colors
        self.position = np.array(position)
        self.size = size
        self.rotation = np.array(rotation)

    def set_position(self, position):
        self.position = np.array(position)

    def set_size(self, size):
        self.size = size
        self.vertices = self.vertices / self.size  # Reset vertices to original size and then scale
        self.vertices *= size

    def set_rotation(self, rotation):
        self.rotation = np.array(rotation)

    def draw(self):
        glPushMatrix()  # Save the current transformation matrix
        glTranslatef(*self.position)  # Apply translation
        glRotatef(self.rotation[0], 1, 0, 0)  # Rotate around x-axis
        glRotatef(self.rotation[1], 0, 1, 0)  # Rotate around y-axis
        glRotatef(self.rotation[2], 0, 0, 1)  # Rotate around z-axis

        # Draw each face of the shape
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            glColor3fv(self.colors[i % len(self.colors)])  # Set color for each face
            for vertex in face:
                glVertex3fv(self.vertices[vertex])  # Specify each vertex of the face
        glEnd()

        # Draw edges
        glBegin(GL_LINES)
        glColor3fv((0, 0, 0))  # Set edge color to black
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glPopMatrix()  # Restore the original transformation matrix


class Cube(Shape):
    def __init__(self, colors, position=(0, 0, 0), size=1, rotation=(0, 0, 0)):
        # Define vertices, edges, and faces for a cube
        vertices = [
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1]
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
        ]
        faces = [
            (0, 1, 2, 3),  # Back face
            (4, 5, 6, 7),  # Front face
            (0, 1, 5, 4),  # Right face
            (2, 3, 7, 6),  # Left face
            (1, 2, 6, 5),  # Bottom face
            (0, 3, 7, 4)   # Top face
        ]

        # Initialize the Shape with cube parameters and dynamic colors
        super().__init__(vertices, edges, faces, colors, position, size)


class OpenGLApp:
    def __init__(self):
        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)  # Enable depth testing

        # Set up perspective
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -10)  # Move the camera back

        # Define colors for the cubes (can be any desired colors)
        colors = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, 0, 1), (0, 1, 1)
        ]

        # Create a grid of cubes
        self.cubes = []
        cube_size = 0.5  # Set the size of each cube
        spacing = 1.0  # Set the spacing between cubes
        grid_size = 5  # Set the grid size (5x5)

        for x in range(grid_size):
            for y in range(grid_size):
                position = (x * spacing, y * spacing, 0)  # Position cubes in a grid
                self.cubes.append(Cube(colors, position=position, size=cube_size))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Clear color and depth buffer
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Draw all cubes in the grid
            for cube in self.cubes:
                cube.draw()

            pygame.display.flip()
            clock.tick(60)  # Limit the frame rate to 60 FPS


if __name__ == "__main__":
    app = OpenGLApp()
    app.run()
