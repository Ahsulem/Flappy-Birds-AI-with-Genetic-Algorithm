import pygame
import random
from config import (SCREEN_HEIGHT, PIPE_WIDTH, PIPE_GAP, 
                    PIPE_VELOCITY, GREEN, DARK_GREEN)


class Pipe:
    """Represents a pair of pipes (top and bottom)."""
    
    def __init__(self, x):
        """
        Initialize a pipe pair at the given x position.
        
        Args:
            x: Starting x position of the pipe
        """
        self.x = x
        self.width = PIPE_WIDTH
        self.gap = PIPE_GAP
        self.velocity = PIPE_VELOCITY
        self.passed = False
        
        # Random gap position (leaving room for the gap)
        min_top = 50
        max_top = SCREEN_HEIGHT - self.gap - 50
        self.top = random.randint(min_top, max_top)  # Bottom of top pipe
        self.bottom = self.top + self.gap  # Top of bottom pipe
    
    def update(self):
        """Move the pipe to the left."""
        self.x -= self.velocity
    
    def is_off_screen(self):
        """Check if the pipe has moved off the left side of the screen."""
        return self.x + self.width < 0
    
    def collides_with(self, bird):
        """
        Check if the pipe collides with a bird.
        
        Args:
            bird: The bird to check collision with
            
        Returns:
            True if there is a collision, False otherwise
        """
        bird_rect = bird.get_rect()
        
        # Top pipe rectangle
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        
        # Bottom pipe rectangle
        bottom_rect = pygame.Rect(self.x, self.bottom, self.width, 
                                  SCREEN_HEIGHT - self.bottom)
        
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)
    
    def draw(self, screen):
        """Draw the pipe pair on the screen."""
        # Draw top pipe
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, DARK_GREEN, top_rect, 3)
        
        # Draw top pipe cap
        cap_height = 20
        cap_rect = pygame.Rect(self.x - 5, self.top - cap_height, 
                               self.width + 10, cap_height)
        pygame.draw.rect(screen, GREEN, cap_rect)
        pygame.draw.rect(screen, DARK_GREEN, cap_rect, 3)
        
        # Draw bottom pipe
        bottom_rect = pygame.Rect(self.x, self.bottom, self.width, 
                                  SCREEN_HEIGHT - self.bottom)
        pygame.draw.rect(screen, GREEN, bottom_rect)
        pygame.draw.rect(screen, DARK_GREEN, bottom_rect, 3)
        
        # Draw bottom pipe cap
        cap_rect = pygame.Rect(self.x - 5, self.bottom, 
                               self.width + 10, cap_height)
        pygame.draw.rect(screen, GREEN, cap_rect)
        pygame.draw.rect(screen, DARK_GREEN, cap_rect, 3)
