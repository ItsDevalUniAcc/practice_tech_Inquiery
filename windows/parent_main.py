import pygame
import sys
import os
import subprocess

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
LIGHT_BLUE = (100, 200, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
DARK_BLUE = (0, 50, 150)
GREEN = (50, 200, 50)
LIGHT_GREEN = (100, 255, 100)
PURPLE = (150, 50, 200)
LIGHT_PURPLE = (180, 100, 240)
ORANGE = (255, 150, 50)
LIGHT_ORANGE = (255, 180, 100)
YELLOW = (255, 230, 0)
GOLD = (255, 215, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MemoryMath - Parent Dashboard")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont('Arial', 48, bold=True)
heading_font = pygame.font.SysFont('Arial', 36, bold=True)
subheading_font = pygame.font.SysFont('Arial', 28, bold=True)
button_font = pygame.font.SysFont('Arial', 24, bold=True)
text_font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

# Global variables for resources
background_img = None
logo_img = None
images_loaded = False

# Load parent data
parent_username = "Parent"
child_name = "Student"
child_level = "Level 1"
child_scores = {}

try:
    if os.path.exists("current_parent.txt"):
        with open("current_parent.txt", "r") as f:
            parent_username = f.read().strip()

    if os.path.exists("current_child.txt"):
        with open("current_child.txt", "r") as f:
            lines = f.readlines()
            if len(lines) >= 1:
                child_name = lines[0].strip()
            if len(lines) >= 2:
                child_level = lines[1].strip()
except Exception as e:
    print(f"Error loading parent/child data: {e}")

# Load child scores - in a real app, this would be retrieved from a database
# For now, we'll use hardcoded data based on the parent account
parent_accounts = {
    "user1": {
        "child_scores": {
            "Memory Math": 45,
            "Word Builder": 38,
            "English Pro": 7,
            "Football Quiz": 6,
            "Car Parking": 20
        }
    },
    "user2": {
        "child_scores": {
            "Memory Math": 52,
            "Word Builder": 45,
            "English Pro": 8,
            "Football Quiz": 7,
            "Car Parking": 30
        }
    },
    "user3": {
        "child_scores": {
            "Memory Math": 58,
            "Word Builder": 52,
            "English Pro": 9,
            "Football Quiz": 8,
            "Car Parking": 30
        }
    }
}

# Get child scores for the current parent
if parent_username in parent_accounts:
    child_scores = parent_accounts[parent_username]["child_scores"]

# Load images
try:
    # Load background image
    if os.path.exists('memorymath_login_bg.jpg'):
        background_img = pygame.image.load('memorymath_login_bg.jpg')
        background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load logo image
    if os.path.exists('memorymath_logo.png'):
        logo_img = pygame.image.load('memorymath_logo.png')
        logo_img = pygame.transform.scale(logo_img, (200, 100))  # Adjust size as needed

    images_loaded = True
    print("Successfully loaded image files.")
except pygame.error as e:
    print(f"Warning: Could not load some image files. Error: {e}")
    images_loaded = False

# Try to load background music
try:
    pygame.mixer.init()
    if os.path.exists("memorymath_parent.mp3"):
        pygame.mixer.music.load("memorymath_parent.mp3")
        pygame.mixer.music.set_volume(0.4)  # Set volume to 40%
        music_loaded = True
        pygame.mixer.music.play(-1)  # Loop indefinitely
        print("Loaded parent dashboard background music")
    else:
        music_loaded = False
        print("Could not find memorymath_parent.mp3")
except Exception as e:
    print(f"Warning: Could not initialize music. Error: {e}")
    music_loaded = False


# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK, border_radius=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.active = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)

        pygame.draw.rect(screen, BLACK, self.rect, width=2, border_radius=self.border_radius)

        text_surf = button_font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def show_parent_dashboard():
    """Display the parent dashboard screen"""
    # Create buttons
    logout_button = Button(SCREEN_WIDTH - 120, 20, 100, 40, "Logout", ORANGE, LIGHT_ORANGE, WHITE)
    view_rankings_button = Button(SCREEN_WIDTH // 2 - 150, 540, 300, 50,
                                  f"View {child_name}'s Rankings", BLUE, LIGHT_BLUE, WHITE)

    # Create info button for game descriptions - POSITIONED RELATIVE TO SCREEN WIDTH
    info_button = Button(SCREEN_WIDTH // 2 + 270, 100, 40, 40, "?", YELLOW, LIGHT_ORANGE, BLACK)

    # Variable to track info popup state
    show_info_popup = False

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos

                    if logout_button.is_clicked(mouse_pos):
                        print("Parent logging out")
                        # Return to main login screen
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "login_screen.py"])
                        return

                    if view_rankings_button.is_clicked(mouse_pos):
                        print("Viewing rankings")
                        # Go to rankings screen
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "view_rankings_parent.py"])
                        return

                    if info_button.is_clicked(mouse_pos):
                        # Toggle info popup
                        show_info_popup = not show_info_popup

            # Close info popup on any key press
            if event.type == pygame.KEYDOWN and show_info_popup:
                show_info_popup = False

        # Draw the background
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            # Gradient background as fallback
            for y in range(SCREEN_HEIGHT):
                # Create a gradient from dark blue to light blue
                color = (
                    int(DARK_BLUE[0] + (LIGHT_BLUE[0] - DARK_BLUE[0]) * y / SCREEN_HEIGHT),
                    int(DARK_BLUE[1] + (LIGHT_BLUE[1] - DARK_BLUE[1]) * y / SCREEN_HEIGHT),
                    int(DARK_BLUE[2] + (LIGHT_BLUE[2] - DARK_BLUE[2]) * y / SCREEN_HEIGHT)
                )
                pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Draw logo if available
        if logo_img:
            screen.blit(logo_img, (SCREEN_WIDTH // 2 - logo_img.get_width() // 2, 30))
        else:
            # Draw title text as fallback
            title_text = title_font.render("Memory Math", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
            screen.blit(title_text, title_rect)

        # Draw child's name with attractive background bar - MOVED UP
        name_bar_width = 500
        name_bar_height = 50
        name_bar_rect = pygame.Rect(SCREEN_WIDTH // 2 - name_bar_width // 2, 100, name_bar_width, name_bar_height)

        # Draw a gradient background for the child's name WITH ROUNDED CORNERS
        pygame.draw.rect(screen, PURPLE, name_bar_rect, border_radius=15)  # Base color

        # Gradient effect over the rounded rectangle
        gradient_surface = pygame.Surface((name_bar_width, name_bar_height), pygame.SRCALPHA)
        for y in range(name_bar_height):
            alpha = int(255 * y / name_bar_height)  # Gradient transparency
            grad_color = (
                int(PURPLE[0] + (LIGHT_PURPLE[0] - PURPLE[0]) * y / name_bar_height),
                int(PURPLE[1] + (LIGHT_PURPLE[1] - PURPLE[1]) * y / name_bar_height),
                int(PURPLE[2] + (LIGHT_PURPLE[2] - PURPLE[2]) * y / name_bar_height)
            )
            pygame.draw.line(gradient_surface, (*grad_color, alpha),
                             (0, y), (name_bar_width, y))

        # Apply the gradient with rounded corners
        mask = pygame.Surface((name_bar_width, name_bar_height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255), mask.get_rect(), border_radius=15)
        gradient_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(gradient_surface, name_bar_rect)

        # Add border
        pygame.draw.rect(screen, BLACK, name_bar_rect, width=2, border_radius=15)

        # Draw child name on the left side of the bar
        child_progress_text = subheading_font.render(f"{child_name}'s Progress", True, WHITE)
        child_progress_rect = child_progress_text.get_rect(midleft=(name_bar_rect.left + 20, name_bar_rect.centery))
        screen.blit(child_progress_text, child_progress_rect)

        # Draw level on the right side of the bar
        level_name = child_level.split(" - ")[0] if " - " in child_level else child_level
        level_text = text_font.render(level_name, True, WHITE)
        level_rect = level_text.get_rect(midright=(name_bar_rect.right - 20, name_bar_rect.centery))
        screen.blit(level_text, level_rect)

        # Draw information button - CHANGED TO YELLOW
        info_button = Button(SCREEN_WIDTH - 70, 180, 40, 40, "?", YELLOW, LIGHT_ORANGE, BLACK)
        info_button.draw()

        # Draw larger info box with rounded corners - MADE TALLER & MOVED UP
        info_box = pygame.Rect(SCREEN_WIDTH // 2 - 350, 160, 700, 360)

        # Draw a nice shadow effect
        shadow_offset = 5
        shadow_rect = pygame.Rect(info_box.left + shadow_offset, info_box.top + shadow_offset,
                                  info_box.width, info_box.height)
        pygame.draw.rect(screen, (30, 30, 30, 128), shadow_rect, border_radius=15)

        # Draw the main white box
        pygame.draw.rect(screen, WHITE, info_box, border_radius=15)
        pygame.draw.rect(screen, BLACK, info_box, width=2, border_radius=15)

        # Draw horizontal decorative line
        line_y = info_box.top + 50
        pygame.draw.line(screen, LIGHT_BLUE,
                         (info_box.left + 20, line_y),
                         (info_box.right - 20, line_y), 3)

        # Draw game scores in an improved table format
        # Table header
        header_y = line_y + 20
        pygame.draw.rect(screen, LIGHT_BLUE,
                         (info_box.left + 20, header_y, info_box.width - 40, 30),
                         border_radius=5)

        # Draw headers
        game_header = text_font.render("Game", True, BLACK)
        score_header = text_font.render("Score", True, BLACK)

        screen.blit(game_header, (info_box.left + 50, header_y + 5))
        screen.blit(score_header, (info_box.right - 120, header_y + 5))

        # Draw game scores in a table format
        row_y = header_y + 30
        row_height = 30  # Increased row height for better spacing

        # Draw alternating row backgrounds
        for i, (game, score) in enumerate(child_scores.items()):
            row_rect = pygame.Rect(info_box.left + 20, row_y + i * row_height,
                                   info_box.width - 40, row_height)

            # Alternate row colors
            if i % 2 == 0:
                pygame.draw.rect(screen, WHITE, row_rect)
            else:
                pygame.draw.rect(screen, GRAY, row_rect)

            # Game name
            game_text = small_font.render(game, True, BLACK)
            screen.blit(game_text, (info_box.left + 50, row_y + i * row_height + 8))

            # Score
            score_text = small_font.render(str(score), True, BLACK)
            screen.blit(score_text, (info_box.right - 120, row_y + i * row_height + 8))

        # Draw total score with nice styling
        total_score = sum(child_scores.values())
        total_y = row_y + len(child_scores) * row_height + 20  # Added more space

        # Total row background
        total_rect = pygame.Rect(info_box.left + 20, total_y, info_box.width - 40, 40)  # Made taller
        pygame.draw.rect(screen, DARK_BLUE, total_rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, total_rect, width=1, border_radius=5)

        # Total text
        total_label = text_font.render("TOTAL SCORE:", True, WHITE)
        total_value = text_font.render(str(total_score), True, GOLD)

        screen.blit(total_label, (info_box.left + 50, total_y + 10))
        screen.blit(total_value, (info_box.right - 120, total_y + 10))

        # Draw buttons
        logout_button.draw()
        view_rankings_button.draw()

        # Draw info popup if active
        if show_info_popup:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Black with 70% opacity
            screen.blit(overlay, (0, 0))

            # Info popup box
            popup_width = 650
            popup_height = 450
            popup_rect = pygame.Rect(SCREEN_WIDTH // 2 - popup_width // 2,
                                     SCREEN_HEIGHT // 2 - popup_height // 2,
                                     popup_width, popup_height)

            # Draw popup with shadow
            shadow_offset = 8
            shadow_rect = pygame.Rect(popup_rect.left + shadow_offset, popup_rect.top + shadow_offset,
                                      popup_width, popup_height)
            pygame.draw.rect(screen, (20, 20, 20), shadow_rect, border_radius=15)

            # Main popup
            pygame.draw.rect(screen, WHITE, popup_rect, border_radius=15)
            pygame.draw.rect(screen, BLACK, popup_rect, width=2, border_radius=15)

            # Popup title
            popup_title = heading_font.render("Game Information", True, BLUE)
            popup_title_rect = popup_title.get_rect(center=(popup_rect.centerx, popup_rect.top + 30))
            screen.blit(popup_title, popup_title_rect)

            # Horizontal line
            pygame.draw.line(screen, LIGHT_BLUE,
                             (popup_rect.left + 20, popup_rect.top + 60),
                             (popup_rect.right - 20, popup_rect.top + 60), 2)

            # Game descriptions - Enhanced with educational benefits
            game_info = {
                "Memory Math": {
                    "description": "A card-matching game with mathematical equations.",
                    "benefits": "Enhances mathematical skills, improves memory and concentration, develops pattern recognition abilities."
                },
                "Word Builder": {
                    "description": "Form words from given letters to solve puzzles.",
                    "benefits": "Expands vocabulary, strengthens spelling skills, improves word recognition and language processing."
                },
                "English Pro": {
                    "description": "Interactive English language exercises with word formation and memory games.",
                    "benefits": "Develops reading comprehension, enhances grammar understanding, builds vocabulary in context."
                },
                "Football Quiz": {
                    "description": "Sports-themed quiz with multiple-choice questions.",
                    "benefits": "Improves general knowledge, develops quick thinking and decision making, makes learning fun through gamification."
                },
                "Car Parking": {
                    "description": "Puzzle game requiring logical movement of vehicles.",
                    "benefits": "Develops spatial reasoning, improves problem-solving abilities, enhances strategic thinking and planning."
                }
            }

            # Create a content area for scrolling
            content_area = pygame.Rect(popup_rect.left + 20, popup_rect.top + 70,
                                       popup_width - 40, popup_height - 100)

            # Display game info with proper formatting
            info_y = content_area.top
            line_spacing = 16  # Reduced for better fit

            for game, info in game_info.items():
                # Only draw if in view (basic scrolling)
                if info_y > content_area.top - 60 and info_y < content_area.bottom:
                    # Game name with colored background
                    game_bg_rect = pygame.Rect(content_area.left, info_y, content_area.width, 30)
                    pygame.draw.rect(screen, LIGHT_BLUE, game_bg_rect, border_radius=5)

                    game_text = text_font.render(game, True, BLACK)
                    screen.blit(game_text, (content_area.left + 10, info_y + 5))
                    info_y += 35

                    # Game description with label
                    if info_y < content_area.bottom:
                        desc_label = small_font.render("Description:", True, DARK_BLUE)
                        screen.blit(desc_label, (content_area.left + 10, info_y))
                        info_y += line_spacing + 2

                        desc_text = small_font.render(info["description"], True, BLACK)
                        screen.blit(desc_text, (content_area.left + 20, info_y))
                        info_y += line_spacing + 5

                    # Educational benefits with label
                    if info_y < content_area.bottom:
                        benefit_label = small_font.render("How it helps:", True, DARK_BLUE)
                        screen.blit(benefit_label, (content_area.left + 10, info_y))
                        info_y += line_spacing + 2

                        # Split benefits into multiple lines if needed
                        benefits_text = info["benefits"]
                        max_width = content_area.width - 30

                        words = benefits_text.split()
                        line = words[0]
                        for word in words[1:]:
                            test_line = line + " " + word
                            # If adding this word would make line too long, render current line and start new line
                            test_width = small_font.size(test_line)[0]
                            if test_width < max_width:
                                line = test_line
                            else:
                                line_text = small_font.render(line, True, BLACK)
                                if info_y < content_area.bottom:
                                    screen.blit(line_text, (content_area.left + 20, info_y))
                                    info_y += line_spacing
                                line = word

                        # Render last line
                        if info_y < content_area.bottom:
                            last_line = small_font.render(line, True, BLACK)
                            screen.blit(last_line, (content_area.left + 20, info_y))

                    info_y += line_spacing + 15  # Space between games

                # Even if not in view, update position for scrolling
                else:
                    # Approximate height of game entry
                    info_y += 35 + line_spacing * 5 + 15

            # Draw close instruction
            close_text = small_font.render("Press any key to close this window", True, DARK_GRAY)
            close_rect = close_text.get_rect(center=(popup_rect.centerx, popup_rect.bottom - 20))
            screen.blit(close_text, close_rect)

        pygame.display.flip()
        clock.tick(60)

    # Stop music and quit if window is closed
    if music_loaded:
        pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


# Start the program if this file is run directly
if __name__ == "__main__":
    show_parent_dashboard()