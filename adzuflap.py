# DISCLAIMER!
# Sa mga gagamit ng code, please ignore some of my crashout moments as comments 
# Is funny so ininwan ko lang HAHAHAAH JUST REMOVE JUST REMOVE SORRY


import pygame
import random
import os

pygame.init()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Blue")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# wow magic ah gravity looking ah i cant its so cooked chat (Can adjust any of the 4 constants below to liking)
GRAVITY = 0.5
BIRD_JUMP = -8.5
PIPE_SPEED = 4
PIPE_GAP = 301

# Images
bird_image = pygame.image.load("gdsc.png")
bird_image = pygame.transform.scale(bird_image, (50, 50))

pipe_image = pygame.image.load("pipe_copy.png")
pipe_image = pygame.transform.scale(pipe_image, (80, 400))

background_image = pygame.image.load("ultibg_copy.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_image_loadingScreen = pygame.image.load("ultibg_copy.png")
background_image_loadingScreen = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Bird looking ah 
class Bird:
    def __init__(self):
        self.image = bird_image
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)

    def jump(self):
        self.velocity = BIRD_JUMP

    def draw(self):
        screen.blit(self.image, self.rect) # Just found out that blit is short for block transfer, it doesnt even make sense wtf 

# Pipe looking ah criss cross apple sauce
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.top_rect = pygame.Rect(self.x, 0, 80, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, 80, SCREEN_HEIGHT - (self.height + PIPE_GAP))
        self.top_image = pygame.transform.flip(pipe_image, False, True) # I FINALLY GOT THE PIPES TO FLIP THANK THE HEAVENS
        self.bottom_image = pipe_image
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        screen.blit(self.top_image, (self.x, self.height - self.top_image.get_height()))
        screen.blit(self.bottom_image, (self.x, self.height + PIPE_GAP))

    def off_screen(self):
        return self.x < -self.top_image.get_width()

    def collides_with(self, bird):
        return self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect)

# H E L P E R
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Saves score
def save_score(name, score):
    with open("scoring.rtf", mode="a") as file:
        file.write(f"Name: {name} | Score: {score}\n")

# Get Top 10 Scores (rtf pls)
def get_top_scores(limit=10):
    scores = []

    if not os.path.isfile("scoring.rtf"):
        return [("No scores yet", 0)]

    with open("scoring.rtf", "r") as file:
        for line in file:
            try:
                parts = line.strip().split("|")
                name_part = parts[0].split(":")[1].strip()
                score_part = int(parts[1].split(":")[1].strip())
                scores.append((name_part, score_part))
            except:
                pass

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:limit]

# Get player name input (im using mac, no need rtf for this shi ah)
def get_player_name():
    font = pygame.font.Font(None, 36)
    name = ""
    entering_name = True

    while entering_name:
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
    countdown_active = False
    countdown_start_time = None

    while not ready:
        screen.blit(background_image_loadingScreen, (0, 0))
        draw_text("Flappy Blue", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

        # Show Top 10 (or does it HMMM)
        top_scores = get_top_scores()
        draw_text("Top 10 Players", pygame.font.Font(None, 28), WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.6)
        for i, (player, scr) in enumerate(top_scores):
            draw_text(f"{i+1}. {player} - {scr}", pygame.font.Font(None, 28), WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.55 + (i * 20))

        if not countdown_active:
            draw_text("Press SPACE to start", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            draw_text(str(countdown), font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not countdown_active:
                    countdown_active = True
                    countdown_start_time = pygame.time.get_ticks()

        if countdown_active: # ew math
            elapsed_time = pygame.time.get_ticks() - countdown_start_time
            if elapsed_time >= 1000:
                countdown -= 1
                countdown_start_time = pygame.time.get_ticks()
            if countdown == 0:
                ready = True

        pygame.display.flip()
    return True

# Game over screen
def game_over_screen(score):
    top_scores = get_top_scores()
    highest_score = top_scores[0][1] if top_scores else 0
    is_new_high = score > highest_score

    name = get_player_name()
    save_score(name, score)

    # Update leaderboard after saving
    top_scores = get_top_scores()

    decision = None
    while decision is None:
        screen.blit(background_image, (0, 0))
        draw_text("Game Over", pygame.font.Font(None, 48), WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text(f"Score: {score}", pygame.font.Font(None, 48), WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.3)

        # Show Top 10 Scores
        draw_text("Top 10 Players", pygame.font.Font(None, 40), WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        for i, (player, scr) in enumerate(top_scores):
            color = RED if is_new_high and player == name and scr == score else WHITE
            draw_text(f"{i+1}. {player} - {scr}", pygame.font.Font(None, 30), color, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.9 + (i * 25))

        if is_new_high:
            draw_text("NEW HIGH SCORE!", pygame.font.Font(None, 36), RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.55)

        draw_text("R to Restart", pygame.font.Font(None, 36), WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.15)
        draw_text("Q to Quit", pygame.font.Font(None, 36), WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.08)

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

# Game loop
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
            for pipe in pipes:
                pipe.update()
                if pipe.x + pipe.top_rect.width < bird.rect.left and not pipe.passed:
                    score += 1
                    pipe.passed = True

            if bird.rect.top < 0 or bird.rect.bottom > SCREEN_HEIGHT or any(pipe.collides_with(bird) for pipe in pipes):
                game_over = True

            pipes = [pipe for pipe in pipes if not pipe.off_screen()]
            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())

        screen.blit(background_image, (0, 0)) 
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        font = pygame.font.Font(None, 60)
        score_text = font.render(f"{score}", True, WHITE)
        screen.blit(score_text, (190, 150))

        pygame.display.flip()
        clock.tick(60)

        if game_over:
            decision = game_over_screen(score)
            if decision == "restart":
                if start_screen():
                    game_loop()
            elif decision == "quit":
                pygame.quit()
                return

# Start (ng pagiging kayo yieee)
if start_screen():
    game_loop()
