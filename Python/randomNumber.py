from sympy import nextprime, prevprime
import time
import matplotlib.pyplot as plt
import numpy as np

class SimpleRandom:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        current_time = int(''.join(str(time.time()).split(".")))
        closest_prime = self.closest_prime(current_time)
        self.seed = (self.seed * 48271) % closest_prime  # Using a known multiplier
        return self.seed % closest_prime

    def randint(self, min_value, max_value):
        if min_value > max_value:
            raise ValueError("min_value must be less than or equal to max_value")
        return min_value + self.next() % (max_value - min_value + 1)

    def sequence(self, min_value, max_value, size):
        if min_value > max_value:
            raise ValueError("min_value must be less than or equal to max_value")
        return [self.randint(min_value, max_value) for _ in range(size)]

    def closest_prime(self, n):
        return n - min(n - prevprime(n), nextprime(n) - n)

    def generate_amounts(self, min_value, max_value, sequence_size):
        raw_numbers = np.random.randint(min_value, max_value + 1, size=sequence_size)
        unique_counts = len(set(raw_numbers))
        amounts = {val: (raw_numbers == val).sum() for val in range(min_value, max_value + 1) if val in raw_numbers}
        return amounts

    def plot_amounts(self, amounts, plot_number):
        plt.clf()  # Clear the current figure
        lengths = list(amounts.keys())
        counts = list(amounts.values())

        # Create a bar graph with visible separation
        bar_width = 0.4
        x = np.arange(len(lengths))

        plt.bar(x, counts, color='blue', width=bar_width, align='center')
        plt.xlabel('Unique Sequence Lengths')
        plt.ylabel('Counts')
        plt.title(f'Counts of Unique Sequence Lengths - Plot {plot_number}')
        plt.xticks(x, lengths)  # Set x-ticks to be the lengths
        plt.grid(axis='y')
        plt.tight_layout()  # Improve layout
        plt.draw()  # Update the plot

    def show_plots(self, num_plots, sequence_size, min_value=0, max_value=100):
        amounts_list = [self.generate_amounts(min_value, max_value, sequence_size) for _ in range(num_plots)]

        self.current_plot = 0
        self.total_plots = num_plots

        fig, ax = plt.subplots(figsize=(10, 5))
        self.plot_amounts(amounts_list[self.current_plot], self.current_plot + 1)

        # Navigation buttons
        ax_prev = plt.axes([0.1, 0.01, 0.1, 0.05])  # Previous button position
        ax_next = plt.axes([0.8, 0.01, 0.1, 0.05])  # Next button position

        btn_prev = plt.Button(ax_prev, 'Previous')
        btn_next = plt.Button(ax_next, 'Next')

        def update_plot(new_index):
            self.current_plot = new_index
            self.plot_amounts(amounts_list[self.current_plot], self.current_plot + 1)

        def on_prev_clicked(event):
            if self.current_plot > 0:
                update_plot(self.current_plot - 1)

        def on_next_clicked(event):
            if self.current_plot < self.total_plots - 1:
                update_plot(self.current_plot + 1)

        btn_prev.on_clicked(on_prev_clicked)
        btn_next.on_clicked(on_next_clicked)

        plt.show()

# Example usage
sr = SimpleRandom(100)

# Generate and display interactive plots
start_time = time.time()
sr.show_plots(num_plots=5, sequence_size=100)
print(f"Execution Time: {time.time() - start_time:.4f} seconds")
