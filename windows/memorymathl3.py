import pygame
import random
import sys
import time
import subprocess
import os
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 120
MARGIN = 20
ROWS = 4  # Changed from 3 to 4 rows
COLS = 4  # Kept as 4 columns
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (20, 60, 120)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (50, 200, 50)
LIGHT_GREEN = (100, 255, 100)
YELLOW = (255, 230, 0)
PURPLE = (150, 50, 200)
LIGHT_PURPLE = (180, 100, 240)
PINK = (255, 100, 200)
LIGHT_PINK = (255, 150, 220)
ORANGE = (255, 150, 0)
LIGHT_ORANGE = (255, 180, 50)
RED = (255, 50, 50)
LIGHT_RED = (255, 100, 100)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arithmetic Card Matching Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24, bold=True)
big_font = pygame.font.SysFont('Arial', 36, bold=True)
small_font = pygame.font.SysFont('Arial', 18)

# Global variables for resources
card_flip_sound = None
match_sound = None
error_sound = None
success_sound = None
sounds_loaded = False
music_loaded = False

# Try to load sound effects and music
try:
    pygame.mixer.init()

    # Sound effects
    if os.path.exists("card_flip.wav"):
        card_flip_sound = pygame.mixer.Sound("card_flip.wav")
        print("Loaded card_flip.wav")

    if os.path.exists("memorymath_success.mp3"):
        match_sound = pygame.mixer.Sound("memorymath_success.mp3")
        print("Loaded memorymath_success.mp3")

    if os.path.exists("memorymath_error.mp3"):
        error_sound = pygame.mixer.Sound("memorymath_error.mp3")
        print("Loaded memorymath_error.mp3")

    if os.path.exists("success_sound.wav"):
        success_sound = pygame.mixer.Sound("success_sound.wav")
        print("Loaded success_sound.wav")

    # Background music
    if os.path.exists("memorymath_bg.mp3"):
        pygame.mixer.music.load("memorymath_bg.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
        music_loaded = True
        print("Loaded background music")

    sounds_loaded = True
    print("Successfully initialized sound system.")
except Exception as e:
    print(f"Warning: Could not initialize sound. Playing without sound effects. Error: {e}")
    sounds_loaded = False
    music_loaded = False


# Create pairs of equivalent arithmetic expressions
def create_arithmetic_pairs():
    # Each tuple contains (problem_text, answer)
    possible_problems = [
        ("45 + 30", 75),
        ("90 - 25", 65),
        ("8 × 7", 56),
        ("96 ÷ 4", 24),
        ("62 + 18", 80),
        ("100 - 37", 63),
        ("9 × 6", 54),
        ("84 ÷ 2", 42),
        ("33 + 44", 77),
        ("70 - 28", 42),
        ("12 × 5", 60),
        ("81 ÷ 3", 27),
        ("47 + 36", 83),
        ("88 - 19", 69),
        ("7 × 9", 63),
        ("72 ÷ 3", 24),

    ]

    # Shuffle the problems
    random.shuffle(possible_problems)

    # Select 8 answers (for 8 pairs) instead of 6
    used_answers = []
    pairs = []

    for problem in possible_problems:
        if len(pairs) >= 16:  # We need 16 cards total (8 pairs)
            break

        if problem[1] not in used_answers:
            matching_problems = [p for p in possible_problems if p[1] == problem[1] and p[0] != problem[0]]
            if matching_problems:
                # Add this problem and a matching one
                match = random.choice(matching_problems)
                pairs.append((problem[0], problem[1]))
                pairs.append((match[0], problem[1]))
                used_answers.append(problem[1])

    # If we couldn't find enough pairs with different answers, fill with duplicates
    remaining_pairs_needed = 8 - len(used_answers)  # Need 8 pairs total
    if remaining_pairs_needed > 0:
        for _ in range(remaining_pairs_needed):
            answer = random.randint(2, 20)
            pairs.append((f"{answer} + 0", answer))
            pairs.append((f"{answer} - 0", answer))

    return pairs


# Enhanced Card class with beautiful visuals
class Card:
    def __init__(self, x, y, width, height, problem, answer):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.problem = problem
        self.answer = answer
        self.is_flipped = False
        self.is_matched = False
        self.rect = pygame.Rect(x, y, width, height)
        self.flip_progress = 0
        self.animating = False
        self.flip_speed = 15

        # Generate a visually appealing color based on the answer value
        # This creates a unique but consistent color for each card pair
        hue = (answer * 25) % 360
        self.color = self.hsv_to_rgb(hue, 0.7, 0.8)
        self.light_color = self.hsv_to_rgb(hue, 0.6, 0.9)

    def hsv_to_rgb(self, h, s, v):
        # Convert HSV color to RGB
        h = h / 360.0
        if s == 0.0:
            return (int(v * 255), int(v * 255), int(v * 255))

        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))

        i = i % 6
        if i == 0:
            return (int(v * 255), int(t * 255), int(p * 255))
        elif i == 1:
            return (int(q * 255), int(v * 255), int(p * 255))
        elif i == 2:
            return (int(p * 255), int(v * 255), int(t * 255))
        elif i == 3:
            return (int(p * 255), int(q * 255), int(v * 255))
        elif i == 4:
            return (int(t * 255), int(p * 255), int(v * 255))
        else:
            return (int(v * 255), int(p * 255), int(q * 255))

    def draw(self):
        # Handle flip animation
        if self.animating:
            self.flip_progress += self.flip_speed
            if self.flip_progress >= 180:
                self.flip_progress = 0
                self.animating = False

            # Calculate scale factor for flip animation (width changes during flip)
            scale_factor = abs(math.cos(math.radians(self.flip_progress)))

            # Ensure width doesn't go below 1 pixel to avoid errors
            width = max(1, int(self.width * scale_factor))
            height = self.height

            # Center the card during animation
            x_offset = (self.width - width) // 2
            adjusted_x = self.x + x_offset

            # First half of animation shows back/front, second half shows front/back
            if self.flip_progress < 90:
                if self.is_flipped:  # Flipping from back to front
                    self.draw_card_back(adjusted_x, self.y, width, height)
                else:  # Flipping from front to back
                    self.draw_card_front(adjusted_x, self.y, width, height)
            else:
                if self.is_flipped:  # Flipping from back to front
                    self.draw_card_front(adjusted_x, self.y, width, height)
                else:  # Flipping from front to back
                    self.draw_card_back(adjusted_x, self.y, width, height)
        else:
            # Normal drawing (no animation)
            if self.is_matched:
                self.draw_matched_card()
            elif self.is_flipped:
                self.draw_card_front(self.x, self.y, self.width, self.height)
            else:
                self.draw_card_back(self.x, self.y, self.width, self.height)

    def draw_card_front(self, x, y, width, height):
        # Enhanced card front with gradient effect
        rect = pygame.Rect(x, y, width, height)

        # Draw shadow (only if width is not too small during animation)
        if width > 10:
            shadow_offset = 4
            shadow_rect = pygame.Rect(x + shadow_offset, y + shadow_offset, width, height)
            pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=10)

        # Draw card with gradient effect
        for i in range(5):
            blend_factor = i / 5
            color = (
                int(self.color[0] * (1 - blend_factor) + self.light_color[0] * blend_factor),
                int(self.color[1] * (1 - blend_factor) + self.light_color[1] * blend_factor),
                int(self.color[2] * (1 - blend_factor) + self.light_color[2] * blend_factor)
            )
            inner_rect = pygame.Rect(x, y + i * height // 5, width, height // 5)
            pygame.draw.rect(screen, color, inner_rect, border_radius=10)

        # Draw border
        pygame.draw.rect(screen, BLACK, rect, width=2, border_radius=10)

        # Create background for text (making sure dimensions are positive)
        text_bg_width = max(1, width - 20)  # Ensure width is at least 1
        text_bg_height = 40

        # Skip text rendering if the card is too narrow during animation
        if text_bg_width < 10:
            return

        text_bg_rect = pygame.Rect(
            x + (width - text_bg_width) // 2,
            y + (height - text_bg_height) // 2,
            text_bg_width,
            text_bg_height
        )

        # Draw text background with slightly transparent white
        s = pygame.Surface((text_bg_width, text_bg_height), pygame.SRCALPHA)
        s.fill((255, 255, 255, 220))  # White with alpha
        screen.blit(s, text_bg_rect)
        pygame.draw.rect(screen, BLACK, text_bg_rect, width=1, border_radius=5)

        # Draw problem text
        text = font.render(self.problem, True, BLACK)
        text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text, text_rect)

    def draw_card_back(self, x, y, width, height):
        # Enhanced card back with decorative elements
        rect = pygame.Rect(x, y, width, height)

        # Draw shadow (only if width is not too small during animation)
        if width > 10:
            shadow_offset = 4
            shadow_rect = pygame.Rect(x + shadow_offset, y + shadow_offset, width, height)
            pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=10)

        # Draw main background with gradient
        for i in range(5):
            blend_factor = i / 5
            color = (
                int(DARK_BLUE[0] * (1 - blend_factor) + BLUE[0] * blend_factor),
                int(DARK_BLUE[1] * (1 - blend_factor) + BLUE[1] * blend_factor),
                int(DARK_BLUE[2] * (1 - blend_factor) + BLUE[2] * blend_factor)
            )
            inner_rect = pygame.Rect(x, y + i * height // 5, width, height // 5)
            pygame.draw.rect(screen, color, inner_rect, border_radius=10)

        # Draw a border around the card
        pygame.draw.rect(screen, BLACK, rect, width=2, border_radius=10)

        # Skip decorative elements if card is too narrow during animation
        if width < 20:
            return

        # Add decorative pattern
        # Inner border
        margin = 10
        inner_rect = pygame.Rect(x + margin, y + margin, width - 2 * margin, height - 2 * margin)
        pygame.draw.rect(screen, LIGHT_BLUE, inner_rect, width=2, border_radius=5)

        # Draw "?" in the center
        q_text = big_font.render("?", True, WHITE)
        q_rect = q_text.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(q_text, q_rect)

    def draw_matched_card(self):
        # Special appearance for matched cards
        # Draw the card front with green tint
        self.draw_card_front(self.x, self.y, self.width, self.height)

        # Add green overlay to indicate matched status
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        s.fill((100, 255, 100, 128))  # Semi-transparent green
        screen.blit(s, (self.x, self.y))

        # Add a small checkmark
        check_text = font.render("✓", True, GREEN)
        check_rect = check_text.get_rect(center=(self.x + self.width - 20, self.y + self.height - 20))
        screen.blit(check_text, check_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) and not self.is_matched and not self.animating

    def flip(self):
        if not self.is_matched and not self.animating:
            self.is_flipped = not self.is_flipped
            self.animating = True
            self.flip_progress = 0
            return True
        return False


# Game class
class ArithmeticCardGame:
    def __init__(self):
        self.cards = []
        self.first_flipped = None
        self.second_flipped = None
        self.wait_time = 0
        self.matches_found = 0
        self.attempts = 0
        self.flips = 0
        self.game_over = False
        self.score = 0
        self.start_time = time.time()
        self.end_time = None
        self.time_penalty_applied = 0  # To track the applied time penalties

        # Start background music if loaded
        if music_loaded:
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely

        self.setup_game()

    def setup_game(self):
        # Create pairs of cards
        arithmetic_pairs = create_arithmetic_pairs()

        # Create and position cards
        card_list = []
        for problem, answer in arithmetic_pairs:
            card_list.append(Card(0, 0, CARD_WIDTH, CARD_HEIGHT, problem, answer))

        # Shuffle the cards
        random.shuffle(card_list)

        # Position cards in a grid - move all cards to the left to avoid overlapping with score panel
        total_width = COLS * CARD_WIDTH + (COLS - 1) * MARGIN
        total_height = ROWS * CARD_HEIGHT + (ROWS - 1) * MARGIN

        # Calculate start_x to ensure cards don't overlap with score panel
        score_panel_width = 180  # Width of the score panel on the right
        available_width = SCREEN_WIDTH - score_panel_width - 10  # 10px extra margin

        start_x = (available_width - total_width) // 2
        start_y = (SCREEN_HEIGHT - total_height) // 2

        for i in range(ROWS):
            for j in range(COLS):
                index = i * COLS + j
                if index < len(card_list):
                    x = start_x + j * (CARD_WIDTH + MARGIN)
                    y = start_y + i * (CARD_HEIGHT + MARGIN)
                    card_list[index].x = x
                    card_list[index].y = y
                    card_list[index].rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

        self.cards = card_list

    def handle_click(self, pos):
        # If we're waiting for cards to flip back, ignore clicks
        if self.wait_time > 0:
            return

        # If game is over, ignore clicks
        if self.game_over:
            return

        # Check if we clicked on a card
        for card in self.cards:
            if card.is_clicked(pos):
                # Start flip animation
                if card.flip():
                    # Play card flip sound
                    if sounds_loaded and card_flip_sound:
                        card_flip_sound.play()

                    self.flips += 1

                    # Check if this is the first or second card flipped
                    if self.first_flipped is None:
                        self.first_flipped = card
                    else:
                        self.second_flipped = card
                        self.attempts += 1

                        # Check if we have a match
                        if self.first_flipped.answer == self.second_flipped.answer:
                            # Play match sound
                            if sounds_loaded and match_sound:
                                match_sound.play()

                            self.first_flipped.is_matched = True
                            self.second_flipped.is_matched = True
                            self.matches_found += 1

                            # Add score for match (10 points per match)
                            self.score += 10

                            # Reset flipped cards
                            self.first_flipped = None
                            self.second_flipped = None

                            # Check if all pairs are found
                            if self.matches_found == 8:  # Changed from 6 to 8 pairs
                                self.game_over = True
                                self.end_time = time.time()

                                # Stop background music
                                if music_loaded:
                                    pygame.mixer.music.stop()
                        else:
                            # Play error sound
                            if sounds_loaded and error_sound:
                                error_sound.play()

                            # No match, set wait time before flipping back
                            self.wait_time = 60  # 60 frames = 1 second at 60 FPS

                # We found a card to flip, so stop checking
                break

    def update(self):
        # Update wait time and flip back cards if needed
        if self.wait_time > 0:
            self.wait_time -= 1
            if self.wait_time == 0:
                # Start the flip back animation
                self.first_flipped.flip()
                self.second_flipped.flip()
                self.first_flipped = None
                self.second_flipped = None

        # Apply time penalty: -1 point per 10 seconds
        if not self.game_over:
            current_time = time.time()
            elapsed_seconds = int(current_time - self.start_time)
            time_penalties_due = elapsed_seconds // 10

            # Only apply new penalties
            new_penalties = time_penalties_due - self.time_penalty_applied
            if new_penalties > 0:
                self.score = max(0, self.score - new_penalties)
                self.time_penalty_applied = time_penalties_due

    def draw(self):
        # Draw gradient background
        for y in range(SCREEN_HEIGHT):
            # Create a gradient from dark blue to light blue
            color = (
                int(DARK_BLUE[0] + (LIGHT_BLUE[0] - DARK_BLUE[0]) * y / SCREEN_HEIGHT),
                int(DARK_BLUE[1] + (LIGHT_BLUE[1] - DARK_BLUE[1]) * y / SCREEN_HEIGHT),
                int(DARK_BLUE[2] + (LIGHT_BLUE[2] - DARK_BLUE[2]) * y / SCREEN_HEIGHT)
            )
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Draw all cards
        for card in self.cards:
            card.draw()

        # Create info panel on the right side (similar to original)
        panel_rect = pygame.Rect(SCREEN_WIDTH - 180, 10, 170, 240)
        # Draw a semi-transparent panel
        s = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        s.fill((255, 255, 255, 180))  # White with alpha
        screen.blit(s, panel_rect)
        pygame.draw.rect(screen, BLACK, panel_rect, width=2, border_radius=10)

        # Add a title to the panel
        panel_title = font.render("Game Stats", True, BLACK)
        screen.blit(panel_title, (panel_rect.centerx - panel_title.get_width() // 2, panel_rect.y + 10))

        # Draw a line under the title
        pygame.draw.line(screen, BLACK,
                         (panel_rect.x + 10, panel_rect.y + 40),
                         (panel_rect.right - 10, panel_rect.y + 40),
                         2)

        # Draw the score with colored background (like original)
        score_label = font.render("Score:", True, BLACK)
        screen.blit(score_label, (panel_rect.x + 15, panel_rect.y + 50))

        score_bg = pygame.Rect(panel_rect.x + 90, panel_rect.y + 50, 65, 30)
        pygame.draw.rect(screen, GREEN, score_bg, border_radius=5)
        pygame.draw.rect(screen, BLACK, score_bg, width=1, border_radius=5)

        score_text = font.render(str(self.score), True, WHITE)
        screen.blit(score_text, (score_bg.centerx - score_text.get_width() // 2,
                                 score_bg.centery - score_text.get_height() // 2))

        # Attempts
        attempts_label = font.render("Tries:", True, BLACK)
        screen.blit(attempts_label, (panel_rect.x + 15, panel_rect.y + 90))

        attempts_bg = pygame.Rect(panel_rect.x + 90, panel_rect.y + 90, 65, 30)
        pygame.draw.rect(screen, BLUE, attempts_bg, border_radius=5)
        pygame.draw.rect(screen, BLACK, attempts_bg, width=1, border_radius=5)

        attempts_text = font.render(str(self.attempts), True, WHITE)
        screen.blit(attempts_text, (attempts_bg.centerx - attempts_text.get_width() // 2,
                                    attempts_bg.centery - attempts_text.get_height() // 2))

        # Flips
        flips_label = font.render("Flips:", True, BLACK)
        screen.blit(flips_label, (panel_rect.x + 15, panel_rect.y + 130))

        flips_bg = pygame.Rect(panel_rect.x + 90, panel_rect.y + 130, 65, 30)
        pygame.draw.rect(screen, PURPLE, flips_bg, border_radius=5)
        pygame.draw.rect(screen, BLACK, flips_bg, width=1, border_radius=5)

        flips_value = font.render(str(self.flips), True, WHITE)
        screen.blit(flips_value, (flips_bg.centerx - flips_value.get_width() // 2,
                                  flips_bg.centery - flips_value.get_height() // 2))

        # Free flips (keeping this from original)
        free_flips = max(0, 5 - self.flips)
        free_flips_bg = pygame.Rect(panel_rect.x + 90, panel_rect.y + 170, 65, 30)
        pygame.draw.rect(screen, PINK, free_flips_bg, border_radius=5)
        pygame.draw.rect(screen, BLACK, free_flips_bg, width=1, border_radius=5)

        free_text = font.render(str(free_flips), True, WHITE)
        screen.blit(free_text, (free_flips_bg.centerx - free_text.get_width() // 2,
                                free_flips_bg.centery - free_text.get_height() // 2))

        free_label = font.render("Free:", True, BLACK)
        screen.blit(free_label, (panel_rect.x + 15, panel_rect.y + 170))

        # Time
        time_label = font.render("Time:", True, BLACK)
        screen.blit(time_label, (panel_rect.x + 15, panel_rect.y + 210))

        # Calculate time based on whether game is over or not
        if self.game_over and self.end_time:
            elapsed_time = int(self.end_time - self.start_time)
        else:
            elapsed_time = int(time.time() - self.start_time)

        # Create a time display with minutes:seconds format
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_str = f"{minutes}:{seconds:02d}"

        time_bg = pygame.Rect(panel_rect.x + 90, panel_rect.y + 210, 65, 30)
        pygame.draw.rect(screen, ORANGE, time_bg, border_radius=5)
        pygame.draw.rect(screen, BLACK, time_bg, width=1, border_radius=5)

        time_text = font.render(time_str, True, WHITE)
        screen.blit(time_text, (time_bg.centerx - time_text.get_width() // 2,
                                time_bg.centery - time_text.get_height() // 2))

        # Draw game over screen if needed
        if self.game_over:
            self.draw_game_over()

    def draw_game_over(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Semi-transparent black
        screen.blit(overlay, (0, 0))

        # Continue button for game over screen
        continue_btn_width = 200
        continue_btn_height = 50
        continue_btn_x = (SCREEN_WIDTH - continue_btn_width) // 2
        continue_btn_y = SCREEN_HEIGHT - 100

        continue_btn = pygame.Rect(continue_btn_x, continue_btn_y, continue_btn_width, continue_btn_height)

        # Draw continue button
        pygame.draw.rect(screen, GREEN, continue_btn, border_radius=10)
        pygame.draw.rect(screen, BLACK, continue_btn, width=2, border_radius=10)

        continue_text = font.render("Continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=continue_btn.center)
        screen.blit(continue_text, continue_rect)

        # Draw congratulations message
        congrats = big_font.render("Congratulations!", True, WHITE)
        congrats_rect = congrats.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(congrats, congrats_rect)

        # Draw final score
        score_text = big_font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        # Draw time
        elapsed_time = int(self.end_time - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_str = f"Time: {minutes}:{seconds:02d}"

        time_text = font.render(time_str, True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(time_text, time_rect)

    def get_game_data(self):
        """Return game data for the summary screen"""
        elapsed_time = int(self.end_time - self.start_time) if self.end_time else int(time.time() - self.start_time)
        return {
            'score': self.score,
            'matches': self.matches_found,
            'attempts': self.attempts,
            'flips': self.flips,
            'time': elapsed_time
        }


# Main function
def main():
    # Create and start the game
    game = ArithmeticCardGame()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos

                    # Handle normal card clicks
                    game.handle_click(mouse_pos)

                    # Check for continue button click in game over screen
                    if game.game_over:
                        continue_btn_width = 200
                        continue_btn_height = 50
                        continue_btn_x = (SCREEN_WIDTH - continue_btn_width) // 2
                        continue_btn_y = SCREEN_HEIGHT - 100

                        continue_btn = pygame.Rect(continue_btn_x, continue_btn_y,
                                                   continue_btn_width, continue_btn_height)

                        if continue_btn.collidepoint(mouse_pos):
                            # Play a success sound if available
                            if sounds_loaded and success_sound:
                                success_sound.play()
                                pygame.time.delay(500)  # Wait for sound to play a bit

                            # Exit to summary screen
                            pygame.quit()

                            # Pass game data to summary screen
                            game_data = game.get_game_data()
                            subprocess.run([
                                "python", "memorymath_summery.py",
                                str(game_data['score']),
                                str(game_data['matches']),
                                str(game_data['attempts']),
                                str(game_data['flips']),
                                str(game_data['time'])
                            ])
                            return  # Exit function to prevent further game updates

        # Update game state
        game.update()

        # Draw the game
        game.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# Start the game if this file is run directly
if __name__ == "__main__":
    main()