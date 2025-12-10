# ===========================================
# PIPE CLASS - The Obstacles
# ===========================================

import pygame
import random
from config import *

class Pipe:
    def __init__(self, x=None):
        self.x = x if x is not None else SCREEN_WIDTH
        
        min_gap_top = 80
        max_gap_top = SCREEN_HEIGHT - 50 - PIPE_GAP - 80
        
        self.gap_top = random.randint(min_gap_top, max_gap_top)
        self.gap_bottom = self.gap_top + PIPE_GAP
        self.passed = False
    
    def update(self):
        self.x -= PIPE_SPEED
    
    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0
    
    def collides_with(self, bird):
        if not bird.alive:
            return False
        
        bird_left = bird.x - BIRD_RADIUS
        bird_right = bird.x + BIRD_RADIUS
        bird_top = bird.y - BIRD_RADIUS
        bird_bottom = bird.y + BIRD_RADIUS
        
        pipe_left = self.x
        pipe_right = self.x + PIPE_WIDTH
        
        if bird_right > pipe_left and bird_left < pipe_right:
            if bird_top < self.gap_top or bird_bottom > self.gap_bottom:
                return True
        
        return False
    
    def draw(self, screen):
        # Top pipe
        top_pipe_rect = pygame.Rect(self. x, 0, PIPE_WIDTH, self.gap_top)
        pygame.draw.rect(screen, GREEN, top_pipe_rect)
        
        # Top cap
        top_cap_rect = pygame.Rect(self.x - 5, self.gap_top - 20, PIPE_WIDTH + 10, 20)
        pygame.draw.rect(screen, GREEN, top_cap_rect)
        
        # Bottom pipe
        bottom_pipe_rect = pygame. Rect(self.x, self.gap_bottom, PIPE_WIDTH, SCREEN_HEIGHT - 50 - self.gap_bottom)
        pygame.draw.rect(screen, GREEN, bottom_pipe_rect)
        
        # Bottom cap
        bottom_cap_rect = pygame.Rect(self.x - 5, self. gap_bottom, PIPE_WIDTH + 10, 20)
        pygame.draw.rect(screen, GREEN, bottom_cap_rect)
        
        # Dark edges
        pygame.draw.rect(screen, (20, 100, 20), top_pipe_rect, 3)
        pygame.draw.rect(screen, (20, 100, 20), bottom_pipe_rect, 3)
        pygame.draw.rect(screen, (20, 100, 20), top_cap_rect, 3)
        pygame.draw.rect(screen, (20, 100, 20), bottom_cap_rect, 3)


class PipeManager:
    def __init__(self):
        self.pipes = []
        self. spawn_timer = PIPE_SPAWN_RATE - 30  # Spawn first pipe sooner
    
    def update(self):
        for pipe in self.pipes:
            pipe. update()
        
        self.pipes = [pipe for pipe in self. pipes if not pipe.is_off_screen()]
        
        self.spawn_timer += 1
        if self.spawn_timer >= PIPE_SPAWN_RATE: 
            self.pipes.append(Pipe())
            self.spawn_timer = 0
    
    def draw(self, screen):
        for pipe in self.pipes:
            pipe.draw(screen)
    
    def check_collisions(self, birds):
        for bird in birds: 
            if not bird.alive:
                continue
            for pipe in self.pipes:
                if pipe.collides_with(bird):
                    bird.die()
    
    def check_passed(self, birds):
        for pipe in self.pipes:
            if pipe.passed:
                continue
            for bird in birds:
                if bird.alive and bird.x > pipe.x + PIPE_WIDTH:
                    pipe.passed = True
                    for b in birds:
                        if b.alive:
                            b. score += 1
                            b.fitness += 100
                    break
    
    def reset(self):
        self.pipes = []
        self.spawn_timer = PIPE_SPAWN_RATE - 30  # Spawn first pipe sooner