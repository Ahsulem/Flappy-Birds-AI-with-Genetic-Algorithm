# ===========================================
# FLAPPY BIRD AI - MAIN GAME LOOP
# ===========================================

import pygame
from config import *
from bird import Bird

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display. set_caption("Flappy Bird AI - Genetic Algorithm")
clock = pygame.time.Clock()

def main():
    running = True
    
    # Create a test bird (manual control for now)
    test_bird = Bird()
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Manual control for testing (SPACE to flap)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    test_bird.flap()
        
        # Update bird
        test_bird. update()
        
        # Clear screen
        screen.fill(SKY_BLUE)
        
        # Draw ground
        pygame.draw. rect(screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # Draw bird
        test_bird.draw(screen, is_best=True)
        
        # Display instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to flap!", True, BLACK)
        screen. blit(text, (SCREEN_WIDTH // 2 - 100, 30))
        
        # Show if bird is dead
        if not test_bird.alive:
            dead_text = font. render("CRASHED!  Close and restart.", True, RED)
            screen.blit(dead_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame. quit()

if __name__ == "__main__":
    main() 