import pygame
import sys
import os

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 180, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
DARK_BLUE = (0, 50, 150)
SCROLL_BAR_COLOR = (150, 150, 150)
SCROLL_BUTTON_COLOR = (100, 100, 100)

# Try to load background music
try:
    pygame.mixer.init()
    if os.path.exists("memorymath_fireworks.mp3"):
        pygame.mixer.music.load("memorymath_fireworks.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
        music_loaded = True
        print("Loaded background music for summary screen")
    else:
        music_loaded = False
        print("Could not find memorymath_fireworks.mp3 for summary screen")
except Exception as e:
    print(f"Warning: Could not initialize music for summary screen. Error: {e}")
    music_loaded = False


def show_summary(screen, game_data):
    """
    Display the game summary screen

    Parameters:
    screen (pygame.Surface): The main game display surface
    game_data (dict): Dictionary containing game statistics

    Returns:
    str: Action to take ('restart', 'quit', or None)
    """
    # Start background music if available
    if music_loaded:
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    # Prepare fonts
    big_font = pygame.font.SysFont('Arial', 48, bold=True)
    medium_font = pygame.font.SysFont('Arial', 32)
    font = pygame.font.SysFont('Arial', 24)

    # Calculate star rating based on score
    if game_data['score'] >= 50:
        stars = 5
    elif game_data['score'] >= 40:
        stars = 4
    elif game_data['score'] >= 30:
        stars = 3
    elif game_data['score'] >= 20:
        stars = 2
    else:
        stars = 1

    # Performance message based on stars
    if stars >= 4:
        performance_msg = "Outstanding Work!"
    elif stars == 3:
        performance_msg = "Great Effort!"
    else:
        performance_msg = "Keep Practicing!"

    # Define variables for buttons and layout
    y_pos = 300  # Starting position for statistics text
    line_height = 35  # Spacing between lines of text

    button_width = 150
    button_height = 50
    button_y = 530  # Moved button down a bit

    # Define button rectangle - only one button now
    continue_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                                button_y, button_width, button_height)

    # Main loop for the summary screen
    summary_running = True
    action = None

    while summary_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            # Check for button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if Continue button is clicked
                    if continue_rect.collidepoint(mouse_pos):
                        # Save detailed game data for final summary
                        save_game_data(game_data)

                        # Simply run next game and quit
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        os.system(f"{sys.executable} englishpro_instructions.py")
                        sys.exit()

        # Draw background with gradient
        for y in range(SCREEN_HEIGHT):
            # Create a gradient from dark blue to light blue
            color = (
                int(DARK_BLUE[0] + (LIGHT_BLUE[0] - DARK_BLUE[0]) * y / SCREEN_HEIGHT),
                int(DARK_BLUE[1] + (LIGHT_BLUE[1] - DARK_BLUE[1]) * y / SCREEN_HEIGHT),
                int(DARK_BLUE[2] + (LIGHT_BLUE[2] - DARK_BLUE[2]) * y / SCREEN_HEIGHT)
            )
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Title
        title_text = big_font.render("Word Builder Complete!", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 70))

        # Add a fancy box around the title
        pygame.draw.rect(screen, GOLD,
                         (title_rect.left - 20, title_rect.top - 10,
                          title_rect.width + 40, title_rect.height + 20),
                         border_radius=15)
        pygame.draw.rect(screen, BLACK,
                         (title_rect.left - 20, title_rect.top - 10,
                          title_rect.width + 40, title_rect.height + 20),
                         width=3, border_radius=15)

        screen.blit(title_text, title_rect)

        # Performance message
        performance_text = medium_font.render(performance_msg, True, WHITE)
        screen.blit(performance_text,
                    (SCREEN_WIDTH // 2 - performance_text.get_width() // 2, 130))

        # Star rating
        star_width = 40
        star_spacing = 10
        total_stars_width = stars * star_width + (stars - 1) * star_spacing
        start_x = (SCREEN_WIDTH - total_stars_width) // 2

        for i in range(stars):
            # Draw a simple star shape
            star_x = start_x + i * (star_width + star_spacing)

            # Draw a gold star
            points = []
            for j in range(5):
                # Outer points of the star
                angle = j * 2 * 3.14159 / 5 - 3.14159 / 2
                points.append((star_x + star_width // 2 + int(
                    star_width // 2 * 0.9 * pygame.math.Vector2(1, 0).rotate(angle * 180 / 3.14159).x),
                               170 + star_width // 2 + int(
                                   star_width // 2 * 0.9 * pygame.math.Vector2(1, 0).rotate(angle * 180 / 3.14159).y)))

                # Inner points of the star
                angle += 3.14159 / 5
                points.append((star_x + star_width // 2 + int(
                    star_width // 2 * 0.4 * pygame.math.Vector2(1, 0).rotate(angle * 180 / 3.14159).x),
                               170 + star_width // 2 + int(
                                   star_width // 2 * 0.4 * pygame.math.Vector2(1, 0).rotate(angle * 180 / 3.14159).y)))

            pygame.draw.polygon(screen, GOLD, points)
            pygame.draw.polygon(screen, BLACK, points, width=1)

        # Game summary box
        summary_box = pygame.Rect(SCREEN_WIDTH // 2 - 180, 230, 360, 280)
        pygame.draw.rect(screen, WHITE, summary_box, border_radius=10)
        pygame.draw.rect(screen, BLACK, summary_box, width=2, border_radius=10)

        # Summary heading
        summary_heading = medium_font.render("Game Summary", True, BLACK)
        screen.blit(summary_heading,
                    (SCREEN_WIDTH // 2 - summary_heading.get_width() // 2, 240))

        # Draw horizontal line under heading
        pygame.draw.line(screen, BLACK,
                         (summary_box.left + 20, 280),
                         (summary_box.right - 20, 280), 2)

        # Reset y_pos for statistics
        y_pos = 300

        # Final score
        final_score_text = font.render(f"Final Score: {game_data['score']}", True, BLACK)
        screen.blit(final_score_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # Words solved
        words_text = font.render(f"Words Solved: {game_data['words_solved']}", True, BLACK)
        screen.blit(words_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # Hints used
        hints_text = font.render(f"Hints Used: {'Yes' if game_data['hints_used'] else 'No'}", True, BLACK)
        screen.blit(hints_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # Time taken
        time_text = font.render(f"Time Played: {game_data['time']} seconds", True, BLACK)
        screen.blit(time_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # Bonus info
        if 'bonus' in game_data:
            bonus_text = font.render(f"Bonus Points: {game_data['bonus']}", True, BLACK)
            screen.blit(bonus_text, (summary_box.left + 30, y_pos))
            y_pos += line_height

        # Continue button
        continue_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                                    button_y, button_width, button_height)
        pygame.draw.rect(screen, GREEN, continue_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, continue_rect, width=2, border_radius=10)

        continue_text = font.render("Continue", True, BLACK)
        continue_text_rect = continue_text.get_rect(center=continue_rect.center)
        screen.blit(continue_text, continue_text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return action


def save_game_data(game_data):
    """
    Save detailed game data to a file for the final summary

    Parameters:
    game_data (dict): Dictionary containing game statistics
    """
    try:
        # Create a more detailed data file for the final summary to use
        with open("word_builder_data.txt", "w") as f:
            f.write(f"{game_data['words_solved']}\n")
            f.write(f"{'true' if game_data['hints_used'] else 'false'}\n")
            f.write(f"{game_data['time']}\n")
            if 'bonus' in game_data:
                f.write(f"{game_data['bonus']}\n")
            else:
                f.write("0\n")

        # Make sure the score is also saved
        with open("word_builder_score.txt", "w") as f:
            f.write(f"{game_data['score']}")

        print("Successfully saved Word Builder game data for final summary")
    except Exception as e:
        print(f"Error saving game data: {e}")


# If this file is run directly, show a summary screen with data from the game
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Word Builder - Summary")

    # Try to read score and other game data from files
    try:
        with open("word_builder_score.txt", "r") as f:
            score = int(f.read().strip())

        # Try to read additional game data
        words_solved = 0
        hints_used = False
        time_played = 120

        try:
            with open("word_builder_data.txt", "r") as f:
                lines = f.readlines()
                if len(lines) >= 1:
                    words_solved = int(lines[0].strip())
                if len(lines) >= 2:
                    hints_used = lines[1].strip().lower() == "true"
                if len(lines) >= 3:
                    time_played = int(lines[2].strip())
        except:
            # If we can't read the detailed data, estimate from score
            words_solved = score // 10 + score % 10 // 5  # Estimate based on score (10 pts per word, 5 with hint)
            hints_used = (score % 10 > 0)  # If score is not divisible by 10, assume hints were used
            print("Could not read detailed game data. Using estimates based on score.")

    except:
        # Use default score if file cannot be read
        score = 30
        words_solved = 3
        hints_used = False
        time_played = 120
        print("Could not read score from file. Using default score.")

    # Prepare game data
    game_data = {
        'score': score,
        'words_solved': words_solved,
        'hints_used': hints_used,
        'time': time_played,
        'bonus': 0  # No bonus by default
    }

    action = show_summary(screen, game_data)
    print(f"Action returned: {action}")

    # Stop music before quitting
    if music_loaded:
        pygame.mixer.music.stop()

    # Action handling is done within the event loop
    pygame.quit()
    sys.exit()