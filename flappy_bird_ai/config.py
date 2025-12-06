# Configuration settings for Flappy Bird AI

# Screen settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
SKY_BLUE = (135, 206, 235)
RED = (255, 0, 0)

# Bird settings
BIRD_X = 100
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_RADIUS = 15
GRAVITY = 0.5
JUMP_STRENGTH = -8 #did it negative cuz Y goes downward and gravity comes to play
FLAP_STRENGTH = -8
MAX_VELOCITY = 10

# Pipe settings
PIPE_WIDTH = 60
PIPE_GAP = 150 #vertical gap between pipes top & bottom
PIPE_VELOCITY = 4
PIPE_SPAWN_RATE = 90  # frames between pipe spawns

# Neural Network settings
INPUT_SIZE = 5  # bird_y, bird_velocity, pipe_x, pipe_top, pipe_bottom
HIDDEN_SIZE = 8
OUTPUT_SIZE = 1  # jump or not

# Genetic Algorithm settings
POPULATION_SIZE = 50
MUTATION_RATE = 0.1
MUTATION_STRENGTH = 0.5
ELITISM_COUNT = 5
