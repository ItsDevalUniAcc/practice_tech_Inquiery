import pygame
import sys
import os
import json
import pathlib

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
SCORE_FILE = "highscores.json"

# Initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Football Quiz - Summary")
clock = pygame.time.Clock()

# Fonts
big_font = pygame.font.SysFont('Arial', 48, bold=True)
medium_font = pygame.font.SysFont('Arial', 32)
font = pygame.font.SysFont('Arial', 24)

# Try to load background music
try:
    pygame.mixer.music.load("memorymath_fireworks.mp3")
    pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
    music_loaded = True
    print("Loaded background music for summary screen")
except Exception as e:
    print(f"Warning: Could not initialize music for summary screen. Error: {e}")
    music_loaded = False


# Load scores function
def load_scores(limit=5):
    if pathlib.Path(SCORE_FILE).exists():
        with open(SCORE_FILE) as f:
            return json.load(f)[:limit]
    return []


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

    # Calculate star rating based on score
    total_goals = game_data['score']
    total_questions = game_data['total_questions']
    success = game_data['success']

    if total_goals >= total_questions:  # All questions correct
        stars = 5
        performance_msg = "Outstanding! Perfect score!"
    elif total_goals >= total_questions * 0.8:  # 80%+ correct
        stars = 4
        performance_msg = "Excellent shooting!"
    elif total_goals >= total_questions * 0.6:  # 60%+ correct
        stars = 3
        performance_msg = "Good job!"
    elif total_goals >= total_questions * 0.4:  # 40%+ correct
        stars = 2
        performance_msg = "Nice try!"
    else:  # Less than 40% correct
        stars = 1
        performance_msg = "Keep practicing!"

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
                        # Save game data for final summary
                        save_game_data(game_data)

                        # Launch the next game
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        os.system(f"{sys.executable} carparking_instructions.py")  # Assuming this is the next game
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
        title_text = big_font.render("Football Quiz Complete!", True, WHITE)
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

        # Goals/Score
        goals_text = font.render(f"Goals Scored: {total_goals}/{total_questions}", True, BLACK)
        screen.blit(goals_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # Completion Status
        completion_status = "Completed!" if success else "Incomplete"
        completion_text = font.render(f"Game Status: {completion_status}", True, BLACK)
        screen.blit(completion_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # Accuracy
        accuracy = int((total_goals / total_questions) * 100) if total_questions > 0 else 0
        accuracy_text = font.render(f"Accuracy: {accuracy}%", True, BLACK)
        screen.blit(accuracy_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # Star Rating
        star_text = font.render(f"Star Rating: {stars}/5", True, BLACK)
        screen.blit(star_text, (summary_box.left + 30, y_pos))
        y_pos += line_height

        # High Score info
        high_scores = load_scores()
        if high_scores:
            high_score = high_scores[0]
            high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
            screen.blit(high_score_text, (summary_box.left + 30, y_pos))

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
    Save game data for final summary

    Parameters:
    game_data (dict): Dictionary containing game statistics
    """
    try:
        # Save to football quiz specific score file
        with open("football_quiz_score.txt", "w") as f:
            f.write(f"{game_data['score']}")

        # Save more detailed information
        with open("football_quiz_data.txt", "w") as f:
            f.write(f"{game_data['score']}\n")
            f.write(f"{game_data['total_questions']}\n")
            f.write(f"{'1' if game_data['success'] else '0'}\n")
            accuracy = int((game_data['score'] / game_data['total_questions']) * 100) if game_data[
                                                                                             'total_questions'] > 0 else 0
            f.write(f"{accuracy}\n")

        print("Successfully saved Football Quiz game data for final summary")
    except Exception as e:
        print(f"Error saving game data: {e}")


# If this file is run directly, show a summary screen with data from the game
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Football Quiz - Summary")

    # Get score and success from command line arguments
    score = 0
    success = False

    if len(sys.argv) >= 3:
        try:
            score = int(sys.argv[1])
            success = sys.argv[2] == '1'
        except:
            # Use default values if parsing fails
            print("Could not parse command line arguments, using defaults")

    # Prepare game data
    game_data = {
        'score': score,
        'total_questions': 8,  # Total number of questions in the quiz
        'success': success
    }

    action = show_summary(screen, game_data)
    print(f"Action returned: {action}")

    # Stop music before quitting
    if music_loaded:
        pygame.mixer.music.stop()

    # Action handling is done within the event loop
    pygame.quit()
    sys.exit()