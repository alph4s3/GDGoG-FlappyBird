#Libraries:

import pygame # pygame 
import random # for randomizing the locaation of the pipes
import os # to read files (only needed if you're using rtf)

pygame.init()

# DIMENSIONS TYPE SHII AHHH
# First, set the Height and Width of the screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Sets constant "screen" to display the screen later on when initializing
pygame.display.set_caption("Flappy Blue") # Window's caption

# COLORS RAHRAHAH
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Important constants (will be used later in the code)
GRAVITY = 0.5 # Constant gravity for how fast or slow the bird falls
BIRD_JUMP = -8.5 # Setting the constant bird_jump to -10 opposite to gravity
PIPE_SPEED = 4 # Speed of how the pipes pass
PIPE_GAP = 301 # Gap of the pipe between the top pipe to the bottom pipe

# GDSC PICS RAHHH
bird_image = pygame.image.load("gdsc.png")
bird_image = pygame.transform.scale(bird_image, (50, 50))  

pipe_image = pygame.image.load("pipe_copy.png")
pipe_image = pygame.transform.scale(pipe_image, (80, 400))  

background_image = pygame.image.load("ultibg_copy.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  

background_image_loadingScreen = pygame.image.load("ultibg.png")
background_image_loadingScreen = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  

# OOP BIRD AND PIPE AHHH
class Bird:
	#functions for bird class

    def __init__(self): # Called dunder init, initalizes the bird (double underscore = special character)
        self.image = bird_image
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def update(self): # updates how the bird moves
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)

    def jump(self): # how the bird jumps
        self.velocity = BIRD_JUMP

    def draw(self): # creates the bird
        screen.blit(self.image, self.rect)

class Pipe:
    def __init__(self): # initializing the pipes (double underscore = special character)
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.top_rect = pygame.Rect(self.x, 0, 80, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, 80, SCREEN_HEIGHT - (self.height + PIPE_GAP))
        self.top_image = pygame.transform.flip(pipe_image, False, True)  # Flip the pipe image for the top pipe
        self.bottom_image = pipe_image
        self.passed = False  # TO SEE IF BIRD PASS A PIPE 

    def update(self): # updates the pipes
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
 
    def draw(self): # draws the pipes
        screen.blit(self.top_image, (self.x, self.height - self.top_image.get_height())) # Blit means that the picture draws above the previous image
        screen.blit(self.bottom_image, (self.x, self.height + PIPE_GAP))

    def off_screen(self): # the pipes the dont exist
        return self.x < -self.top_image.get_width()

    def collides_with(self, bird): # when the bird collides with the pipes
        return self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect)

# TO SEE TEXT
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

#SAVES NAME (rtf version)
def save_score(name, score):
    file_exists = os.path.isfile("scoring.rtf")
    
    with open("scoring.rtf", mode="a") as file:
        file.write(f"Name: {name} | Score: {score}\n")
        

# GETS NAME FUNCTION THINGY (after game ends)
def get_player_name():
    font = pygame.font.Font(None, 36)
    name = ""
    entering_name = True

    while entering_name:
    	#adzu background drawing fr
        screen.blit(background_image, (0, 0))  
        draw_text("Enter your name:", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text(name, font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return ""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        pygame.display.flip()

    return name

# Start screen 
def start_screen():
    font = pygame.font.Font(None, 48)
    ready = False
    countdown = 3 
    countdown_active = False  # While countdown hasn't started
    countdown_start_time = None  # To track when the countdown started

    while not ready:
        screen.blit(background_image_loadingScreen, (0, 0))  # Draw background
        draw_text("Flappy Blue", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

        if not countdown_active:
            draw_text("Press SPACE to start", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            draw_text(str(countdown), font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Display countdown

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not countdown_active:
                    countdown_active = True
                    countdown_start_time = pygame.time.get_ticks()  # Record the start time of the countdown

        # Added a countdown logic :-)
        if countdown_active:
            elapsed_time = pygame.time.get_ticks() - countdown_start_time
            if elapsed_time >= 1000:  # 1000 = 1 second
                countdown -= 1
                countdown_start_time = pygame.time.get_ticks()  # Reset the start time for the next countdown step
            if countdown == 0:  # Countdown finished
                ready = True

        pygame.display.flip()
        
    return True


# It's over for you lil bro
def game_over_screen(score):
    name = get_player_name()
    save_score(name, score)

    font = pygame.font.Font(None, 48)
    decision = None

    while decision is None:
        screen.blit(background_image, (0, 0))  # STILL DRAWS ADZU BACKGROUND YUMS
        draw_text("Game Over", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text(f"Score: {score}", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Jed: 9 ", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.70)
        draw_text("R to Restart", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.35)
        draw_text("Q to Quit", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    decision = "restart"
                if event.key == pygame.K_q:
                    decision = "quit"

        pygame.display.flip()

    return decision

# MAIN LOOP AFTER SO MANY CLASSES AHHH
def game_loop():
    bird = Bird()
    pipes = [Pipe()]
    clock = pygame.time.Clock()
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if not game_over:
            bird.update()

            # pipe updating and all
            for pipe in pipes:
                pipe.update()

                # If passes pipe, plus 1 frfr
                if pipe.x + pipe.top_rect.width < bird.rect.left and not pipe.passed:
                    score += 1
                    pipe.passed = True

            # if ded, then game over true
            if bird.rect.top < 0 or bird.rect.bottom > SCREEN_HEIGHT or any(pipe.collides_with(bird) for pipe in pipes):
                game_over = True

            # Removes pipes if it passes so that no laggy laggy ah
            pipes = [pipe for pipe in pipes if not pipe.off_screen()]
            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())

        screen.blit(background_image, (0, 0))  
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # sHows score
        font = pygame.font.Font(None, 60)
        score_text = font.render(f"{score}", True, WHITE)
        screen.blit(score_text, (190, 150))

        pygame.display.flip()
        clock.tick(60)

        # if game over fr
        if game_over:
            decision = game_over_screen(score)
            if decision == "restart": 
            	if start_screen():           	
                	game_loop()
            elif decision == "quit":
                pygame.quit()
                return

# Start the game
if start_screen():
    game_loop()
