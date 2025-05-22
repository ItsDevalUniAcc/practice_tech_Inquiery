import pygame
import sys
import os
import random
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 6
CELL_SIZE = 80
BOARD_OFFSET_X = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
BOARD_OFFSET_Y = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2 + 50
COLORS = {
    'background': (240, 240, 245),
    'grid': (200, 200, 210),
    'text': (50, 50, 60),
    'button': (100, 150, 200),
    'button_hover': (120, 170, 220),
    'button_text': (255, 255, 255),
    'player_car': (255, 100, 100),
    'other_car': (100, 150, 255),
    'truck': (100, 200, 150),
    'highlight': (255, 255, 100, 150),
    'star': (255, 215, 0),
    'star_empty': (200, 200, 200),
    'exit': (255, 100, 100, 100),
    'white': (255, 255, 255)  # Adding white color definition
}
FPS = 60


class Car:
    def __init__(self, x, y, length, horizontal, color, is_player=False):
        self.x = x
        self.y = y
        self.length = length
        self.horizontal = horizontal
        self.color = color
        self.is_player = is_player
        self.target_x = x
        self.target_y = y
        self.moving = False
        self.speed = 0.1

    def move(self, dx, dy):
        """Move the car by dx, dy if possible. Returns True if move was successful."""
        if self.moving:
            return False

        self.target_x = self.x + dx
        self.target_y = self.y + dy
        self.moving = True
        return True

    def update(self):
        """Update car position for smooth animation"""
        if self.moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < self.speed:
                self.x = self.target_x
                self.y = self.target_y
                self.moving = False
            else:
                self.x += dx * self.speed
                self.y += dy * self.speed

    def draw(self, screen, selected=False):
        """Draw the car on the screen with optional highlight"""
        x_pos = BOARD_OFFSET_X + self.x * CELL_SIZE
        y_pos = BOARD_OFFSET_Y + self.y * CELL_SIZE

        if self.horizontal:
            width = self.length * CELL_SIZE
            height = CELL_SIZE
        else:
            width = CELL_SIZE
            height = self.length * CELL_SIZE

        # Draw car body with rounded corners
        rect = pygame.Rect(x_pos, y_pos, width, height)
        pygame.draw.rect(screen, self.color, rect, border_radius=10)

        # Add some details to make cars look better
        if self.horizontal:
            pygame.draw.ellipse(screen, (self.color[0] // 2, self.color[1] // 2, self.color[2] // 2),
                                pygame.Rect(x_pos + 5, y_pos + 5, 20, height - 10))
            pygame.draw.ellipse(screen, (self.color[0] // 2, self.color[1] // 2, self.color[2] // 2),
                                pygame.Rect(x_pos + width - 25, y_pos + 5, 20, height - 10))
        else:
            pygame.draw.ellipse(screen, (self.color[0] // 2, self.color[1] // 2, self.color[2] // 2),
                                pygame.Rect(x_pos + 5, y_pos + 5, width - 10, 20))
            pygame.draw.ellipse(screen, (self.color[0] // 2, self.color[1] // 2, self.color[2] // 2),
                                pygame.Rect(x_pos + 5, y_pos + height - 25, width - 10, 20))

        # Highlight if selected
        if selected:
            highlight_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, COLORS['highlight'], (0, 0, width, height), border_radius=10)
            screen.blit(highlight_surface, (x_pos, y_pos))


class Level:
    def __init__(self, difficulty, cars, exit_pos, perfect_moves):
        self.difficulty = difficulty
        self.cars = cars
        self.exit_pos = exit_pos
        self.perfect_moves = perfect_moves
        self.car_objects = []
        self.player_car = None
        self.move_count = 0
        self.move_history = []
        self.selected_car = None
        self.solved = False

        # Create car objects
        for car_data in cars:
            car = Car(
                x=car_data['x'],
                y=car_data['y'],
                length=car_data['length'],
                horizontal=car_data['horizontal'],
                color=car_data['color'],
                is_player=car_data.get('is_player', False)
            )
            self.car_objects.append(car)
            if car.is_player:
                self.player_car = car

    def reset(self):
        """Reset the level to its initial state"""
        for i, car_data in enumerate(self.cars):
            self.car_objects[i].x = car_data['x']
            self.car_objects[i].y = car_data['y']
            self.car_objects[i].target_x = car_data['x']
            self.car_objects[i].target_y = car_data['y']
            self.car_objects[i].moving = False
        self.move_count = 0
        self.move_history = []
        self.selected_car = None
        self.solved = False

    def is_valid_position(self, car, x, y):
        """Check if a car can be placed at (x, y) without overlapping others"""
        for other in self.car_objects:
            if other == car:
                continue

            if car.horizontal:
                car_rect = pygame.Rect(x, y, car.length, 1)
                other_rect = pygame.Rect(other.x, other.y, other.length if other.horizontal else 1,
                                         1 if other.horizontal else other.length)
            else:
                car_rect = pygame.Rect(x, y, 1, car.length)
                other_rect = pygame.Rect(other.x, other.y, other.length if other.horizontal else 1,
                                         1 if other.horizontal else other.length)

            if car_rect.colliderect(other_rect):
                return False

        # Check boundaries
        if x < 0 or y < 0:
            return False
        if car.horizontal and x + car.length > GRID_SIZE:
            return False
        if not car.horizontal and y + car.length > GRID_SIZE:
            return False

        return True

    def move_car(self, car, dx, dy):
        """Attempt to move a car by (dx, dy). Returns True if successful."""
        if not self.is_valid_position(car, car.x + dx, car.y + dy):
            return False

        # Record move for undo
        self.move_history.append((car, dx, dy))
        self.move_count += 1

        return car.move(dx, dy)

    def undo_move(self):
        """Undo the last move. Returns True if successful."""
        if not self.move_history:
            return False

        car, dx, dy = self.move_history.pop()
        self.move_count -= 1
        return car.move(-dx, -dy)

    def check_win(self):
        """Check if the player has won (player car reached exit)"""
        if not self.player_car:
            return False

        exit_x, exit_y = self.exit_pos
        if self.player_car.horizontal:
            return (self.player_car.x + self.player_car.length == exit_x and
                    self.player_car.y == exit_y)
        else:
            return (self.player_car.x == exit_x and
                    self.player_car.y + self.player_car.length == exit_y)

    def update(self):
        """Update level state"""
        # Update car positions
        for car in self.car_objects:
            car.update()

        # Check for win condition
        if not self.solved and self.check_win():
            self.solved = True

    def draw(self, screen):
        """Draw the level"""
        # Draw grid
        for x in range(GRID_SIZE + 1):
            pygame.draw.line(screen, COLORS['grid'],
                             (BOARD_OFFSET_X + x * CELL_SIZE, BOARD_OFFSET_Y),
                             (BOARD_OFFSET_X + x * CELL_SIZE, BOARD_OFFSET_Y + GRID_SIZE * CELL_SIZE), 2)
        for y in range(GRID_SIZE + 1):
            pygame.draw.line(screen, COLORS['grid'],
                             (BOARD_OFFSET_X, BOARD_OFFSET_Y + y * CELL_SIZE),
                             (BOARD_OFFSET_X + GRID_SIZE * CELL_SIZE, BOARD_OFFSET_Y + y * CELL_SIZE), 2)

        # Draw exit
        exit_x, exit_y = self.exit_pos
        exit_rect = pygame.Rect(
            BOARD_OFFSET_X + exit_x * CELL_SIZE - 5 if exit_x == GRID_SIZE else BOARD_OFFSET_X + exit_x * CELL_SIZE,
            BOARD_OFFSET_Y + exit_y * CELL_SIZE - 5 if exit_y == GRID_SIZE else BOARD_OFFSET_Y + exit_y * CELL_SIZE,
            CELL_SIZE + 10 if exit_x == GRID_SIZE or exit_y == GRID_SIZE else CELL_SIZE,
            CELL_SIZE + 10 if exit_x == GRID_SIZE or exit_y == GRID_SIZE else CELL_SIZE
        )
        pygame.draw.rect(screen, COLORS['exit'], exit_rect, border_radius=5)

        # Draw cars
        for car in self.car_objects:
            car.draw(screen, selected=(car == self.selected_car))

        # Draw move count
        font = pygame.font.SysFont('Arial', 24)
        moves_text = font.render(f"Moves: {self.move_count}", True, COLORS['text'])
        screen.blit(moves_text, (20, 20))

    def calculate_stars(self):
        """Calculate how many stars the player earned"""
        if self.move_count <= self.perfect_moves:
            return 3
        elif self.move_count <= self.perfect_moves * 1.5:
            return 2
        elif self.move_count <= self.perfect_moves * 2:
            return 1
        return 0


class Button:
    def __init__(self, x, y, width, height, text,
                 color=COLORS['button'],
                 hover_color=COLORS['button_hover']):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        """Draw the button"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, COLORS['text'], self.rect, 2, border_radius=5)

        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(self.text, True, COLORS['button_text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        """Check if mouse is hovering over the button"""
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, click):
        """Check if button is clicked"""
        return click and self.rect.collidepoint(pos)


def main():
    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Car Parking Puzzle")
    clock = pygame.time.Clock()

    # Create the level
    level = Level(
        difficulty="Easy",
        cars=[
            {'x': 2, 'y': 2, 'length': 2, 'horizontal': True, 'color': COLORS['player_car'], 'is_player': True},
            {'x': 2, 'y': 0, 'length': 2, 'horizontal': False, 'color': COLORS['other_car']},
            {'x': 4, 'y': 1, 'length': 2, 'horizontal': False, 'color': COLORS['other_car']},
            {'x': 0, 'y': 3, 'length': 2, 'horizontal': True, 'color': COLORS['truck']}
        ],
        exit_pos=(6, 2),
        perfect_moves=4
    )

    # Create buttons
    menu_button = Button(20, SCREEN_HEIGHT - 70, 120, 50, "Menu")
    reset_button = Button(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 70, 120, 50, "Reset")
    undo_button = Button(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 70, 120, 50, "Undo")

    # Create a Continue button for when the level is solved
    continue_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 60, "Continue",
                             color=COLORS['button'], hover_color=(0, 180, 0))

    # Main game loop
    running = True
    level_complete = False
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_click = True

            if event.type == pygame.KEYDOWN:
                # Keyboard controls
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    level.reset()
                    level_complete = False
                elif event.key == pygame.K_u:
                    level.undo_move()
                elif level.selected_car:
                    if event.key == pygame.K_LEFT:
                        level.move_car(level.selected_car, -1, 0)
                    elif event.key == pygame.K_RIGHT:
                        level.move_car(level.selected_car, 1, 0)
                    elif event.key == pygame.K_UP:
                        level.move_car(level.selected_car, 0, -1)
                    elif event.key == pygame.K_DOWN:
                        level.move_car(level.selected_car, 0, 1)

        # Update level
        level.update()

        # Check if level is solved
        if level.solved and not level_complete:
            level_complete = True
            # Save the move count and stars for the summary
            move_count = level.move_count
            stars = level.calculate_stars()
            print(f"Level solved! Moves: {move_count}, Stars: {stars}")

            # Save results to file for summary page
            try:
                with open("carparking_data.txt", "w") as f:
                    f.write(f"{move_count}\n")  # Line 1: Moves made
                    f.write(f"{stars}\n")  # Line 2: Stars earned
                    f.write(f"{level.perfect_moves}\n")  # Line 3: Perfect move count
            except:
                print("Error: Could not save level data to file.")

        # Draw the game
        screen.fill(COLORS['background'])

        # Draw level
        level.draw(screen)

        # Draw buttons
        menu_button.check_hover(mouse_pos)
        reset_button.check_hover(mouse_pos)
        undo_button.check_hover(mouse_pos)

        menu_button.draw(screen)
        reset_button.draw(screen)
        undo_button.draw(screen)

        # Show completion screen if level is solved
        if level_complete:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Semi-transparent black
            screen.blit(overlay, (0, 0))

            # Draw level complete message
            font = pygame.font.SysFont('Arial', 48, bold=True)
            complete_text = font.render("Level Complete!", True, COLORS['white'])
            screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

            # Draw star rating
            stars = level.calculate_stars()
            star_size = 40
            total_width = 3 * star_size + 20
            start_x = (SCREEN_WIDTH - total_width) // 2
            start_y = SCREEN_HEIGHT // 2 - 40

            for i in range(3):
                x = start_x + i * (star_size + 10)
                y = start_y
                if i < stars:
                    # Draw filled star
                    pygame.draw.polygon(screen, COLORS['star'], [
                        (x + star_size // 2, y),
                        (x + star_size // 4, y + star_size // 2.5),
                        (x, y + star_size // 2.5),
                        (x + star_size // 4, y + star_size // 1.5),
                        (x + star_size // 5, y + star_size),
                        (x + star_size // 2, y + star_size // 1.5),
                        (x + star_size - star_size // 5, y + star_size),
                        (x + star_size - star_size // 4, y + star_size // 1.5),
                        (x + star_size, y + star_size // 2.5),
                        (x + star_size - star_size // 4, y + star_size // 2.5)
                    ])
                else:
                    # Draw empty star
                    pygame.draw.polygon(screen, COLORS['star_empty'], [
                        (x + star_size // 2, y),
                        (x + star_size // 4, y + star_size // 2.5),
                        (x, y + star_size // 2.5),
                        (x + star_size // 4, y + star_size // 1.5),
                        (x + star_size // 5, y + star_size),
                        (x + star_size // 2, y + star_size // 1.5),
                        (x + star_size - star_size // 5, y + star_size),
                        (x + star_size - star_size // 4, y + star_size // 1.5),
                        (x + star_size, y + star_size // 2.5),
                        (x + star_size - star_size // 4, y + star_size // 2.5)
                    ])

            # Display move count
            font = pygame.font.SysFont('Arial', 28)
            moves_text = font.render(f"Moves: {level.move_count}", True, COLORS['white'])
            screen.blit(moves_text, (SCREEN_WIDTH // 2 - moves_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

            # Draw continue button
            continue_button.check_hover(mouse_pos)
            continue_button.draw(screen)

            if continue_button.is_clicked(mouse_pos, mouse_click):
                pygame.quit()
                os.system(f"{sys.executable} carparking_summary.py")
                sys.exit()

        # Handle button clicks
        if menu_button.is_clicked(mouse_pos, mouse_click):
            # Return to menu/instructions
            pygame.quit()
            os.system(f"{sys.executable} carparking_instructions.py")
            sys.exit()

        if reset_button.is_clicked(mouse_pos, mouse_click):
            level.reset()
            level_complete = False

        if undo_button.is_clicked(mouse_pos, mouse_click):
            level.undo_move()

        # Handle car selection and movement with mouse if level not complete
        if not level_complete and mouse_click and not any(
                btn.is_hovered for btn in [menu_button, reset_button, undo_button]):
            grid_x = (mouse_pos[0] - BOARD_OFFSET_X) // CELL_SIZE
            grid_y = (mouse_pos[1] - BOARD_OFFSET_Y) // CELL_SIZE

            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                # Find which car was clicked
                clicked_car = None
                for car in level.car_objects:
                    if car.horizontal:
                        if (car.y == grid_y and car.x <= grid_x < car.x + car.length):
                            clicked_car = car
                            break
                    else:
                        if (car.x == grid_x and car.y <= grid_y < car.y + car.length):
                            clicked_car = car
                            break

                if clicked_car:
                    if level.selected_car == clicked_car:
                        # Try to move in the direction of the click relative to car center
                        car_center_x = clicked_car.x + clicked_car.length / 2 if clicked_car.horizontal else clicked_car.x + 0.5
                        car_center_y = clicked_car.y + 0.5 if clicked_car.horizontal else clicked_car.y + clicked_car.length / 2

                        dx = grid_x - car_center_x
                        dy = grid_y - car_center_y

                        if clicked_car.horizontal:
                            if abs(dx) > abs(dy):  # Horizontal movement
                                direction = 1 if dx > 0 else -1
                                level.move_car(clicked_car, direction, 0)
                        else:  # Vertical movement
                            if abs(dy) > abs(dx):  # Vertical movement
                                direction = 1 if dy > 0 else -1
                                level.move_car(clicked_car, 0, direction)
                    else:
                        level.selected_car = clicked_car
                else:
                    level.selected_car = None

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()