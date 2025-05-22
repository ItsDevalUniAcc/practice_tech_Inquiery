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

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MemoryMath - Teacher Dashboard")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont('Arial', 48, bold=True)
heading_font = pygame.font.SysFont('Arial', 36, bold=True)
button_font = pygame.font.SysFont('Arial', 24, bold=True)
text_font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

# Global variables for resources
background_img = None
logo_img = None
images_loaded = False

# Get teacher username
teacher_username = "Teacher"
try:
    if os.path.exists("current_teacher.txt"):
        with open("current_teacher.txt", "r") as f:
            teacher_username = f.read().strip()
except Exception as e:
    print(f"Error loading teacher data: {e}")

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
    if os.path.exists("memorymath_teacher.mp3"):
        pygame.mixer.music.load("memorymath_teacher.mp3")
        pygame.mixer.music.set_volume(0.4)  # Set volume to 40%
        music_loaded = True
        pygame.mixer.music.play(-1)  # Loop indefinitely
        print("Loaded teacher dashboard background music")
    else:
        music_loaded = False
        print("Could not find memorymath_teacher.mp3")
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


def show_teacher_main():
    """Display the teacher dashboard main screen"""

    # Create buttons
    logout_button = Button(SCREEN_WIDTH - 120, 20, 100, 40, "Logout", ORANGE, LIGHT_ORANGE, WHITE)

    # New buttons for teacher functionality
    view_students_button = Button(SCREEN_WIDTH // 2 - 125, 300, 250, 60,
                                  "View Student Details", BLUE, LIGHT_BLUE, WHITE)

    view_rankings_button = Button(SCREEN_WIDTH // 2 - 125, 380, 250, 60,
                                  "View Student Rankings", PURPLE, LIGHT_PURPLE, WHITE)

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
                        print("Teacher logging out")
                        # Return to main login screen
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "login_screen.py"])
                        return

                    # Handle view students button
                    if view_students_button.is_clicked(mouse_pos):
                        print("Viewing student details")
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "student_details.py"])
                        return

                    # Handle view rankings button
                    if view_rankings_button.is_clicked(mouse_pos):
                        print("Viewing student rankings")
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "view_rankings_teacher.py"])
                        return

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
            screen.blit(logo_img, (SCREEN_WIDTH // 2 - logo_img.get_width() // 2, 50))
        else:
            # Draw title text as fallback
            title_text = title_font.render("Memory Math", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(title_text, title_rect)

        # Draw teacher dashboard heading
        dashboard_text = heading_font.render("Teacher Dashboard", True, WHITE)
        dashboard_rect = dashboard_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(dashboard_text, dashboard_rect)

        # Draw welcome message
        welcome_text = text_font.render(f"Welcome back, {teacher_username}!", True, WHITE)
        welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(welcome_text, welcome_rect)

        # Draw action message
        action_text = small_font.render("Please select an option:", True, YELLOW)
        action_rect = action_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
        screen.blit(action_text, action_rect)

        # Draw buttons
        logout_button.draw()
        view_students_button.draw()
        view_rankings_button.draw()

        pygame.display.flip()
        clock.tick(60)

    # Stop music and quit if window is closed
    if music_loaded:
        pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


# Start the program if this file is run directly
if __name__ == "__main__":
    show_teacher_main()