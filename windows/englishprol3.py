import pygame
import random
import sys
import os
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 50, 150)
LIGHT_BLUE = (100, 180, 255)
SOFT_BLUE = (80, 130, 200)
DEEP_BLUE = (60, 100, 180)
LIGHT_GREY = (230, 230, 230)
DARK_GREY = (180, 180, 180)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("English Pro - Level 3")

font = pygame.font.SysFont('Arial', 48)
small_font = pygame.font.SysFont('Arial', 36)

# Create a gradient background similar to your other games
background_img = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    # Create a gradient from dark blue to light blue
    color = (
        int(DARK_BLUE[0] + (LIGHT_BLUE[0] - DARK_BLUE[0]) * y / HEIGHT),
        int(DARK_BLUE[1] + (LIGHT_BLUE[1] - DARK_BLUE[1]) * y / HEIGHT),
        int(DARK_BLUE[2] + (LIGHT_BLUE[2] - DARK_BLUE[2]) * y / HEIGHT)
    )
    pygame.draw.line(background_img, color, (0, y), (WIDTH, y))

# Level 3 has even longer and more complex words
words = [
    "planet", "language", "science", "weather", "keyboard", "volcano", "dinosaur", "electric", "library", "history",
    "gravity", "triangle", "recycle", "magnet", "calendar", "adventure", "explorer", "strategy", "invention", "machine"
]


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def create_modern_button(text, x, y, width, height, active=False):
    mouse = pygame.mouse.get_pos()
    hovered = x + width > mouse[0] > x and y + height > mouse[1] > y

    base_color = DEEP_BLUE if active else LIGHT_GREY
    hover_color = SOFT_BLUE if active else DARK_GREY
    draw_color = hover_color if hovered else base_color

    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, draw_color, button_rect, border_radius=12)
    pygame.draw.rect(screen, BLACK, button_rect, width=2, border_radius=12)
    draw_text(text, small_font, BLACK, screen, x + width // 2, y + height // 2)

    return button_rect, hovered


def playing_game_with_boxes(puzzle_word, correct_word, title):
    input_text = ""
    while True:
        screen.blit(background_img, (0, 0))

        # Draw a title box
        title_box = pygame.Rect(WIDTH // 2 - 200, 20, 400, 60)
        pygame.draw.rect(screen, WHITE, title_box, border_radius=10)
        pygame.draw.rect(screen, BLACK, title_box, width=2, border_radius=10)
        draw_text(title, font, DARK_BLUE, screen, WIDTH // 2, 50)

        box_width = 60
        box_height = 70
        spacing = 15
        total_width = len(correct_word) * (box_width + spacing)
        start_x = WIDTH // 2 - total_width // 2

        for i, char in enumerate(puzzle_word):
            rect_x = start_x + i * (box_width + spacing)
            rect_y = 150
            box_rect = pygame.Rect(rect_x, rect_y, box_width, box_height)
            pygame.draw.rect(screen, WHITE, box_rect, border_radius=10)
            pygame.draw.rect(screen, DARK_BLUE, box_rect, width=4, border_radius=10)  # border

            if char != '_':
                draw_text(char.upper(), small_font, DARK_BLUE, screen, rect_x + box_width // 2,
                          rect_y + box_height // 2)

        # Create input box
        input_box = pygame.Rect(WIDTH // 2 - 200, 350, 400, 60)
        pygame.draw.rect(screen, WHITE, input_box, border_radius=10)
        pygame.draw.rect(screen, BLACK, input_box, width=2, border_radius=10)

        draw_text("Enter your response:", small_font, BLACK, screen, WIDTH // 2, 300)
        draw_text(input_text, small_font, BLACK, screen, WIDTH // 2, 350 + 30)

        # Create submit button
        submit_button, submit_hovered = create_modern_button("Submit", WIDTH // 2 - 60, 450, 120, 50, active=True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text.lower() == correct_word
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and submit_hovered:  # Left click on submit button
                    return input_text.lower() == correct_word


def memory_game(word):
    screen.blit(background_img, (0, 0))

    # Create a fancy box for the word to memorize
    word_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 40, 300, 80)
    pygame.draw.rect(screen, WHITE, word_box, border_radius=15)
    pygame.draw.rect(screen, DARK_BLUE, word_box, width=3, border_radius=15)

    draw_text("Memorize:", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 60)
    draw_text(word, font, DARK_BLUE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()

    # For level 3, reduce the memorization time to increase difficulty
    pygame.time.delay(2000)  # Only 2 seconds to memorize instead of 3

    screen.blit(background_img, (0, 0))
    draw_text("Now type the word from memory!", small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()
    pygame.time.delay(1000)

    return memory_input_phase(word)


def memory_input_phase(correct_word):
    input_text = ""
    while True:
        screen.blit(background_img, (0, 0))

        # Draw a title box
        title_box = pygame.Rect(WIDTH // 2 - 200, 20, 400, 60)
        pygame.draw.rect(screen, WHITE, title_box, border_radius=10)
        pygame.draw.rect(screen, BLACK, title_box, width=2, border_radius=10)
        draw_text("Memory Challenge", font, DARK_BLUE, screen, WIDTH // 2, 50)

        # Create input box
        input_box = pygame.Rect(WIDTH // 2 - 200, 350, 400, 60)
        pygame.draw.rect(screen, WHITE, input_box, border_radius=10)
        pygame.draw.rect(screen, BLACK, input_box, width=2, border_radius=10)

        draw_text("Enter the word:", small_font, WHITE, screen, WIDTH // 2, 300)
        draw_text(input_text, small_font, BLACK, screen, WIDTH // 2, 350 + 30)

        # Create submit button
        submit_button, submit_hovered = create_modern_button("Submit", WIDTH // 2 - 60, 450, 120, 50, active=True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text.lower() == correct_word
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and submit_hovered:  # Left click on submit button
                    return input_text.lower() == correct_word


def main():
    # Randomly select words for the game
    all_words = random.sample(words, 10)
    word_completion_words = all_words[:5]
    memory_words = all_words[5:]
    score = 0
    start_time = time.time()

    # Phase 1: Word Completion
    completion_score = 0
    for word in word_completion_words:
        # For level 3, increase the challenge by removing most letters
        missing_indices = random.sample(range(len(word)), k=max(3, len(word) // 2 + 1))
        display_word = list(word)
        for idx in missing_indices:
            display_word[idx] = '_'
        display_word = ''.join(display_word)
        if playing_game_with_boxes(display_word, word, "Word Completion"):
            score += 1
            completion_score += 1

    # Phase 2: Memory Game
    memory_score = 0
    for word in memory_words:
        if memory_game(word):
            score += 1
            memory_score += 1

    # Calculate time played
    end_time = time.time()
    total_time = round(end_time - start_time, 2)

    # Save game data for summary screen
    try:
        with open("englishpro_score.txt", "w") as f:
            f.write(str(score))

        with open("englishpro_data.txt", "w") as f:
            f.write(f"{score}\n")  # Score
            f.write(f"{total_time}\n")  # Time played
            f.write(f"{completion_score}\n")  # Word completion score
            f.write(f"{memory_score}\n")  # Memory game score
            f.write("3\n")  # Level number (level 3)
    except:
        print("Could not save game data to file")

    # Show simple message before going to summary screen
    screen.blit(background_img, (0, 0))

    # Create a fancy message box
    message_text = f"Game Complete!"
    message_font = font.render(message_text, True, WHITE)
    message_rect = message_font.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    pygame.draw.rect(screen, DEEP_BLUE,
                     (message_rect.left - 20, message_rect.top - 10,
                      message_rect.width + 40, message_rect.height + 20),
                     border_radius=15)
    pygame.draw.rect(screen, BLACK,
                     (message_rect.left - 20, message_rect.top - 10,
                      message_rect.width + 40, message_rect.height + 20),
                     width=3, border_radius=15)

    screen.blit(message_font, message_rect)

    # Create a wider continue button with better text positioning
    button_width = 200
    button_height = 60
    continue_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 50, button_width, button_height)
    pygame.draw.rect(screen, GREEN, continue_button, border_radius=10)
    pygame.draw.rect(screen, BLACK, continue_button, width=2, border_radius=10)

    # Create button text
    button_text = small_font.render("Continue", True, BLACK)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 + button_height // 2))
    screen.blit(button_text, button_rect)

    # Check if mouse is hovering over the button
    mouse_pos = pygame.mouse.get_pos()
    continue_hovered = continue_button.collidepoint(mouse_pos)

    pygame.display.update()

    # Wait for continue button click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and continue_button.collidepoint(event.pos):  # Left click on continue button
                    waiting = False
                    pygame.quit()
                    os.system(f"{sys.executable} englishpro_summary.py")
                    sys.exit()

        # Update hover state for button (change button color on hover)
        mouse_pos = pygame.mouse.get_pos()
        if continue_button.collidepoint(mouse_pos):
            if not continue_hovered:
                # Change to hover state
                continue_hovered = True
                pygame.draw.rect(screen, (100, 255, 100), continue_button, border_radius=10)
                pygame.draw.rect(screen, BLACK, continue_button, width=2, border_radius=10)
                screen.blit(button_text, button_rect)
                pygame.display.update()
        elif continue_hovered:
            # Change back to normal state
            continue_hovered = False
            pygame.draw.rect(screen, GREEN, continue_button, border_radius=10)
            pygame.draw.rect(screen, BLACK, continue_button, width=2, border_radius=10)
            screen.blit(button_text, button_rect)
            pygame.display.update()


# Run the game
if __name__ == "__main__":
    main()