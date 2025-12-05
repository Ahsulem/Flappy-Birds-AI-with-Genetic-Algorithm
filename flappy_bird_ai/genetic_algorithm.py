import numpy as np
import random
from config import (POPULATION_SIZE, MUTATION_RATE, MUTATION_STRENGTH, 
                    ELITISM_COUNT, SCREEN_HEIGHT)
from bird import Bird


class GeneticAlgorithm:
    """Genetic algorithm for evolving bird neural networks."""
    
    def __init__(self):
        """Initialize the genetic algorithm with a population of birds."""
        self.generation = 1
        self.best_fitness = 0
        self.best_score = 0
        self.population = self.create_population()
    
    def create_population(self):
        """Create a new population of birds."""
        return [Bird(SCREEN_HEIGHT // 2) for _ in range(POPULATION_SIZE)]
    
    def get_alive_birds(self):
        """Get all birds that are still alive."""
        return [bird for bird in self.population if bird.alive]
    
    def all_dead(self):
        """Check if all birds are dead."""
        return len(self.get_alive_birds()) == 0
    
    def evolve(self):
        """
        Evolve the population to create the next generation.
        Uses elitism, selection, crossover, and mutation.
        """
        # Sort population by fitness
        self.population.sort(key=lambda b: b.fitness, reverse=True)
        
        # Track best fitness and score
        if self.population[0].fitness > self.best_fitness:
            self.best_fitness = self.population[0].fitness
        if self.population[0].score > self.best_score:
            self.best_score = self.population[0].score
        
        # Create new population
        new_population = []
        
        # Elitism: keep the best birds unchanged
        for i in range(ELITISM_COUNT):
            elite_bird = Bird(SCREEN_HEIGHT // 2)
            elite_bird.brain = self.population[i].brain.copy()
            new_population.append(elite_bird)
        
        # Fill the rest with offspring
        while len(new_population) < POPULATION_SIZE:
            # Select parents
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            
            # Create child through crossover
            child = Bird(SCREEN_HEIGHT // 2)
            child.brain = self.crossover(parent1.brain, parent2.brain)
            
            # Mutate child
            self.mutate(child.brain)
            
            new_population.append(child)
        
        # Update population and generation
        self.population = new_population
        self.generation += 1
    
    def select_parent(self):
        """
        Select a parent using tournament selection.
        
        Returns:
            Selected bird
        """
        tournament_size = 5
        tournament = random.sample(self.population, tournament_size)
        return max(tournament, key=lambda b: b.fitness)
    
    def crossover(self, brain1, brain2):
        """
        Perform crossover between two neural networks.
        
        Args:
            brain1: First parent's neural network
            brain2: Second parent's neural network
            
        Returns:
            New neural network with mixed weights
        """
        from neural_network import NeuralNetwork
        
        child_brain = NeuralNetwork(
            brain1.input_size,
            brain1.hidden_size,
            brain1.output_size
        )
        
        weights1 = brain1.get_weights()
        weights2 = brain2.get_weights()
        
        # Uniform crossover
        child_weights = np.where(
            np.random.random(len(weights1)) < 0.5,
            weights1,
            weights2
        )
        
        child_brain.set_weights(child_weights)
        return child_brain
    
    def mutate(self, brain):
        """
        Mutate a neural network's weights.
        
        Args:
            brain: Neural network to mutate
        """
        weights = brain.get_weights()
        
        for i in range(len(weights)):
            if random.random() < MUTATION_RATE:
                # Add Gaussian noise
                weights[i] += np.random.randn() * MUTATION_STRENGTH
        
        brain.set_weights(weights)
    
    def reset_population(self):
        """Reset all birds for a new round."""
        for bird in self.population:
            bird.y = SCREEN_HEIGHT // 2
            bird.velocity = 0
            bird.alive = True
            bird.score = 0
            bird.fitness = 0
            bird.time_alive = 0
