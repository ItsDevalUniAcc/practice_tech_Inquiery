import pygame
import sys
import os
import subprocess
import json
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
DARK_GRAY = (100, 100, 100)
DARK_BLUE = (0, 50, 150)
GREEN = (50, 200, 50)
LIGHT_GREEN = (100, 255, 100)
PURPLE = (150, 50, 200)
LIGHT_PURPLE = (180, 100, 240)
ORANGE = (255, 150, 50)
LIGHT_ORANGE = (255, 180, 100)
YELLOW = (255, 230, 0)
RED = (255, 80, 80)
LIGHT_RED = (255, 150, 150)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MemoryMath - Student Details")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont('Arial', 48, bold=True)
heading_font = pygame.font.SysFont('Arial', 36, bold=True)
subheading_font = pygame.font.SysFont('Arial', 28, bold=True)
button_font = pygame.font.SysFont('Arial', 24, bold=True)
text_font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)
table_font = pygame.font.SysFont('Arial', 20)

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


# Dropdown class for level selection
class Dropdown:
    def __init__(self, x, y, width, height, options, selected_index=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_index = selected_index
        self.is_open = False
        self.option_rects = []

        # Create option rects
        for i in range(len(options)):
            self.option_rects.append(pygame.Rect(x, y + (i + 1) * height, width, height))

    def draw(self):
        # Draw selected option
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, width=2)
        text_surf = text_font.render(self.options[self.selected_index], True, BLACK)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surf, text_rect)

        # Draw dropdown arrow
        arrow_points = [
            (self.rect.right - 20, self.rect.centery - 5),
            (self.rect.right - 10, self.rect.centery + 5),
            (self.rect.right - 30, self.rect.centery + 5)
        ]
        pygame.draw.polygon(screen, BLACK, arrow_points)

        # Draw options if dropdown is open
        if self.is_open:
            for i, option_rect in enumerate(self.option_rects):
                pygame.draw.rect(screen, WHITE, option_rect)
                pygame.draw.rect(screen, BLACK, option_rect, width=1)
                option_text = text_font.render(self.options[i], True, BLACK)
                option_text_rect = option_text.get_rect(midleft=(option_rect.x + 10, option_rect.centery))
                screen.blit(option_text, option_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos

                if self.rect.collidepoint(mouse_pos):
                    self.is_open = not self.is_open
                    return False

                if self.is_open:
                    for i, option_rect in enumerate(self.option_rects):
                        if option_rect.collidepoint(mouse_pos):
                            self.selected_index = i
                            self.is_open = False
                            return True
                    # Click outside options closes dropdown
                    self.is_open = False

        return False


# Sample student data - in a real app, this would come from a database
def load_students():
    # For demonstration, create some sample student data
    students = [
        {"name": "Alex", "level": "Level 1 - Beginner",
         "scores": {"Memory Math": 45, "Word Builder": 38, "English Pro": 7, "Football Quiz": 6, "Car Parking": 20}},
        {"name": "Taylor", "level": "Level 2 - Explorer",
         "scores": {"Memory Math": 52, "Word Builder": 45, "English Pro": 8, "Football Quiz": 7, "Car Parking": 30}},
        {"name": "Jordan", "level": "Level 1 - Beginner",
         "scores": {"Memory Math": 35, "Word Builder": 28, "English Pro": 6, "Football Quiz": 5, "Car Parking": 10}},
        {"name": "Casey", "level": "Level 2 - Explorer",
         "scores": {"Memory Math": 48, "Word Builder": 42, "English Pro": 8, "Football Quiz": 7, "Car Parking": 20}},
        {"name": "Morgan", "level": "Level 3 - Master",
         "scores": {"Memory Math": 58, "Word Builder": 52, "English Pro": 9, "Football Quiz": 8, "Car Parking": 30}},
        {"name": "Riley", "level": "Level 1 - Beginner",
         "scores": {"Memory Math": 40, "Word Builder": 30, "English Pro": 6, "Football Quiz": 4, "Car Parking": 20}},
        {"name": "Jamie", "level": "Level 1 - Beginner",
         "scores": {"Memory Math": 38, "Word Builder": 32, "English Pro": 5, "Football Quiz": 6, "Car Parking": 10}}
    ]

    # In a real application, this would load from a database or file
    # try:
    #     with open("students.json", "r") as f:
    #         students = json.load(f)
    # except:
    #     # Fall back to sample data if file doesn't exist
    #     pass

    return students


def save_student_level(student_name, new_level):
    """Save the updated student level."""
    students = load_students()

    # Find the student and update their level
    for student in students:
        if student["name"] == student_name:
            student["level"] = new_level
            break

    # In a real application, save to a database or file
    # try:
    #     with open("students.json", "w") as f:
    #         json.dump(students, f, indent=2)
    #     return True
    # except:
    #     return False

    # For the demo, we'll just return success
    return True


def show_student_details():
    """Display student details screen for teachers."""
    students = load_students()

    # Create buttons
    back_button = Button(20, 20, 100, 40, "Back", ORANGE, LIGHT_ORANGE, WHITE)

    # Create list of student buttons on the left side
    student_buttons = []
    student_btn_y = 190  # Moved down to avoid overlap with heading
    for student in students:
        student_buttons.append(Button(50, student_btn_y, 200, 40,
                                      student["name"], BLUE, LIGHT_BLUE, WHITE))
        student_btn_y += 50

    # Create update level button (initially hidden)
    update_button = Button(550, 450, 120, 40, "Update", GREEN, LIGHT_GREEN, BLACK)

    # Create level dropdown (initially hidden)
    level_options = ["Level 1", "Level 2", "Level 3"]
    level_dropdown = Dropdown(350, 450, 180, 40, level_options)

    # Variables to track selected student
    selected_student = None
    selected_index = -1

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle dropdown events if a student is selected
            if selected_student:
                level_dropdown.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos

                    if back_button.is_clicked(mouse_pos):
                        print("Going back to teacher dashboard")
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "teacher_main.py"])
                        return

                    # Check student buttons
                    for i, btn in enumerate(student_buttons):
                        if btn.is_clicked(mouse_pos):
                            selected_student = students[i]
                            selected_index = i

                            # Set dropdown to current student level - extract level number
                            level_number = int(selected_student["level"].split(" ")[1].split(" ")[0])
                            level_dropdown.selected_index = level_number - 1  # Level 1 = index 0

                    # Check update button
                    if selected_student and update_button.is_clicked(mouse_pos):
                        # Get full level text (with description) while keeping same format
                        level_num = level_dropdown.selected_index + 1

                        # Map level number to full level text
                        level_descriptions = {
                            1: "Level 1 - Beginner",
                            2: "Level 2 - Explorer",
                            3: "Level 3 - Master"
                        }
                        new_level = level_descriptions[level_num]

                        if save_student_level(selected_student["name"], new_level):
                            # Update local data too
                            students[selected_index]["level"] = new_level
                            selected_student["level"] = new_level
                            print(f"Updated {selected_student['name']}'s level to {new_level}")

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
            screen.blit(logo_img, (SCREEN_WIDTH // 2 - logo_img.get_width() // 2, 20))

        # Draw main heading - centered on screen
        heading_text = heading_font.render("Student Details", True, WHITE)
        heading_rect = heading_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(heading_text, heading_rect)

        # Draw student list heading - moved down to avoid overlap
        student_list_text = subheading_font.render("Select a Student:", True, WHITE)
        screen.blit(student_list_text, (50, 150))

        # Draw student details section if a student is selected
        if selected_student:
            # White background box for student details - MADE TALLER
            details_box = pygame.Rect(300, 160, 450, 380)  # Increased height from 340 to 380
            pygame.draw.rect(screen, WHITE, details_box, border_radius=10)
            pygame.draw.rect(screen, BLACK, details_box, width=2, border_radius=10)

            # Draw student details heading - LEFT ALIGNED
            details_heading = subheading_font.render(f"{selected_student['name']}'s Details", True, BLACK)
            details_heading_rect = details_heading.get_rect(midleft=(details_box.left + 30, details_box.top + 30))
            screen.blit(details_heading, details_heading_rect)

            # Draw level in a colored box - right aligned
            level_box = pygame.Rect(details_box.right - 180, details_box.top + 15, 150, 30)
            pygame.draw.rect(screen, BLUE, level_box, border_radius=5)
            pygame.draw.rect(screen, BLACK, level_box, width=1, border_radius=5)

            # Simplified level text (without "Beginner", etc.)
            level_name = selected_student["level"].split(" - ")[0]  # Get just "Level 1", "Level 2", etc.
            level_text = small_font.render(level_name, True, WHITE)
            level_rect = level_text.get_rect(center=(level_box.centerx, level_box.centery))
            screen.blit(level_text, level_rect)

            # Draw horizontal line under heading
            pygame.draw.line(screen, BLACK,
                             (details_box.left + 20, details_box.top + 60),
                             (details_box.right - 20, details_box.top + 60), 2)

            # Draw table for game scores - moved up
            table_top = details_box.top + 80
            table_width = 390
            row_height = 30

            # Table header
            header_rect = pygame.Rect(details_box.left + 30, table_top, table_width, row_height)
            pygame.draw.rect(screen, LIGHT_BLUE, header_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, header_rect, width=1, border_radius=5)

            # Header text - using smaller font
            game_header = small_font.render("Game", True, BLACK)
            score_header = small_font.render("Score", True, BLACK)

            # Position headers with proper spacing
            screen.blit(game_header, (header_rect.x + 20, header_rect.centery - game_header.get_height() // 2))
            screen.blit(score_header, (header_rect.right - 70, header_rect.centery - score_header.get_height() // 2))

            # Table rows - single column layout
            row_y = table_top + row_height
            game_index = 0

            # Display all games in a single column
            for game, score in selected_student["scores"].items():
                row_rect = pygame.Rect(details_box.left + 30, row_y, table_width, row_height)

                # Alternate row colors
                if game_index % 2 == 0:
                    pygame.draw.rect(screen, WHITE, row_rect)
                else:
                    pygame.draw.rect(screen, GRAY, row_rect)

                pygame.draw.rect(screen, BLACK, row_rect, width=1)

                # Game name and score
                game_text = small_font.render(game, True, BLACK)
                score_text = small_font.render(str(score), True, BLACK)

                # Left-align game name, right-align score
                screen.blit(game_text, (row_rect.x + 20, row_rect.centery - game_text.get_height() // 2))
                screen.blit(score_text, (row_rect.right - 70, row_rect.centery - score_text.get_height() // 2))

                row_y += row_height
                game_index += 1

            # Draw total score row
            total_score = sum(selected_student["scores"].values())
            total_row_rect = pygame.Rect(details_box.left + 30, row_y, table_width, row_height)
            pygame.draw.rect(screen, DARK_BLUE, total_row_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, total_row_rect, width=1, border_radius=5)

            total_text = small_font.render("TOTAL", True, WHITE)
            total_score_text = small_font.render(str(total_score), True, WHITE)

            screen.blit(total_text, (total_row_rect.x + 20, total_row_rect.centery - total_text.get_height() // 2))
            screen.blit(total_score_text,
                        (total_row_rect.right - 70, total_row_rect.centery - total_score_text.get_height() // 2))

            # Draw level dropdown and update button directly without label
            # Ensure they stay within the white box
            level_dropdown.rect.x = details_box.left + 50
            level_dropdown.rect.y = row_y + 50  # Position below total score with spacing

            # Make sure dropdown doesn't go outside the box vertically
            max_dropdown_y = details_box.bottom - 50
            if level_dropdown.rect.y > max_dropdown_y:
                level_dropdown.rect.y = max_dropdown_y

            # Update option rects for dropdown - limited to stay inside box
            for i, option_rect in enumerate(level_dropdown.option_rects):
                option_rect.x = level_dropdown.rect.x
                option_rect.y = level_dropdown.rect.y + (i + 1) * level_dropdown.rect.height

            # Update button position - next to dropdown
            update_button.rect.x = level_dropdown.rect.right + 30
            update_button.rect.y = level_dropdown.rect.y

            # Ensure update button stays within the white box
            if update_button.rect.right > details_box.right - 30:
                update_button.rect.x = details_box.right - update_button.rect.width - 30

            # Draw level dropdown
            level_dropdown.draw()

            # Draw update button
            update_button.draw()
        else:
            # Draw instruction when no student is selected
            select_text = text_font.render("← Please select a student to view details", True, WHITE)
            select_rect = select_text.get_rect(center=(SCREEN_WIDTH - 250, 250))
            screen.blit(select_text, select_rect)

        # Draw student list
        for btn in student_buttons:
            btn.draw()

        # Draw back button
        back_button.draw()

        pygame.display.flip()
        clock.tick(60)

    # Stop music and quit if window is closed
    if music_loaded:
        pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


# Start the program if this file is run directly
if __name__ == "__main__":
    show_student_details()