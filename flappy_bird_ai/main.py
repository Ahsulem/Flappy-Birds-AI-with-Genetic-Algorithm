# ===========================================
# FLAPPY BIRD AI - MAIN GAME LOOP
# ===========================================

import pygame
import os
from config import *
from bird import Bird
from pipe import PipeManager
from genetic_algorithm import GeneticAlgorithm
from neural_network import NeuralNetwork

# Initialize Pygame
pygame.init()
screen = pygame.display. set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI - Genetic Algorithm")
clock = pygame.time. Clock()

def main():
    running = True
    
    # Initialize Genetic Algorithm
    ga = GeneticAlgorithm()
    
    # Create initial population
    print(f"Creating {POPULATION_SIZE} birds...")
    birds = ga.create_initial_population(Bird)
    print(f"Created {len(birds)} birds!")
    
    # Create pipe manager
    pipe_manager = PipeManager()
    
    # Initialize fitness graph
    graph = None
    show_graph = True
    try:
        from fitness_graph import FitnessGraph
        graph = FitnessGraph()
        print("Fitness graph initialized!")
    except Exception as e:
        print(f"Could not create graph: {e}")
        print("Continuing without graph...  (Press G to try again)")
        show_graph = False
    
    # Game fonts
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)
    
    # Speed control
    game_speed = 1
    speed_options = [1, 2, 5, 10]
    speed_index = 0
    
    # Demo mode
    demo_mode = False
    
    while running:
        # Event handling
        for event in pygame. event.get():
            if event.type == pygame.QUIT: 
                running = False
            
            if event.type == pygame. KEYDOWN:
                # Speed control
                if event.key == pygame.K_s:
                    speed_index = (speed_index + 1) % len(speed_options)
                    game_speed = speed_options[speed_index]
                    print(f"Speed:  {game_speed}x")
                
                # Reset
                if event.key == pygame. K_r:
                    ga = GeneticAlgorithm()
                    birds = ga. create_initial_population(Bird)
                    pipe_manager.reset()
                    demo_mode = False
                    print("Reset!")
                
                # Save best brain
                if event.key == pygame.K_b:
                    best_bird = max(birds, key=lambda b:  b.fitness)
                    best_bird.brain.save("best_brain.json")
                
                # Load best brain (demo mode)
                if event.key == pygame.K_l:
                    if os.path.exists("best_brain.json"):
                        loaded_brain = NeuralNetwork. load("best_brain.json")
                        birds = [Bird(neural_network=loaded_brain)]
                        pipe_manager.reset()
                        demo_mode = True
                        print("Demo mode: Watching saved brain!")
                    else:
                        print("No saved brain found!  Press B to save one first.")
                
                # Toggle graph
                if event.key == pygame. K_g:
                    if graph and show_graph:
                        graph.close()
                        graph = None
                        show_graph = False
                        print("Graph closed")
                    else:
                        try:
                            from fitness_graph import FitnessGraph
                            graph = FitnessGraph()
                            show_graph = True
                            # Update with existing data
                            if ga.best_fitness_history:
                                graph.update(ga. best_fitness_history, ga. avg_fitness_history)
                            print("Graph opened")
                        except Exception as e:
                            print(f"Could not create graph: {e}")
        
        # ============ GAME LOGIC ============
        for _ in range(game_speed):
            # Birds think
            for bird in birds:
                bird.think(pipe_manager.pipes)
            
            # Update birds
            for bird in birds:
                bird.update()
            
            # Update pipes
            pipe_manager. update()
            
            # Check collisions
            pipe_manager. check_collisions(birds)
            pipe_manager.check_passed(birds)
            
            # Count alive
            alive_count = sum(1 for bird in birds if bird.alive)
            
            # Evolution when all dead
            if alive_count == 0:
                if demo_mode:
                    # Restart demo with same brain
                    loaded_brain = NeuralNetwork. load("best_brain.json")
                    birds = [Bird(neural_network=loaded_brain)]
                    pipe_manager.reset()
                else:
                    # Normal evolution
                    best_fitness = max(b.fitness for b in birds)
                    print(f"Generation {ga.generation} complete!  Best fitness: {best_fitness}")
                    
                    birds = ga.create_next_generation(birds, Bird)
                    pipe_manager.reset()
                    
                    # Update graph
                    if graph and show_graph:
                        try:
                            graph.update(ga.best_fitness_history, ga.avg_fitness_history)
                        except Exception as e: 
                            print(f"Graph error: {e}")
                break
        
        # Get stats
        best_bird = max(birds, key=lambda b: b. fitness)
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
                bird.draw(screen, is_best=False)
        best_bird.draw(screen, is_best=True)
        
        # ============ UI - LEFT PANEL ============
        panel = pygame.Surface((200, 175))
        panel.set_alpha(200)
        panel.fill((30, 30, 30))
        screen.blit(panel, (10, 10))
        pygame.draw.rect(screen, WHITE, (10, 10, 200, 175), 2)
        
        # Title
        if demo_mode:
            title = font.render("🎬 DEMO", True, YELLOW)
        else:
            title = font. render(f"🧬 Gen:  {ga.generation}", True, WHITE)
        screen.blit(title, (20, 15))
        
        alive_text = small_font.render(f"Alive: {alive_count}/{len(birds)}", True, WHITE)
        screen.blit(alive_text, (20, 50))
        
        score_text = small_font.render(f"Score: {best_bird.score}", True, WHITE)
        screen.blit(score_text, (20, 75))
        
        fitness_text = small_font.render(f"Fitness: {best_bird.fitness}", True, WHITE)
        screen.blit(fitness_text, (20, 100))
        
        speed_text = small_font.render(f"Speed: {game_speed}x", True, WHITE)
        screen.blit(speed_text, (20, 125))
        
        # Best ever
        if ga.best_fitness_history and not demo_mode:
            best_ever = max(ga.best_fitness_history)
            best_text = small_font.render(f"Best Ever: {best_ever}", True, YELLOW)
            screen.blit(best_text, (20, 150))
        
        # ============ UI - RIGHT PANEL (Controls) ============
        controls_panel = pygame.Surface((160, 140))
        controls_panel.set_alpha(200)
        controls_panel.fill((30, 30, 30))
        screen.blit(controls_panel, (SCREEN_WIDTH - 170, 10))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 170, 10, 160, 140), 2)
        
        ctrl_title = small_font.render("⌨ Controls", True, YELLOW)
        screen.blit(ctrl_title, (SCREEN_WIDTH - 160, 15))
        
        controls = [
            ("S", "Speed"),
            ("R", "Reset"),
            ("B", "Save Brain"),
            ("L", "Load Brain"),
            ("G", "Graph")
        ]
        
        for i, (key, action) in enumerate(controls):
            ctrl_text = small_font.render(f"{key}: {action}", True, WHITE)
            screen.blit(ctrl_text, (SCREEN_WIDTH - 160, 40 + i * 20))
        
        # Update display
        pygame.display. flip()
        clock.tick(FPS)
    
    # Cleanup
    if graph:
        graph.close()
    pygame.quit()

if __name__ == "__main__": 
    main()