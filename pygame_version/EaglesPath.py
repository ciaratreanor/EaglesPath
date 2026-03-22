import warnings
# Suppress the UserWarning related to pkg_resources being deprecated
warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated as an API.*")

import pygame
import sys
import math

# Configuration & Initialization
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eagle's Path")
clock = pygame.time.Clock()

#Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CRIMSON = (153, 0, 31)
PASTEL_GOLD = (255, 223, 186)
BRIGHT_GOLD = (255, 235, 204)

FONT_SIZE = 20

try:
    font = pygame.font.Font("data/PixelifySans-Regular.ttf", FONT_SIZE)
except pygame.error:
    # Fallback to system font if the custom file is not found.
    print(f"Custom font 'PixelifySans-Regular.ttf' not found. Falling back to Arial system font at size {FONT_SIZE}.")
    font = pygame.font.SysFont("Arial", FONT_SIZE)

# Score Variables & State Management (Module-level)
social_score = 0
athlete_score = 0
achiever_score = 0
creative_score = 0
activist_score = 0
spiritual_score = 0
cultural_score = 0

social_clubs = ["Campus Activities Board", "Residence Hall Association", "Cooking Club"]
athlete_clubs =["Basketball Club", "Bike BC", "Ultimate Frisbee Club"]
achiever_clubs = ["Boston College Computer Science Society", "Boston College Investment Club", "Public Health Club"]
creative_clubs = ["Boston College Symphony Orchestra", "Boston College Art Club", "UPrising Dance Crew"]
activist_clubs = ["Eagle Political Society", "EcoPledge", "Ignatian Family Teach-in for Justice"]
spiritual_clubs = ["BC ALIVE", "InterVarsity Christian Fellowship", "Buddhism Club"]
cultural_clubs = ["International Club", "Black Student Forum", "Chinese Students Association"]

game_state = "menu"
current_question_index = 0

# Button Setup
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 100
BUTTON_TEXT_COLOR = CRIMSON
BUTTON_RADIUS = 12

BUTTON_AREA_HEIGHT = 220
IMAGE_AREA_HEIGHT = SCREEN_HEIGHT - BUTTON_AREA_HEIGHT
BUTTON_HEIGHT_Q = 100
BUTTON_Q_ROW_PADDING = 15
BUTTON_Q_ROW_MARGIN = 10

# Menu and Results page images
MENU_ICON_FILENAME = "data/eaglespath.png"
RESULTS_ICON_FILENAME = "data/bc_pixelated.png"

# Image/Position Storage
image_assets = {}

# Function to load, scale, and center images
def load_and_center_image(filename):
    """Loads, scales to fit within the IMAGE_AREA_HEIGHT, and centers an image."""
    try:
        temp_img = pygame.image.load(filename).convert_alpha()
        orig_w, orig_h = temp_img.get_size()

        # Calculate maximum target dimensions for the top area
        target_max_w = SCREEN_WIDTH
        target_max_h = IMAGE_AREA_HEIGHT

        # Calculate scale factor to fill entire screen
        scale_factor = max(target_max_w / orig_w, target_max_h / orig_h)

        new_w = int(orig_w * scale_factor)
        new_h = int(orig_h * scale_factor)

        # Scale the image
        scaled_img = pygame.transform.scale(temp_img, (new_w, new_h))

        # Calculate centered position (relative to the top-left of the screen)
        center_x = (SCREEN_WIDTH - new_w) // 2
        center_y = (IMAGE_AREA_HEIGHT - new_h) // 2 + 40

        return scaled_img, (center_x, center_y)
    except pygame.error as e:
        print(f"Warning: Could not load custom image '{filename}'. Error: {e}")
        return None, (0, 0) # Fallback

# Helper function to wrap text onto multiple lines
def wrap_text(text, font, max_width):
    """Splits text into lines that fit within max_width."""
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + ' ' + word if current_line else word
        test_width, _ = font.size(test_line)

        if test_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

# Function to draw wrapped text with a background box
def draw_text_box(surface, text, text_color, bg_color, font, max_width, center_x, center_y, padding=20):
    """Draws multi-line text centered, with a background box."""
    lines = wrap_text(text, font, max_width - (2 * padding))
    line_height = font.get_height()

    # Calculate box dimensions
    max_line_width = 0
    for line in lines:
        max_line_width = max(max_line_width, font.size(line)[0])

    box_width = max_line_width + (2 * padding)
    box_height = (len(lines) * line_height) + (2 * padding)

    # Box rectangle (centered)
    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (center_x, center_y)

    # Draw the background box
    pygame.draw.rect(surface, bg_color, box_rect, border_radius=BUTTON_RADIUS)

    # Draw the text lines
    start_y = box_rect.top + padding
    for line in lines:
        text_surface = font.render(line, True, text_color)
        text_rect = text_surface.get_rect(centerx=center_x)
        text_rect.top = start_y
        surface.blit(text_surface, text_rect)
        start_y += line_height

    return box_rect.height # Return height of the box drawn

# Function to create button surfaces with text
def create_button_images(text, color, hover_color):

    img = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
    clicked_img = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)

    pygame.draw.rect(img, color, img.get_rect(), border_radius=BUTTON_RADIUS)
    pygame.draw.rect(clicked_img, hover_color, clicked_img.get_rect(), border_radius=BUTTON_RADIUS)

    # Use 20px padding for wrapping inside the button
    lines = wrap_text(text, font, BUTTON_WIDTH - 20)

    line_height = font.get_height()
    total_text_height = len(lines) * line_height
    start_y = (BUTTON_HEIGHT - total_text_height) // 2

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(BUTTON_WIDTH // 2, start_y + (i * line_height) + (line_height // 2)))

        img.blit(text_surface, text_rect)
        clicked_img.blit(text_surface, text_rect)

    return img, clicked_img


# Button class with 7 attribute scores
class Button():
    """A clickable button with hover state that holds score values."""
    def __init__(self, x, y, image, clicked_image,
                 achiever_value, social_value, creative_value, activist_value,
                 athlete_value, spiritual_value, cultural_value):
        # Image setup
        self.original_image = image
        self.clicked_image = clicked_image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Score attributes
        self.achiever_value = achiever_value
        self.social_value = social_value
        self.creative_value = creative_value
        self.activist_value = activist_value
        self.athlete_value = athlete_value
        self.spiritual_value = spiritual_value
        self.cultural_value = cultural_value

    def check_click(self, pos):
        """Returns True if the given position (from a MOUSEBUTTONDOWN event)
           is inside the button rect."""
        return self.rect.collidepoint(pos)

    def draw(self):
        pos = pygame.mouse.get_pos()
        current_image = self.original_image

        if self.rect.collidepoint(pos):
            current_image = self.clicked_image # Hover effect

        screen.blit(current_image, (self.rect.x, self.rect.y))

    def get_scores(self):
        # Return all 7 scores in the order they will be unpacked
        return (self.achiever_value, self.social_value, self.creative_value,
                self.activist_value, self.athlete_value, self.spiritual_value,
                self.cultural_value)


# Generated button images for use
start_img, start_img_hover = create_button_images("PRESS TO PLAY!", PASTEL_GOLD, BRIGHT_GOLD)

# Question Data and Button Generation Setup (includes images for each question page)
QUESTION_DATA = [
    {
        "prompt": "Q1: Your group is behind on a big assignment. One person hasn’t done their part, and the deadline’s tomorrow.",
        "filename": "data/bapst_pixelated.png",
        "options": [
            "Redo the missing section yourself so the project looks polished",
            "Call a group meeting to talk it through",
            "Redesign the slides to make them more engaging",
            "Email the professor asking for an extension and explain the issue",
            "Offer to lead a late-night work session with snacks",
            "Help everyone manage stress and remind them it’s just one grade",
            "Check in with the missing person privately",
        ],
        "scores": [
            (2, 0, 0, 1, 1, 0, 0),
            (1, 2, 0, 0, 0, 0, 1),
            (1, 1, 2, 0, 0, 0, 0),
            (1, 0, 0, 2, 0, 0, 1),
            (1, 1, 0, 0, 2, 0, 0),
            (0, 1, 0, 0, 0, 2, 1),
            (0, 1, 0, 0, 0, 1, 2),
        ]
    },
    {
        "prompt": "Q2: You’re wandering through the annual student club fair. What table grabs your attention?",
        "filename": "data/quad_pixelated.png",
        "options": [
            "One with flyers about scholarships and research opportunities.",
            "A table playing loud music and handing out stickers.",
            "A booth with students painting a banner",
            "A group giving out buttons about voting rights.",
            "A sports demo where you can try rock climbing",
            "A table sharing foods from different cultures.",
            "A quiet setup with candles for meditation and reflection.",
        ],
        "scores": [
            (2, 0, 1, 1, 0, 0, 0),
            (0, 2, 1, 0, 1, 0, 0),
            (0, 0, 2, 1, 0, 0, 1),
            (1, 0, 0, 2, 0, 0, 1),
            (1, 1, 0, 0, 2, 0, 0),
            (0, 1, 0, 0, 0, 1, 2),
            (0, 0, 1, 0, 0, 2, 1),
        ]
    },
    {
        "prompt": "Q3: It’s 11:30 PM and you’ve just finished studying. You have an early class tomorrow, but your phone buzzes with an invite.",
        "filename": "data/ignatius_pixelated.png",
        "options": [
            "Stay up and finish revising your notes — you’ll thank yourself later.",
            "Go to your friend’s room to hang out and decompress.",
            "Start sketching because you’re suddenly inspired.",
            "Join a late-night discussion about campus policies.",
            "Lace up your shoes for a quick run under the stars.",
            "Call your mom and talk about something you’ve been thinking about.",
            "Sit quietly for ten minutes to reflect before bed.",
        ],
        "scores": [
            (2, 0, 0, 0, 1, 1, 0),
            (0, 2, 1, 0, 0, 0, 1),
            (0, 1, 2, 0, 0, 1, 0),
            (1, 1, 0, 2, 0, 0, 0),
            (1, 0, 0, 0, 2, 1, 0),
            (0, 1, 0, 0, 0, 1, 2),
            (0, 0, 1, 0, 0, 2, 1),
        ]
    },
    {
        "prompt": "Q4: Your professor mentions a community service opportunity this weekend. What catches your interest?",
        "filename": "data/red_tree_pixelated.png",
        "options": [
            "Tutoring local kids",
            "Organizing a charity 5K",
            "Creating posters to advertise the event.",
            "Volunteering at a cultural center.",
            "Helping manage logistics and schedules.",
            "Preparing a reflection or prayer for the closing.",
            "Helping spread the word among other communities",
        ],
        "scores": [
            (2, 0, 0, 1, 0, 0, 1),
            (1, 0, 0, 1, 2, 0, 0),
            (1, 0, 2, 1, 0, 0, 0),
            (0, 1, 0, 0, 0, 1, 2),
            (1, 2, 0, 0, 1, 0, 0),
            (0, 0, 1, 0, 0, 2, 1),
            (1, 1, 0, 2, 0, 0, 0),
        ]
    },
    {
        "prompt": "Q5: It’s a rare free morning. How do you spend it?",
        "filename": "data/gasson_pixelated.png",
        "options": [
            "Plan your week and set new goals.",
            "Brunch with friends — you need to catch up.",
            "Work on your photography project outside.",
            "Attend a social justice workshop on campus.",
            "Join an intramural scrimmage.",
            "Cook a traditional meal with your roommates.",
            "Walk to a quiet garden to clear your mind.",
        ],
        "scores": [
            (2, 0, 0, 0, 1, 1, 0),
            (0, 2, 1, 0, 0, 0, 1),
            (1, 0, 2, 0, 0, 1, 0),
            (0, 0, 0, 2, 0, 1, 1),
            (1, 1, 0, 0, 2, 0, 0),
            (0, 1, 0, 0, 0, 1, 2),
            (0, 0, 1, 0, 0, 2, 1),
        ]
    }
]

MAX_QUESTIONS = len(QUESTION_DATA)
all_question_buttons = []
BUTTON_MARGIN = 16

# 2 rows of 7 buttons for answers
BUTTON_Q_START_Y_ROW1 = SCREEN_HEIGHT - BUTTON_AREA_HEIGHT + BUTTON_Q_ROW_PADDING
BUTTON_Q_START_Y_ROW2 = BUTTON_Q_START_Y_ROW1 + BUTTON_HEIGHT_Q + BUTTON_Q_ROW_MARGIN

# Adjust button size for 4-button row layout
NEW_BUTTON_WIDTH = 230

# Recalculate Row 1 (4 buttons) centering
ROW1_WIDTH_NEW = (4 * NEW_BUTTON_WIDTH) + (3 * BUTTON_MARGIN)
ROW1_START_X_NEW = (SCREEN_WIDTH - ROW1_WIDTH_NEW) // 2

# Recalculate Row 2 (3 buttons) centering
ROW2_WIDTH_NEW = (3 * NEW_BUTTON_WIDTH) + (2 * BUTTON_MARGIN)
ROW2_START_X_NEW = (SCREEN_WIDTH - ROW2_WIDTH_NEW) // 2


# Function to create button images with specific width/height
def create_resized_button_images(text, color, hover_color, w, h):
    img = pygame.Surface((w, h), pygame.SRCALPHA)
    clicked_img = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(img, color, img.get_rect(), border_radius=BUTTON_RADIUS)
    pygame.draw.rect(clicked_img, hover_color, clicked_img.get_rect(), border_radius=BUTTON_RADIUS)
    lines = wrap_text(text, font, w - 20)
    line_height = font.get_height()
    total_text_height = len(lines) * line_height
    start_y = (h - total_text_height) // 2
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(w // 2, start_y + (i * line_height) + (line_height // 2)))
        img.blit(text_surface, text_rect)
        clicked_img.blit(text_surface, text_rect)
    return img, clicked_img

# Image Preloading

# Load and store menu/results images
image_assets["menu"] = load_and_center_image(MENU_ICON_FILENAME)
image_assets["results"] = load_and_center_image(RESULTS_ICON_FILENAME)

# Load question-specific images
for i, q_data in enumerate(QUESTION_DATA):
    key = f"quiz_{i}"
    image_assets[key] = load_and_center_image(q_data["filename"])


# Function to initialize all button instances for all 5 questions
for i, q_data in enumerate(QUESTION_DATA):
    buttons_for_q = []

    for j in range(7):
        # Determine X and Y based on which row the button belongs to
        if j < 4: # Row 1 buttons
            x = ROW1_START_X_NEW + j * (NEW_BUTTON_WIDTH + BUTTON_MARGIN)
            y = BUTTON_Q_START_Y_ROW1
        else: # Row 2 buttons
            row_index = j - 4
            x = ROW2_START_X_NEW + row_index * (NEW_BUTTON_WIDTH + BUTTON_MARGIN)
            y = BUTTON_Q_START_Y_ROW2

        option_text = q_data["options"][j]

        img, img_hover = create_resized_button_images(option_text, PASTEL_GOLD, BRIGHT_GOLD, NEW_BUTTON_WIDTH, BUTTON_HEIGHT_Q)

        scores = q_data["scores"][j]

        btn = Button(
            x, y,
            img, img_hover,
            achiever_value=scores[0], social_value=scores[1], creative_value=scores[2], activist_value=scores[3],
            athlete_value=scores[4], spiritual_value=scores[5], cultural_value=scores[6]
        )
        buttons_for_q.append(btn)
    all_question_buttons.append(buttons_for_q)


# Menu Button Instance
start_menu_button = Button(
    0, 0,
    start_img, start_img_hover,
    0, 0, 0, 0, 0, 0, 0
)


# Game Loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if game_state == "menu":
                if start_menu_button.check_click(mouse_pos):
                    # Reset scores and start quiz
                    social_score = 0
                    athlete_score = 0
                    achiever_score = 0
                    creative_score = 0
                    activist_score = 0
                    spiritual_score = 0
                    cultural_score = 0
                    current_question_index = 0
                    game_state = "quiz"
                    break

            elif game_state == "quiz":
                if current_question_index < MAX_QUESTIONS:
                    current_buttons = all_question_buttons[current_question_index]

                    button_clicked = None
                    for button in current_buttons:
                        if button.check_click(mouse_pos):
                            button_clicked = button
                            break

                    if button_clicked:
                        achiever_add, social_add, creative_add, activist_add, athlete_add, spiritual_add, cultural_add = button_clicked.get_scores()

                        # Update scores
                        achiever_score += achiever_add
                        social_score += social_add
                        creative_score += creative_add
                        activist_score += activist_add
                        athlete_score += athlete_add
                        spiritual_score += spiritual_add
                        cultural_score += cultural_add

                        current_question_index += 1
                        break


    # Game State Logic

    # MENU STATE
    if game_state == "menu":
        # Draw Image Area
        img, pos = image_assets["menu"]
        if img:
            screen.blit(img, pos)
        else:
            pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, IMAGE_AREA_HEIGHT))
            pygame.draw.rect(screen, WHITE, (10, 10, SCREEN_WIDTH - 20, IMAGE_AREA_HEIGHT - 20), 2)
            fallback_text = font.render(f"Image Placeholder: Load {MENU_ICON_FILENAME}", True, WHITE)
            screen.blit(fallback_text, (SCREEN_WIDTH // 2 - fallback_text.get_width() // 2, 50))

        # Draw Instructions

        menu_instructions = "Make choices to discover clubs at BC for you!"
        draw_text_box(screen, menu_instructions, CRIMSON, PASTEL_GOLD, font,
                      SCREEN_WIDTH * 0.8, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)

        # Start Buttons
        start_menu_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40 - BUTTON_HEIGHT)
        start_menu_button.draw()

    # QUIZ STATE
    elif game_state == "quiz":

        if current_question_index < MAX_QUESTIONS:
            current_data = QUESTION_DATA[current_question_index]
            current_buttons = all_question_buttons[current_question_index]

            # Image Area for each question
            img_key = f"quiz_{current_question_index}"
            img, pos = image_assets.get(img_key, (None, (0, 0)))

            if img:
                screen.blit(img, pos)
            else:
                # Draw fallback for the specific question image
                pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, IMAGE_AREA_HEIGHT))
                pygame.draw.rect(screen, WHITE, (10, 10, SCREEN_WIDTH - 20, IMAGE_AREA_HEIGHT - 20), 2)

                fallback_text_line1 = font.render(f"Image Placeholder: Load {current_data['filename']}", True, WHITE)
                fallback_text_line2 = font.render(f"Question {current_question_index + 1}", True, WHITE)

                screen.blit(fallback_text_line1, (SCREEN_WIDTH // 2 - fallback_text_line1.get_width() // 2, 50))
                screen.blit(fallback_text_line2, (SCREEN_WIDTH // 2 - fallback_text_line2.get_width() // 2, 80))

            # Prompt
            draw_text_box(screen, current_data["prompt"], CRIMSON, PASTEL_GOLD, font,
                          SCREEN_WIDTH * 0.8, SCREEN_WIDTH // 2, 30) # Fixed position near top

            # Button background
            pygame.draw.rect(screen, CRIMSON, (0, SCREEN_HEIGHT - BUTTON_AREA_HEIGHT, SCREEN_WIDTH, BUTTON_AREA_HEIGHT))

            # Buttons
            for button in current_buttons:
                button.draw()
        else:
            game_state = "results"


    # RESULTS
    elif game_state == "results":

        # Draw Image Area
        img, pos = image_assets["results"]
        if img:
            screen.blit(img, pos)
        else:
            pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, IMAGE_AREA_HEIGHT))
            pygame.draw.rect(screen, WHITE, (10, 10, SCREEN_WIDTH - 20, IMAGE_AREA_HEIGHT - 20), 2)
            fallback_text = font.render(f"Image Placeholder: Load {RESULTS_ICON_FILENAME}", True, WHITE)
            screen.blit(fallback_text, (SCREEN_WIDTH // 2 - fallback_text.get_width() // 2, 50))


        # Calculate the highest scoring categories
        scores_map = {
            "Achiever": achiever_score, "Social": social_score, "Creative": creative_score,
            "Activist": activist_score, "Athlete": athlete_score, "Spiritual": spiritual_score,
            "Cultural": cultural_score,
        }

        scores_list = sorted(scores_map.items(), key=lambda item: item[1], reverse=True)


        # Results page title
        top_match_text = f"Matching Complete! Your Top Clubs are listed below!"
        draw_text_box(screen, top_match_text, CRIMSON, PASTEL_GOLD, font,
                      SCREEN_WIDTH * 0.7, SCREEN_WIDTH // 2, 175)

        # Draw crimson background for results summary
        pygame.draw.rect(screen, CRIMSON, (0, SCREEN_HEIGHT - BUTTON_AREA_HEIGHT, SCREEN_WIDTH, BUTTON_AREA_HEIGHT))

        # Display club matches
        y_offset = SCREEN_HEIGHT - BUTTON_AREA_HEIGHT + 15

        score_header = font.render("Boston College Club Matches:", True, WHITE)
        screen.blit(score_header, (SCREEN_WIDTH // 2 - score_header.get_width() // 2, y_offset))
        y_offset += 30

        column_width = SCREEN_WIDTH // 2

        # Display clubs of highest value category
        if scores_list[0][0] == "Achiever":
            for i, club in enumerate(achiever_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width // 2 - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[0][0] == "Social":
            for i, club in enumerate(social_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width // 2 - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[0][0] == "Athlete":
            for i, club in enumerate(athlete_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width // 2 - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[0][0] == "Creative":
            for i, club in enumerate(creative_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width // 2 - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[0][0] == "Activist":
            for i, club in enumerate(activist_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width // 2 - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[0][0] == "Spiritual":
            for i, club in enumerate(spiritual_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width // 2 - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[0][0] == "Cultural":
            for i, club in enumerate(cultural_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width // 2 - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))


        # Displplsy clubs of second highest category
        if scores_list[1][0] == "Achiever":
            for i, club in enumerate(achiever_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width + (column_width // 2) - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[1][0] == "Social":
            for i, club in enumerate(social_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width + (column_width // 2) - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[1][0] == "Athlete":
            for i, club in enumerate(athlete_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width + (column_width // 2) - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[1][0] == "Creative":
            for i, club in enumerate(creative_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width + (column_width // 2) - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[1][0] == "Activist":
            for i, club in enumerate(activist_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width + (column_width // 2) - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[1][0] == "Spiritual":
            for i, club in enumerate(spiritual_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width + (column_width // 2) - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))
        elif scores_list[1][0] == "Cultural":
            for i, club in enumerate(cultural_clubs):
              score_text = font.render(club, True, PASTEL_GOLD)
              x_pos = column_width + (column_width // 2) - score_text.get_width() // 2
              screen.blit(score_text, (x_pos, y_offset + (i * 30)))



    pygame.display.update()

pygame.quit()
sys.exit()

