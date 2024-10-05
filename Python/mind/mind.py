import random
import math
import sys
import csv

class NeuralNetwork:
    def __init__(self, layers):
        """
        Initialize the neural network.

        Parameters:
        - layers: List of integers representing the number of neurons in each layer.
                  For example, [2, 3, 1] represents a network with:
                  - 2 input neurons
                  - 3 neurons in one hidden layer
                  - 1 output neuron
        """
        self.layers = layers
        self.num_layers = len(layers)

        # Initialize weights and biases with random values between -1 and 1
        # Weights are between layers: weights[l][i][j] represents the weight from
        # neuron i in layer l to neuron j in layer l+1
        self.weights = []
        for l in range(self.num_layers - 1):
            layer_weights = []
            for _ in range(layers[l]):
                neuron_weights = [random.uniform(-1, 1) for _ in range(layers[l + 1])]
                layer_weights.append(neuron_weights)
            self.weights.append(layer_weights)

        # Biases for each layer except the input layer
        self.biases = []
        for l in range(1, self.num_layers):
            layer_biases = [random.uniform(-1, 1) for _ in range(layers[l])]
            self.biases.append(layer_biases)

    def sigmoid(self, x):
        """Sigmoid activation function."""
        # Prevent overflow
        if x < -700:
            return 0.0
        return 1 / (1 + math.exp(-x))

    def sigmoid_derivative(self, x):
        """Derivative of the sigmoid function."""
        return x * (1 - x)

    def feedforward(self, input_vector):
        """
        Perform a feedforward pass.

        Parameters:
        - input_vector: List of input values.

        Returns:
        - activations: List of activations for each layer.
        """
        if len(input_vector) != self.layers[0]:
            raise ValueError(f"Expected input vector of size {self.layers[0]}, got {len(input_vector)}")

        activations = [input_vector]

        for l in range(1, self.num_layers):
            prev_activations = activations[-1]
            layer_biases = self.biases[l - 1]
            layer_weights = self.weights[l - 1]
            layer_activations = []

            for j in range(self.layers[l]):
                # Weighted sum
                activation = sum(prev_activations[i] * layer_weights[i][j] for i in range(self.layers[l - 1])) + layer_biases[j]
                # Activation function
                activated = self.sigmoid(activation)
                layer_activations.append(activated)

            activations.append(layer_activations)

        return activations

    def backpropagate(self, activations, expected_output, learning_rate):
        """
        Perform backpropagation and update weights and biases.

        Parameters:
        - activations: List of activations for each layer from feedforward.
        - expected_output: List of expected output values.
        - learning_rate: Current learning rate.
        """
        # Initialize lists to hold errors and deltas for each layer
        errors = [None] * (self.num_layers - 1)  # No error for input layer
        deltas = [None] * (self.num_layers - 1)

        # Calculate error for the output layer
        output_activations = activations[-1]
        if len(expected_output) != self.layers[-1]:
            raise ValueError(f"Expected output vector of size {self.layers[-1]}, got {len(expected_output)}")

        errors[-1] = [expected_output[j] - output_activations[j] for j in range(self.layers[-1])]
        deltas[-1] = [errors[-1][j] * self.sigmoid_derivative(output_activations[j]) for j in range(self.layers[-1])]

        # Calculate error for hidden layers (backwards)
        for l in range(self.num_layers - 2, 0, -1):
            errors[l - 1] = []
            deltas[l - 1] = []
            for i in range(self.layers[l]):
                error = sum(self.weights[l - 1][i][j] * deltas[l][j] for j in range(self.layers[l + 1]))
                errors[l - 1].append(error)
                delta = error * self.sigmoid_derivative(activations[l][i])
                deltas[l - 1].append(delta)

        # Update weights and biases
        for l in range(self.num_layers - 1):
            for i in range(self.layers[l]):
                for j in range(self.layers[l + 1]):
                    self.weights[l][i][j] += learning_rate * deltas[l][j] * activations[l][i]
            for j in range(self.layers[l + 1]):
                self.biases[l][j] += learning_rate * deltas[l][j]

    def load_inputs(self, file_path):
        """
        Load input data from a CSV file.

        Parameters:
        - file_path: Path to the input CSV file.

        Returns:
        - inputs: List of input vectors.
        """
        inputs = []
        try:
            with open(file_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # Convert string values to floats
                    input_vector = [float(value) for value in row]
                    if len(input_vector) != self.layers[0]:
                        raise ValueError(f"Each input must have {self.layers[0]} values.")
                    inputs.append(input_vector)
        except FileNotFoundError:
            print(f"Inputs file '{file_path}' not found.")
            sys.exit(1)
        except ValueError as ve:
            print(f"Value error in inputs file: {ve}")
            sys.exit(1)
        return inputs

    def load_expected_outputs(self, file_path):
        """
        Load expected output data from a CSV file.

        Parameters:
        - file_path: Path to the expected output CSV file.

        Returns:
        - outputs: List of expected output vectors.
        """
        outputs = []
        try:
            with open(file_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # Convert string values to floats
                    output_vector = [float(value) for value in row]
                    if len(output_vector) != self.layers[-1]:
                        raise ValueError(f"Each output must have {self.layers[-1]} values.")
                    outputs.append(output_vector)
        except FileNotFoundError:
            print(f"Expected outputs file '{file_path}' not found.")
            sys.exit(1)
        except ValueError as ve:
            print(f"Value error in outputs file: {ve}")
            sys.exit(1)
        return outputs

    def train_recursive(
        self,
        inputs,
        expected_outputs,
        learning_rate,
        tolerance_percent,
        max_iterations,
        max_no_improve,
        iteration=0,
        best_error=float('inf'),
        patience_counter=0
    ):
        """
        Recursively train the neural network.

        Parameters:
        - inputs: List of input vectors.
        - expected_outputs: List of expected output vectors.
        - learning_rate: Current learning rate.
        - tolerance_percent: Tolerance percentage for stopping.
        - max_iterations: Maximum number of iterations.
        - max_no_improve: Number of iterations to wait for improvement before reducing learning rate.
        - iteration: Current iteration count.
        - best_error: Best mean squared error observed.
        - patience_counter: Counter for iterations without improvement.
        """
        if iteration >= max_iterations:
            print(f"Reached maximum iterations ({max_iterations}) with best MSE: {best_error:.6f}")
            return

        total_error = 0
        for input_vector, expected_output in zip(inputs, expected_outputs):
            # Forward pass
            activations = self.feedforward(input_vector)

            # Calculate error for this sample (mean squared error)
            sample_error = sum((expected_output[j] - activations[-1][j]) ** 2 for j in range(self.layers[-1]))
            total_error += sample_error

            # Backward pass
            self.backpropagate(activations, expected_output, learning_rate)

        # Compute mean squared error across all samples
        mse = total_error / len(inputs)

        # Check for improvement
        if mse < best_error:
            best_error = mse
            patience_counter = 0
        else:
            patience_counter += 1

        # If no improvement for 'max_no_improve' iterations, reduce learning rate
        if patience_counter >= max_no_improve:
            learning_rate *= 0.5
            patience_counter = 0
            print(f"Iteration {iteration}: No improvement. Reducing learning rate to {learning_rate:.6f}")

            # If learning rate becomes too small, stop training
            if learning_rate < 1e-6:
                print("Learning rate too small. Stopping training.")
                return

        # Check if all predictions are within the tolerance
        within_tolerance = True
        for input_vector, expected_output in zip(inputs, expected_outputs):
            activations = self.feedforward(input_vector)
            for j in range(self.layers[-1]):
                y = expected_output[j]
                y_pred = activations[-1][j]
                if y != 0:
                    percent_error = abs((y_pred - y) / y) * 100
                else:
                    percent_error = abs(y_pred) * 100
                if percent_error > tolerance_percent:
                    within_tolerance = False
                    break
            if not within_tolerance:
                break

        if within_tolerance:
            print(f"Training complete at iteration {iteration} with MSE: {mse:.6f}")
            return

        # Log progress every 1000 iterations
        if iteration % 1000 == 0 and iteration != 0:
            print(f"Iteration {iteration}, MSE: {mse:.6f}, Learning Rate: {learning_rate:.6f}")

        # Recursive call for the next iteration
        self.train_recursive(
            inputs,
            expected_outputs,
            learning_rate,
            tolerance_percent,
            max_iterations,
            max_no_improve,
            iteration + 1,
            best_error,
            patience_counter
        )

    def train(
        self,
        inputs,
        expected_outputs,
        initial_learning_rate=0.1,
        tolerance_percent=1.0,
        max_iterations=100000,
        max_no_improve=1000
    ):
        """
        Public method to start training the neural network.

        Parameters:
        - inputs: List of input vectors.
        - expected_outputs: List of expected output vectors.
        - initial_learning_rate: Starting learning rate.
        - tolerance_percent: Tolerance percentage for stopping.
        - max_iterations: Maximum number of iterations.
        - max_no_improve: Number of iterations to wait for improvement before reducing learning rate.
        """
        try:
            self.train_recursive(
                inputs,
                expected_outputs,
                initial_learning_rate,
                tolerance_percent,
                max_iterations,
                max_no_improve
            )
        except RecursionError:
            print("Reached Python's recursion limit. Consider increasing the recursion limit or using an iterative approach.")

    def predict(self, input_vector):
        """
        Generate prediction for a given input vector.

        Parameters:
        - input_vector: List of input values.

        Returns:
        - output_vector: List of output values.
        """
        activations = self.feedforward(input_vector)
        return activations[-1]

# Example Usage
if __name__ == "__main__":
    # Increase the recursion limit if necessary
    # Be cautious: setting it too high can cause a crash
    sys.setrecursionlimit(10000)

    # Specify file paths
    inputs_file = 'inputs.csv'
    outputs_file = 'outputs.csv'

    # Define network architecture
    # Example for XOR problem: 2 inputs, 2 hidden neurons, 1 output
    layers = [2, 2, 1]

    # Create neural network instance
    nn = NeuralNetwork(layers)

    # Load data from files
    inputs = nn.load_inputs(inputs_file)
    expected_outputs = nn.load_expected_outputs(outputs_file)

    # Define training parameters
    initial_learning_rate = 0.5
    tolerance_percent = 1.0  # 1%
    max_iterations = 100000
    max_no_improve = 1000  # Number of iterations to wait before reducing learning rate

    # Train the neural network
    nn.train(
        inputs,
        expected_outputs,
        initial_learning_rate=initial_learning_rate,
        tolerance_percent=tolerance_percent,
        max_iterations=max_iterations,
        max_no_improve=max_no_improve
    )

    # Test the neural network
    print("\nTesting the Neural Network:")
    for input_vector in inputs:
        prediction = nn.predict(input_vector)
        # For binary classification, round the output to nearest integer
        predicted = [round(p) for p in prediction]
        print(f"Input: {input_vector}, Predicted Output: {predicted}")
