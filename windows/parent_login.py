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
RED = (255, 50, 50)
LIGHT_RED = (255, 100, 100)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MemoryMath - Parent Login")
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
    if os.path.exists("memorymath_login.mp3"):
        pygame.mixer.music.load("memorymath_login.mp3")
        pygame.mixer.music.set_volume(0.3)  # Set volume to 30%
        music_loaded = True
        pygame.mixer.music.play(-1)  # Loop indefinitely
        print("Loaded login background music")
    else:
        music_loaded = False
        print("Could not find memorymath_login.mp3")
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


# Text input class
class TextInput:
    def __init__(self, x, y, width, height, placeholder="", is_password=False, max_length=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.is_password = is_password
        self.max_length = max_length
        self.active = False

    def draw(self):
        # Draw input box
        color = LIGHT_BLUE if self.active else WHITE
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, width=2, border_radius=5)

        # Draw text or placeholder
        if self.text:
            # Show asterisks if password
            display_text = '*' * len(self.text) if self.is_password else self.text
            text_surface = text_font.render(display_text, True, BLACK)
        else:
            text_surface = small_font.render(self.placeholder, True, DARK_GRAY)

        # Ensure text fits within the box
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif len(self.text) < self.max_length:
                # Only add printable characters
                if event.unicode.isprintable():
                    self.text += event.unicode
            return True  # Event was handled
        return False


# Parent accounts - in a real app, these would be stored securely
parent_accounts = {
    "user1": {
        "password": "pass1",
        "child_name": "Alex",
        "child_level": "Level 1 - Beginner",
        "child_scores": {
            "Memory Math": 45,
            "Word Builder": 38,
            "English Pro": 7,
            "Football Quiz": 6,
            "Car Parking": 20
        }
    },
    "user2": {
        "password": "pass2",
        "child_name": "Taylor",
        "child_level": "Level 2 - Explorer",
        "child_scores": {
            "Memory Math": 52,
            "Word Builder": 45,
            "English Pro": 8,
            "Football Quiz": 7,
            "Car Parking": 30
        }
    },
    "user3": {
        "password": "pass3",
        "child_name": "Morgan",
        "child_level": "Level 3 - Master",
        "child_scores": {
            "Memory Math": 58,
            "Word Builder": 52,
            "English Pro": 9,
            "Football Quiz": 8,
            "Car Parking": 30
        }
    }
}


def show_parent_login():
    """Display the parent login screen"""
    # Create text inputs
    username_input = TextInput(SCREEN_WIDTH // 2 - 150, 300, 300, 40, "Username")
    password_input = TextInput(SCREEN_WIDTH // 2 - 150, 360, 300, 40, "Password", is_password=True)

    # Create login button
    login_button = Button(SCREEN_WIDTH // 2 - 100, 430, 200, 50, "Login", GREEN, LIGHT_GREEN, BLACK)

    # Create back button
    back_button = Button(20, 20, 100, 40, "Back", ORANGE, LIGHT_ORANGE, WHITE)

    # Error message
    error_message = ""
    show_error = False
    error_timer = 0

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle text input events
            username_input.handle_event(event)
            password_input.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos

                    if back_button.is_clicked(mouse_pos):
                        # Return to main login screen
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "login_screen.py"])
                        return

                    if login_button.is_clicked(mouse_pos):
                        # Validate login
                        username = username_input.text
                        password = password_input.text

                        if username in parent_accounts and parent_accounts[username]["password"] == password:
                            # Login successful - save parent username to file
                            try:
                                with open("current_parent.txt", "w") as f:
                                    f.write(username)
                                # Also save child data for easy access
                                with open("current_child.txt", "w") as f:
                                    f.write(parent_accounts[username]["child_name"] + "\n")
                                    f.write(parent_accounts[username]["child_level"])
                            except Exception as e:
                                print(f"Error saving parent data: {e}")

                            # Launch parent dashboard
                            if music_loaded:
                                pygame.mixer.music.stop()
                            pygame.quit()
                            subprocess.run(["python", "parent_main.py"])
                            return
                        else:
                            # Login failed
                            error_message = "Invalid username or password!"
                            show_error = True
                            error_timer = 180  # Show for 3 seconds (60 fps * 3)

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

        # Draw login heading
        login_text = heading_font.render("Parent Login", True, WHITE)
        login_rect = login_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(login_text, login_rect)

        # Draw text inputs
        username_label = text_font.render("Username:", True, WHITE)
        screen.blit(username_label, (SCREEN_WIDTH // 2 - 150, 270))
        username_input.draw()

        password_label = text_font.render("Password:", True, WHITE)
        screen.blit(password_label, (SCREEN_WIDTH // 2 - 150, 330))
        password_input.draw()

        # Draw login button
        login_button.draw()

        # Draw back button
        back_button.draw()

        # Draw error message if needed
        if show_error and error_timer > 0:
            error_text = text_font.render(error_message, True, RED)
            error_rect = error_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
            screen.blit(error_text, error_rect)
            error_timer -= 1
            if error_timer <= 0:
                show_error = False

        pygame.display.flip()
        clock.tick(60)

    # Stop music and quit if window is closed
    if music_loaded:
        pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


# Start the program if this file is run directly
if __name__ == "__main__":
    show_parent_login()