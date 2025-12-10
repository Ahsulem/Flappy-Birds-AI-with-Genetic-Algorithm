# ===========================================
# BIRD CLASS - The AI Agent
# ===========================================

import pygame
from config import *
from neural_network import NeuralNetwork

class Bird:
    def __init__(self, neural_network=None):
        self.x = BIRD_X
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.alive = True
        self.fitness = 0
        self.score = 0
        
        if neural_network is None:
            self.brain = NeuralNetwork()
        else:
            self.brain = neural_network
    
    def flap(self):
        if self.alive:
            self.velocity = FLAP_STRENGTH
    
    def update(self):
        if not self.alive:
            return
        
        self.velocity += GRAVITY
        self.y += self.velocity
        self.fitness += 1
        
        # Ceiling
        if self.y - BIRD_RADIUS <= 0:
            self.y = BIRD_RADIUS
            self.velocity = 0
        
        # Ground
        if self.y + BIRD_RADIUS >= SCREEN_HEIGHT - 50:
            self.y = SCREEN_HEIGHT - 50 - BIRD_RADIUS
            self.die()
    
    def die(self):
        self.alive = False
    
    def draw(self, screen, is_best=False):
        if not self.alive:
            return
        
        color = ORANGE if is_best else YELLOW
        pygame.draw.circle(screen, color, (int(self. x), int(self.y)), BIRD_RADIUS)
        
        # Eye
        eye_x = int(self.x + 5)
        eye_y = int(self.y - 3)
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 5)
        pygame.draw.circle(screen, BLACK, (eye_x + 2, eye_y), 2)
        
        # Beak
        beak_rect = pygame.Rect(self.x + BIRD_RADIUS - 2, self.y + 2, 10, 5)
        pygame.draw.rect(screen, ORANGE if not is_best else RED, beak_rect)
    
    def think(self, pipes):
        if self.brain is None or not self.alive:
            return
        
        # Find next pipe
        next_pipe = None
        for pipe in pipes: 
            if pipe.x + PIPE_WIDTH > self.x:
                next_pipe = pipe
                break
        
        if next_pipe is None:
            return
        
        # Neural network inputs
        inputs = [
            self.y / SCREEN_HEIGHT,
            next_pipe.gap_top / SCREEN_HEIGHT,
            next_pipe.gap_bottom / SCREEN_HEIGHT,
            (self.velocity + 10) / 20
        ]
        
        output = self.brain.forward(inputs)
        
        if output[0] > 0.5:
            self.flap()