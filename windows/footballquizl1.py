import pygame
import sys
import os
import random
import json
import pathlib

# Constants
WIDTH, HEIGHT = 960, 640
GOAL_Y = 140
GOAL_L, GOAL_R = WIDTH // 2 - 120, WIDTH // 2 + 120
QUESTION_TIME = 8  # seconds
QUESTION_TOTAL = 8  # number of questions
TIP_MS = 1000
SCORE_FILE = "highscores.json"
DIFFICULTY = "EASY"


# Question generation
def make_question():
    a, b = random.randint(0, 50), random.randint(0, 50)
    op = random.choice(["+", "-"])
    text = f"{a} {op} {b} = ?"
    ans = eval(f"{a}{op}{b}")
    return text, ans


# Score file tool
def load_scores(limit=5):
    if pathlib.Path(SCORE_FILE).exists():
        with open(SCORE_FILE) as f:
            return json.load(f)[:limit]
    return []


def save_score(sc, limit=5):
    scores = load_scores(limit - 1) + [sc]
    with open(SCORE_FILE, "w") as f:
        json.dump(sorted(scores, reverse=True)[:limit], f)


# Initialize Pygame and audio
pygame.init()
pygame.mixer.init()
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Football Quiz – {DIFFICULTY}")
clock = pygame.time.Clock()

# Use Georgia serif font for all text
fBig = pygame.font.SysFont("Georgia", 52)
fMid = pygame.font.SysFont("Georgia", 36)
fSm = pygame.font.SysFont("Georgia", 24)


# Load sound effects
def sfx(name):
    try:
        return pygame.mixer.Sound(name)
    except:
        return None


goal_sfx, miss_sfx = sfx("goal.mp3"), sfx("miss.mp3")

# Try to load background music
try:
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.play(-1)
except:
    pass

# Visual elements
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT - 70, 20, 20)
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 40, 50, 30)


def draw_pitch():
    scr.fill((30, 150, 30))
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(scr, (26, 135, 26), (0, y, WIDTH, 20))
    pygame.draw.rect(scr, (255, 255, 255), (GOAL_L, GOAL_Y + 90, 240, 2))
    pygame.draw.rect(scr, (255, 255, 255), (GOAL_L, GOAL_Y, 240, 8))
    pygame.draw.rect(scr, (255, 255, 255), (GOAL_L, GOAL_Y, 8, 90))
    pygame.draw.rect(scr, (255, 255, 255), (GOAL_R - 8, GOAL_Y, 8, 90))


def reset_ball():
    ball.topleft = (WIDTH // 2 - 10, HEIGHT - 70)
    player.midbottom = (WIDTH // 2, HEIGHT - 40)
    return 0, -12


# Main game function
def main_game():
    score = q_no = 0
    question, answer = make_question()
    typed = ""
    q_start = pygame.time.get_ticks()
    vx, vy = reset_ball()
    shot_res = None
    tip, tipT = "", 0

    while True:
        dt = clock.tick(60)
        keys = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if shot_res is None and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    try:
                        ok = int(typed) == answer
                    except:
                        ok = False
                    shot_res = "goal" if ok else "miss"
                    vx = random.randint(-3, 3) if ok else random.choice(list(range(-12, -7)) + list(range(7, 13)))
                elif e.key == pygame.K_BACKSPACE:
                    typed = typed[:-1]
                else:
                    typed += e.unicode

        # Check for time running out
        if shot_res is None and (pygame.time.get_ticks() - q_start) / 1000 >= QUESTION_TIME:
            shot_res = "miss"
            vx = random.choice(list(range(-12, -7)) + list(range(7, 13)))

        # Handle ball movement after shooting
        if shot_res is not None:
            if keys[pygame.K_LEFT]:
                player.x -= 6
            if keys[pygame.K_RIGHT]:
                player.x += 6
            player.clamp_ip(scr.get_rect())
            ball.x += vx
            ball.y += vy

            # Check if ball entered goal area
            if ball.bottom <= GOAL_Y + 12:
                success_now = (shot_res == "goal")
                tip = "GOAL !" if success_now else "MISS !"
                tipT = pygame.time.get_ticks()

                if success_now:
                    score += 1
                    goal_sfx and goal_sfx.play()
                else:
                    miss_sfx and miss_sfx.play()
                    save_score(score)

                    # Create a gradient background for the transition screen
                    transition_bg = pygame.Surface((WIDTH, HEIGHT))
                    for y in range(HEIGHT):
                        # Create a gradient from dark blue to light blue
                        color = (
                            int(0 + (100) * y / HEIGHT),
                            int(50 + (130) * y / HEIGHT),
                            int(150 + (50) * y / HEIGHT)
                        )
                        pygame.draw.line(transition_bg, color, (0, y), (WIDTH, y))

                    # Show transition screen with gradient background
                    scr.blit(transition_bg, (0, 0))

                    # Create a fancy box for the title
                    msg_text = fBig.render("Game Over!", True, (255, 50, 50))
                    msg_rect = msg_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))

                    # Draw a gold box around the title
                    pygame.draw.rect(scr, (255, 215, 0),
                                     (msg_rect.left - 20, msg_rect.top - 10,
                                      msg_rect.width + 40, msg_rect.height + 20),
                                     border_radius=15)
                    pygame.draw.rect(scr, (0, 0, 0),
                                     (msg_rect.left - 20, msg_rect.top - 10,
                                      msg_rect.width + 40, msg_rect.height + 20),
                                     width=3, border_radius=15)

                    scr.blit(msg_text, msg_rect)

                    # Draw "Continue to Summary" button
                    continue_btn = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 60)
                    pygame.draw.rect(scr, (0, 200, 0), continue_btn, border_radius=10)
                    pygame.draw.rect(scr, (0, 0, 0), continue_btn, 2, border_radius=10)

                    btn_text = fMid.render("Continue", True, (0, 0, 0))
                    btn_rect = btn_text.get_rect(center=continue_btn.center)
                    scr.blit(btn_text, btn_rect)

                    pygame.display.update()

                    # Wait for button click
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                if continue_btn.collidepoint(event.pos):
                                    waiting = False

                    # Go to summary screen
                    pygame.quit()
                    os.system(f"{sys.executable} footballquiz_summary.py {score} 0")
                    sys.exit()

                q_no += 1
                if q_no >= QUESTION_TOTAL:
                    save_score(score)

                    # Create a gradient background for the transition screen
                    transition_bg = pygame.Surface((WIDTH, HEIGHT))
                    for y in range(HEIGHT):
                        # Create a gradient from dark blue to light blue
                        color = (
                            int(0 + (100) * y / HEIGHT),
                            int(50 + (130) * y / HEIGHT),
                            int(150 + (50) * y / HEIGHT)
                        )
                        pygame.draw.line(transition_bg, color, (0, y), (WIDTH, y))

                    # Show transition screen with gradient background
                    scr.blit(transition_bg, (0, 0))

                    # Create a fancy box for the title
                    msg_text = fBig.render("All Questions Complete!", True, (255, 215, 0))
                    msg_rect = msg_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))

                    # Draw a gold box around the title
                    pygame.draw.rect(scr, (255, 215, 0),
                                     (msg_rect.left - 20, msg_rect.top - 10,
                                      msg_rect.width + 40, msg_rect.height + 20),
                                     border_radius=15)
                    pygame.draw.rect(scr, (0, 0, 0),
                                     (msg_rect.left - 20, msg_rect.top - 10,
                                      msg_rect.width + 40, msg_rect.height + 20),
                                     width=3, border_radius=15)

                    scr.blit(msg_text, msg_rect)

                    # Draw "Continue to Summary" button
                    continue_btn = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 60)
                    pygame.draw.rect(scr, (0, 200, 0), continue_btn, border_radius=10)
                    pygame.draw.rect(scr, (0, 0, 0), continue_btn, 2, border_radius=10)

                    btn_text = fMid.render("Continue", True, (0, 0, 0))
                    btn_rect = btn_text.get_rect(center=continue_btn.center)
                    scr.blit(btn_text, btn_rect)

                    pygame.display.update()

                    # Wait for button click
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                if continue_btn.collidepoint(event.pos):
                                    waiting = False

                    # Go to summary screen
                    pygame.quit()
                    os.system(f"{sys.executable} footballquiz_summary.py {score} 1")
                    sys.exit()

                # Reset for next question
                question, answer = make_question()
                typed = ""
                q_start = pygame.time.get_ticks()
                vx, vy = reset_ball()
                shot_res = None

        # Draw the game screen
        draw_pitch()
        pygame.draw.rect(scr, (50, 50, 220), player)
        pygame.draw.ellipse(scr, (250, 250, 250), ball)

        # HUD
        hud_rect = pygame.Rect(10, 10, 180, 40)
        pygame.draw.rect(scr, (0, 0, 0), hud_rect, border_radius=6)
        pygame.draw.rect(scr, (255, 255, 255), hud_rect, 2, border_radius=6)
        left = max(0, QUESTION_TIME - int((pygame.time.get_ticks() - q_start) / 1000))
        scr.blit(fSm.render(f"G:{score}   T:{left}s", True, (255, 255, 255)), (20, 18))

        # Question
        scr.blit(fMid.render(question, True, (0, 0, 0)),
                 fMid.render(question, True, (0, 0, 0)).get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))

        # Input box
        input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 10, 200, 50)
        pygame.draw.rect(scr, (255, 255, 255), input_box, border_radius=10)
        pygame.draw.rect(scr, (0, 0, 180), input_box, 2, border_radius=10)
        scr.blit(fMid.render(typed, True, (0, 0, 180)),
                 fMid.render(typed, True, (0, 0, 180)).get_rect(center=input_box.center))

        # Tip
        if tip and pygame.time.get_ticks() - tipT < TIP_MS:
            col = (255, 215, 0) if tip == "GOAL !" else (255, 50, 50)
            scr.blit(fBig.render(tip, True, col),
                     fBig.render(tip, True, col).get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120)))
        elif tip:
            tip = ""

        pygame.display.update()


# Main function
def main():
    # Start the game directly
    main_game()


# Run the game
if __name__ == "__main__":
    main()