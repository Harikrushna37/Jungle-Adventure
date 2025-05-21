import pygame
import random
import sys


pygame.init()

# Screen visualisation
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jungle Banana Adventure")

# Fonts and colors
font = pygame.font.SysFont("comicsansms", 32)
big_font = pygame.font.SysFont("comicsansms", 48)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# images
bg_img = pygame.image.load("images/jungle_background.jpg")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

player_img = pygame.image.load("images/player.png")
player_img = pygame.transform.scale(player_img, (80, 80))
player_x = 50
player_y = HEIGHT // 2 - 40

banana_img = pygame.image.load("images/banana 2.png")
banana_img = pygame.transform.scale(banana_img, (40, 40))

# sounds
correct_sound = pygame.mixer.Sound("sounds/correct_music.wav")
wrong_sound = pygame.mixer.Sound("sounds/wrong_music.wav")
pygame.mixer.music.load("sounds/jungle_music.mp3")
pygame.mixer.music.play(-1)

# variables
bananas_collected = 0
level = 1
question = ""
correct_answer = 0
options = []
selected = None

def generate_question(level):
    global question, correct_answer, options
    operations = ['+', '-', '*', '/']
    op = random.choice(operations)
    a = random.randint(1, level * 5)
    b = random.randint(1, level * 5)
    if op == '/':
        a = a * b
    question = f"{a} {op} {b}"

    try:
        correct_answer = eval(question)
        correct_answer = int(correct_answer)
    except ZeroDivisionError:
        correct_answer = 0

    options = [correct_answer]
    while len(options) < 4:
        fake = random.randint(correct_answer - 10, correct_answer + 10)
        if fake != correct_answer and fake not in options:
            options.append(fake)
    random.shuffle(options)

generate_question(level)

def draw_ui():
    screen.blit(bg_img, (0, 0))
    screen.blit(player_img, (player_x, player_y))

    # maths questions
    question_text = big_font.render(f"Solve: {question}", True, WHITE)
    screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 50))

    # buttons
    for i, option in enumerate(options):
        btn_rect = pygame.Rect(100 + i * 170, 200, 150, 60)
        color = GREEN if selected == i else WHITE
        pygame.draw.rect(screen, color, btn_rect, border_radius=10)
        opt_text = font.render(str(option), True, BLACK)
        screen.blit(opt_text, (btn_rect.x + 45, btn_rect.y + 10))

    # score count
    screen.blit(banana_img, (10, 10))
    banana_text = font.render(f"x {bananas_collected}", True, WHITE)
    screen.blit(banana_text, (60, 15))

    # level
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (WIDTH - 180, 15))

def check_answer(index):
    global bananas_collected, selected, level
    if options[index] == correct_answer:
        correct_sound.play()
        bananas_collected += 1
        if bananas_collected % 5 == 0:
            level += 1
    else:
        wrong_sound.play()
        bananas_collected = max(0, bananas_collected - 1)
    selected = None
    generate_question(level)

#  loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    screen.fill(BLACK)

    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, option in enumerate(options):
                btn_rect = pygame.Rect(100 + i * 170, 200, 150, 60)
                if btn_rect.collidepoint(pos):
                    selected = i
                    check_answer(i)

    pygame.display.flip()

pygame.quit()
sys.exit()
