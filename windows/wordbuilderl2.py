import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Constants
WIDTH, HEIGHT = 800, 600  # Adjusted to match your other games
GAME_TIME = 130  # in seconds (slightly less than level 1)
COLORS = {
    "blue": (0, 100, 255),
    "light_blue": (100, 180, 255),
    "green": (0, 255, 0),
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "orange": (200, 100, 0),
    "dark_blue": (0, 50, 150),
    "yellow": (255, 255, 0),
    "gold": (255, 215, 0),
    "gray": (200, 200, 200)
}

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Builder Game - Level 2")
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont("Arial", 24, bold=True)
clock = pygame.time.Clock()

# Background - Create a gradient background similar to your other games
background_img = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    # Create a gradient from dark blue to light blue
    color = (
        int(COLORS["dark_blue"][0] + (COLORS["light_blue"][0] - COLORS["dark_blue"][0]) * y / HEIGHT),
        int(COLORS["dark_blue"][1] + (COLORS["light_blue"][1] - COLORS["dark_blue"][1]) * y / HEIGHT),
        int(COLORS["dark_blue"][2] + (COLORS["light_blue"][2] - COLORS["dark_blue"][2]) * y / HEIGHT)
    )
    pygame.draw.line(background_img, color, (0, y), (WIDTH, y))


# Sound setup
class SoundManager:
    def __init__(self):
        self.enabled = True
        self.music_playing = False

        try:
            # Load background music
            pygame.mixer.music.load("background_music.mp3")
            pygame.mixer.music.set_volume(0.5)

            # Load sound effects
            self.correct_sound = pygame.mixer.Sound("correct.mp3")
            self.wrong_sound = pygame.mixer.Sound("wrong.mp3")
            self.game_over_sound = pygame.mixer.Sound("game_over.mp3")
        except:
            print("Could not load all sound files. Check that audio files exist.")
            self.enabled = False

    def play_music(self):
        if self.enabled and not self.music_playing:
            pygame.mixer.music.play(-1)  # Loop forever
            self.music_playing = True

    def stop_music(self):
        if self.enabled and self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

    def toggle_music(self):
        if self.music_playing:
            self.stop_music()
        else:
            self.play_music()

    def play_sound(self, sound_type):
        if not self.enabled:
            return

        if sound_type == "correct":
            self.correct_sound.play()
        elif sound_type == "wrong":
            self.wrong_sound.play()
        elif sound_type == "game_over":
            self.game_over_sound.play()


# Create sound manager
sound_manager = SoundManager()

# Word categories and hints for level 2 (medium length words)
CATEGORIES = {
    "Animals": ["zebra", "dolphin", "squirrel", "penguin", "kangaroo"],
    "Fruits": ["pineapple", "strawberry", "blueberry", "watermelon", "pomegranate"],
    "School Supplies": ["notebook", "sharpener", "backpack", "highlighter", "calculator"],
    "Food": ["spaghetti", "hamburger", "pancake", "sausage", "chocolate"],
    "Nature": ["mountain", "volcano", "rainbow", "waterfall", "thunderstorm"]
}

HINTS = {
    "zebra": "A striped black-and-white animal found in Africa.",
    "dolphin": "A smart sea animal that jumps and whistles.",
    "squirrel": "A small furry animal that climbs trees and eats nuts.",
    "penguin": "A black-and-white bird that can't fly but swims well.",
    "kangaroo": "An Australian animal that hops and carries a baby in its pouch.",

    "pineapple": "A tropical fruit with spiky skin and sweet yellow flesh.",
    "strawberry": "A small red fruit with tiny seeds on its surface.",
    "blueberry": "A small round blue fruit often used in muffins.",
    "watermelon": "A large green fruit with red juicy flesh and black seeds.",
    "pomegranate": "A red fruit filled with many juicy seeds inside.",

    "notebook": "A book with blank or lined pages for writing notes.",
    "sharpener": "A tool used to make pencils sharp.",
    "backpack": "A bag carried on your back to hold school items.",
    "highlighter": "A pen used to mark important text in bright colors.",
    "calculator": "A small device used to do math calculations.",

    "spaghetti": "Long, thin pasta often served with sauce.",
    "hamburger": "A sandwich with a meat patty inside a bun.",
    "pancake": "A round, flat cake eaten for breakfast, often with syrup.",
    "sausage": "A long roll of meat, often eaten at breakfast or in a hot dog.",
    "chocolate": "A sweet treat made from cocoa, often in bars or candy.",

    "mountain": "A tall natural rise on Earth, bigger than a hill.",
    "volcano": "A mountain that can erupt with lava and ash.",
    "rainbow": "A colorful arc seen in the sky after rain.",
    "waterfall": "Water falling from a high place, like a cliff or rocks.",
    "thunderstorm": "A weather event with heavy rain, thunder, and lightning."
}

# Button definitions - adjusted positions for 800x600 screen
hint_button = pygame.Rect(WIDTH - 160, HEIGHT - 60, 140, 40)
submit_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 80, 120, 40)
music_button = pygame.Rect(WIDTH - 150, 20, 130, 40)


class WordGame:
    def __init__(self):
        self.used_words = set()
        self.reset_game()

    def reset_game(self):
        """Reset all game variables for a new game"""
        self.selected_category = ""
        self.current_word = ""
        self.shuffled_letters = []
        self.letter_positions = []
        self.selected_letters = []
        self.hint_used = False
        self.any_hint_used = False
        self.showing_hint = False
        self.score = 0
        self.words_solved = 0
        self.start_ticks = 0

        # Get first word
        self.load_next_word()

    def get_random_word(self):
        # """Get a random word from any category that hasn't been used recently"""
        all_words = []
        for category, words in CATEGORIES.items():
            for word in words:
                if word not in self.used_words:
                    all_words.append((category, word))

        if not all_words:  # If all words have been used
            self.used_words.clear()  # Reset used words
            for category, words in CATEGORIES.items():
                for word in words:
                    all_words.append((category, word))

        random_category, random_word = random.choice(all_words)
        self.used_words.add(random_word)
        return random_category, random_word

    def load_next_word(self):
        # """Prepare the next word for the game"""
        self.selected_category, self.current_word = self.get_random_word()
        self.shuffled_letters = list(self.current_word)
        random.shuffle(self.shuffled_letters)

        # Determine layout based on word length
        letter_width = 60  # Width of each letter box
        spacing = 20  # Space between letters
        max_letters_per_row = 8  # Maximum letters in a single row

        # Calculate if we need multiple rows
        if len(self.shuffled_letters) <= max_letters_per_row:
            # Single row layout
            total_width = len(self.shuffled_letters) * (letter_width + spacing) - spacing
            start_x = (WIDTH - total_width) // 2

            self.letter_positions = []
            for i in range(len(self.shuffled_letters)):
                x = start_x + i * (letter_width + spacing) + letter_width // 2
                y = HEIGHT // 2
                self.letter_positions.append((x, y))
        else:
            # Multi-row layout (two rows)
            letters_in_row1 = len(self.shuffled_letters) // 2
            letters_in_row2 = len(self.shuffled_letters) - letters_in_row1

            # First row
            total_width_row1 = letters_in_row1 * (letter_width + spacing) - spacing
            start_x_row1 = (WIDTH - total_width_row1) // 2

            # Second row
            total_width_row2 = letters_in_row2 * (letter_width + spacing) - spacing
            start_x_row2 = (WIDTH - total_width_row2) // 2

            self.letter_positions = []

            # Add positions for first row
            for i in range(letters_in_row1):
                x = start_x_row1 + i * (letter_width + spacing) + letter_width // 2
                y = HEIGHT // 2 - 50  # First row above center
                self.letter_positions.append((x, y))

            # Add positions for second row
            for i in range(letters_in_row2):
                x = start_x_row2 + i * (letter_width + spacing) + letter_width // 2
                y = HEIGHT // 2 + 50  # Second row below center
                self.letter_positions.append((x, y))

        self.selected_letters = []
        self.hint_used = False
        self.showing_hint = False

    def start_timer(self):
        # """Start the game timer"""
        self.start_ticks = pygame.time.get_ticks()

    def get_time_left(self):
        # """Calculate time left in the game"""
        seconds_passed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        return max(0, GAME_TIME - int(seconds_passed))

    def check_word(self):
        # """Check if the selected letters form the correct word"""
        return ''.join(self.selected_letters).lower() == self.current_word


class GameUI:
    def __init__(self, game, sound_manager):
        self.game = game
        self.sound_manager = sound_manager
        self.final_score = 0

    def draw_button(self, rect, color, text, text_color=COLORS["white"]):
        # """Draw a button with text - styled like your other game buttons"""
        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, COLORS["black"], rect, width=2, border_radius=10)

        text_surf = small_font.render(text, True, text_color)
        text_x = rect.x + (rect.width - text_surf.get_width()) // 2
        text_y = rect.y + (rect.height - text_surf.get_height()) // 2
        screen.blit(text_surf, (text_x, text_y))

    def draw_letters(self, letters, positions):
        # """Draw letter boxes on screen"""
        for i, letter in enumerate(letters):
            text = font.render(letter.upper(), True, COLORS["white"])
            rect = text.get_rect(center=positions[i])

            # Draw a rounded rectangle for the letter background
            # Use a fixed size for letter boxes to prevent overlap
            letter_rect = pygame.Rect(
                positions[i][0] - 30,  # Center x - half width
                positions[i][1] - 30,  # Center y - half height
                60,  # Fixed width
                60  # Fixed height
            )
            pygame.draw.rect(screen, COLORS["blue"], letter_rect, border_radius=10)
            pygame.draw.rect(screen, COLORS["black"], letter_rect, width=2, border_radius=10)

            screen.blit(text, rect)

    def draw_game_screen(self):
        # """Draw the main game screen"""
        screen.blit(background_img, (0, 0))

        # Draw a fancy box for the selected word display
        selected_word_box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 4 - 30, 400, 60)
        pygame.draw.rect(screen, COLORS["white"], selected_word_box, border_radius=15)
        pygame.draw.rect(screen, COLORS["black"], selected_word_box, width=2, border_radius=15)

        # Draw HUD with styled boxes like your other games
        # Time box
        time_box = pygame.Rect(10, 70, 180, 40)
        pygame.draw.rect(screen, (0, 0, 100, 180), time_box, border_radius=10)
        pygame.draw.rect(screen, COLORS["black"], time_box, width=2, border_radius=10)
        time_text = small_font.render(f"Time Left: {self.game.get_time_left()}s", True, COLORS["white"])
        screen.blit(time_text, (time_box.x + 10, time_box.y + 10))

        # Category box
        cat_box = pygame.Rect(10, 10, 300, 40)
        pygame.draw.rect(screen, (0, 0, 100, 180), cat_box, border_radius=10)
        pygame.draw.rect(screen, COLORS["black"], cat_box, width=2, border_radius=10)
        cat_text = small_font.render(f"Category: {self.game.selected_category}", True, COLORS["white"])
        screen.blit(cat_text, (cat_box.x + 10, cat_box.y + 10))

        # Score box
        score_box = pygame.Rect(320, 10, 300, 40)
        pygame.draw.rect(screen, (0, 0, 100, 180), score_box, border_radius=10)
        pygame.draw.rect(screen, COLORS["black"], score_box, width=2, border_radius=10)
        score_text = small_font.render(f"Score: {self.game.score} | Words: {self.game.words_solved}", True,
                                       COLORS["white"])
        screen.blit(score_text, (score_box.x + 10, score_box.y + 10))

        # Draw music button
        if self.sound_manager.enabled:
            self.draw_button(music_button, COLORS["dark_blue"],
                             "Music " + ("ON" if self.sound_manager.music_playing else "OFF"))

        # Draw letters and buttons
        self.draw_letters(self.game.shuffled_letters, self.game.letter_positions)

        # Draw selected letters
        selected_text = font.render(''.join(self.game.selected_letters).upper(), True, COLORS["black"])
        screen.blit(selected_text, (WIDTH // 2 - selected_text.get_width() // 2, HEIGHT // 4))

        # Draw buttons
        self.draw_button(hint_button, COLORS["orange"], "Show Hint")
        self.draw_button(submit_button, COLORS["green"], "Submit")

        # Draw hint if showing
        if self.game.showing_hint:
            hint_text = f"Hint: {HINTS.get(self.game.current_word, 'No hint available.')}"
            hint_render = small_font.render(hint_text, True, COLORS["black"])

            # Create a background for the hint box - styled like your other game elements
            hint_box_width = hint_render.get_width() + 20
            hint_box_height = 50
            hint_box = pygame.Rect(
                WIDTH // 2 - hint_box_width // 2,
                HEIGHT - 150,
                hint_box_width,
                hint_box_height
            )

            # Draw hint box with rounded corners
            pygame.draw.rect(screen, (255, 255, 200), hint_box, border_radius=10)
            pygame.draw.rect(screen, COLORS["gold"], hint_box, width=2, border_radius=10)

            # Draw hint text
            screen.blit(hint_render, (hint_box.x + 10, hint_box.y + (hint_box_height - hint_render.get_height()) // 2))

    def show_game_over(self, message):
        # Just show a simple message and launch the summary screen
        screen.blit(background_img, (0, 0))

        # Create a fancy box for the game over message
        message_text = font.render(message, True, COLORS["red"])
        message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))

        # Draw a gold box around the message
        pygame.draw.rect(screen, COLORS["gold"],
                         (message_rect.left - 20, message_rect.top - 10,
                          message_rect.width + 40, message_rect.height + 20),
                         border_radius=15)
        pygame.draw.rect(screen, COLORS["black"],
                         (message_rect.left - 20, message_rect.top - 10,
                          message_rect.width + 40, message_rect.height + 20),
                         width=3, border_radius=15)

        screen.blit(message_text, message_rect)

        # Create and draw continue button
        continue_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
        self.draw_button(continue_button, COLORS["green"], "Continue", COLORS["white"])

        # Add message about continuing
        next_game_text = small_font.render("Continue to summary", True, COLORS["white"])
        screen.blit(next_game_text, (WIDTH // 2 - next_game_text.get_width() // 2, HEIGHT // 2 + 120))

        # Play game over sound
        self.sound_manager.play_sound("game_over")

        pygame.display.flip()

        # Save final score
        self.final_score = self.game.score

        # Write score and game data to file for later use
        try:
            with open("word_builder_score.txt", "w") as f:
                f.write(str(self.final_score))

            # Also write words solved and hints used for the summary screen
            with open("word_builder_data.txt", "w") as f:
                f.write(f"{self.game.words_solved}\n")
                f.write(f"{self.game.any_hint_used}\n")
                # Calculate time played
                time_played = GAME_TIME - self.game.get_time_left()
                f.write(f"{int(time_played)}\n")
                f.write(f"2\n")  # Level number (level 2)
        except:
            print("Could not save game data to file")

        # Wait for continue button click
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        # Launch summary screen
                        pygame.quit()
                        os.system(f"{sys.executable} wordbuilder_summary.py")
                        sys.exit()


def main():
    # Initialize game components
    game = WordGame()
    ui = GameUI(game, sound_manager)

    # Start with music playing
    sound_manager.play_music()

    # Start the game timer
    game.start_timer()

    # Main game loop
    running = True
    while running:
        # Draw game screen
        ui.draw_game_screen()

        # Check if time's up
        if game.get_time_left() <= 0:
            ui.show_game_over("Time's Up!")
            break

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Check button clicks
                if sound_manager.enabled and music_button.collidepoint(mx, my):
                    sound_manager.toggle_music()

                elif hint_button.collidepoint(mx, my):
                    game.hint_used = True
                    game.any_hint_used = True
                    game.showing_hint = True

                elif submit_button.collidepoint(mx, my):
                    if game.check_word():
                        # Correct answer
                        sound_manager.play_sound("correct")

                        # Update score
                        game.score += 5 if game.hint_used else 10
                        game.words_solved += 1

                        # Show correct message
                        screen.blit(background_img, (0, 0))
                        cat_text = small_font.render(f"Category: {game.selected_category}", True, COLORS["white"])
                        score_text = small_font.render(f"Score: {game.score} | Words Solved: {game.words_solved}", True,
                                                       COLORS["white"])
                        screen.blit(cat_text, (10, 10))
                        screen.blit(score_text, (10, 40))

                        selected_text = font.render(''.join(game.selected_letters).upper(), True, COLORS["black"])
                        screen.blit(selected_text, (WIDTH // 2 - selected_text.get_width() // 2, HEIGHT // 4))

                        correct_text = font.render("Correct!", True, COLORS["green"])
                        screen.blit(correct_text, (WIDTH // 2 - correct_text.get_width() // 2, HEIGHT // 2))

                        pygame.display.flip()
                        pygame.time.wait(1000)
                        game.load_next_word()
                    else:
                        # Wrong answer
                        sound_manager.play_sound("wrong")
                        pygame.time.wait(500)
                        ui.show_game_over("Wrong Word!")
                        running = False

                else:
                    # Check letter clicks - use fixed-size collision detection
                    for i, pos in enumerate(game.letter_positions):
                        letter_rect = pygame.Rect(pos[0] - 30, pos[1] - 30, 60, 60)
                        if letter_rect.collidepoint(mx, my):
                            # Only add if we haven't selected this letter already
                            used = False
                            for j, other_pos in enumerate(game.letter_positions):
                                if i != j and game.shuffled_letters[j] in game.selected_letters:
                                    other_rect = pygame.Rect(other_pos[0] - 30, other_pos[1] - 30, 60, 60)
                                    if other_rect.collidepoint(mx, my):
                                        used = True
                                        break

                            if not used:
                                game.selected_letters.append(game.shuffled_letters[i])

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and game.selected_letters:
                    game.selected_letters.pop()
                elif event.key == pygame.K_m and sound_manager.enabled:
                    sound_manager.toggle_music()

        pygame.display.flip()
        clock.tick(30)

    # Clean up and prepare for the next game
    if sound_manager.music_playing:
        sound_manager.stop_music()


if __name__ == "__main__":
    main()