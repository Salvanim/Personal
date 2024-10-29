import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
from numbers import Number

class Vector:
    def __init__(self, components, origin=None):
        if not all(isinstance(c, (int, float)) for c in components):
            raise ValueError("All components must be numeric values.")

        self.components = components
        self.origin = origin if isinstance(origin, Vector) or origin is None else Vector(origin)

    def magnitude(self):
        return math.sqrt(sum(c**2 for c in self.components))

    def direction(self):
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot calculate direction of a zero vector.")

        if len(self.components) == 2:
            angle = math.atan2(self.components[1], self.components[0])
            return [angle]
        else:
            return [math.acos(c / mag) for c in self.components]

    def get_origin_coordinates(self):
        """Calculate the origin coordinates of the vector."""
        if self.origin:
            return [sum(x) for x in zip(self.origin.get_origin_coordinates(), self.origin.components)]
        else:
            return [0] * len(self.components)

    def plot(self):
        """Displays the vector with respect to its origin, allowing higher-dimensional scrolling."""
        dim = max(len(self.components), len(self.get_origin_coordinates()))

        if dim == 2:
            # 2D plot with custom origin
            self._plot_2d(*self.get_origin_coordinates(), *self.components[:2])

        elif dim == 3:
            # 3D plot with custom origin
            self._plot_3d(*self.get_origin_coordinates(), *self.components[:3])

        else:
            # Higher dimensions with sliders
            self._plot_high_dim()

    def _plot_2d(self, ox, oy, vx, vy):
        plt.figure()
        plt.quiver(ox, oy, vx, vy, angles='xy', scale_units='xy', scale=1)
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid()
        plt.title(f"2D Vector with Origin: [{ox}, {oy}] to [{ox + vx}, {oy + vy}]")
        plt.show()

    def _plot_3d(self, ox, oy, oz, vx, vy, vz):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.quiver(ox, oy, oz, vx, vy, vz)
        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])
        ax.set_zlim([-10, 10])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title(f"3D Vector with Origin: [{ox}, {oy}, {oz}] to [{ox + vx}, {oy + vy}, {oz + vz}]")
        plt.show()

    def _plot_high_dim(self):
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)

        # Display only the first two components initially
        ox, oy = self.get_origin_coordinates()[:2]
        vx, vy = self.components[:2]
        quiv = ax.quiver(ox, oy, vx, vy, angles='xy', scale_units='xy', scale=1)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Higher-Dimensional Vector Visualization with Origin (2D slices)")
        ax.grid()

        # Create sliders for each dimension > 2
        sliders = []
        for i in range(2, max(len(self.components), len(self.get_origin_coordinates()))):
            ax_slider = plt.axes([0.1, 0.1 - i * 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
            slider = Slider(ax_slider, f'Dim {i+1}', -10, 10, valinit=self.components[i] if i < len(self.components) else 0)
            sliders.append(slider)

        # Update function for sliders
        def update(val):
            vx_updated = [s.val if i >= 2 else self.components[i] for i, s in enumerate(sliders)]
            ox, oy = self.get_origin_coordinates()[:2]
            quiv.set_UVC(vx_updated[0], vx_updated[1])
            fig.canvas.draw_idle()

        # Connect each slider to the update function
        for slider in sliders:
            slider.on_changed(update)

        plt.show()

    def __repr__(self):
        origin_repr = self.get_origin_coordinates()
        return f"Vector({self.components}, origin={origin_repr})"

# Example usage
v1 = Vector([3, 4])                       # 2D vector from origin [0, 0]
v2 = Vector([1, 2, 3])                    # 3D vector from origin [0, 0, 0]
v3 = Vector([4, 5, 6], origin=v1)         # 3D vector originating from v1's endpoint
v4 = Vector([3, 4, 5, 6, 7], origin=[1, 2, 3, 4, 5]) # 5D vector with custom origin

# Call plot method
v1.plot()  # Plots a 2D vector
v2.plot()  # Plots a 3D vector
v3.plot()  # Plots a 3D vector originating from v1's endpoint
v4.plot()  # Allows dimension scrolling for 5D vector with custom origin
