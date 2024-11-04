import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# DimensionalSpace class as defined earlier
class DimensionalSpace:
    def __init__(self, x=0, i=0, O=0):
        self.x = x
        self.i = i
        self.O = O

    def as_vector(self):
        return np.array([self.x, self.i, self.O])

    def divide_by_zero(self):
        # Apply the custom division by zero rule: a/0 = a * O
        return DimensionalSpace(self.x * self.O, self.i * self.O, self.O)

# Function to plot points in the 3D space with connections and clicking
def plot_3d_space(points, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extracting coordinates for each axis
    x_vals = [p.x for p in points]
    i_vals = [p.i for p in points]
    O_vals = [p.O for p in points]

    # Plotting the points
    scatter = ax.scatter(x_vals, i_vals, O_vals, c='b', marker='o', label='Original Points')

    # Connect points with lines
    for idx in range(len(points) - 1):
        ax.plot([points[idx].x, points[idx + 1].x],
                [points[idx].i, points[idx + 1].i],
                [points[idx].O, points[idx + 1].O], c='b', linestyle='--')

    # Add labels
    ax.set_xlabel('Real (x)')
    ax.set_ylabel('Imaginary (i)')
    ax.set_zlabel('O')
    ax.set_title(title)

    # Function to show point information on click
    def on_click(event):
        if event.inaxes == ax:
            # Get the clicked point's coordinates
            clicked_point = [event.xdata, event.ydata]
            closest_point_idx = np.argmin(np.sqrt((x_vals - clicked_point[0])**2 + (i_vals - clicked_point[1])**2))
            # Get the coordinates of the closest point
            point_info = f"Clicked Point: (x: {points[closest_point_idx].x}, i: {points[closest_point_idx].i}, O: {points[closest_point_idx].O})"
            print(point_info)

    # Connect the click event to the function
    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.legend()
    plt.show()

# Function to plot original and transformed points with connections
def plot_before_after(points):
    # Create a new figure for original vs transformed
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_vals = [p.x for p in points]
    i_vals = [p.i for p in points]
    O_vals = [p.O for p in points]

    # Apply division by zero to each point
    transformed_points = [p.divide_by_zero() for p in points]

    x_vals_trans = [p.x for p in transformed_points]
    i_vals_trans = [p.i for p in transformed_points]
    O_vals_trans = [p.O for p in transformed_points]

    # Plotting original points and connect them with lines
    scatter = ax.scatter(x_vals, i_vals, O_vals, c='b', marker='o', label='Original Points')
    for idx in range(len(points) - 1):
        ax.plot([points[idx].x, points[idx + 1].x],
                [points[idx].i, points[idx + 1].i],
                [points[idx].O, points[idx + 1].O], c='b', linestyle='--')

    # Plotting transformed points after division by zero
    scatter_trans = ax.scatter(x_vals_trans, i_vals_trans, O_vals_trans, c='r', marker='^', label='After Division by Zero')
    for idx in range(len(transformed_points) - 1):
        ax.plot([transformed_points[idx].x, transformed_points[idx + 1].x],
                [transformed_points[idx].i, transformed_points[idx + 1].i],
                [transformed_points[idx].O, transformed_points[idx + 1].O], c='r', linestyle='-')

    # Add labels
    ax.set_xlabel('Real (x)')
    ax.set_ylabel('Imaginary (i)')
    ax.set_zlabel('O')
    ax.set_title('Original vs After Division by Zero')
    ax.legend()

    # Function to show point information on click
    def on_click(event):
        if event.inaxes == ax:
            # Get the clicked point's coordinates
            clicked_point = [event.xdata, event.ydata]
            closest_point_idx = np.argmin(np.sqrt((x_vals + x_vals_trans - clicked_point[0])**2 + (i_vals + i_vals_trans - clicked_point[1])**2))
            # Get the coordinates of the closest point
            if closest_point_idx < len(points):
                point_info = f"Clicked Original Point: (x: {points[closest_point_idx].x}, i: {points[closest_point_idx].i}, O: {points[closest_point_idx].O})"
            else:
                idx_trans = closest_point_idx - len(points)
                point_info = f"Clicked Transformed Point: (x: {transformed_points[idx_trans].x}, i: {transformed_points[idx_trans].i}, O: {transformed_points[idx_trans].O})"
            print(point_info)

    # Connect the click event to the function
    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.legend()
    plt.show()

# Example usage
# Define a few points in the custom 3D space
points = [
    DimensionalSpace(3, 4, 5),
    DimensionalSpace(1, 2, 3),
    DimensionalSpace(-2, 3, 1),
    DimensionalSpace(4, -1, 2)
]

# Plot original points with connections
plot_3d_space(points, "Original Points in 3D Space")

# Plot original vs transformed points with connections
plot_before_after(points)
