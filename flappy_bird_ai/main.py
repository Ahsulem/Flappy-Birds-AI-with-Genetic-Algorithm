import pygame
import sys
from config import *
from pipe import Pipe
from genetic_algorithm import GeneticAlgorithm

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display. set_caption("Flappy Bird AI via Genetic Algorithm ft. Ahmad Suleman and Fatima Hasan")
clock = pygame.time.Clock()

def main ():
    running = True
    # Event Handling Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        #For updating and drawing game elements, birds, pipes, etc.
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()