import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("A Special Game for My Love")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193)
HOVER_PINK = (255, 105, 180)
LIGHT_RED = (255, 102, 102)
FINAL_MESSAGE_COLOR = (255, 240, 245)
BACKGROUND_COLOR = (240, 240, 255)

# Load background music (Replace with your music file path)
#pygame.mixer.music.load('your_music_file.mp3')
#pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Helper function to load images with error handling
def load_image(path):
    if os.path.exists(path):
        return pygame.image.load(path)
    else:
        print(f"Error: Image not found at path: {path}")
        return pygame.Surface((screen_width, screen_height))  # Create a fallback surface

# Load images with proper paths
image1 = pygame.image.load('IMG_1663.jpg')
image2 = pygame.image.load('IMG_3534.jpg')
image3 = pygame.image.load('IMG_4301.jpg')
image4 = pygame.image.load('IMG_1158.jpg')
image5 = pygame.image.load('IMG_3425.jpg')
image6 = pygame.image.load('Screenshot (419).png')
image7 = load_image('IMG_4923.jpg')

# Resizing images to fit the screen with smoothing
image1 = pygame.transform.smoothscale(image1, (screen_width, screen_height))
image2 = pygame.transform.smoothscale(image2, (screen_width, screen_height))
image3 = pygame.transform.smoothscale(image3, (screen_width, screen_height))
image4 = pygame.transform.smoothscale(image4, (screen_width, screen_height))
image5 = pygame.transform.smoothscale(image5, (screen_width, screen_height))
image6 = pygame.transform.smoothscale(image6, (screen_width, screen_height))
image7 = pygame.transform.smoothscale(image7, (screen_width, screen_height))

# List of images for the storyline
images = [image1, image2, image3, image4, image5, image6, image7]

# Corresponding messages for each image
messages = [
    "I will never stop trying for you", "You always make me feel so special",
    "You brighten my life every single day.",
    "Every adventure with you is unforgetable",
    "I'm sorry for getting on your nerves",
    "Thank you for putting up with me",
    "Together, we are unstoppable.",
    "You are my forever and always."
]

# Final celebration message (you can use one or two lines)
final_message = ["I love you,", "to the end of the world!"]

# Fonts for messages and choices
font = pygame.font.SysFont(None, 45)
choice_font = pygame.font.SysFont(None, 35)
final_font = pygame.font.SysFont(None, 50, bold=True)

# Button class for loving actions with improved appearance
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 40)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=15)  # Rounded corners
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=15)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False

# Create buttons for loving actions with better spacing
hug_button = Button("Hugs", 100, 450, 180, 50, PINK, HOVER_PINK)
handhold_button = Button("Our smiles", 320, 450, 200, 50, PINK, HOVER_PINK)
gift_button = Button("Surprise Gifts", 540, 450, 180, 50, PINK, HOVER_PINK)

# Heart particle animation with rotation, scaling, and interaction
class HeartParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(15, 30)
        self.color = PINK
        self.speed = random.uniform(1, 2)
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(1, 3)
        self.scale_speed = random.uniform(0.02, 0.05)
        self.clicked = False

    def draw_heart(self, screen):
        heart_points = [
            (self.x, self.y - self.size // 4),  # Top point
            (self.x - self.size // 2, self.y),  # Left bottom
            (self.x + self.size // 2, self.y)   # Right bottom
        ]
        pygame.draw.polygon(screen, self.color, heart_points)
        pygame.draw.circle(screen, self.color, (self.x - self.size // 4, self.y - self.size // 4), self.size // 4)
        pygame.draw.circle(screen, self.color, (self.x + self.size // 4, self.y - self.size // 4), self.size // 4)

    def float_up(self, screen):
        self.y -= self.speed
        self.angle += self.rotation_speed
        self.size += self.scale_speed  # Scaling the heart
        if self.y < -self.size or self.clicked:
            self.y = screen_height + random.randint(0, 100)
            self.x = random.randint(0, screen_width)
            self.clicked = False  # Reset the clicked state
        self.draw_heart(screen)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.x - self.size // 2 <= mouse_pos[0] <= self.x + self.size // 2 and \
               self.y - self.size // 2 <= mouse_pos[1] <= self.y + self.size // 2:
                self.clicked = True

# Generate floating heart particles
heart_particles = [HeartParticle(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(30)]

# Confetti hearts for final celebration
confetti_particles = []

# Game loop variables
running = True
current_image = 0  # Start with the first image
fade_in = True
fade_alpha = 0  # Alpha level for fading effect
clock = pygame.time.Clock()
show_loving_actions = False  # Control when actions appear
love_meter = 0  # Love meter that fills up
love_meter_display = 0  # Love meter displayed (animated to gradually fill)
celebration_triggered = False  # Track if celebration has occurred
celebration_time = 0  # Timer for celebration sequence
celebration_duration = 300  # Number of frames to show the final celebration

# Function to display text with a fade effect
def draw_message(text, alpha):
    message_text = font.render(text, True, WHITE)
    message_text.set_alpha(alpha)  # Set transparency
    screen.blit(message_text, (100, 50))  # Adjust position as needed

# Function to draw the love meter with animated fill
def draw_love_meter():
    global love_meter_display
    if love_meter_display < love_meter:
        love_meter_display += 2  # Gradually fill the love meter
    meter_color = LIGHT_RED if love_meter_display >= 150 else RED
    pygame.draw.rect(screen, meter_color, pygame.Rect(50, 550, love_meter_display, 30))
    pygame.draw.rect(screen, WHITE, pygame.Rect(50, 550, 200, 30), 2)  # Love meter border
    love_text = font.render(f"Love Meter: {love_meter_display}%", True, WHITE)
    screen.blit(love_text, (50, 510))

# Final celebration: Trigger heart confetti and final message
def trigger_celebration():
    global celebration_triggered, confetti_particles
    if not celebration_triggered:
        celebration_triggered = True
        # Generate confetti hearts
        confetti_particles = [HeartParticle(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(50)]

# Draw final celebration message (handling 1 or 2 lines)
def draw_final_message():
    if len(final_message) == 1:
        # Single line message
        final_text = final_font.render(final_message[0], True, FINAL_MESSAGE_COLOR)
        final_text_rect = final_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(final_text, final_text_rect)
    elif len(final_message) > 1:
        # Multi-line message
        line1_text = final_font.render(final_message[0], True, FINAL_MESSAGE_COLOR)
        line2_text = final_font.render(final_message[1], True, FINAL_MESSAGE_COLOR)
        # Position both lines of text in the center of the screen
        line1_rect = line1_text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
        line2_rect = line2_text.get_rect(center=(screen_width // 2, screen_height // 2 + 40))
        screen.blit(line1_text, line1_rect)
        screen.blit(line2_text, line2_rect)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display background with subtle color change
    screen.fill(BACKGROUND_COLOR)

    # Display the current image
    screen.blit(images[current_image], (0, 0))

    # Apply fading effect to messages
    if fade_in:
        fade_alpha += 5  # Adjust fade speed
        if fade_alpha >= 255:
            fade_alpha = 255  # Max alpha value
            fade_in = False
            show_loving_actions = True  # Show loving actions after fade-in

    # Display the corresponding message
    draw_message(messages[current_image], fade_alpha)

    # Display loving actions
    if show_loving_actions and not celebration_triggered:
        hug_button.draw(screen)
        handhold_button.draw(screen)
        gift_button.draw(screen)

        if hug_button.is_clicked():
            current_image = (current_image + 1) % len(images)  # Go to the next image for "Hug"
            love_meter += 30  # Increase love meter more
            fade_in = True
            fade_alpha = 0
            show_loving_actions = False  # Reset loving actions display

        elif handhold_button.is_clicked():
            current_image = (current_image + 1) % len(images)  # Go to the next image for "Hold Hands"
            love_meter += 25  # Adjust love meter increase
            fade_in = True
            fade_alpha = 0
            show_loving_actions = False

        elif gift_button.is_clicked():
            current_image = (current_image + 1) % len(images)  # Go to the next image for "Surprise Gift"
            love_meter += 45  # Adjust love meter increase
            fade_in = True
            fade_alpha = 0
            show_loving_actions = False

        # Trigger final celebration if love meter reaches 200%
        if love_meter >= 200:
            trigger_celebration()

    # Animate floating hearts with rotation and scaling, and check for clicks
    for particle in heart_particles:
        particle.float_up(screen)
        particle.check_click()

    # Draw love meter
    draw_love_meter()

    # Handle final celebration
    if celebration_triggered:
        celebration_time += 1
        draw_final_message()
        for confetti in confetti_particles:
            confetti.float_up(screen)

        if celebration_time > celebration_duration:  # Display final celebration for some time
            pygame.quit()
            sys.exit()

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit FPS to 60

# Clean up
pygame.quit()
sys.exit()
