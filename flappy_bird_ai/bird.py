import pygame
from config import (BIRD_X, BIRD_WIDTH, BIRD_HEIGHT, GRAVITY, 
                    JUMP_STRENGTH, MAX_VELOCITY, SCREEN_HEIGHT,
                    INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, YELLOW, ORANGE)
from neural_network import NeuralNetwork


class Bird:
    """Represents a bird controlled by a neural network."""
    
    def __init__(self, y=None):
        """Initialize the bird at the given y position."""
        self.x = BIRD_X
        self.y = y if y is not None else SCREEN_HEIGHT // 2
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.velocity = 0
        self.alive = True
        self.score = 0
        self.fitness = 0
        self.time_alive = 0
        
        # Neural network brain
        self.brain = NeuralNetwork(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
    
    def jump(self):
        """Make the bird jump."""
        self.velocity = JUMP_STRENGTH
    
    def update(self):
        """Update bird position and velocity."""
        if not self.alive:
            return
        
        # Apply gravity
        self.velocity += GRAVITY
        
        # Limit velocity
        self.velocity = max(min(self.velocity, MAX_VELOCITY), -MAX_VELOCITY)
        
        # Update position
        self.y += self.velocity
        
        # Increment time alive
        self.time_alive += 1
        
        # Check boundaries
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y + self.height > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
            self.die()
    
    def die(self):
        """Mark the bird as dead and calculate fitness."""
        self.alive = False
        # Fitness is based on time alive and score
        self.fitness = self.time_alive + (self.score * 100)
    
    def think(self, pipe):
        """
        Use the neural network to decide whether to jump.
        
        Args:
            pipe: The nearest pipe to consider
        """
        if not self.alive or pipe is None:
            return
        
        # Normalize inputs
        inputs = [
            self.y / SCREEN_HEIGHT,  # Bird's y position
            self.velocity / MAX_VELOCITY,  # Bird's velocity
            pipe.x / 400,  # Pipe's x position (normalized by screen width)
            pipe.top / SCREEN_HEIGHT,  # Top pipe's bottom y
            pipe.bottom / SCREEN_HEIGHT  # Bottom pipe's top y
        ]
        
        # Get output from neural network
        output = self.brain.forward(inputs)
        
        # Jump if output is greater than 0.5
        if output > 0.5:
            self.jump()
    
    def get_rect(self):
        """Get the bird's rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        """Draw the bird on the screen."""
        if not self.alive:
            return
        
        # Draw bird body (ellipse for a rounder look)
        bird_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.ellipse(screen, YELLOW, bird_rect)
        pygame.draw.ellipse(screen, ORANGE, bird_rect, 2)
        
        # Draw eye
        eye_x = self.x + self.width - 8
        eye_y = self.y + 6
        pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), 4)
        pygame.draw.circle(screen, (0, 0, 0), (eye_x + 1, eye_y), 2)
        
        # Draw beak
        beak_points = [
            (self.x + self.width, self.y + self.height // 2 - 2),
            (self.x + self.width + 8, self.y + self.height // 2),
            (self.x + self.width, self.y + self.height // 2 + 2)
        ]
        pygame.draw.polygon(screen, ORANGE, beak_points)
