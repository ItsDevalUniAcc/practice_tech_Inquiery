import pygame
import sys

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


def show_instructions(screen):
    """
    Display the game instructions screen with scrolling capability

    Parameters:
    screen (pygame.Surface): The main game display surface

    Returns:
    bool: Whether to start the game (True) or quit (False)
    """
    # Prepare fonts
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    heading_font = pygame.font.SysFont('Arial', 32, bold=True)
    font = pygame.font.SysFont('Arial', 24)
    small_font = pygame.font.SysFont('Arial', 20)

    # Button dimensions
    button_width = 180
    button_height = 60
    button_y = 520

    # Define play button
    play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, button_y, button_width, button_height)

    # Scrolling variables
    scroll_y = 0
    scroll_speed = 20
    max_scroll = 0  # Will be set after content is created

    # Scroll bar dimensions
    scroll_bar_width = 20
    scroll_bar_height = 360
    scroll_bar_x = SCREEN_WIDTH - 70
    scroll_bar_y = 120

    # Scroll button dimensions and initial position
    scroll_button_width = scroll_bar_width
    scroll_button_height = 60  # Adjust based on content
    scroll_button_x = scroll_bar_x
    scroll_button_y = scroll_bar_y

    # Dragging state
    dragging_scroll = False

    # Create a surface for the instructions content
    # This will be larger than the visible area to allow scrolling
    content_width = SCREEN_WIDTH - 160  # Adjust for padding and scroll bar
    content_height = 600  # Make it shorter since we only need how to play
    content_surface = pygame.Surface((content_width, content_height))
    content_surface.fill(WHITE)

    # Visible area of the content (viewport)
    viewport_rect = pygame.Rect(70, 120, content_width, 360)

    # Render all the content onto the content surface
    # How to Play heading
    how_to_play_text = heading_font.render("How to Play", True, BLACK)
    how_to_play_rect = how_to_play_text.get_rect(center=(content_width // 2, 30))
    content_surface.blit(how_to_play_text, how_to_play_rect)

    # Horizontal line
    pygame.draw.line(content_surface, BLACK, (20, 60), (content_width - 20, 60), 2)

    # Game instructions with better spacing
    instructions = [
        "Find matching pairs of cards with equal answers.",
        "Each card has a math problem on it, like '3+2' or '10-5'.",
        "Click on a card to flip it and see the math problem.",
        "Try to find two cards that have the same answer (like '3+2' and '6-1').",
        "If they match, the cards stay face-up and turn green.",
        "If they don't match, the cards flip back over.",
        "Find all 6 matching pairs to win the game!",
        "",
        "Scoring Rules:",
        "• +10 points for each matching pair you find",
        "• First 5 card flips are free",
        "• -1 point for each flip after the first 5",
        "• -1 point for every 10 seconds that pass"
    ]

    y_pos = 80
    line_spacing = 36  # Increased spacing between lines

    for line in instructions:
        text = font.render(line, True, BLACK)
        content_surface.blit(text, (30, y_pos))
        y_pos += line_spacing

    # Set the maximum scroll value (content height - viewport height)
    max_scroll = max(0, y_pos - viewport_rect.height)

    # Calculate scroll button height based on content
    visible_ratio = min(1.0, viewport_rect.height / y_pos)
    scroll_button_height = max(30, int(scroll_bar_height * visible_ratio))

    # Main loop for the instructions screen
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()

                    # Check for scroll bar dragging
                    scroll_button_rect = pygame.Rect(scroll_button_x, scroll_button_y,
                                                     scroll_button_width, scroll_button_height)
                    if scroll_button_rect.collidepoint(mouse_pos):
                        dragging_scroll = True
                        drag_start_y = mouse_pos[1]
                        initial_scroll = scroll_y
                    # Check if play button is clicked
                    elif play_button_rect.collidepoint(mouse_pos):
                        return True  # This line is important - it returns True when Play Now is clicked
                    # Check if clicked inside viewport for scrolling
                    elif viewport_rect.collidepoint(mouse_pos):
                        # Don't handle clicks on content for now
                        pass

                elif event.button == 4:  # Mouse wheel up
                    scroll_y = max(0, scroll_y - scroll_speed)
                elif event.button == 5:  # Mouse wheel down
                    scroll_y = min(max_scroll, scroll_y + scroll_speed)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging_scroll = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_scroll:
                    # Calculate new scroll position based on mouse movement
                    mouse_pos = pygame.mouse.get_pos()
                    drag_offset = mouse_pos[1] - drag_start_y
                    scroll_ratio = scroll_bar_height / max(1, max_scroll)
                    scroll_y = min(max_scroll, max(0, initial_scroll + drag_offset / scroll_ratio))

        # Calculate scroll button position based on scroll_y
        if max_scroll > 0:
            scroll_progress = scroll_y / max_scroll
            scroll_button_y = scroll_bar_y + scroll_progress * (scroll_bar_height - scroll_button_height)

        # Draw gradient background
        for y in range(SCREEN_HEIGHT):
            color = (
                int(DARK_BLUE[0] + (LIGHT_BLUE[0] - DARK_BLUE[0]) * y / SCREEN_HEIGHT),
                int(DARK_BLUE[1] + (LIGHT_BLUE[1] - DARK_BLUE[1]) * y / SCREEN_HEIGHT),
                int(DARK_BLUE[2] + (LIGHT_BLUE[2] - DARK_BLUE[2]) * y / SCREEN_HEIGHT)
            )
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Title
        title_text = title_font.render("Math Card Matching Game", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        # Draw the background box for the viewport
        instruction_box = pygame.Rect(50, 100, SCREEN_WIDTH - 100, 400)
        pygame.draw.rect(screen, WHITE, instruction_box, border_radius=15)
        pygame.draw.rect(screen, BLACK, instruction_box, width=2, border_radius=15)

        # Draw the content surface at the scrolled position
        # Create a subsurface of the content corresponding to the current scroll position
        subsurface_rect = pygame.Rect(0, scroll_y, viewport_rect.width, viewport_rect.height)
        # Make sure we don't try to get a subsurface outside the content surface
        if subsurface_rect.bottom > content_surface.get_height():
            subsurface_rect.bottom = content_surface.get_height()
            subsurface_rect.top = max(0, subsurface_rect.bottom - viewport_rect.height)

        # Blit the visible portion of the content to the screen
        screen.blit(content_surface, viewport_rect, subsurface_rect)

        # Draw scroll bar background
        pygame.draw.rect(screen, SCROLL_BAR_COLOR,
                         (scroll_bar_x, scroll_bar_y, scroll_bar_width, scroll_bar_height))

        # Draw scroll button
        pygame.draw.rect(screen, SCROLL_BUTTON_COLOR,
                         (scroll_button_x, scroll_button_y, scroll_button_width, scroll_button_height),
                         border_radius=5)

        # Draw up and down arrows on scroll button
        arrow_color = WHITE
        # Up arrow
        pygame.draw.polygon(screen, arrow_color, [
            (scroll_button_x + scroll_button_width // 2, scroll_button_y + 5),
            (scroll_button_x + 5, scroll_button_y + 15),
            (scroll_button_x + scroll_button_width - 5, scroll_button_y + 15)
        ])

        # Down arrow
        pygame.draw.polygon(screen, arrow_color, [
            (scroll_button_x + scroll_button_width // 2, scroll_button_y + scroll_button_height - 5),
            (scroll_button_x + 5, scroll_button_y + scroll_button_height - 15),
            (scroll_button_x + scroll_button_width - 5, scroll_button_y + scroll_button_height - 15)
        ])

        # Play button
        mouse_pos = pygame.mouse.get_pos()
        button_color = (100, 255, 100) if play_button_rect.collidepoint(mouse_pos) else GREEN

        pygame.draw.rect(screen, button_color, play_button_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, play_button_rect, width=2, border_radius=10)

        play_text = heading_font.render("Play Now", True, BLACK)
        play_text_rect = play_text.get_rect(center=play_button_rect.center)
        screen.blit(play_text, play_text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return False

    return False


# If this file is run directly, show instruction screen and launch the game when ready
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Instructions Screen")

    result = show_instructions(screen)
    print(f"Start game: {result}")  # Debug output to confirm return value

    if result:
        # User clicked Play Now, launch the card game
        pygame.quit()  # Close this window first
        import subprocess

        subprocess.run(["python", "memorymathl1.py"])  # Start the card game
    else:
        # User chose to quit
        pygame.quit()
        sys.exit()