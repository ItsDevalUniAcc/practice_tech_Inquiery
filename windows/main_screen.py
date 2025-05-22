import pygame
import sys
import os
import subprocess
import math
import random

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
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
DARK_BLUE = (0, 50, 150)
GREEN = (50, 200, 50)
LIGHT_GREEN = (100, 255, 100)
PURPLE = (150, 50, 200)
LIGHT_PURPLE = (180, 100, 240)
ORANGE = (255, 150, 50)
LIGHT_ORANGE = (255, 180, 100)
YELLOW = (255, 230, 0)
LIGHT_YELLOW = (255, 255, 150)
CRAYON_RED = (255, 105, 97)
CRAYON_ORANGE = (255, 175, 84)
CRAYON_PURPLE = (170, 130, 255)
CRAYON_PINK = (255, 182, 193)
CHALK_WHITE = (235, 235, 235)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SkillScape - Main Menu")
clock = pygame.time.Clock()

# Fonts - Using more childlike fonts for primary school vibe
try:
    # Try to use Comic Sans or similar fonts if available
    title_font = pygame.font.SysFont('comicsansms', 48, bold=True)
    heading_font = pygame.font.SysFont('comicsansms', 36, bold=True)
    button_font = pygame.font.SysFont('comicsansms', 24, bold=True)
    text_font = pygame.font.SysFont('comicsansms', 24)
    small_font = pygame.font.SysFont('comicsansms', 18)
except:
    # Fall back to Arial if Comic Sans is not available
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    heading_font = pygame.font.SysFont('Arial', 36, bold=True)
    button_font = pygame.font.SysFont('Arial', 24, bold=True)
    text_font = pygame.font.SysFont('Arial', 24)
    small_font = pygame.font.SysFont('Arial', 18)

# Global variables for resources
background_img = None
logo_img = None
profile_icon = None
images_loaded = False

# Load current student data
current_student = {
    "name": "Guest",
    "level": "Level 1 - Beginner",
    "icon": None
}

try:
    if os.path.exists("current_student.txt"):
        with open("current_student.txt", "r") as f:
            lines = f.readlines()
            if len(lines) >= 3:
                current_student["name"] = lines[0].strip()
                current_student["level"] = lines[1].strip()
                current_student["icon"] = lines[2].strip()
except Exception as e:
    print(f"Error loading student data: {e}")

# Load images
try:
    # Load background image
    if os.path.exists('memorymath_login_bg.jpg'):
        background_img = pygame.image.load('memorymath_login_bg.jpg')
        background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load logo image
    if os.path.exists('main_logo.png'):
        logo_img = pygame.image.load('main_logo.png')
        logo_img = pygame.transform.scale(logo_img, (350, 100))  # Adjust size as needed

    # Load student profile icon
    if current_student["icon"] and os.path.exists(current_student["icon"]):
        profile_icon = pygame.image.load(current_student["icon"])
        profile_icon = pygame.transform.scale(profile_icon, (60, 60))  # Larger icon for profile

    images_loaded = True
    print("Successfully loaded image files.")
except pygame.error as e:
    print(f"Warning: Could not load some image files. Error: {e}")
    images_loaded = False

# Try to load background music
try:
    pygame.mixer.init()
    if os.path.exists("memorymath_main.mp3"):
        pygame.mixer.music.load("memorymath_main.mp3")
        pygame.mixer.music.set_volume(0.4)  # Set volume to 40%
        music_loaded = True
        print("Loaded main screen background music")
    else:
        music_loaded = False
        print("Could not find memorymath_main.mp3")
except Exception as e:
    print(f"Warning: Could not initialize music. Error: {e}")
    music_loaded = False


# Enhanced Button class with animation effects
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK, border_radius=15):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.active = False
        self.animation_value = 0  # For animation effects
        self.pulsing = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        hovering = self.rect.collidepoint(mouse_pos)

        # Update animation
        if hovering and not self.pulsing:
            self.pulsing = True
            self.animation_value = 0
        elif not hovering and self.pulsing:
            self.pulsing = False

        if self.pulsing:
            self.animation_value = (self.animation_value + 0.1) % 6.28  # 2*pi
            pulse_scale = 1.0 + 0.05 * abs(math.sin(self.animation_value))
        else:
            pulse_scale = 1.0

        # Calculate the actual size based on animation
        actual_width = int(self.rect.width * pulse_scale)
        actual_height = int(self.rect.height * pulse_scale)
        x_offset = (actual_width - self.rect.width) // 2
        y_offset = (actual_height - self.rect.height) // 2

        # Draw shadow for 3D effect
        shadow_rect = pygame.Rect(
            self.rect.x + 4 - x_offset,
            self.rect.y + 4 - y_offset,
            actual_width,
            actual_height
        )
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=self.border_radius)

        # Draw the button with hover effect
        button_rect = pygame.Rect(
            self.rect.x - x_offset,
            self.rect.y - y_offset,
            actual_width,
            actual_height
        )

        if hovering:
            pygame.draw.rect(screen, self.hover_color, button_rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(screen, self.color, button_rect, border_radius=self.border_radius)

        pygame.draw.rect(screen, BLACK, button_rect, width=2, border_radius=self.border_radius)

        # Draw text
        text_surf = button_font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Simple floating animation elements to add visual interest
class FloatingElement:
    def __init__(self, x, y, image=None, color=None, size=30, speed=0.5):
        self.x = x
        self.y = y
        self.original_y = y
        self.image = image
        self.color = color
        self.size = size
        self.speed = speed
        self.offset = random.random() * 6.28  # Random starting position in the cycle
        self.amplitude = random.randint(5, 15)  # How far it moves up and down

    def update(self):
        # Make the element float up and down
        self.y = self.original_y + math.sin(pygame.time.get_ticks() / 1000 + self.offset) * self.amplitude

    def draw(self):
        if self.image:
            screen.blit(self.image, (self.x - self.size // 2, self.y - self.size // 2))
        elif self.color:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            # Add a highlight to make it look like a bubble
            pygame.draw.circle(screen, WHITE, (int(self.x - self.size // 3), int(self.y - self.size // 3)),
                               self.size // 4)


def show_main_screen():
    """Display the main screen after login"""
    # Position variables for UI elements
    logo_y = 100  # Y position for the logo
    welcome_y = 180  # Y position for the welcome text

    # Start background music if loaded
    if music_loaded:
        pygame.mixer.music.play(-1)  # Loop indefinitely

    # Create buttons with better styling
    start_button = Button(
        SCREEN_WIDTH // 2 - 125,
        350,
        250, 60,
        "Start Journey",
        GREEN,
        LIGHT_GREEN,
        WHITE
    )

    logout_button = Button(
        20,
        20,
        100, 40,
        "Logout",
        ORANGE,
        LIGHT_ORANGE,
        WHITE
    )

    rankings_button = Button(
        SCREEN_WIDTH // 2 - 125,
        430,
        250, 50,
        "View Rankings",
        BLUE,
        LIGHT_BLUE,
        WHITE
    )

    # Create some floating decorative elements
    floating_elements = []

    # Add skill symbols as floating elements
    skill_symbols = ["♫", "✎", "♞", "✿", "★", "♥"]  # Music, Art, Strategy, Nature, Achievement, Wellness
    skill_colors = [CRAYON_RED, CRAYON_ORANGE, CRAYON_PURPLE, CRAYON_PINK, LIGHT_GREEN, LIGHT_BLUE]

    for _ in range(15):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        symbol = random.choice(skill_symbols)
        color = random.choice(skill_colors)
        size = random.randint(15, 35)
        speed = random.uniform(0.3, 1.0)

        # Create a surface with the skill symbol
        symbol_surface = text_font.render(symbol, True, color)

        # Create the floating element
        element = FloatingElement(x, y, image=symbol_surface, size=size, speed=speed)
        floating_elements.append(element)

    # Main loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos

                    if start_button.is_clicked(mouse_pos):
                        print("Starting journey...")
                        if music_loaded:
                            pygame.mixer.music.stop()
                        # Launch instructions screen
                        pygame.quit()
                        subprocess.run(["python", "MemoryMath_instructions.py"])
                        return

                    elif logout_button.is_clicked(mouse_pos):
                        print("Logging out...")
                        if music_loaded:
                            pygame.mixer.music.stop()
                        # Return to login screen
                        pygame.quit()
                        subprocess.run(["python", "login_screen.py"])
                        return

                    elif rankings_button.is_clicked(mouse_pos):
                        print("Viewing rankings...")
                        if music_loaded:
                            pygame.mixer.music.stop()
                        # Launch rankings screen
                        pygame.quit()
                        subprocess.run(["python", "student_rankings.py"])
                        return

        # Update floating elements
        for element in floating_elements:
            element.update()

        # Draw the background
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            # Create a more colorful gradient background as fallback
            for y in range(SCREEN_HEIGHT):
                # Create a gradient from blue to light blue with a hint of purple
                color = (
                    int(50 + (180 - 50) * y / SCREEN_HEIGHT),  # R
                    int(150 + (230 - 150) * y / SCREEN_HEIGHT),  # G
                    int(255)  # B - keep blue high for a cheerful sky color
                )
                pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Draw floating elements behind everything else
        for element in floating_elements:
            element.draw()

        # Draw logo if available
        if logo_img:
            logo_rect = logo_img.get_rect(center=(SCREEN_WIDTH // 2, logo_y))
            screen.blit(logo_img, logo_rect)
        else:
            # Draw title text as fallback
            title_text = title_font.render("SkillScape", True, CRAYON_PURPLE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, logo_y))

            # Add a shadow for better visibility
            shadow_text = title_font.render("SkillScape", True, BLACK)
            shadow_rect = title_rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            screen.blit(shadow_text, shadow_rect)

            screen.blit(title_text, title_rect)

        # Draw profile section with enhanced styling
        # Create a smaller profile box with semi-transparency and rounded corners
        profile_rect = pygame.Rect(SCREEN_WIDTH - 180, 20, 160, 60)

        # Draw shadow for 3D effect
        shadow_rect = pygame.Rect(profile_rect.x + 4, profile_rect.y + 4, profile_rect.width, profile_rect.height)
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=15)

        # Draw semi-transparent background
        s = pygame.Surface((profile_rect.width, profile_rect.height), pygame.SRCALPHA)
        s.fill((255, 255, 255, 180))  # More visible white background
        screen.blit(s, profile_rect)

        # Draw border
        pygame.draw.rect(screen, BLACK, profile_rect, width=2, border_radius=15)

        # Draw profile icon with better styling
        if profile_icon:
            # Draw a circular background for the icon
            pygame.draw.circle(screen, WHITE, (profile_rect.x + 30, profile_rect.y + 30), 24)
            pygame.draw.circle(screen, BLACK, (profile_rect.x + 30, profile_rect.y + 30), 24, width=2)

            # Scale down the icon for a better fit
            small_profile_icon = pygame.transform.scale(profile_icon, (40, 40))

            # Position the icon within the circle
            icon_rect = small_profile_icon.get_rect(center=(profile_rect.x + 30, profile_rect.y + 30))
            screen.blit(small_profile_icon, icon_rect)
            name_x = profile_rect.x + 60
        else:
            # Draw a nicer placeholder circle if no icon
            pygame.draw.circle(screen, BLUE, (profile_rect.x + 30, profile_rect.y + 30), 24)
            pygame.draw.circle(screen, BLACK, (profile_rect.x + 30, profile_rect.y + 30), 24, width=2)

            # Add initial with slight shadow for depth
            shadow_text = small_font.render(current_student["name"][0], True, BLACK)
            shadow_rect = shadow_text.get_rect(center=(profile_rect.x + 32, profile_rect.y + 32))
            screen.blit(shadow_text, shadow_rect)

            text = small_font.render(current_student["name"][0], True, WHITE)
            text_rect = text.get_rect(center=(profile_rect.x + 30, profile_rect.y + 30))
            screen.blit(text, text_rect)
            name_x = profile_rect.x + 60

        # Draw student name with better styling
        name_text = small_font.render(current_student["name"], True, BLACK)
        screen.blit(name_text, (name_x, profile_rect.y + 15))

        # Extract just the level number (e.g., "Level 2" from "Level 2 - Explorer")
        level_parts = current_student["level"].split(" - ")
        level_number = level_parts[0] if len(level_parts) > 0 else current_student["level"]

        # Draw simplified level
        level_text = small_font.render(level_number, True, BLUE)
        screen.blit(level_text, (name_x, profile_rect.y + 35))

        # Draw a colorful banner at the BOTTOM of the screen
        footer_height = 80
        footer_rect = pygame.Rect(0, SCREEN_HEIGHT - footer_height, SCREEN_WIDTH, footer_height)

        # Draw a colorful banner
        pygame.draw.rect(screen, CRAYON_ORANGE, footer_rect)

        # Add a playful scalloped top edge to the banner
        scallop_radius = 15
        for x in range(scallop_radius, SCREEN_WIDTH, scallop_radius * 2):
            pygame.draw.circle(screen, CRAYON_ORANGE, (x, footer_rect.top), scallop_radius)

        # Draw welcome message with decorative background
        welcome_text = heading_font.render(f"Hello, {current_student['name']}!", True, CRAYON_PURPLE)
        welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH // 2, welcome_y))

        # Add a fun background for the welcome message
        welcome_bg = pygame.Rect(
            welcome_rect.left - 20,
            welcome_rect.top - 10,
            welcome_rect.width + 40,
            welcome_rect.height + 20
        )
        pygame.draw.rect(screen, LIGHT_YELLOW, welcome_bg, border_radius=15)
        pygame.draw.rect(screen, BLACK, welcome_bg, width=2, border_radius=15)

        screen.blit(welcome_text, welcome_rect)

        # Draw big heading with shadow for better visibility
        heading_text = title_font.render("Start Your Learning Journey", True, WHITE)
        heading_rect = heading_text.get_rect(center=(SCREEN_WIDTH // 2, 280))

        # Add shadow
        shadow_heading = title_font.render("Start Your Learning Journey", True, BLACK)
        shadow_heading_rect = heading_rect.copy()
        shadow_heading_rect.x += 3
        shadow_heading_rect.y += 3
        screen.blit(shadow_heading, shadow_heading_rect)

        screen.blit(heading_text, heading_rect)

        # Draw buttons
        logout_button.draw()
        start_button.draw()
        rankings_button.draw()

        pygame.display.flip()
        clock.tick(60)

    # Stop music if we're exiting
    if music_loaded:
        pygame.mixer.music.stop()

    pygame.quit()
    sys.exit()


# Start the program if this file is run directly
if __name__ == "__main__":
    show_main_screen()