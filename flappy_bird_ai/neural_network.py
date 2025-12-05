import numpy as np


class NeuralNetwork:
    """Simple feedforward neural network for the bird's brain."""
    
    def __init__(self, input_size, hidden_size, output_size):
        """Initialize the neural network with random weights."""
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Initialize weights with Xavier initialization
        self.weights_input_hidden = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        
        # Initialize biases
        self.bias_hidden = np.zeros((1, hidden_size))
        self.bias_output = np.zeros((1, output_size))
    
    def sigmoid(self, x):
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def relu(self, x):
        """ReLU activation function."""
        return np.maximum(0, x)
    
    def forward(self, inputs):
        """
        Forward pass through the network.
        
        Args:
            inputs: Input array of shape (input_size,) or (1, input_size)
            
        Returns:
            Output value between 0 and 1
        """
        inputs = np.array(inputs).reshape(1, -1)
        
        # Hidden layer with ReLU activation
        hidden = self.relu(np.dot(inputs, self.weights_input_hidden) + self.bias_hidden)
        
        # Output layer with sigmoid activation
        output = self.sigmoid(np.dot(hidden, self.weights_hidden_output) + self.bias_output)
        
        return output[0][0]
    
    def get_weights(self):
        """Get all weights and biases as a flat array."""
        return np.concatenate([
            self.weights_input_hidden.flatten(),
            self.weights_hidden_output.flatten(),
            self.bias_hidden.flatten(),
            self.bias_output.flatten()
        ])
    
    def set_weights(self, weights):
        """Set all weights and biases from a flat array."""
        idx = 0
        
        # Input to hidden weights
        size = self.input_size * self.hidden_size
        self.weights_input_hidden = weights[idx:idx + size].reshape(self.input_size, self.hidden_size)
        idx += size
        
        # Hidden to output weights
        size = self.hidden_size * self.output_size
        self.weights_hidden_output = weights[idx:idx + size].reshape(self.hidden_size, self.output_size)
        idx += size
        
        # Hidden bias
        size = self.hidden_size
        self.bias_hidden = weights[idx:idx + size].reshape(1, self.hidden_size)
        idx += size
        
        # Output bias
        size = self.output_size
        self.bias_output = weights[idx:idx + size].reshape(1, self.output_size)
    
    def copy(self):
        """Create a copy of this neural network."""
        new_nn = NeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        new_nn.set_weights(self.get_weights().copy())
        return new_nn
