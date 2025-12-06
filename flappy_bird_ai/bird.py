import pygame
from config import *
from neural_network import NeuralNetwork

class Bird:
    def __init__(self, neural_network=None):
        # Position (bird starts in middle of screen vertically)
        self.x = BIRD_X
        self.y = SCREEN_HEIGHT // 2
        
        # Physics
        self.velocity = 0  # Current vertical velocity
        
        # State
        self.alive = True
        self.fitness = 0  # How well this bird performed
        self.score = 0    # Pipes passed
        
        # Brain (neural network) - will be added in Phase 2
        self.brain = neural_network
    
    def flap(self):
        """Make the bird flap (jump up)"""
        if self.alive:
            self.velocity = JUMP_STRENGTH
    
    def update(self):
        """Update bird physics each frame"""
        if not self.alive:
            return
        
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self. velocity
        
        # Increase fitness for surviving (each frame alive = +1 fitness)
        self.fitness += 1
        
        # Check boundaries (ceiling and floor)
        if self.y - BIRD_RADIUS <= 0:  # Hit ceiling
            self.y = BIRD_RADIUS
            self.velocity = 0
        
        if self.y + BIRD_RADIUS >= SCREEN_HEIGHT - 50:  # Hit ground
            self.y = SCREEN_HEIGHT - 50 - BIRD_RADIUS
            self. die()
    
    def die(self):
        """Bird has crashed"""
        self.alive = False
    
    def draw(self, screen, is_best=False):
        """Draw the bird on screen"""
        if not self.alive:
            return
        
        # Best bird gets a special color (orange), others are yellow
        color = ORANGE if is_best else YELLOW
        
        # Draw body (circle)
        pygame.draw.circle(screen, color, (int(self.x), int(self. y)), BIRD_RADIUS)
        
        # Draw eye (small white circle with black pupil)
        eye_x = int(self. x + 5)
        eye_y = int(self.y - 3)
        pygame. draw.circle(screen, WHITE, (eye_x, eye_y), 5)  # Eye white
        pygame.draw.circle(screen, BLACK, (eye_x + 2, eye_y), 2)  # Pupil
        
        # Draw beak (small orange triangle/rectangle)
        beak_rect = pygame.Rect(self.x + BIRD_RADIUS - 2, self.y + 2, 10, 5)
        pygame. draw.rect(screen, ORANGE if not is_best else RED, beak_rect)
    
    def think(self, pipes):
        """
        Use neural network to decide whether to flap. 
        Will be implemented in Phase 2! 
        """
        if self.brain is None:
            return
        
        # Find the next pipe to navigate
        next_pipe = None
        for pipe in pipes:
            if pipe.x + PIPE_WIDTH > self.x:  # Pipe is ahead of bird
                next_pipe = pipe
                break
        
        if next_pipe is None:
            return
        
        # Prepare inputs for neural network (normalized to 0-1 range)
        inputs = [
            self.y / SCREEN_HEIGHT,                              # Bird's Y position
            next_pipe.gap_top / SCREEN_HEIGHT,                   # Top of gap
            next_pipe.gap_bottom / SCREEN_HEIGHT,                # Bottom of gap  
            self.velocity / 10                                    # Bird's velocity
        ]
        
        # Get decision from brain
        output = self.brain. forward(inputs)
        
        # If output > 0.5, flap! 
        if output[0] > 0.5:
            self.flap()