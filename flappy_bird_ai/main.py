# ===========================================
# FLAPPY BIRD AI - MAIN GAME LOOP
# ===========================================

import pygame
from config import *
from bird import Bird
from pipe import PipeManager
from genetic_algorithm import GeneticAlgorithm

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI - Genetic Algorithm")
clock = pygame.time.Clock()

def main():
    running = True
    
    # Initialize Genetic Algorithm
    ga = GeneticAlgorithm()
    
    # Create initial population - THIS IS KEY! 
    print(f"Creating {POPULATION_SIZE} birds...")
    birds = ga.create_initial_population(Bird)
    print(f"Created {len(birds)} birds!")
    
    # Create pipe manager
    pipe_manager = PipeManager()
    
    # Game fonts
    font = pygame.font. Font(None, 36)
    small_font = pygame.font.Font(None, 28)
    
    # Speed control
    game_speed = 1
    speed_options = [1, 2, 5, 10]
    speed_index = 0
    
    while running:
        # Event handling
        for event in pygame. event.get():
            if event.type == pygame.QUIT: 
                running = False
            
            if event.type == pygame. KEYDOWN:
                if event.key == pygame.K_s:
                    speed_index = (speed_index + 1) % len(speed_options)
                    game_speed = speed_options[speed_index]
                    print(f"Speed:  {game_speed}x")
                
                if event.key == pygame. K_r:
                    ga = GeneticAlgorithm()
                    birds = ga.create_initial_population(Bird)
                    pipe_manager.reset()
                    print("Reset!")
                
                if event.key == pygame.K_b:
                    best_bird = max(birds, key=lambda b:  b.fitness)
                    best_bird.brain.save("best_brain.json")
        
        # ============ GAME LOGIC ============
        for _ in range(game_speed):
            # Birds think
            for bird in birds: 
                bird.think(pipe_manager.pipes)
            
            # Update birds
            for bird in birds: 
                bird.update()
            
            # Update pipes
            pipe_manager.update()
            
            # Check collisions
            pipe_manager.check_collisions(birds)
            pipe_manager.check_passed(birds)
            
            # Count alive
            alive_count = sum(1 for bird in birds if bird.alive)
            
            # Evolution when all dead
            if alive_count == 0:
                print(f"Generation {ga.generation} complete!  Best fitness: {max(b.fitness for b in birds)}")
                birds = ga.create_next_generation(birds, Bird)
                pipe_manager.reset()
                break
        
        # Get stats
        best_bird = max(birds, key=lambda b: b.fitness)
        alive_count = sum(1 for bird in birds if bird.alive)
        
        # ============ DRAWING ============
        screen.fill(SKY_BLUE)
        
        # Draw pipes
        pipe_manager.draw(screen)
        
        # Draw ground
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        pygame.draw.rect(screen, (20, 100, 20), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 5))
        
        # Draw ALL birds
        for bird in birds: 
            if bird != best_bird:
                bird. draw(screen, is_best=False)
        best_bird.draw(screen, is_best=True)
        
        # ============ UI ============
        # Stats panel
        panel = pygame.Surface((200, 150))
        panel.set_alpha(200)
        panel.fill((30, 30, 30))
        screen.blit(panel, (10, 10))
        
        gen_text = font.render(f"Gen: {ga.generation}", True, WHITE)
        screen.blit(gen_text, (20, 15))
        
        alive_text = small_font.render(f"Alive: {alive_count}/{len(birds)}", True, WHITE)
        screen.blit(alive_text, (20, 50))
        
        score_text = small_font.render(f"Score: {best_bird.score}", True, WHITE)
        screen.blit(score_text, (20, 75))
        
        fitness_text = small_font.render(f"Fitness: {best_bird.fitness}", True, WHITE)
        screen.blit(fitness_text, (20, 100))
        
        speed_text = small_font.render(f"Speed: {game_speed}x (S)", True, WHITE)
        screen.blit(speed_text, (20, 125))
        
        # Pipe count debug
        pipe_debug = small_font.render(f"Pipes: {len(pipe_manager.pipes)}", True, YELLOW)
        screen.blit(pipe_debug, (SCREEN_WIDTH - 100, 10))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()