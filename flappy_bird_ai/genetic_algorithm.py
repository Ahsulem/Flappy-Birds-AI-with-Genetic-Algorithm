# ===========================================
# GENETIC ALGORITHM - Evolution Engine
# ===========================================

import numpy as np
import random
from neural_network import NeuralNetwork
from config import POPULATION_SIZE, MUTATION_RATE, MUTATION_STRENGTH

class GeneticAlgorithm: 
    def __init__(self):
        self.generation = 1
        self.best_fitness_history = []
        self.avg_fitness_history = []
    
    def create_initial_population(self, Bird):
        return [Bird() for _ in range(POPULATION_SIZE)]
    
    def calculate_fitness(self, birds):
        return sorted(birds, key=lambda b: b.fitness, reverse=True)
    
    def selection(self, birds, num_parents=10):
        sorted_birds = self.calculate_fitness(birds)
        return sorted_birds[:num_parents]
    
    def crossover(self, parent_a, parent_b):
        child = NeuralNetwork()
        
        mask = np.random.rand(*parent_a.weights_input_hidden.shape) > 0.5
        child. weights_input_hidden = np.where(mask, parent_a.weights_input_hidden, parent_b.weights_input_hidden)
        
        mask = np.random.rand(*parent_a.bias_hidden.shape) > 0.5
        child.bias_hidden = np.where(mask, parent_a.bias_hidden, parent_b.bias_hidden)
        
        mask = np. random.rand(*parent_a. weights_hidden_output.shape) > 0.5
        child.weights_hidden_output = np.where(mask, parent_a.weights_hidden_output, parent_b.weights_hidden_output)
        
        mask = np.random.rand(*parent_a.bias_output.shape) > 0.5
        child. bias_output = np.where(mask, parent_a.bias_output, parent_b.bias_output)
        
        return child
    
    def mutate(self, brain):
        mutation_mask = np.random.rand(*brain.weights_input_hidden.shape) < MUTATION_RATE
        mutations = np.random.randn(*brain.weights_input_hidden.shape) * MUTATION_STRENGTH
        brain.weights_input_hidden += mutation_mask * mutations
        
        mutation_mask = np.random. rand(*brain.bias_hidden. shape) < MUTATION_RATE
        mutations = np.random. randn(*brain.bias_hidden.shape) * MUTATION_STRENGTH
        brain.bias_hidden += mutation_mask * mutations
        
        mutation_mask = np. random.rand(*brain.weights_hidden_output.shape) < MUTATION_RATE
        mutations = np.random.randn(*brain.weights_hidden_output.shape) * MUTATION_STRENGTH
        brain.weights_hidden_output += mutation_mask * mutations
        
        mutation_mask = np. random.rand(*brain.bias_output.shape) < MUTATION_RATE
        mutations = np. random.randn(*brain.bias_output.shape) * MUTATION_STRENGTH
        brain.bias_output += mutation_mask * mutations
    
    def create_next_generation(self, birds, Bird):
        sorted_birds = self.calculate_fitness(birds)
        best_fitness = sorted_birds[0].fitness
        avg_fitness = sum(b.fitness for b in birds) / len(birds)
        
        self.best_fitness_history.append(best_fitness)
        self.avg_fitness_history.append(avg_fitness)
        
        parents = self.selection(birds, num_parents=10)
        new_birds = []
        
        # Elitism:  keep best 2 unchanged
        best_brain = parents[0].brain.copy()
        new_birds.append(Bird(neural_network=best_brain))
        
        if len(parents) > 1:
            second_best_brain = parents[1].brain. copy()
            new_birds. append(Bird(neural_network=second_best_brain))
        
        # Create rest through crossover + mutation
        while len(new_birds) < POPULATION_SIZE:
            parent_a = random.choice(parents[: 5])
            parent_b = random.choice(parents)
            
            child_brain = self.crossover(parent_a.brain, parent_b.brain)
            self.mutate(child_brain)
            
            new_birds. append(Bird(neural_network=child_brain))
        
        self.generation += 1
        return new_birds
    
    def get_stats(self):
        return {
            'generation': self.generation,
            'best_fitness_history': self.best_fitness_history,
            'avg_fitness_history': self.avg_fitness_history
        }