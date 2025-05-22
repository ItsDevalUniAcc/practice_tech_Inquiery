import pygame
import sys
import os
import subprocess
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
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MemoryMath - Teacher Rankings View")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont('Arial', 48, bold=True)
heading_font = pygame.font.SysFont('Arial', 36, bold=True)
button_font = pygame.font.SysFont('Arial', 24, bold=True)
text_font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)
table_font = pygame.font.SysFont('Arial', 20)
rank_font = pygame.font.SysFont('Arial', 22, bold=True)

# Global variables for resources
background_img = None
logo_img = None
medal_imgs = [None, None, None]  # Gold, Silver, Bronze
images_loaded = False

# Get teacher username
teacher_username = "Teacher"
try:
    if os.path.exists("current_teacher.txt"):
        with open("current_teacher.txt", "r") as f:
            teacher_username = f.read().strip()
except Exception as e:
    print(f"Error loading teacher data: {e}")

# Sample student data - in a real app, this would come from a database
# We'll create 3 levels of students
level1_students = [
    {"name": "Alex", "score": random.randint(30, 100), "time": random.randint(30, 120)},
    {"name": "Taylor", "score": random.randint(30, 100), "time": random.randint(30, 120)},
    {"name": "Jordan", "score": random.randint(30, 100), "time": random.randint(30, 120)},
    {"name": "Casey", "score": random.randint(30, 100), "time": random.randint(30, 120)},
    {"name": "Morgan", "score": random.randint(30, 100), "time": random.randint(30, 120)},
    {"name": "Riley", "score": random.randint(30, 100), "time": random.randint(30, 120)},
    {"name": "Jamie", "score": random.randint(30, 100), "time": random.randint(30, 120)}
]

level2_students = [
    {"name": "Taylor", "score": random.randint(40, 120), "time": random.randint(25, 100)},
    {"name": "Casey", "score": random.randint(40, 120), "time": random.randint(25, 100)},
    {"name": "Avery", "score": random.randint(40, 120), "time": random.randint(25, 100)},
    {"name": "Quinn", "score": random.randint(40, 120), "time": random.randint(25, 100)},
    {"name": "Rowan", "score": random.randint(40, 120), "time": random.randint(25, 100)}
]

level3_students = [
    {"name": "Morgan", "score": random.randint(60, 150), "time": random.randint(20, 90)},
    {"name": "Skyler", "score": random.randint(60, 150), "time": random.randint(20, 90)},
    {"name": "Dakota", "score": random.randint(60, 150), "time": random.randint(20, 90)},
    {"name": "Jordan", "score": random.randint(60, 150), "time": random.randint(20, 90)}
]

# Sort students by score (higher is better), with time as tiebreaker (lower is better)
level1_students.sort(key=lambda x: (x["score"], -x["time"]), reverse=True)
level2_students.sort(key=lambda x: (x["score"], -x["time"]), reverse=True)
level3_students.sort(key=lambda x: (x["score"], -x["time"]), reverse=True)

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

    # Load medal images
    medal_paths = ['gold_medal.png', 'silver_medal.png', 'bronze_medal.png']
    for i, path in enumerate(medal_paths):
        if os.path.exists(path):
            medal_imgs[i] = pygame.image.load(path)
            medal_imgs[i] = pygame.transform.scale(medal_imgs[i], (30, 30))

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
        print("Loaded rankings background music")
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


# Tab class for level selection with rounded corners and different colors
class TabButton:
    def __init__(self, x, y, width, height, text, index):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.index = index
        self.active = False

        # Assign different colors based on level
        if index == 0:  # Level 1
            self.color = BLUE
            self.active_color = LIGHT_BLUE
        elif index == 1:  # Level 2
            self.color = GREEN
            self.active_color = LIGHT_GREEN
        else:  # Level 3
            self.color = PURPLE
            self.active_color = LIGHT_PURPLE

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.active_color, self.rect, border_radius=10)
            text_color = BLACK
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
            text_color = WHITE

        pygame.draw.rect(screen, BLACK, self.rect, width=2, border_radius=10)

        text_surf = button_font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def draw_medal(rank, x, y):
    """Draw a medal icon for top 3 ranks"""
    if rank < 1 or rank > 3:
        return

    medal_index = rank - 1
    if medal_imgs[medal_index]:
        screen.blit(medal_imgs[medal_index], (x, y))
    else:
        # Fallback colors if medal images not available
        medal_colors = [GOLD, SILVER, BRONZE]
        pygame.draw.circle(screen, medal_colors[medal_index], (x + 15, y + 15), 15)
        medal_text = rank_font.render(str(rank), True, BLACK)
        medal_rect = medal_text.get_rect(center=(x + 15, y + 15))
        screen.blit(medal_text, medal_rect)


def show_teacher_rankings():
    """Display student rankings for teachers to view"""
    # Create buttons
    back_button = Button(20, 20, 100, 40, "Back", ORANGE, LIGHT_ORANGE, WHITE)
    export_button = Button(SCREEN_WIDTH - 120, 20, 100, 40, "Export", GREEN, LIGHT_GREEN, WHITE)
    info_button = Button(SCREEN_WIDTH - 70, 140, 40, 40, "?", YELLOW, LIGHT_ORANGE, BLACK)

    # Variables for export notification
    export_notification = False
    export_notification_time = 0
    NOTIFICATION_DURATION = 2000  # 2 seconds

    # Variable to track info popup state
    show_info_popup = False

    # Create tabs for different levels - with improved design
    tab_width = 160
    tab_height = 40  # Reduced height
    tab_spacing = 10
    tabs_y = 140  # Moved up

    # Calculate total width of all tabs and spacing
    total_tabs_width = tab_width * 3 + tab_spacing * 2
    tabs_start_x = SCREEN_WIDTH // 2 - total_tabs_width // 2

    tabs = [
        TabButton(tabs_start_x, tabs_y, tab_width, tab_height, "Level 1", 0),
        TabButton(tabs_start_x + tab_width + tab_spacing, tabs_y, tab_width, tab_height, "Level 2", 1),
        TabButton(tabs_start_x + (tab_width + tab_spacing) * 2, tabs_y, tab_width, tab_height, "Level 3", 2)
    ]

    # Set the active tab
    active_tab = 0
    tabs[active_tab].active = True

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos

                    if back_button.is_clicked(mouse_pos):
                        print("Going back to teacher dashboard")
                        # Return to teacher dashboard
                        if music_loaded:
                            pygame.mixer.music.stop()
                        pygame.quit()
                        subprocess.run(["python", "teacher_main.py"])
                        sys.exit()  # Changed return to sys.exit()

                    if export_button.is_clicked(mouse_pos):
                        # Export the rankings to the desktop
                        print("Exporting rankings to desktop")

                        try:
                            # Get path to desktop
                            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                            export_filename = f"rankings_level{active_tab + 1}.txt"
                            export_path = os.path.join(desktop_path, export_filename)

                            with open(export_path, "w") as f:
                                f.write(f"# MemoryMath Level {active_tab + 1} Rankings\n")
                                f.write(f"# Generated on {pygame.time.get_ticks() // 1000} seconds into session\n\n")

                                students = [level1_students, level2_students, level3_students][active_tab]
                                for i, student in enumerate(students):
                                    minutes = student["time"] // 60
                                    seconds = student["time"] % 60
                                    time_str = f"{minutes}:{seconds:02d}"
                                    f.write(
                                        f"{i + 1}. {student['name']} - Score: {student['score']}, Time: {time_str}\n")

                            # Visual feedback for successful export
                            print(f"Rankings exported to {export_path}")

                            # Create a temporary notification
                            export_notification = True
                            export_notification_time = pygame.time.get_ticks()
                        except Exception as e:
                            print(f"Failed to export rankings: {e}")
                            export_notification = False

                    if info_button.is_clicked(mouse_pos):
                        # Toggle info popup
                        show_info_popup = not show_info_popup

                    # Check tab clicks
                    for i, tab in enumerate(tabs):
                        if tab.is_clicked(mouse_pos):
                            # Deactivate all tabs
                            for t in tabs:
                                t.active = False
                            # Activate clicked tab
                            tab.active = True
                            active_tab = i

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
            screen.blit(logo_img, (SCREEN_WIDTH // 2 - logo_img.get_width() // 2, 10))  # Moved up

        # Teacher username element removed as requested

        # Draw rankings heading with attractive orange background bar
        heading_bar_width = 550
        heading_bar_height = 50  # Reduced height
        heading_bar_rect = pygame.Rect(SCREEN_WIDTH // 2 - heading_bar_width // 2, 75, heading_bar_width,
                                       heading_bar_height)  # Moved up

        # Draw an orange background with rounded corners
        pygame.draw.rect(screen, ORANGE, heading_bar_rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, heading_bar_rect, width=2, border_radius=15)

        # Draw rankings text
        rankings_text = heading_font.render("Student Rankings", True, WHITE)
        rankings_rect = rankings_text.get_rect(center=(heading_bar_rect.centerx, heading_bar_rect.centery))
        screen.blit(rankings_text, rankings_rect)

        # Draw tabs
        for tab in tabs:
            tab.draw()

        # Draw info button
        info_button.draw()

        # Draw rankings table
        # Table header
        table_width = 600
        table_height = 40
        header_rect = pygame.Rect(SCREEN_WIDTH // 2 - table_width // 2, 200, table_width, table_height)  # Moved up
        pygame.draw.rect(screen, DARK_BLUE, header_rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, header_rect, width=1, border_radius=8)

        # Header columns
        col_widths = [60, 350, 100, 90]  # Rank, Name, Score, Time
        col_x = header_rect.x

        header_texts = ["Rank", "Student Name", "Score", "Time"]
        for i, text in enumerate(header_texts):
            text_surf = table_font.render(text, True, WHITE)
            if i == 0:  # Center rank
                text_rect = text_surf.get_rect(center=(col_x + col_widths[i] // 2, header_rect.centery))
            elif i == 1:  # Left align name
                text_rect = text_surf.get_rect(midleft=(col_x + 10, header_rect.centery))
            else:  # Center score and time
                text_rect = text_surf.get_rect(center=(col_x + col_widths[i] // 2, header_rect.centery))

            screen.blit(text_surf, text_rect)
            col_x += col_widths[i]

        # Table rows based on active tab
        students_list = [level1_students, level2_students, level3_students][active_tab]
        row_y = header_rect.bottom

        for i, student in enumerate(students_list):
            if i >= 10:  # Show max 10 rows
                break

            row_rect = pygame.Rect(header_rect.x, row_y, table_width, table_height)

            # Alternate row colors
            if i % 2 == 0:
                pygame.draw.rect(screen, WHITE, row_rect)
            else:
                pygame.draw.rect(screen, LIGHT_BLUE, row_rect)

            pygame.draw.rect(screen, BLACK, row_rect, width=1)

            # Draw row data
            col_x = row_rect.x

            # Rank column with medal for top 3
            rank_text = table_font.render(str(i + 1), True, BLACK)
            rank_rect = rank_text.get_rect(center=(col_x + col_widths[0] // 2, row_rect.centery))
            screen.blit(rank_text, rank_rect)

            # Draw medal if top 3
            if i < 3:
                draw_medal(i + 1, col_x + 10, row_rect.y + 5)

            col_x += col_widths[0]

            # Name column
            name_text = table_font.render(student["name"], True, BLACK)
            name_rect = name_text.get_rect(midleft=(col_x + 10, row_rect.centery))
            screen.blit(name_text, name_rect)
            col_x += col_widths[1]

            # Score column
            score_text = table_font.render(str(student["score"]), True, BLACK)
            score_rect = score_text.get_rect(center=(col_x + col_widths[2] // 2, row_rect.centery))
            screen.blit(score_text, score_rect)
            col_x += col_widths[2]

            # Time column (formatted as mm:ss)
            minutes = student["time"] // 60
            seconds = student["time"] % 60
            time_text = table_font.render(f"{minutes}:{seconds:02d}", True, BLACK)
            time_rect = time_text.get_rect(center=(col_x + col_widths[3] // 2, row_rect.centery))
            screen.blit(time_text, time_rect)

            row_y += table_height

        # Draw note if there are no students for this level
        if len(students_list) == 0:
            no_data_text = text_font.render("No rankings data available for this level", True, WHITE)
            no_data_rect = no_data_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
            screen.blit(no_data_text, no_data_rect)

        # Draw notes at bottom for teachers in an attractive box - made smaller
        note_box = pygame.Rect(SCREEN_WIDTH // 2 - 350, row_y + 10, 700, 50)  # Reduced height, moved up
        pygame.draw.rect(screen, DARK_BLUE, note_box, border_radius=10, width=0)
        pygame.draw.rect(screen, BLACK, note_box, border_radius=10, width=2)

        note_text = small_font.render("Rankings are based on highest score. Time is used as a tiebreaker.", True, WHITE)
        note_rect = note_text.get_rect(midleft=(note_box.left + 20, note_box.centery - 10))  # Left-aligned
        screen.blit(note_text, note_rect)

        teacher_note = small_font.render("Use the 'Export' button to save rankings to desktop.", True, YELLOW)
        teacher_note_rect = teacher_note.get_rect(midleft=(note_box.left + 20, note_box.centery + 10))  # Left-aligned
        screen.blit(teacher_note, teacher_note_rect)

        # Draw back and export buttons
        back_button.draw()
        export_button.draw()

        # Display export notification if active
        if export_notification:
            current_time = pygame.time.get_ticks()
            if current_time - export_notification_time < NOTIFICATION_DURATION:
                # Create notification with shadow
                notify_width = 300
                notify_height = 60
                notify_rect = pygame.Rect(SCREEN_WIDTH // 2 - notify_width // 2,
                                          SCREEN_HEIGHT // 4,
                                          notify_width, notify_height)

                # Shadow
                shadow_offset = 5
                shadow_rect = pygame.Rect(notify_rect.left + shadow_offset, notify_rect.top + shadow_offset,
                                          notify_width, notify_height)
                pygame.draw.rect(screen, (20, 20, 20), shadow_rect, border_radius=10)

                # Notification
                pygame.draw.rect(screen, GREEN, notify_rect, border_radius=10)
                pygame.draw.rect(screen, BLACK, notify_rect, width=2, border_radius=10)

                # Text
                notify_text = text_font.render("Rankings Exported!", True, WHITE)
                notify_rect_text = notify_text.get_rect(center=(notify_rect.centerx, notify_rect.centery - 10))
                screen.blit(notify_text, notify_rect_text)

                # Subtext
                sub_text = small_font.render("File saved to desktop", True, WHITE)
                sub_rect = sub_text.get_rect(center=(notify_rect.centerx, notify_rect.centery + 15))
                screen.blit(sub_text, sub_rect)
            else:
                export_notification = False

        # Draw info popup if active
        if show_info_popup:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Black with 70% opacity
            screen.blit(overlay, (0, 0))

            # Info popup box
            popup_width = 500
            popup_height = 250
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
            popup_title = heading_font.render("Rankings Information", True, BLUE)
            popup_title_rect = popup_title.get_rect(center=(popup_rect.centerx, popup_rect.top + 30))
            screen.blit(popup_title, popup_title_rect)

            # Horizontal line
            pygame.draw.line(screen, LIGHT_BLUE,
                             (popup_rect.left + 20, popup_rect.top + 60),
                             (popup_rect.right - 20, popup_rect.top + 60), 2)

            # Ranking explanation text for teachers
            explanation_lines = [
                "Rankings are based on the highest score achieved by each student.",
                "Time is used as a tiebreaker when students have the same score.",
                "Students are automatically sorted across all three difficulty levels.",
                "The 'Export' button allows you to save these rankings as a text file.",
                "Use this data to track student progress and identify learning trends."
            ]

            # Display explanation text
            for i, line in enumerate(explanation_lines):
                line_text = small_font.render(line, True, BLACK)
                y_pos = popup_rect.top + 90 + i * 25
                line_rect = line_text.get_rect(midleft=(popup_rect.left + 30, y_pos))
                screen.blit(line_text, line_rect)

            # Close instruction
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
    show_teacher_rankings()