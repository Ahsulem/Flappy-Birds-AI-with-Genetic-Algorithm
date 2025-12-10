# ===========================================
# FITNESS GRAPH - Visualize Evolution Progress
# ===========================================

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for live updates

class FitnessGraph: 
    def __init__(self):
        """Initialize the fitness graph window"""
        # Enable interactive mode
        plt.ion()
        
        # Create figure and axis
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.fig.canvas.manager.set_window_title('Evolution Progress')
        
        # Initialize empty lines
        self.best_line, = self.ax.plot([], [], 'g-', linewidth=2, label='Best Fitness')
        self.avg_line, = self.ax.plot([], [], 'b--', linewidth=1.5, label='Average Fitness')
        
        # Configure axis
        self.ax.set_xlabel('Generation', fontsize=12)
        self.ax.set_ylabel('Fitness', fontsize=12)
        self.ax.set_title('Genetic Algorithm - Fitness Over Generations', fontsize=14)
        self.ax.legend(loc='upper left')
        self.ax.grid(True, alpha=0.3)
        
        # Set initial limits
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 100)
        
        # Show the plot
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(0.1)
    
    def update(self, best_fitness_history, avg_fitness_history):
        """
        Update the graph with new data. 
        
        Args:
            best_fitness_history: List of best fitness values per generation
            avg_fitness_history: List of average fitness values per generation
        """
        if not best_fitness_history: 
            return
        
        generations = list(range(1, len(best_fitness_history) + 1))
        
        # Update line data
        self.best_line. set_data(generations, best_fitness_history)
        self.avg_line.set_data(generations, avg_fitness_history)
        
        # Adjust axis limits dynamically
        max_gen = max(10, len(generations) + 5)
        max_fitness = max(100, max(best_fitness_history) * 1.1)
        
        self.ax.set_xlim(0, max_gen)
        self.ax.set_ylim(0, max_fitness)
        
        # Add current stats as text
        # Remove old text annotations
        for txt in self.ax.texts:
            txt.remove()
        
        # Add new stats
        current_best = best_fitness_history[-1]
        current_avg = avg_fitness_history[-1]
        all_time_best = max(best_fitness_history)
        
        stats_text = f'Gen {len(generations)}: Best={current_best:. 0f}, Avg={current_avg:.0f}, All-Time Best={all_time_best:.0f}'
        self.ax. text(
            0.5, 0.98, stats_text,
            transform=self.ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            horizontalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )
        
        # Redraw
        self.fig. canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.01)
    
    def close(self):
        """Close the graph window"""
        plt.close(self.fig)