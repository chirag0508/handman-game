import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 900, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")
clock = pygame.time.Clock()
FPS = 60

# Font setup
title_font = pygame.font.SysFont('comicsans', 70)
word_font = pygame.font.SysFont('comicsans', 60)
letter_font = pygame.font.SysFont('comicsans', 40)
category_font = pygame.font.SysFont('comicsans', 30)
score_font = pygame.font.SysFont('comicsans', 30)

# Word categories and words - EXPANDED
word_categories = {
    "Animals": ["ELEPHANT", "GIRAFFE", "PENGUIN", "DOLPHIN", "TIGER", "LION", "ZEBRA", "MONKEY", "KANGAROO", "PANDA", 
               "KOALA", "HEDGEHOG", "SQUIRREL", "RACCOON", "CROCODILE", "FLAMINGO", "PARROT", "OCTOPUS", "WALRUS", "RHINO"],
    "Countries": ["FRANCE", "JAPAN", "CANADA", "BRAZIL", "AUSTRALIA", "MEXICO", "GERMANY", "INDIA", "ITALY", "EGYPT",
                 "THAILAND", "ARGENTINA", "SWEDEN", "PORTUGAL", "IRELAND", "DENMARK", "PERU", "MOROCCO", "TURKEY", "NIGERIA"],
    "Foods": ["PIZZA", "SUSHI", "HAMBURGER", "CHOCOLATE", "PASTA", "TACO", "WAFFLE", "SALAD", "SANDWICH", "CURRY",
             "PANCAKE", "CROISSANT", "LASAGNA", "BURRITO", "CHEESECAKE", "DUMPLING", "RAMEN", "PRETZEL", "MUFFIN", "DONUT"],
    "Sports": ["FOOTBALL", "BASKETBALL", "TENNIS", "SWIMMING", "VOLLEYBALL", "CRICKET", "GOLF", "HOCKEY", "BASEBALL", "SKIING",
              "BADMINTON", "WRESTLING", "BOXING", "ARCHERY", "SURFING", "CYCLING", "FENCING", "ROWING", "SKATEBOARDING", "CLIMBING"],
    "Professions": ["DOCTOR", "TEACHER", "ENGINEER", "ARTIST", "CHEF", "FIREFIGHTER", "PILOT", "SCIENTIST", "ACTOR", "FARMER",
                   "ARCHITECT", "JOURNALIST", "DENTIST", "PROGRAMMER", "ELECTRICIAN", "DETECTIVE", "LAWYER", "MUSICIAN", "ASTRONAUT", "BAKER"],
    "Movies": ["TITANIC", "AVATAR", "INCEPTION", "JAWS", "FROZEN", "GLADIATOR", "JOKER", "GOODFELLAS", "PARASITE", "CASABLANCA",
              "PSYCHO", "ALIEN", "MATRIX", "SPOTLIGHT", "BATMAN", "JURASSIC", "SHREK", "GODFATHER", "BRAVEHEART", "ROCKY"],
    "Technology": ["COMPUTER", "INTERNET", "SMARTPHONE", "BLUETOOTH", "PROCESSOR", "KEYBOARD", "MONITOR", "WEBCAM", "ROUTER", "DATABASE",
                  "ALGORITHM", "SOFTWARE", "HARDWARE", "FIREWALL", "SERVER", "LAPTOP", "HEADPHONES", "TABLET", "PRINTER", "SCANNER"],
    "Fruits": ["APPLE", "BANANA", "ORANGE", "STRAWBERRY", "PINEAPPLE", "WATERMELON", "GRAPE", "PEACH", "MANGO", "KIWI",
              "LEMON", "CHERRY", "BLUEBERRY", "PAPAYA", "COCONUT", "APRICOT", "RASPBERRY", "PLUM", "AVOCADO", "POMEGRANATE"],
    "Vehicles": ["BICYCLE", "AIRPLANE", "SUBMARINE", "HELICOPTER", "MOTORCYCLE", "AMBULANCE", "BULLDOZER", "SAILBOAT", "TRACTOR", "LIMOUSINE",
                "CONVERTIBLE", "SPACESHIP", "RICKSHAW", "SCOOTER", "ESCALATOR", "TROLLEY", "HOVERCRAFT", "FORKLIFT", "CONTAINER", "CARAVAN"]
}

# Combine all words into one list for random selection
all_words = []
for category, words in word_categories.items():
    all_words.extend([(word, category) for word in words])

# REPOSITIONED HANGMAN - Move it to left side of screen
# Hangman stages - with adjusted coordinates to fit on left side
HANGMAN_STAGES = [
    # Stage 0: Base
    [(50, 350, 150, 350)],
    # Stage 1: Vertical pole
    [(50, 350, 150, 350), (100, 350, 100, 100)],
    # Stage 2: Horizontal pole
    [(50, 350, 150, 350), (100, 350, 100, 100), (100, 100, 200, 100)],
    # Stage 3: Rope
    [(50, 350, 150, 350), (100, 350, 100, 100), (100, 100, 200, 100), (200, 100, 200, 130)],
    # Stage 4: Head
    [(50, 350, 150, 350), (100, 350, 100, 100), (100, 100, 200, 100), (200, 100, 200, 130), (200, 150, 20)],
    # Stage 5: Body
    [(50, 350, 150, 350), (100, 350, 100, 100), (100, 100, 200, 100), (200, 100, 200, 130), 
     (200, 150, 20), (200, 150, 200, 230)],
    # Stage 6: Left arm
    [(50, 350, 150, 350), (100, 350, 100, 100), (100, 100, 200, 100), (200, 100, 200, 130), 
     (200, 150, 20), (200, 150, 200, 230), (200, 170, 160, 190)],
    # Stage 7: Right arm
    [(50, 350, 150, 350), (100, 350, 100, 100), (100, 100, 200, 100), (200, 100, 200, 130), 
     (200, 150, 20), (200, 150, 200, 230), (200, 170, 160, 190), (200, 170, 240, 190)],
    # Stage 8: Left leg
    [(50, 350, 150, 350), (100, 350, 100, 100), (100, 100, 200, 100), (200, 100, 200, 130), 
     (200, 150, 20), (200, 150, 200, 230), (200, 170, 160, 190), (200, 170, 240, 190),
     (200, 230, 160, 280)],
    # Stage 9: Right leg (Complete hangman)
    [(50, 350, 150, 350), (100, 350, 100, 100), (100, 100, 200, 100), (200, 100, 200, 130), 
     (200, 150, 20), (200, 150, 200, 230), (200, 170, 160, 190), (200, 170, 240, 190),
     (200, 230, 160, 280), (200, 230, 240, 280)]
]

class Button:
    def __init__(self, x, y, letter, width=40, height=40):
        self.x = x
        self.y = y
        self.letter = letter
        self.width = width
        self.height = height
        self.color = WHITE
        self.text_color = BLACK
        self.is_clicked = False
        self.is_correct = False
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0, 5)
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height), 2, 5)
        text = letter_font.render(self.letter, 1, self.text_color)
        win.blit(text, (self.x + (self.width//2 - text.get_width()//2), 
                        self.y + (self.height//2 - text.get_height()//2)))
        
    def is_over(self, pos):
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
            return True
        return False
        
class HangmanGame:
    def __init__(self):
        self.reset_game()
        self.score = 0
        self.high_score = self.load_high_score()
        
    def reset_game(self):
        # Choose a random word and its category
        self.word, self.category = random.choice(all_words)
        self.guessed = set()
        self.wrong_guesses = 0
        self.game_status = "playing"  # "playing", "won", "lost"
        
        # Create letter buttons - CENTERED on screen
        self.buttons = []
        start_x = (WIDTH - 13 * 40) // 2  # Center the first row (A-M)
        for i, letter in enumerate("ABCDEFGHIJKLM"):
            self.buttons.append(Button(start_x + i*40, 400, letter))
        
        start_x = (WIDTH - 13 * 40) // 2  # Center the second row (N-Z)
        for i, letter in enumerate("NOPQRSTUVWXYZ"):
            self.buttons.append(Button(start_x + i*40, 450, letter))
    
    def load_high_score(self):
        try:
            if os.path.exists("hangman_highscore.txt"):
                with open("hangman_highscore.txt", "r") as f:
                    return int(f.read().strip())
        except:
            pass
        return 0
    
    def save_high_score(self):
        with open("hangman_highscore.txt", "w") as f:
            f.write(str(self.high_score))
            
    def draw_word(self, win):
        display_word = ""
        for letter in self.word:
            if letter in self.guessed:
                display_word += letter + " "
            else:
                display_word += "_ "
                
        text = word_font.render(display_word, 1, BLACK)
        win.blit(text, (WIDTH//2 - text.get_width()//2, 300))
        
    def draw_category(self, win):
        text = category_font.render(f"Category: {self.category}", 1, BLUE)
        win.blit(text, (WIDTH//2 - text.get_width()//2, 250))
        
    def draw_hangman(self, win):
        # Draw the current stage of the hangman
        current_stage = min(self.wrong_guesses, len(HANGMAN_STAGES) - 1)
        
        for element in HANGMAN_STAGES[current_stage]:
            if len(element) == 4:  # Line
                pygame.draw.line(win, BLACK, (element[0], element[1]), (element[2], element[3]), 5)
            elif len(element) == 3:  # Circle
                pygame.draw.circle(win, BLACK, (element[0], element[1]), element[2], 5)
                
    def draw_score(self, win):
        score_text = score_font.render(f"Score: {self.score}", 1, BLACK)
        high_score_text = score_font.render(f"High Score: {self.high_score}", 1, BLACK)
        win.blit(score_text, (20, 20))
        win.blit(high_score_text, (20, 60))
        
    def draw_game_result(self, win):
        if self.game_status == "won":
            text = title_font.render("You Won!", 1, GREEN)
        else:  # lost
            text = title_font.render("Game Over", 1, RED)
            # Show the correct word
            word_text = word_font.render(f"The word was: {self.word}", 1, RED)
            win.blit(word_text, (WIDTH//2 - word_text.get_width()//2, 180))
            
        win.blit(text, (WIDTH//2 - text.get_width()//2, 100))
        
        # Prompt to play again
        again_text = letter_font.render("Press SPACE to play again", 1, BLACK)
        win.blit(again_text, (WIDTH//2 - again_text.get_width()//2, 520))
        
    def check_won(self):
        for letter in self.word:
            if letter not in self.guessed:
                return False
        return True
        
    def guess(self, letter):
        self.guessed.add(letter)
        
        # Check if letter is in the word
        if letter in self.word:
            # Find the button for this letter and mark it as correct
            for button in self.buttons:
                if button.letter == letter:
                    button.color = GREEN
                    button.is_correct = True
                    break
            
            # Check if the player has won
            if self.check_won():
                self.game_status = "won"
                self.score += len(self.word) * 10 - self.wrong_guesses * 5
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
        else:
            self.wrong_guesses += 1
            # Find the button for this letter and mark it as incorrect
            for button in self.buttons:
                if button.letter == letter:
                    button.color = RED
                    break
                    
            # Check if the player has lost
            if self.wrong_guesses >= len(HANGMAN_STAGES) - 1:
                self.game_status = "lost"
    
    def draw(self, win):
        win.fill(LIGHT_BLUE)
        
        # Draw the title
        title_text = title_font.render("Hangman", 1, BLACK)
        win.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 20))
        
        # Draw the hangman
        self.draw_hangman(win)
        
        # Draw category
        self.draw_category(win)
        
        # Draw the current state of the word
        self.draw_word(win)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(win)
            
        # Draw score
        self.draw_score(win)
        
        # Draw game result if game is over
        if self.game_status in ["won", "lost"]:
            self.draw_game_result(win)
            
        pygame.display.update()
        
    def handle_click(self, pos):
        if self.game_status == "playing":
            for button in self.buttons:
                if button.is_over(pos) and not button.is_clicked:
                    button.is_clicked = True
                    self.guess(button.letter)
                    return

def main():
    game = HangmanGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.handle_click(pos)
                
            if event.type == pygame.KEYDOWN:
                # Check for SPACE key press to restart game
                if event.key == pygame.K_SPACE and game.game_status in ["won", "lost"]:
                    game.reset_game()
                    
                # Allow keyboard letter input
                if game.game_status == "playing" and ord('a') <= event.key <= ord('z'):
                    letter = chr(event.key).upper()
                    for button in game.buttons:
                        if button.letter == letter and not button.is_clicked:
                            button.is_clicked = True
                            game.guess(letter)
                            break
        
        game.draw(screen)
        clock.tick(FPS)

if __name__ == "__main__":
    main()