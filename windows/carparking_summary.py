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

    # Get the star rating from game data
    stars = game_data['stars']

    # Performance message based on stars
    if stars == 3:
        performance_msg = "Perfect Solution!"
    elif stars == 2:
        performance_msg = "Great job!"
    elif stars == 1:
        performance_msg = "Good effort!"
    else:
        performance_msg = "Puzzle solved!"

    # Define variables for buttons and layout
    y_pos = 300  # Starting position for statistics text
    line_height = 35  # Spacing between lines of text

    button_width = 180  # Made button wider for the longer text
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
                        # Save game data for final summary
                        save_game_data(game_data)

                        # Run the final summary script
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        os.system(f"{sys.executable} final_summary.py")
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
        title_text = big_font.render("Puzzle Complete!", True, WHITE)
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
        total_stars_width = 3 * star_width + (3 - 1) * star_spacing  # Always draw 3 stars total
        start_x = (SCREEN_WIDTH - total_stars_width) // 2

        for i in range(3):
            # Draw a simple star shape
            star_x = start_x + i * (star_width + star_spacing)

            # Decide if star should be filled or empty
            star_color = GOLD if i < stars else (200, 200, 200)  # Gold for filled, gray for empty

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

            pygame.draw.polygon(screen, star_color, points)
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

        # Your Moves
        moves_text = font.render(f"Your Moves: {game_data['moves']}", True, BLACK)
        screen.blit(moves_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # Perfect Moves
        perfect_text = font.render(f"Perfect Solution: {game_data['perfect_moves']} moves", True, BLACK)
        screen.blit(perfect_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # Efficiency
        if game_data['perfect_moves'] > 0:
            efficiency = int((game_data['perfect_moves'] / max(1, game_data['moves'])) * 100)
            efficiency_text = font.render(f"Efficiency: {efficiency}%", True, BLACK)
            screen.blit(efficiency_text, (summary_box.left + 30, y_pos))
            y_pos += line_height

        # Star Rating
        star_rating_text = font.render(f"Star Rating: {stars}/3", True, BLACK)
        screen.blit(star_rating_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # Difficulty
        difficulty_text = font.render("Difficulty: Easy", True, BLACK)
        screen.blit(difficulty_text, (summary_box.left + 30, y_pos))

        # Continue button
        continue_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                                    button_y, button_width, button_height)
        pygame.draw.rect(screen, GREEN, continue_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, continue_rect, width=2, border_radius=10)

        # Changed button text to indicate this leads to final summary
        continue_text = font.render("View Final Results", True, BLACK)
        continue_text_rect = continue_text.get_rect(center=continue_rect.center)
        screen.blit(continue_text, continue_text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return action


def save_game_data(game_data):
    """
    Save game data for final summary

    Parameters:
    game_data (dict): Dictionary containing game statistics
    """
    try:
        # Save the data to a file for the final summary to read
        # We keep the original carparking_data.txt file but include more data
        with open("carparking_data.txt", "w") as f:
            f.write(f"{game_data['moves']}\n")
            f.write(f"{game_data['stars']}\n")
            f.write(f"{game_data['perfect_moves']}\n")
            if game_data['perfect_moves'] > 0:
                efficiency = int((game_data['perfect_moves'] / max(1, game_data['moves'])) * 100)
                f.write(f"{efficiency}\n")
            else:
                f.write("0\n")

        print("Successfully saved Car Parking Puzzle data for final summary")
    except Exception as e:
        print(f"Error saving game data: {e}")


# If this file is run directly, show a summary screen with data from the game
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Car Parking Puzzle - Summary")

    # Try to read game data from file
    try:
        with open("carparking_data.txt", "r") as f:
            lines = f.readlines()
            moves = int(lines[0].strip())
            stars = int(lines[1].strip())
            perfect_moves = int(lines[2].strip())
    except:
        # Use default values if file cannot be read
        moves = 8
        stars = 1
        perfect_moves = 4
        print("Could not read game data from file. Using default values.")

    # Prepare game data
    game_data = {
        'moves': moves,
        'stars': stars,
        'perfect_moves': perfect_moves
    }

    action = show_summary(screen, game_data)
    print(f"Action returned: {action}")

    # Stop music before quitting
    if music_loaded:
        pygame.mixer.music.stop()

    # Action handling is done within the event loop
    pygame.quit()
    sys.exit()