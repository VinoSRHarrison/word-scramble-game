import pygame
import random
import os
import sys

class WordScrambleGame:
    def __init__(self):
        print("Initializing Pygame...", flush=True)
        pygame.init()
        print("Initializing Mixer...", flush=True)
        pygame.mixer.init()

        self.WIDTH, self.HEIGHT = 800, 600
        print(f"Setting display mode to {self.WIDTH}x{self.HEIGHT}...", flush=True)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Word Scramble Game")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Fonts
        print("Loading fonts...", flush=True)
        self.FONT = pygame.font.Font(None, 74)
        self.SMALL_FONT = pygame.font.Font(None, 36)

        # Assets
        print("Loading assets...", flush=True)
        self.load_assets()
        print("Initialization complete!", flush=True)

        self.words = {
            'easy': ["cat", "dog", "sun", "bat", "hat", "pen", "pig", "cup", "bag", "bed", "car", "bus", "egg", "fan", "jam", "key", "lid", "map", "net", "owl", "pan", "rat", "top", "van", "win", "zip", "ant", "bee", "cow", "day", "ear", "fog", "gun", "hen", "ice", "jug", "kit", "log", "man"],
            'medium': ["apple", "grape", "house", "chair", "table", "bread", "brick", "snake", "light", "grass", "mount", "camel", "tiger", "brush", "cloud", "dream", "frogs", "juice", "knife", "lemon", "money", "night", "ocean", "piano", "queen", "river", "sugar", "train", "unity", "voice", "water", "xerox", "youth", "zebra", "amber", "blank", "clear", "drive", "earth", "fence", "giant"],
            'hard': ["python", "scramble", "pygame", "elephant", "dolphins", "keyboard", "notebook", "umbrella", "electric", "mystical", "journeys", "hospital", "printing", "blizzard", "calendar", "marathon", "valuable", "firework", "outreach", "festival", "sandwich", "superior", "triangle", "backyard", "amazing", "identify", "optimize", "generate", "sunshine", "mountain", "preserve", "recharge", "aquarium", "treasure", "umbrella", "galaxies", "painting", "sympathy", "together", "wildlife", "business"]
        }

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.reset_game_state()

    def load_assets(self):
        try:
            self.d_screen = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "imge.jpg")).convert(), (self.WIDTH, self.HEIGHT))
            self.g_screen = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "pngtree.png")).convert(), (self.WIDTH, self.HEIGHT))
            self.g_over_screen = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "background.jpg")).convert(), (self.WIDTH, self.HEIGHT))
            self.timer_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "TunePocket-Countdown-Timer-10-Sec-1-Preview.mp3"))
        except Exception as e:
            print(f"Error loading assets: {e}")
            # Fallbacks if assets missing
            self.d_screen = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.d_screen.fill(self.BLACK)
            self.g_screen = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.g_screen.fill((50, 50, 50))
            self.g_over_screen = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.g_over_screen.fill((100, 0, 0))
            self.timer_sound = None

    def reset_game_state(self):
        self.score = 0
        self.state = 'MENU'
        self.difficulty = 'easy'
        self.word_list = []
        self.reset_round()

    def reset_round(self):
        if not self.word_list:
            self.word_list = self.words[self.difficulty]
        self.current_word = random.choice(self.word_list)
        self.scrambled_word = self.scramble_word(self.current_word)
        self.player_input = ""
        self.timer = 30.0 # Standard round time = 60s
        self.sound_played = False
        self.message = ""
        self.message_timer = 0

    def scramble_word(self, word):
        word_chars = list(word)
        original = word
        # Limit tries to prevent infinite loop on short/repetitive words
        for _ in range(100):
            random.shuffle(word_chars)
            if ''.join(word_chars) != original or len(word) <= 1:
                break
        return ''.join(word_chars)

    def draw_text(self, text, font, color, x, y):
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def handle_menu_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.difficulty = 'easy'
                    self.start_game()
                elif event.key == pygame.K_2:
                    self.difficulty = 'medium'
                    self.start_game()
                elif event.key == pygame.K_3:
                    self.difficulty = 'hard'
                    self.start_game()
        return True

    def start_game(self):
        self.word_list = self.words[self.difficulty]
        self.state = 'PLAYING'
        self.score = 0
        self.reset_round()

    def handle_playing_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.player_input.lower() == self.current_word:
                        self.score += 1
                        self.message = "Correct!"
                        self.message_timer = 1.0  # Show for 1 second
                        self.reset_round()
                    else:
                        self.message = "Try Again!"
                        self.message_timer = 1.0
                elif event.key == pygame.K_BACKSPACE:
                    self.player_input = self.player_input[:-1]
                else:
                    if event.unicode.isalpha():
                        self.player_input += event.unicode
        return True

    def handle_game_over_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state = 'MENU'
                elif event.key == pygame.K_q:
                    return False
        return True

    def update(self):
        dt = 1 / self.FPS
        if self.state == 'PLAYING':
            self.timer -= dt
            
            # Sound logic fix: Play once when 10 seconds remain
            if self.timer <= 10.0 and self.timer > 0 and not self.sound_played:
                if self.timer_sound:
                    self.timer_sound.play()
                self.sound_played = True

            if self.message_timer > 0:
                self.message_timer -= dt
            else:
                self.message = ""

            if self.timer <= 0:
                self.state = 'GAME_OVER'

    def draw(self):
        if self.state == 'MENU':
            self.screen.blit(self.d_screen, (0, 0))
            self.draw_text("SELECT DIFFICULTY", self.FONT, self.WHITE, self.WIDTH // 2 - 250, self.HEIGHT // 2 - 150)
            self.draw_text("1. Easy", self.SMALL_FONT, self.GREEN, self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50)
            self.draw_text("2. Medium", self.SMALL_FONT, self.BLACK, self.WIDTH // 2 - 100, self.HEIGHT // 2)
            self.draw_text("3. Hard", self.SMALL_FONT, self.RED, self.WIDTH // 2 - 100, self.HEIGHT // 2 + 50)

        elif self.state == 'PLAYING':
            self.screen.blit(self.g_screen, (0, 0))
            self.draw_text(f"Scrambled: {self.scrambled_word}", self.FONT, self.WHITE, 50, 50)
            self.draw_text(f"Your Guess: {self.player_input}", self.SMALL_FONT, self.BLUE, 50, 150)
            self.draw_text(f"Score: {self.score}", self.SMALL_FONT, self.GREEN, 50, 250)
            
            # Change timer color when time is low
            time_color = self.RED if self.timer <= 10 else self.WHITE
            self.draw_text(f"Time Left: {int(self.timer)}", self.SMALL_FONT, time_color, 50, 350)

            if self.message:
                msg_color = self.GREEN if self.message == "Correct!" else self.RED
                self.draw_text(self.message, self.SMALL_FONT, msg_color, self.WIDTH // 2 - 50, self.HEIGHT // 2 + 50)

        elif self.state == 'GAME_OVER':
            self.screen.blit(self.g_over_screen, (0, 0))
            self.draw_text("Game Over!", self.FONT, self.RED, self.WIDTH // 2 - 150, self.HEIGHT // 2 - 100)
            self.draw_text(f"Your Score: {self.score}", self.SMALL_FONT, self.BLACK, self.WIDTH // 2 - 100, self.HEIGHT // 2)
            self.draw_text("Press R to Restart or Q to Quit", self.SMALL_FONT, self.BLUE, self.WIDTH // 2 - 200, self.HEIGHT // 2 + 50)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            
            if self.state == 'MENU':
                running = self.handle_menu_events(events)
            elif self.state == 'PLAYING':
                running = self.handle_playing_events(events)
            elif self.state == 'GAME_OVER':
                running = self.handle_game_over_events(events)
                
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

        try:
            pygame.quit()
        except Exception:
            pass

if __name__ == "__main__":
    game = WordScrambleGame()
    game.run()
