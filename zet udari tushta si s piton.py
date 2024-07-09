from PIL import Image
import random
import pygame
import sys

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("C:\\Users\\User\\Desktop\\aha\\Undyne Theme  Battle Against A True Hero Undertale  EPIC VERSION.mp3")
pygame.mixer.music.play(-1)

def generate_random_background_image(width, height, file_name):
    # Create a new image with RGB mode
    image = Image.new('RGB', (width, height))
    
    # Generate random pixels
    pixels = [
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for _ in range(width * height)
    ]
    
    # Update image with random pixels
    image.putdata(pixels)
    
    # Save the image
    image.save(file_name)

# Parameters for background image
width, height = 980, 980  # Size of the background image
file_name = 'background.png'

generate_random_background_image(width, height, file_name)
print(f"Random background image generated and saved as {file_name}")

# Initialize Pygame and game settings
pygame.init()

cell_size = 28
cell_number = 35
screen_size = cell_size * cell_number
screen = pygame.display.set_mode((screen_size, screen_size + 30))  # Extra 30 pixels for score
clock = pygame.time.Clock()

# Load images
background_image = pygame.image.load(file_name)
head_image = pygame.image.load("C:/Users/User/Desktop/aha/glava.png")
fruit_image = pygame.image.load("C:/Users/User/Desktop/aha/apl.png")

# Resize images
head_size = int(cell_size * 3)
fruit_size = int(cell_size * 2)

background_image = pygame.transform.scale(background_image, (screen_size, screen_size))
head_image = pygame.transform.scale(head_image, (head_size, head_size))
fruit_image = pygame.transform.scale(fruit_image, (fruit_size, fruit_size))

# Snake body color
SNAKE_COLOR = (0, 0, 0)

# Load sound
eat_sound = pygame.mixer.Sound("C:/Users/User/Desktop/aha/eat_sound.wav")

class Snake:
    def __init__(self):
        self.body = [[5, 10], [4, 10], [3, 10]]
        self.direction = [1, 0]
        self.new_block = False
        self.score = 0

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]])
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]])
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
        self.score += 1
        eat_sound.play()

    def draw_snake(self):
        for block in self.body[1:]:
            pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(block[0] * cell_size, block[1] * cell_size, cell_size, cell_size))
        head = self.body[0]
        head_x = head[0] * cell_size - (head_size - cell_size) // 2
        head_y = head[1] * cell_size - (head_size - cell_size) // 2
        rotated_head = pygame.transform.rotate(head_image, self.get_head_angle())
        screen.blit(rotated_head, (head_x, head_y))
        
        if len(self.body) > 1:
            last_block = self.body[-1]
            x = last_block[0] * cell_size + cell_size // 2
            y = last_block[1] * cell_size + cell_size // 2
            radius = cell_size // 2
            pygame.draw.circle(screen, SNAKE_COLOR, (x, y), radius)

    def get_head_angle(self):
        if self.direction == [1, 0]:
            return 90
        elif self.direction == [-1, 0]:
            return 270
        elif self.direction == [0, -1]:
            return 180
        elif self.direction == [0, 1]:
            return 0

    def check_collision(self):
        if not 0 <= self.body[0][0] < cell_number or not 0 <= self.body[0][1] < cell_number:
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False

class Fruit:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.position = [random.randint(0, cell_number - 1), random.randint(0, cell_number - 1)]

    def draw_fruit(self):
        fruit_x = self.position[0] * cell_size - (fruit_size - cell_size) // 2
        fruit_y = self.position[1] * cell_size - (fruit_size - cell_size) // 2
        screen.blit(fruit_image, (fruit_x, fruit_y))

def game_over_prompt():
    font = pygame.font.Font(None, 36)
    game_over_text = font.render('Game Over', True, (255, 0, 0))
    prompt_text = font.render('Press R to restart or Q to quit', True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_size / 2, screen_size / 2))
    prompt_rect = prompt_text.get_rect(center=(screen_size / 2, screen_size / 2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(prompt_text, prompt_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    snake = Snake()
    fruit = Fruit()

    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != [0, 1]:
                    snake.direction = [0, -1]
                elif event.key == pygame.K_DOWN and snake.direction != [0, -1]:
                    snake.direction = [0, 1]
                elif event.key == pygame.K_LEFT and snake.direction != [1, 0]:
                    snake.direction = [-1, 0]
                elif event.key == pygame.K_RIGHT and snake.direction != [-1, 0]:
                    snake.direction = [1, 0]

        snake.move_snake()

        if snake.check_collision():
            result = game_over_prompt()
            if result == "restart":
                snake.__init__()
                fruit.randomize()
            else:
                pygame.quit()
                sys.exit()

        if snake.body[0] == fruit.position:
            fruit.randomize()
            snake.add_block()

        screen.blit(background_image, (0, 0))
        snake.draw_snake()
        fruit.draw_fruit()

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, screen_size, screen_size, 30))
        score_text = font.render(f"Score: {snake.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, screen_size))

        pygame.display.update()
        clock.tick(7)

if __name__ == "__main__":
    main()
