# ===========================================
# NEURAL NETWORK - The Bird's Brain
# ===========================================

import numpy as np
import json
from config import INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE

class NeuralNetwork:
    def __init__(self):
        self.weights_input_hidden = np.random. randn(INPUT_SIZE, HIDDEN_SIZE) * 0.5
        self.bias_hidden = np.random.randn(HIDDEN_SIZE) * 0.5
        self.weights_hidden_output = np.random.randn(HIDDEN_SIZE, OUTPUT_SIZE) * 0.5
        self.bias_output = np.random.randn(OUTPUT_SIZE) * 0.5
    
    def sigmoid(self, x):
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward(self, inputs):
        inputs = np.array(inputs)
        hidden = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        hidden = self.relu(hidden)
        output = np.dot(hidden, self.weights_hidden_output) + self.bias_output
        output = self.sigmoid(output)
        return output
    
    def copy(self):
        new_nn = NeuralNetwork()
        new_nn.weights_input_hidden = self.weights_input_hidden.copy()
        new_nn.bias_hidden = self. bias_hidden.copy()
        new_nn.weights_hidden_output = self.weights_hidden_output.copy()
        new_nn.bias_output = self. bias_output.copy()
        return new_nn
    
    def save(self, filename):
        data = {
            'weights_input_hidden': self.weights_input_hidden.tolist(),
            'bias_hidden': self.bias_hidden.tolist(),
            'weights_hidden_output': self.weights_hidden_output.tolist(),
            'bias_output': self.bias_output.tolist()
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
        print(f"Brain saved to {filename}!")
    
    @staticmethod
    def load(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        nn = NeuralNetwork()
        nn.weights_input_hidden = np.array(data['weights_input_hidden'])
        nn.bias_hidden = np.array(data['bias_hidden'])
        nn.weights_hidden_output = np.array(data['weights_hidden_output'])
        nn.bias_output = np.array(data['bias_output'])
        print(f"Brain loaded from {filename}!")
        return nn