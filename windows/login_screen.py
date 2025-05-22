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
SCREEN_HEIGHT = 1000
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
pygame.display.set_caption("SkillScape - Login")
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
student_icons = []
images_loaded = False

# Mock student data - in a real app, this would come from a database
students = [
    {"name": "Alex", "level": "Level 1 - Beginner", "icon": "student1.png"},
    {"name": "Taylor", "level": "Level 2 - Explorer", "icon": "student2.png"},
    {"name": "Jordan", "level": "Level 3 - Achiever", "icon": "student3.png"},
    {"name": "Casey", "level": "Level 2 - Explorer", "icon": "student4.png"},
    {"name": "Morgan", "level": "Level 4 - Master", "icon": "student5.png"},
]

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

    # Load student icons
    for i in range(1, 6):
        icon_path = f'student{i}.png'
        if os.path.exists(icon_path):
            icon = pygame.image.load(icon_path)
            icon = pygame.transform.scale(icon, (40, 40))  # Small icons for the dropdown
            student_icons.append(icon)
        else:
            student_icons.append(None)

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
        pygame.mixer.music.set_volume(0.4)  # Set volume to 40%
        music_loaded = True
        print("Loaded login background music")
    else:
        music_loaded = False
        print("Could not find memorymath_login.mp3")
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


# ScrollableList class to replace the Dropdown
class ScrollableList:
    def __init__(self, x, y, width, height, items, data=None, bg_color=WHITE, highlight_color=LIGHT_BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.items = items  # Simple list of item names
        self.data = data  # Optional: original data objects for each item
        self.bg_color = bg_color
        self.highlight_color = highlight_color
        self.scroll_offset = 0  # How far scrolled down
        self.selected_index = -1  # Currently selected item
        self.hover_index = -1  # Currently hovered item
        self.item_height = 50  # Height of each item in the list
        self.visible_items = height // self.item_height  # How many items fit in the view
        self.holding_scroll = False
        self.scroll_start_y = 0
        self.scroll_start_offset = 0

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        # Draw shadow for 3D effect
        shadow_rect = pygame.Rect(self.rect.x + 4, self.rect.y + 4, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=15)

        # Draw main list box
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, self.rect, width=2, border_radius=15)

        # Create a clip area for the list items
        screen.set_clip(self.rect.inflate(-4, -4))

        # Calculate items to display based on scroll offset
        start_idx = min(max(0, self.scroll_offset), max(0, len(self.items) - self.visible_items))
        end_idx = min(start_idx + self.visible_items, len(self.items))

        # Draw visible items
        for i in range(start_idx, end_idx):
            item_rect = pygame.Rect(
                self.rect.x,
                self.rect.y + (i - start_idx) * self.item_height,
                self.rect.width,
                self.item_height
            )

            # Check if mouse is over this item
            if item_rect.collidepoint(mouse_pos):
                self.hover_index = i
                pygame.draw.rect(screen, self.highlight_color, item_rect, border_radius=5)
            elif i == self.selected_index:
                pygame.draw.rect(screen, LIGHT_YELLOW, item_rect, border_radius=5)

            # Draw item text
            text_surf = text_font.render(self.items[i], True, BLACK)
            text_rect = text_surf.get_rect(midleft=(item_rect.x + 20, item_rect.centery))
            screen.blit(text_surf, text_rect)

            # If student icons are available, draw them with a circular background
            if self.data and i < len(student_icons) and student_icons[i]:
                icon = student_icons[i]
                # Draw a circular background for the icon
                icon_bg_rect = pygame.Rect(item_rect.x + 15, item_rect.centery - 20, 40, 40)
                pygame.draw.circle(screen, WHITE, icon_bg_rect.center, 22)
                pygame.draw.circle(screen, BLACK, icon_bg_rect.center, 22, width=2)
                screen.blit(icon, icon_bg_rect)

            # Draw a playful separator with some bounce
            if i < end_idx - 1:
                wave_amplitude = 2  # How tall the waves are
                wave_length = 8  # Distance between wave peaks
                for x in range(item_rect.left + 10, item_rect.right - 10, wave_length):
                    y_pos = item_rect.bottom
                    if (x // wave_length) % 2 == 0:
                        y_pos += wave_amplitude
                    else:
                        y_pos -= wave_amplitude

                    # Draw a small colorful dot instead of a line
                    dot_color = (
                        (x * 13) % 200 + 55,
                        (x * 17) % 200 + 55,
                        (x * 23) % 200 + 55
                    )
                    pygame.draw.circle(screen, dot_color, (x, y_pos), 2)

        # Reset clip area
        screen.set_clip(None)

        # Draw scrollbar if needed
        if len(self.items) > self.visible_items:
            # Calculate scrollbar dimensions
            scrollbar_width = 8
            scrollbar_height = self.rect.height - 20  # Padding from top and bottom
            scrollbar_x = self.rect.right - scrollbar_width - 10
            scrollbar_y = self.rect.y + 10

            # Draw scrollbar background
            scrollbar_bg_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)
            pygame.draw.rect(screen, LIGHT_GRAY, scrollbar_bg_rect, border_radius=4)

            # Calculate the thumb position and size based on visible portion
            visible_ratio = min(1.0, self.visible_items / len(self.items))
            thumb_height = max(20, int(scrollbar_height * visible_ratio))

            # Calculate position based on scroll position
            position_ratio = start_idx / max(1, len(self.items) - self.visible_items)
            thumb_y = scrollbar_y + int(position_ratio * (scrollbar_height - thumb_height))

            # Draw scrollbar thumb
            thumb_rect = pygame.Rect(scrollbar_x, thumb_y, scrollbar_width, thumb_height)
            pygame.draw.rect(screen, BLUE, thumb_rect, border_radius=4)

            # Up/down arrow indicators
            arrow_size = 8
            # Up arrow
            pygame.draw.polygon(screen, BLACK, [
                (scrollbar_x + scrollbar_width // 2, scrollbar_y - 5),
                (scrollbar_x + scrollbar_width // 2 - arrow_size // 2, scrollbar_y - 5 + arrow_size),
                (scrollbar_x + scrollbar_width // 2 + arrow_size // 2, scrollbar_y - 5 + arrow_size)
            ])

            # Down arrow
            pygame.draw.polygon(screen, BLACK, [
                (scrollbar_x + scrollbar_width // 2, scrollbar_y + scrollbar_height + 5),
                (scrollbar_x + scrollbar_width // 2 - arrow_size // 2,
                 scrollbar_y + scrollbar_height + 5 - arrow_size),
                (scrollbar_x + scrollbar_width // 2 + arrow_size // 2,
                 scrollbar_y + scrollbar_height + 5 - arrow_size)
            ])

    def is_clicked(self, pos):
        # Check if click is within scrollable list area
        if not self.rect.collidepoint(pos):
            return False

        # Calculate items to display based on scroll offset
        start_idx = min(max(0, self.scroll_offset), max(0, len(self.items) - self.visible_items))
        end_idx = min(start_idx + self.visible_items, len(self.items))

        # Calculate which item was clicked
        item_y_offset = pos[1] - self.rect.y
        item_index = start_idx + (item_y_offset // self.item_height)

        if 0 <= item_index < len(self.items):
            self.selected_index = item_index
            return True

        return True  # Capture the click even if it didn't hit a specific item

    def handle_event(self, event):
        """Handle scrolling events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 1)
                return True
            elif event.button == 5:  # Scroll down
                self.scroll_offset = min(max(0, len(self.items) - self.visible_items), self.scroll_offset + 1)
                return True
            elif event.button == 1 and self.rect.collidepoint(event.pos):  # Left click
                # Check if click is on scrollbar area
                scrollbar_x = self.rect.right - 18  # Scrollbar area width
                if event.pos[0] > scrollbar_x:
                    self.holding_scroll = True
                    self.scroll_start_y = event.pos[1]
                    self.scroll_start_offset = self.scroll_offset
                    return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.holding_scroll:
                self.holding_scroll = False
                return True

        elif event.type == pygame.MOUSEMOTION:
            if self.holding_scroll:
                # Calculate new scroll position
                scroll_ratio = (event.pos[1] - self.scroll_start_y) / self.rect.height
                scroll_change = int(scroll_ratio * len(self.items))
                self.scroll_offset = min(
                    max(0, len(self.items) - self.visible_items),
                    max(0, self.scroll_start_offset + scroll_change)
                )
                return True

        return False

    def get_selected(self):
        if 0 <= self.selected_index < len(self.items):
            if self.data:
                return self.data[self.selected_index]
            else:
                return self.items[self.selected_index]
        return None


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


def show_login_screen():
    """Main function to display and handle the login screen"""
    # Position variables for UI elements
    logo_y = 120  # Y position for the logo
    welcome_y = 200  # Y position for the welcome text
    instruction_y = 250  # Y position for the instruction text

    # Start background music if loaded
    if music_loaded:
        pygame.mixer.music.play(-1)  # Loop indefinitely

    # Create buttons with better center positioning
    btn_padding = 5  # Space between buttons
    teacher_width = 120
    parent_width = 120
    total_btn_width = teacher_width + parent_width + btn_padding
    btn_start_x = (SCREEN_WIDTH - total_btn_width) // 2

    teacher_button = Button(
        btn_start_x,
        20,
        teacher_width, 40,
        "Teacher", BLUE, LIGHT_BLUE, WHITE
    )

    parent_button = Button(
        btn_start_x + teacher_width + btn_padding,
        20,
        parent_width, 40,
        "Parent", PURPLE, LIGHT_PURPLE, WHITE
    )

    # Create a scrollable list of students
    student_names = []
    for student in students:
        student_names.append(student["name"])

    # Create a ScrollableList instead of a Dropdown
    scroll_list_width = 320
    scroll_list_height = 200  # Taller list that can show multiple items
    scroll_list_x = (SCREEN_WIDTH - scroll_list_width) // 2
    scroll_list_y = 280

    # Create the scrollable list
    student_list = ScrollableList(
        scroll_list_x,
        scroll_list_y,
        scroll_list_width,
        scroll_list_height,
        student_names,
        students  # Pass the original data for reference
    )

    # Position login button below the list
    login_button_width = 150
    login_button_height = 50
    login_button_x = (SCREEN_WIDTH - login_button_width) // 2
    login_button_y = scroll_list_y + scroll_list_height + 20

    login_button = Button(
        login_button_x,
        login_button_y,
        login_button_width,
        login_button_height,
        "Login", GREEN, LIGHT_GREEN, WHITE
    )

    # Create some floating decorative elements
    floating_elements = []

    # Add math symbols as floating elements (changed to relevant skills icons/symbols)
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
    selected_student = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos

                    # Check if teacher button is clicked
                    if teacher_button.is_clicked(mouse_pos):
                        print("Teacher login clicked")
                        # Launch teacher login screen
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "teacher_login.py"])
                        return

                    # Check if parent button is clicked
                    elif parent_button.is_clicked(mouse_pos):
                        print("Parent login clicked")
                        # Launch parent login screen
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "parent_login.py"])
                        return

                    # Check if scroll list is clicked
                    elif student_list.is_clicked(mouse_pos):
                        # Scroll list click is handled internally
                        pass

                    # Check if login button is clicked
                    elif login_button.is_clicked(mouse_pos):
                        selected_student = student_list.get_selected()
                        if selected_student:
                            print(f"Logging in as {selected_student['name']}")
                            # Stop music before moving to main screen
                            if music_loaded:
                                pygame.mixer.music.stop()

                            # Launch main screen with the selected student
                            pygame.quit()
                            # Save student data to a file for the main screen to read
                            with open("current_student.txt", "w") as f:
                                f.write(f"{selected_student['name']}\n")
                                f.write(f"{selected_student['level']}\n")
                                f.write(f"{selected_student['icon']}\n")

                            subprocess.run(["python", "main_screen.py"])
                            return

            # Handle scrolling and other events in the scroll list
            student_list.handle_event(event)

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

        # Draw logo (SkillScape)
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

        # Draw a colorful banner at the BOTTOM of the screen
        footer_height = 80
        footer_rect = pygame.Rect(0, SCREEN_HEIGHT - footer_height, SCREEN_WIDTH, footer_height)

        # Draw a colorful banner
        pygame.draw.rect(screen, CRAYON_ORANGE, footer_rect)

        # Add a playful scalloped top edge to the banner
        scallop_radius = 15
        for x in range(scallop_radius, SCREEN_WIDTH, scallop_radius * 2):
            pygame.draw.circle(screen, CRAYON_ORANGE, (x, footer_rect.top), scallop_radius)

        # Draw a colorful welcome message
        welcome_text = heading_font.render("Welcome to SkillScape!", True, CRAYON_PURPLE)
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

        # Draw instruction with consistent center alignment
        instruction_text = text_font.render("Please select your name to begin:", True, BLACK)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, instruction_y))
        screen.blit(instruction_text, instruction_rect)

        # Draw buttons and scroll list
        teacher_button.draw()
        parent_button.draw()
        student_list.draw()  # Draw the scrollable list instead of dropdown
        login_button.draw()

        pygame.display.flip()
        clock.tick(60)

    # Stop music if we're exiting
    if music_loaded:
        pygame.mixer.music.stop()

    pygame.quit()
    sys.exit()


# Start the program if this file is run directly
if __name__ == "__main__":
    show_login_screen()