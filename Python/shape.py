import math
import matplotlib.pyplot as plt

def draw_shape(speed_of_rotation, start_distance, time_stamps, distance_changes, total_time, time_step=0.01):
    """
    Draws a single continuous shape with changing distance from the center point at specific time stamps.

    :param speed_of_rotation: Speed of rotation (radians per second)
    :param start_distance: Initial distance from the center point (radius)
    :param time_stamps: List of times at which the distance from the center point changes
    :param distance_changes: List of values by which the distance changes at the given time stamps
    :param total_time: Total duration for the shape drawing (seconds)
    :param time_step: Time step for simulation (default is 0.01 seconds)
    """

    if len(time_stamps) != len(distance_changes):
        raise ValueError("Time stamps and distance changes lists must be of the same length")

    current_distance = start_distance
    current_angle = 0
    current_time = 0

    # Index for tracking distance changes
    change_index = 0

    # Lists to store the (x, y) coordinates for plotting
    x_values = []
    y_values = []

    # Loop over time to simulate the shape drawing
    while current_time <= total_time:
        # Calculate the current angle based on speed of rotation
        current_angle += speed_of_rotation * time_step

        # Check if the current time matches a time stamp for distance change
        if change_index < len(time_stamps) and current_time >= time_stamps[change_index]:
            current_distance += distance_changes[change_index]
            change_index += 1

        # Convert polar coordinates (r, θ) to Cartesian coordinates (x, y)
        x = current_distance * math.cos(current_angle)
        y = current_distance * math.sin(current_angle)

        # Append coordinates for plotting
        x_values.append(x)
        y_values.append(y)

        # Increment time
        current_time += time_step

    # Plot the shape
    plt.plot(x_values, y_values)
    plt.title("Shape with Changing Distance at Timestamps")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")  # Maintain equal scaling for X and Y axes
    plt.show()

# Example usage:
speed_of_rotation = 1 # Full rotation per second
start_distance = 1
time_stamps = [x * 0.1 for x in range(0, 10)]  # Times at which the distance will change
distance_changes = math.sqrt(2)/2  # Corresponding changes in distance
total_time = 10  # Total duration of the drawing in seconds

draw_shape(speed_of_rotation, start_distance, time_stamps, distance_changes, total_time)
