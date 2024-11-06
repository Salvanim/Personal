import numpy as np
import pygame
import sys

# Signed Distance Function for a circle (Vectorized for multiple points)
def sdf_circle(points, center, radius):
    return np.linalg.norm(points - center, axis=1) - radius

# Raymarching algorithm (Vectorized for efficiency)
def raymarch(origins, directions, max_steps=100, max_dist=100.0, epsilon=0.001):
    dist_traveled = np.zeros(origins.shape[0])
    points = origins.copy()

    for _ in range(max_steps):
        dist_to_surface = sdf_circle(points, np.array([0.0, 0.0]), 1.0)  # Circle centered at origin with radius 1
        hit_mask = dist_to_surface < epsilon

        if np.all(hit_mask):
            break

        dist_traveled += dist_to_surface * ~hit_mask
        points += directions * dist_to_surface[:, np.newaxis]

        if np.any(dist_traveled > max_dist):
            break

    return dist_traveled

# Rendering the scene (Vectorized version)
def render(width, height, fov, player_pos):
    aspect_ratio = width / height

    # Create a grid of screen coordinates
    i_coords = np.tile(np.arange(width), height)
    j_coords = np.repeat(np.arange(height), width)

    # Convert to normalized device coordinates
    x = (2 * (i_coords + 0.5) / width - 1) * aspect_ratio * np.tan(fov / 2)
    y = (1 - 2 * (j_coords + 0.5) / height) * np.tan(fov / 2)

    # Create ray directions (normalize them)
    directions = np.stack([x, y], axis=1)
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)

    # Initialize ray origins (all rays start from the player's position)
    origins = np.tile(player_pos, (width * height, 1))

    # Perform raymarching (vectorized)
    dist_traveled = raymarch(origins, directions)

    # Convert distance to pixel values (for visualization)
    image = np.exp(-dist_traveled).reshape(height, width)

    return image

# Main function
def main():
    width, height = 1000, 1000  # Increase resolution to 10,000 x 10,000
    screenW, screenH = 800, 800
    fov = np.pi / 3  # Field of view (60 degrees)
    player_pos = np.array([2.0, 2.0])  # Starting player position
    speed = 0.1  # Player movement speed

    # Set up pygame screen
    screen = pygame.display.set_mode((screenW, screenH))  # Display at reduced size
    pygame.display.set_caption("Optimized Raymarching")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Move up
            player_pos[1] -= speed
        if keys[pygame.K_s]:  # Move down
            player_pos[1] += speed
        if keys[pygame.K_a]:  # Move left
            player_pos[0] -= speed
        if keys[pygame.K_d]:  # Move right
            player_pos[0] += speed

        # FOV controls
        if keys[pygame.K_q]:  # Decrease FOV
            fov -= 0.01
            fov = max(fov, np.pi / 6)  # Limit minimum FOV (30 degrees)
        if keys[pygame.K_e]:  # Increase FOV
            fov += 0.01
            fov = min(fov, np.pi / 2)  # Limit maximum FOV (90 degrees)

        # Render the scene (vectorized and optimized)
        image = render(width, height, fov, player_pos)

        # Convert numpy array to a surface (downsample for display)
        downsampled_image = image[::10, ::10]  # Downsample for display
        surface = pygame.surfarray.make_surface(np.rot90((image * 255).astype(np.uint8)))
        screen.blit(surface, (0, 0))

        # Refresh display
        pygame.display.update()

        # Cap the frame rate
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
