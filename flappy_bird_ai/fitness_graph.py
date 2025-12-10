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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI - Genetic Algorithm")
clock = pygame.time.Clock()


def draw_graph(screen, best_history, avg_history, x, y, width, height):
    """
    Draw a mini fitness graph directly on the Pygame screen.
    
    Args:
        screen:  Pygame screen surface
        best_history: List of best fitness values per generation
        avg_history: List of average fitness values per generation
        x, y: Top-left corner position of the graph
        width, height:  Size of the graph
    """
    # Draw background
    graph_surface = pygame.Surface((width, height))
    graph_surface.set_alpha(220)
    graph_surface.fill((20, 20, 30))
    screen.blit(graph_surface, (x, y))
    
    # Draw border
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
    
    # Graph title
    font = pygame.font. Font(None, 24)
    title = font.render("Fitness Graph", True, YELLOW)
    screen.blit(title, (x + 10, y + 5))
    
    # If no data yet, show message
    if len(best_history) < 2:
        no_data = font.render("Waiting for data...", True, WHITE)
        screen.blit(no_data, (x + width // 2 - 70, y + height // 2))
        return
    
    # Graph area (with padding)
    padding = 35
    graph_x = x + padding
    graph_y = y + padding
    graph_w = width - padding - 15
    graph_h = height - padding - 25
    
    # Draw axes
    pygame.draw.line(screen, WHITE, (graph_x, graph_y), (graph_x, graph_y + graph_h), 1)  # Y axis
    pygame.draw.line(screen, WHITE, (graph_x, graph_y + graph_h), (graph_x + graph_w, graph_y + graph_h), 1)  # X axis
    
    # Calculate scale
    max_fitness = max(max(best_history), max(avg_history)) * 1.1
    if max_fitness == 0:
        max_fitness = 100
    max_gen = len(best_history)
    
    # Function to convert data to screen coordinates
    def to_screen(gen, fitness):
        sx = graph_x + (gen / max_gen) * graph_w
        sy = graph_y + graph_h - (fitness / max_fitness) * graph_h
        return (int(sx), int(sy))
    
    # Draw grid lines
    for i in range(1, 5):
        # Horizontal grid lines
        gy = graph_y + (i / 4) * graph_h
        pygame.draw.line(screen, (60, 60, 60), (graph_x, gy), (graph_x + graph_w, gy), 1)
        
        # Y-axis labels
        label_val = int(max_fitness * (4 - i) / 4)
        label = font.render(str(label_val), True, (150, 150, 150))
        screen.blit(label, (x + 5, gy - 8))
    
    # Draw best fitness line (green)
    if len(best_history) >= 2:
        best_points = [to_screen(i, best_history[i]) for i in range(len(best_history))]
        pygame.draw. lines(screen, (0, 255, 0), False, best_points, 2)
    
    # Draw average fitness line (blue dashed - we'll use dots)
    if len(avg_history) >= 2:
        avg_points = [to_screen(i, avg_history[i]) for i in range(len(avg_history))]
        # Draw as dotted line
        for i in range(len(avg_points) - 1):
            if i % 2 == 0:  # Skip every other segment for dashed effect
                pygame.draw.line(screen, (100, 150, 255), avg_points[i], avg_points[i + 1], 2)
    
    # Legend
    small_font = pygame.font.Font(None, 18)
    
    # Best fitness legend
    pygame.draw.line(screen, (0, 255, 0), (x + width - 90, y + 8), (x + width - 70, y + 8), 2)
    best_label = small_font.render("Best", True, (0, 255, 0))
    screen.blit(best_label, (x + width - 65, y + 3))
    
    # Avg fitness legend
    pygame.draw. line(screen, (100, 150, 255), (x + width - 90, y + 20), (x + width - 70, y + 20), 2)
    avg_label = small_font.render("Avg", True, (100, 150, 255))
    screen.blit(avg_label, (x + width - 65, y + 15))
    
    # Current generation label
    gen_label = small_font.render(f"Gen: {len(best_history)}", True, WHITE)
    screen.blit(gen_label, (graph_x + graph_w - 50, graph_y + graph_h + 5))


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
    
    # Game fonts
    font = pygame.font. Font(None, 36)
    small_font = pygame.font.Font(None, 28)
    
    # Speed control
    game_speed = 1
    speed_options = [1, 2, 5, 10]
    speed_index = 0
    
    # Demo mode
    demo_mode = False
    
    # Show graph toggle
    show_graph = True
    
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
                    print(f"Speed: {game_speed}x")
                
                # Reset
                if event.key == pygame.K_r:
                    ga = GeneticAlgorithm()
                    birds = ga.create_initial_population(Bird)
                    pipe_manager.reset()
                    demo_mode = False
                    print("Reset!")
                
                # Save best brain
                if event.key == pygame.K_b:
                    best_bird = max(birds, key=lambda b:  b.fitness)
                    best_bird.brain.save("best_brain.json")
                
                # Load best brain (demo mode)
                if event. key == pygame.K_l:
                    if os.path.exists("best_brain.json"):
                        loaded_brain = NeuralNetwork.load("best_brain.json")
                        birds = [Bird(neural_network=loaded_brain)]
                        pipe_manager.reset()
                        demo_mode = True
                        print("Demo mode: Watching saved brain!")
                    else: 
                        print("No saved brain found!  Press B to save one first.")
                
                # Toggle graph
                if event.key == pygame.K_g:
                    show_graph = not show_graph
                    print(f"Graph: {'ON' if show_graph else 'OFF'}")
        
        # ============ GAME LOGIC ============
        for _ in range(game_speed):
            # Birds think
            for bird in birds: 
                bird.think(pipe_manager. pipes)
            
            # Update birds
            for bird in birds: 
                bird.update()
            
            # Update pipes
            pipe_manager.update()
            
            # Check collisions
            pipe_manager.check_collisions(birds)
            pipe_manager.check_passed(birds)
            
            # Count alive
            alive_count = sum(1 for bird in birds if bird. alive)
            
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
                    print(f"Generation {ga.generation} complete! Best fitness: {best_fitness}")
                    
                    birds = ga.create_next_generation(birds, Bird)
                    pipe_manager. reset()
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
        
        # ============ UI - LEFT PANEL ============
        panel = pygame.Surface((200, 175))
        panel.set_alpha(200)
        panel.fill((30, 30, 30))
        screen.blit(panel, (10, 10))
        pygame.draw.rect(screen, WHITE, (10, 10, 200, 175), 2)
        
        # Title
        if demo_mode:
            title = font.render("DEMO", True, YELLOW)
        else:
            title = font. render(f"Gen: {ga.generation}", True, WHITE)
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
        controls_panel = pygame.Surface((145, 145))
        controls_panel.set_alpha(200)
        controls_panel.fill((30, 30, 30))
        screen.blit(controls_panel, (SCREEN_WIDTH - 155, 10))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 155, 10, 145, 145), 2)
        
        ctrl_title = small_font.render("Controls", True, YELLOW)
        screen.blit(ctrl_title, (SCREEN_WIDTH - 145, 15))
        
        controls = [
            ("S", "Speed"),
            ("R", "Reset"),
            ("B", "Save Brain"),
            ("L", "Load Brain"),
            ("G", "Graph")
        ]
        
        for i, (key, action) in enumerate(controls):
            ctrl_text = small_font.render(f"{key}: {action}", True, WHITE)
            screen.blit(ctrl_text, (SCREEN_WIDTH - 145, 40 + i * 20))
        
        # ============ EMBEDDED FITNESS GRAPH ============
        if show_graph and not demo_mode:
            graph_width = 250
            graph_height = 150
            graph_x = SCREEN_WIDTH - graph_width - 10
            graph_y = SCREEN_HEIGHT - 50 - graph_height - 10  # Above ground
            
            draw_graph(
                screen,
                ga.best_fitness_history,
                ga.avg_fitness_history,
                graph_x, graph_y,
                graph_width, graph_height
            )
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()