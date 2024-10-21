import numpy as np
import matplotlib.pyplot as plt

class Curve:
    def __init__(self, center, radius, arc_length):
        """
        center: The center of the circle for the curve point.
        radius: The radius of the circle.
        arc_length: The arc length (along the circle) to trace when intersected.
        """
        self.center = np.array(center)
        self.radius = radius
        self.arc_length = arc_length  # Distance along the arc to trace

def line_circle_intersection(p1, p2, curve):
    """
    Calculates the intersection points between the line (p1, p2) and a curve's circle.
    Returns the closest intersection point and the corresponding distance from p1.
    """
    p1 = np.array(p1)
    p2 = np.array(p2)
    center = curve.center
    radius = curve.radius

    # Define the line as p1 + t * (p2 - p1), and solve for intersection with circle
    d = p2 - p1
    f = p1 - center
    r = radius

    a = np.dot(d, d)
    b = 2 * np.dot(f, d)
    c = np.dot(f, f) - r**2
    discriminant = b**2 - 4*a*c

    if discriminant < 0:
        return None  # No intersection
    elif discriminant == 0:
        t = -b / (2*a)
        intersection = p1 + t * d
        return intersection, np.linalg.norm(intersection - p1)  # One intersection
    else:
        sqrt_discriminant = np.sqrt(discriminant)
        t1 = (-b + sqrt_discriminant) / (2*a)
        t2 = (-b - sqrt_discriminant) / (2*a)
        intersection1 = p1 + t1 * d
        intersection2 = p1 + t2 * d
        # Choose the closest intersection to p1
        if np.linalg.norm(intersection1 - p1) < np.linalg.norm(intersection2 - p1):
            return intersection1, np.linalg.norm(intersection1 - p1)
        else:
            return intersection2, np.linalg.norm(intersection2 - p1)

def trace_circle_arc(curve, start_point, arc_length, num_points=100):
    """
    Generates points along an arc of a circle starting at a specific point.

    curve: Curve object containing the circle's center and radius.
    start_point: The point where the arc should start.
    arc_length: The length of the arc to trace along the circle's edge.
    """
    # Calculate the starting angle based on the position of start_point relative to the center
    center = curve.center
    radius = curve.radius
    start_angle = np.arctan2(start_point[1] - center[1], start_point[0] - center[0])

    # Calculate the angle step based on the arc length and circle circumference
    circumference = 2 * np.pi * radius
    arc_angle = (arc_length / circumference) * 360  # Convert arc length to degrees

    # Generate points along the arc
    theta_values = np.linspace(start_angle, start_angle + np.radians(arc_angle), num_points)
    arc_points = np.array([(center[0] + radius * np.cos(theta), center[1] + radius * np.sin(theta)) for theta in theta_values])

    return arc_points

def generate_shape_with_curves(points, curves):
    """
    Generates a shape by drawing straight lines between control points, but curving around
    circles at certain curve points when the line intersects them.

    points: List of control points defining the shape.
    curves: List of Curve objects specifying the curve points and their parameters.
    """
    # Prepare for plotting
    fig, ax = plt.subplots()

    # Iterate over each line segment between control points
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i+1]
        current_point = np.array(p1)

        # Draw the line and check for curve intersections
        while np.linalg.norm(current_point - np.array(p2)) > 0.01:
            closest_intersection = None
            min_dist = float('inf')

            # Check intersection with all curve points
            for curve in curves:
                result = line_circle_intersection(current_point, p2, curve)
                if result:
                    intersection, dist_to_intersection = result
                    if dist_to_intersection < min_dist:
                        closest_intersection = (intersection, curve)
                        min_dist = dist_to_intersection

            if closest_intersection:
                intersection, curve = closest_intersection

                # Draw straight line to the intersection point
                ax.plot([current_point[0], intersection[0]], [current_point[1], intersection[1]], 'b-')

                # Trace the arc around the curve point
                arc_points = trace_circle_arc(curve, intersection, curve.arc_length)
                ax.plot(arc_points[:, 0], arc_points[:, 1], 'g-')  # Green for the arc

                # Update the current point to the end of the arc
                current_point = arc_points[-1]
            else:
                # No intersection found, draw straight line to p2
                ax.plot([current_point[0], p2[0]], [current_point[1], p2[1]], 'b-')
                break

    # Plot the original control points
    ax.plot([p[0] for p in points], [p[1] for p in points], 'ro', label="Control Points")

    # Plot the centers of the curve points
    for curve in curves:
        circle = plt.Circle(curve.center, curve.radius, color='r', fill=False, linestyle='--')
        ax.add_artist(circle)

    plt.legend()
    plt.show()

# Example usage:
control_points = [(0, 0), (10, 0), (10, 10), (0, 10)]

# Define some curve points that will affect the path
curves = [
    Curve(center=(5, 0), radius=2, arc_length=3),   # Curve near the first line
    Curve(center=(10, 5), radius=2, arc_length=2),  # Curve near the second line
    Curve(center=(5, 10), radius=1.5, arc_length=2) # Curve near the third line
]

generate_shape_with_curves(control_points, curves)
