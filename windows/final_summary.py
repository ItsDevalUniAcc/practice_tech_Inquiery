import pygame
import sys
import os
import json
import pathlib
from data_manager import DataManager
import matplotlib.pyplot as plt


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
RED = (200, 0, 0)

# Try to load background music
try:
    pygame.mixer.init()
    if os.path.exists("memorymath_fireworks.mp3"):
        pygame.mixer.music.load("memorymath_fireworks.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
        music_loaded = True
        print("Loaded background music for final summary screen")
    else:
        music_loaded = False
        print("Could not find memorymath_fireworks.mp3 for final summary screen")
except Exception as e:
    print(f"Warning: Could not initialize music for final summary screen. Error: {e}")
    music_loaded = False
import matplotlib.pyplot as plt

def plot_player_progress(player_name, dm):
    try:
        history = dm.get_player_history(player_name)
        if not history:
            print("No history found to plot.")
            return

        dates = [row['timestamp'] for row in history]
        scores = [row['score'] for row in history]
        modes = [row['mode'] for row in history]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, scores, marker='o', linestyle='-')
        plt.title(f"{player_name}'s Score History")
        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Score")
        plt.tight_layout()
        plt.grid(True)
        plt.savefig("player_progress.png")
        plt.close()
        print("Graph saved as player_progress.png")

    except Exception as e:
        print("Error plotting progress:", e)

def get_current_player():
    """Retrieve the current player's name from storage."""
    try:
        with open("current_student.txt", "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Could not read player name: {e}")
        return "Guest"
    
def load_game_scores():
    """
    Load scores and session details from all games.
    Returns a dictionary with game data including level, duration, accuracy, and mode.
    """
    scores = {
        'game1': {'score': 0, 'level': 1, 'duration': 60.0, 'accuracy': None, 'mode': 'Memory Math'},
        'game2': {'score': 0, 'level': 1, 'duration': 60.0, 'accuracy': None, 'mode': 'Word Builder'},
        'game3': {'score': 0, 'level': 1, 'duration': 60.0, 'accuracy': None, 'mode': 'English Pro'},
        'game4': {'score': 0, 'level': 1, 'duration': 60.0, 'accuracy': None, 'mode': 'Football Quiz'},
        'game5': {'score': 0, 'level': 1, 'duration': 60.0, 'accuracy': None, 'mode': 'Car Parking Puzzle'},
    }

    # Game 1 - Memory Math
    try:
        with open("memorymath_data.txt", "r") as f:
            lines = f.readlines()
            if lines:
                scores['game1']['score'] = int(lines[0].strip())
                if len(lines) > 1: scores['game1']['level'] = int(lines[1].strip())
                if len(lines) > 2: scores['game1']['duration'] = float(lines[2].strip())
                if len(lines) > 3: scores['game1']['accuracy'] = float(lines[3].strip())
    except Exception as e:
        print(f"Memory Math data error: {e}")

    # Game 2 - Word Builder
    try:
        
        
        with open("word_builder_score.txt", "r") as f:
            lines = f.readlines()
            if lines:
                scores['game2']['score'] = int(lines[0].strip())
                if len(lines) > 1: scores['game2']['level'] = int(lines[1].strip())
                if len(lines) > 2: scores['game2']['duration'] = float(lines[2].strip())
                if len(lines) > 3: scores['game2']['accuracy'] = float(lines[3].strip())
    except Exception as e:
        print(f"Word Builder error: {e}")

    # Game 3 - English Pro
    try:
        with open("englishpro_score.txt", "r") as f:
            lines = f.readlines()
            if lines:
                scores['game3']['score'] = int(lines[0].strip())
                if len(lines) > 1: scores['game3']['level'] = int(lines[1].strip())
                if len(lines) > 2: scores['game3']['duration'] = float(lines[2].strip())
                if len(lines) > 3: scores['game3']['accuracy'] = float(lines[3].strip())
    except Exception as e:
        print(f"English Pro error: {e}")

    # Game 4 - Football Quiz
    try:
        if len(sys.argv) >= 2:
            scores['game4']['score'] = int(sys.argv[1])
        else:
            files_to_try = ["football_quiz_score.txt", "football_score.txt", "quiz_score.txt"]
            for file in files_to_try:
                try:
                    with open(file, "r") as f:
                        scores['game4']['score'] = int(f.read().strip())
                        break
                except:
                    continue
        with open("englishpro_score.txt", "r") as f:
            lines = f.readlines()
            if lines:
                scores['game3']['score'] = int(lines[0].strip())
                if len(lines) > 1: scores['game4']['level'] = int(lines[1].strip())
                if len(lines) > 2: scores['game4']['duration'] = float(lines[2].strip())
                if len(lines) > 3: scores['game4']['accuracy'] = float(lines[3].strip())
    except Exception as e:
        print(f"Football Quiz error: {e}")

    # Game 5 - Car Parking Puzzle
    try:
        with open("carparking_data.txt", "r") as f:
            lines = f.readlines()
            if len(lines) > 1:
                stars = int(lines[1].strip())
                scores['game5']['score'] = stars * 10
                scores['game5']['level'] = stars  # Use stars as level
        with open("carparking_data.txt", "r") as f:
            lines = f.readlines()
            if lines:
                scores['game5']['score'] = int(lines[0].strip())
                if len(lines) > 1: scores['game5']['level'] = int(lines[1].strip())
                if len(lines) > 2: scores['game5']['duration'] = float(lines[2].strip())
                if len(lines) > 3: scores['game5']['accuracy'] = float(lines[3].strip())
    except Exception as e:
        print(f"Car Parking error: {e}")

    return scores


def calculate_level_status(total_score):
    """
    Calculate level status based on total score

    Parameters:
    total_score (int): Total score earned across all games

    Returns:
    tuple: (status, motivational_message)
    """
    # Maximum possible score estimate
    estimated_max_score = 250  # Approximate maximum possible
    percentage = (total_score / estimated_max_score) * 100

    if percentage >= 80:  # Very high score
        return "ADVANCED", "Amazing work! Your dedication is truly impressive!"
    elif percentage >= 60:  # Good score
        return "INTERMEDIATE", "Great progress! Keep challenging yourself!"
    elif percentage >= 40:  # Decent score
        return "BASIC", "You're on the right track! Keep practicing!"
    else:
        return "BEGINNER", "Every attempt makes you better. Don't give up!"


def show_final_summary(screen):
    """
    Display the final summary screen

    Parameters:
    screen (pygame.Surface): The main game display surface

    Returns:
    str: Action to take
    """
    # Start background music if available
    if music_loaded:
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    # Prepare fonts - REDUCED FONT SIZES
    big_font = pygame.font.SysFont('Arial', 44, bold=True)  # Reduced from 48
    medium_font = pygame.font.SysFont('Arial', 28, bold=True)  # Reduced from 32
    font = pygame.font.SysFont('Arial', 22)  # Reduced from 24
    small_font = pygame.font.SysFont('Arial', 18)  # For table content

    # Load scores from all games
    game_scores = load_game_scores()
    player_name = get_current_player()
    
    # Calculate total score
    total_score = sum(game['score'] for game in game_scores.values())
    # Get level status
    level_status, motivational_message = calculate_level_status(total_score)

    # Save each game's session data using DataManager
    dm = DataManager()
    for game_key in game_scores:
        data = game_scores[game_key]
        try:
            dm.save_session(
                player_name=player_name,
                score=data['score'],
                level=data['level'],
                duration=data['duration'],
                accuracy=data['accuracy'],
                mode=data['mode']
            )
        except Exception as e:
            print(f"Error saving session for {data['mode']}: {e}")

    # Fetch and print player stats (optional)
    stats = dm.get_stats(player_name=player_name)
    print("Player Stats:", stats)
    plot_player_progress(player_name, dm)


    # Define button variables
    button_width = 160
    button_height = 50
    button_spacing = 20
    button_y = 520

    # Define button rectangles - now 3 buttons
    rankings_rect = pygame.Rect(SCREEN_WIDTH // 2 - (button_width * 3 + button_spacing * 2) // 2,
                                button_y, button_width, button_height)

    main_menu_rect = pygame.Rect(rankings_rect.right + button_spacing,
                                 button_y, button_width, button_height)

    logout_rect = pygame.Rect(main_menu_rect.right + button_spacing,
                              button_y, button_width, button_height)

    # Main loop for the summary screen
    summary_running = True
    action = None

    while summary_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                summary_running = False
                action = "quit"
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    summary_running = False
                    action = "quit"
                    break
                elif event.key == pygame.K_RETURN:
                    summary_running = False
                    action = "main_menu"
                    break
                elif event.key == pygame.K_r:
                    summary_running = False
                    action = "rankings"
                    break
                elif event.key == pygame.K_l:
                    summary_running = False
                    action = "logout"
                    break

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if rankings_rect.collidepoint(mouse_pos):
                    action = "rankings"
                    summary_running = False
                elif main_menu_rect.collidepoint(mouse_pos):
                    action = "main_menu"
                    summary_running = False
                elif logout_rect.collidepoint(mouse_pos):
                    action = "logout"
                    summary_running = False


        # Draw background with gradient
        for y in range(SCREEN_HEIGHT):
            # Create a gradient from dark blue to light blue (simplified)
            color = (
                int(DARK_BLUE[0] + (LIGHT_BLUE[0] - DARK_BLUE[0]) * y / SCREEN_HEIGHT),
                int(DARK_BLUE[1] + (LIGHT_BLUE[1] - DARK_BLUE[1]) * y / SCREEN_HEIGHT),
                int(DARK_BLUE[2] + (LIGHT_BLUE[2] - DARK_BLUE[2]) * y / SCREEN_HEIGHT)
            )
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Level status in top right corner
        level_box = pygame.Rect(SCREEN_WIDTH - 180, 20, 160, 40)
        pygame.draw.rect(screen, WHITE, level_box, border_radius=10)
        pygame.draw.rect(screen, BLACK, level_box, width=2, border_radius=10)

        level_text = font.render(f"Level: {level_status}", True, BLACK)
        level_text_rect = level_text.get_rect(center=level_box.center)
        screen.blit(level_text, level_text_rect)

        # Title - positioned to not overlap with level box
        title_text = big_font.render("LEVEL COMPLETE", True, WHITE)
        # Center the title horizontally but shift it slightly left to avoid overlap
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2 - 40, 60))

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

        # Motivational message
        motivation_text = medium_font.render(motivational_message, True, WHITE)
        screen.blit(motivation_text,
                    (SCREEN_WIDTH // 2 - motivation_text.get_width() // 2, 130))

        # Game summary box - MADE TALLER to ensure content fits
        summary_box = pygame.Rect(150, 180, 500, 300)
        pygame.draw.rect(screen, WHITE, summary_box, border_radius=10)
        pygame.draw.rect(screen, BLACK, summary_box, width=2, border_radius=10)

        # Summary heading
        summary_heading = medium_font.render("Game Performance Summary", True, BLACK)
        summary_heading_rect = summary_heading.get_rect(
            center=(summary_box.left + summary_box.width // 2, 210))
        screen.blit(summary_heading, summary_heading_rect)

        # Draw horizontal line under heading
        pygame.draw.line(screen, BLACK,
                         (summary_box.left + 20, 235),
                         (summary_box.right - 20, 235), 2)

        # Game scores table - using smaller font and better spacing
        # Set positions relative to box edges with proper margins
        left_column_x = summary_box.left + 40  # Game names
        right_column_x = summary_box.right - 60  # Scores

        # Headers - Use smaller font
        game_header = small_font.render("Game", True, BLACK)
        score_header = small_font.render("Score", True, BLACK)

        screen.blit(game_header, (left_column_x, 250))
        screen.blit(score_header, (right_column_x - score_header.get_width(), 250))

        # Draw line under headers
        pygame.draw.line(screen, BLACK,
                         (summary_box.left + 20, 275),
                         (summary_box.right - 20, 275), 1)

        # Game names
        game_names = [
            "Memory Math",
            "Word Builder",
            "English Pro",
            "Football Quiz",
            "Car Parking Puzzle"
        ]

        # Draw game scores - USING SMALLER FONT for table content
        y_pos = 290
        line_height = 30  # Reduced line height

        for i, (game_key, game_name) in enumerate(zip(game_scores.keys(), game_names)):
            # Game name - left aligned
            game_text = small_font.render(game_name, True, BLACK)
            screen.blit(game_text, (left_column_x, y_pos))

            # Score - right aligned
            score_text = small_font.render(str(game_scores[game_key]['score']), True, BLACK)
            score_x = right_column_x - score_text.get_width()
            screen.blit(score_text, (score_x, y_pos))

            y_pos += line_height

        # Make sure we have enough space for total row
        # Ensure the separator line is well within the box
        sep_y = min(y_pos + 5, summary_box.bottom - 45)
        pygame.draw.line(screen, BLACK,
                         (summary_box.left + 20, sep_y),
                         (summary_box.right - 20, sep_y), 1)

        # Total row - ensure it stays within the summary box
        total_y = min(sep_y + 15, summary_box.bottom - 25)
        total_text = small_font.render("TOTAL", True, BLACK)
        screen.blit(total_text, (left_column_x, total_y))

        total_score_text = small_font.render(str(total_score), True, BLACK)
        total_score_x = right_column_x - total_score_text.get_width()
        screen.blit(total_score_text, (total_score_x, total_y))
        # # Top 5 Scores Section
        # leaderboard_y = summary_box.bottom + 10
        # leaderboard_title = small_font.render("Top 5 Scores Per Game", True, WHITE)
        # screen.blit(leaderboard_title, (SCREEN_WIDTH // 2 - leaderboard_title.get_width() // 2, leaderboard_y))

        # leaderboard_y += 30  # spacing

        # for game_key in game_scores:
        #     game_mode = game_scores[game_key]['mode']
        #     top_scores = dm.get_top_scores(limit=5, mode=game_mode)

        #     # Game title
        #     game_title = small_font.render(f"{game_mode}:", True, GOLD)
        #     screen.blit(game_title, (150, leaderboard_y))
        #     leaderboard_y += 20

        #     for row in top_scores:
        #         entry_text = small_font.render(f"{row['player_name']} - {row['score']}", True, WHITE)
        #         screen.blit(entry_text, (170, leaderboard_y))
        #         leaderboard_y += 20

        #     leaderboard_y += 10  # spacing between games

        # Draw buttons - now 3 buttons with different colors

        # Rankings button
        pygame.draw.rect(screen, BLUE, rankings_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, rankings_rect, width=2, border_radius=10)

        rankings_text = font.render("Rankings", True, WHITE)
        rankings_text_rect = rankings_text.get_rect(center=rankings_rect.center)
        screen.blit(rankings_text, rankings_text_rect)

        # Main Menu button
        pygame.draw.rect(screen, GREEN, main_menu_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, main_menu_rect, width=2, border_radius=10)

        main_menu_text = font.render("Main Menu", True, BLACK)
        main_menu_text_rect = main_menu_text.get_rect(center=main_menu_rect.center)
        screen.blit(main_menu_text, main_menu_text_rect)

        # Logout button
        pygame.draw.rect(screen, RED, logout_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, logout_rect, width=2, border_radius=10)

        logout_text = font.render("Logout", True, WHITE)
        logout_text_rect = logout_text.get_rect(center=logout_rect.center)
        screen.blit(logout_text, logout_text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
        
    # dm.export_to_csv("exported_sessions.csv")
    if music_loaded:
        pygame.mixer.music.stop()
    
    if action == "rankings":
        pygame.quit()
        os.system(f"{sys.executable} student_rankings.py")
        sys.exit()
    elif action == "main_menu":
        pygame.quit()
        os.system(f"{sys.executable} main_screen.py")
        sys.exit()
    elif action == "logout":
        pygame.quit()
        os.system(f"{sys.executable} login_screen.py")
        sys.exit()
    

    return action


# If this file is run directly, show the final summary screen
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Level Complete - Final Summary")

    action = show_final_summary(screen)
    print(f"Action returned: {action}")

    # Handle the action returned from the final summary screen
    if action == "quit":
        pygame.quit()
        sys.exit()