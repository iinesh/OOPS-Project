import pygame
import pygame.freetype
import random
import os
import sys
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Screen settings
SCREEN_INFO = pygame.display.Info()
SCREEN_WIDTH = SCREEN_INFO.current_w
SCREEN_HEIGHT = SCREEN_INFO.current_h 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon Battle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

# Assets directories - create these folders in your project directory
IMAGE_DIR = "pokemon_img"
SOUND_DIR = "pokemon_audio"
FONT_DIR = "pokemon_text"

# Type chart (fixed duplicate "Ice")
type_chart = {
    "Fire": {"Water": 0.5, "Grass": 2.0, "Rock": 0.5, "Electric": 1.0, "Fire": 1.0, "Bug": 2.0, "Ice": 2.0, "Steel": 2.0},
    "Water": {"Fire": 2.0, "Grass": 0.5, "Rock": 2.0, "Electric": 0.5, "Water": 1.0, "Ice": 2.0, "Steel": 1.5},
    "Grass": {"Fire": 0.5, "Water": 2.0, "Rock": 2.0, "Electric": 1.0, "Grass": 1.0, "Bug": 0.5, "Flying": 0.5, "Poison": 0.5},
    "Rock": {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Electric": 1.0, "Rock": 1.0, "Steel": 0.5, "Fighting": 2.0},
    "Electric": {"Water": 2.0, "Rock": 0.5, "Grass": 0.5, "Fire": 1.0, "Electric": 1.0, "Flying": 2.0, "Steel": 1.5},
    "Psychic": {"Fighting": 2.0, "Poison": 2.0, "Ghost": 1.0, "Psychic": 1.0, "Bug": 2.0, "Dark": 0.5},
    "Fighting": {"Normal": 2.0, "Ice": 2.0, "Poison": 1.0, "Psychic": 0.5, "Fighting": 1.0, "Fairy": 0.5, "Flying": 0.5},
    "Ghost": {"Ghost": 2.0, "Normal": 0.0, "Psychic": 2.0, "Fighting": 1.0, "Dark": 2.0, "Fairy": 1.0},
    "Normal": {"Fighting": 2.0, "Ghost": 0.0, "Dark": 1.0, "Fairy": 1.0},
    "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Rock": 2.0, "Steel": 1.0, "Fairy": 2.0, "Ice": 2.0},
    "Fairy": {"Fighting": 2.0, "Dragon": 2.0, "Dark": 2.0, "Fairy": 1.0},
    "Dragon": {"Dragon": 2.0, "Fairy": 0.0, "Steel": 0.5, "Flying": 1.0},
    "Ground": {"Fire": 2.0, "Water": 1.0, "Grass": 0.5, "Electric": 2.0, "Bug": 1.0, "Poison": 2.0, "Rock": 2.0, "Flying": 0.0},
    "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Rock": 2.0, "Fighting": 2.0, "Steel": 1.5, "Dragon": 2.0, "Flying": 2.0},
    "Bug": {"Fire": 0.5, "Water": 1.0, "Grass": 2.0, "Electric": 1.0, "Flying": 0.5, "Fighting": 2.0, "Ghost": 1.0},
    "Poison": {"Fire": 1.0, "Water": 1.0, "Grass": 2.0, "Electric": 1.0, "Poison": 0.5, "Psychic": 2.0, "Ghost": 1.0, "Fairy": 2.0},
    "Flying": {"Fire": 1.0, "Water": 1.0, "Grass": 2.0, "Electric": 0.5, "Rock": 2.0, "Bug": 2.0, "Fighting": 2.0},
    "Dark": {"Fighting": 2.0, "Ghost": 2.0, "Fairy": 2.0, "Psychic": 2.0, "Dark": 1.0},
}

# Type colors for UI
type_colors = {
    "Fire": (240, 128, 48),
    "Water": (104, 144, 240),
    "Grass": (120, 200, 80),
    "Rock": (184, 160, 56),
    "Electric": (248, 208, 48),
    "Psychic": (248, 88, 136),
    "Fighting": (192, 48, 40),
    "Ghost": (112, 88, 152),
    "Normal": (168, 168, 120),
    "Steel": (184, 184, 208),
    "Fairy": (238, 153, 172),
    "Dragon": (112, 56, 248),
    "Ground": (224, 192, 104),
    "Ice": (152, 216, 216),
    "Bug": (168, 184, 32),
    "Poison": (160, 64, 160),
    "Flying": (168, 144, 240),
    "Dark": (112, 88, 72),
}

# Asset loading functions
def load_image(filename, scale=None):
    """Load an image and optionally scale it"""
    try:
        image_path = os.path.join(IMAGE_DIR, filename)
        image = pygame.image.load(image_path).convert_alpha()
        if scale:
            return pygame.transform.scale(image, scale)
        return image
    except pygame.error:
        print(f"Could not load image {filename}!")
        # Create a colored placeholder for missing images
        placeholder = pygame.Surface((200, 200), pygame.SRCALPHA)
        placeholder.fill((255, 0, 255))  # Bright pink for visibility
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Missing: {filename}", True, BLACK)
        placeholder.blit(text, (10, 90))
        if scale:
            return pygame.transform.scale(placeholder, scale)
        return placeholder

def load_sound(filename):
    """Load a sound file"""
    try:
        return mixer.Sound(os.path.join(SOUND_DIR, filename))
    except:
        print(f"Could not load sound {filename}!")
        return None

# Load fonts
pygame.freetype.init()
try:
    main_font = pygame.freetype.Font(os.path.join(FONT_DIR, "pokemon.ttf"), 24)
except:
    main_font = pygame.freetype.SysFont(None, 24)
    print("Pokemon font not found, using system font.")

try:
    battle_font = pygame.freetype.Font(os.path.join(FONT_DIR, "pokemon.ttf"), 32)
except:
    battle_font = pygame.freetype.SysFont(None, 32)

# Load background music
try:
    mixer.music.load(os.path.join(SOUND_DIR, "battle_music.mp3"))
    mixer.music.set_volume(0.5)
except:
    print("Battle music not found!")

# Load sound effects
try:
    select_sound = load_sound("select.wav")
    attack_sound = load_sound("attack.wav")
    hit_sound = load_sound("hit.wav")
    victory_sound = load_sound("victory.wav")
    defeat_sound = load_sound("defeat.wav")
except:
    print("Some sound effects couldn't be loaded!")

# Classes
class Move:
    def __init__(self, name, power, type_):
        self.name = name
        self.power = power
        self.type = type_
        
        # Load sound effect based on type
        self.sound = load_sound(f"{type_.lower()}_move.wav")
        if not self.sound:
            self.sound = attack_sound

    def calculate_damage(self, attacker, defender):
        base = (self.power * (attacker.attack / defender.defense))
        multiplier = type_chart.get(self.type, {}).get(defender.type, 1.0)
        return int(base * multiplier), multiplier

class Pokemon:
    def __init__(self, name, type_, hp, attack, defense, moves):
        self.name = name
        self.type = type_
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.moves = moves
        
        # Load images
        self.front_image = load_image(f"{name.lower()}_front.png", (300, 300))
        self.back_image = load_image(f"{name.lower()}_back.png", (300, 300))
        
        # Animation properties
        self.position = (0, 0)  # Will be set in battle setup
        self.original_position = (0, 0)
        self.is_animating = False
        self.animation_frame = 0
        self.animation_type = None
        
        # For damage flash animation
        self.flash_timer = 0
        self.is_flashing = False

    def take_damage(self, dmg):
        self.hp = max(0, self.hp - dmg)
        self.is_flashing = True
        self.flash_timer = 5  # Number of frames to flash
        if hit_sound:
            hit_sound.play()

    def is_fainted(self):
        return self.hp <= 0
        
    def animate_attack(self):
        self.is_animating = True
        self.animation_frame = 0
        self.animation_type = "attack"
        
    def animate_hit(self):
        self.is_animating = True
        self.animation_frame = 0
        self.animation_type = "hit"
        
    def update_animation(self):
        if not self.is_animating:
            return
            
        if self.animation_type == "attack":
            # Move forward then back
            if self.animation_frame < 5:
                self.position = (self.position[0] + 10, self.position[1])
            elif self.animation_frame < 10:
                self.position = (self.position[0] - 10, self.position[1])
            else:
                self.is_animating = False
                self.position = self.original_position
                
        elif self.animation_type == "hit":
            # Shake effect
            if self.animation_frame < 10:
                offset = random.randint(-5, 5)
                self.position = (self.original_position[0] + offset, self.original_position[1] + offset)
            else:
                self.is_animating = False
                self.position = self.original_position
                
        self.animation_frame += 1
        
        # Handle damage flash
        if self.is_flashing:
            if self.flash_timer > 0:
                self.flash_timer -= 1
            else:
                self.is_flashing = False

class LegendaryPokemon(Pokemon):
    def __init__(self, name, type_, hp, attack, defense, moves):
        super().__init__(name, type_, hp, attack, defense, moves)
        # Special effect for legendaries
        self.legendary_aura = load_image("legendary_aura.png", (350, 350))

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK, border_radius=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, BLACK, self.rect, width=2, border_radius=self.border_radius)
        
        text_surf, text_rect = main_font.render(self.text, self.text_color)
        text_rect.center = self.rect.center
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class Battle:
    def __init__(self, player, computer):
        self.player = player
        self.computer = computer
        self.message = "Battle Start!"
        self.current_turn = "player"  # player or computer
        self.battle_state = "choosing_move"  # choosing_move, animating, game_over
        self.animation_timer = 0
        self.winner = None
        self.move_buttons = []
        self.player_move_index = 0  # Store the selected move index
        self.computer_move_index = 0  # Store computer's move index
        
        # Load battle background
        self.background = load_image("battle_background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Set Pokemon positions
        self.player.position = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50)
        self.player.original_position = self.player.position
        self.computer.position = (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50)
        self.computer.original_position = self.computer.position
        
        # Create move buttons
        self.create_move_buttons()
        
        # Message box
        self.message_box = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
        
        # Start music
        try:
            mixer.music.play(-1)  # Loop indefinitely
        except:
            pass

    def create_move_buttons(self):
        self.move_buttons = []
        button_width = 200
        button_height = 60
        padding = 20
        start_x = (SCREEN_WIDTH - (2 * button_width + padding)) // 2
        start_y = SCREEN_HEIGHT - 250
        
        for i, move in enumerate(self.player.moves):
            x = start_x + (i % 2) * (button_width + padding)
            y = start_y + (i // 2) * (button_height + padding)
            
            # Use type color for button
            type_color = type_colors.get(move.type, (200, 200, 200))
            
            # Create a lighter version of the color for hover
            hover_color = tuple(min(c + 40, 255) for c in type_color)
            
            btn = Button(x, y, button_width, button_height, f"{move.name}", type_color, hover_color)
            self.move_buttons.append(btn)

    def effectiveness_text(self, mult):
        if mult > 1:
            return "It's super effective!"
        elif mult < 1 and mult > 0:
            return "It's not very effective..."
        elif mult == 0:
            return "It has no effect!"
        return ""

    def draw_hp_bar(self, surface, pokemon, x, y, width=200, height=20):
        # HP background
        pygame.draw.rect(surface, GRAY, (x, y, width, height))
        
        # Calculate HP percentage
        hp_percentage = pokemon.hp / pokemon.max_hp
        hp_width = int(width * hp_percentage)
        
        # HP color based on remaining health
        if hp_percentage > 0.5:
            color = GREEN
        elif hp_percentage > 0.2:
            color = YELLOW
        else:
            color = RED
            
        # Draw the filled HP bar
        pygame.draw.rect(surface, color, (x, y, hp_width, height))
        
        # Draw the border
        pygame.draw.rect(surface, BLACK, (x, y, width, height), 2)
        
        # Draw HP text
        hp_text, hp_rect = main_font.render(f"HP: {pokemon.hp}/{pokemon.max_hp}", BLACK)
        hp_rect.midtop = (x + width // 2, y + height + 5)
        surface.blit(hp_text, hp_rect)

    def draw_pokemon_info(self, surface, pokemon, x, y, is_player=True):
        # Draw name and type
        name_color = WHITE if is_player else type_colors.get(pokemon.type, WHITE)
        name_text, name_rect = battle_font.render(pokemon.name, name_color)
        name_rect.topleft = (x, y)
        surface.blit(name_text, name_rect)
        
        # Draw type indicator
        type_color = type_colors.get(pokemon.type, (200, 200, 200))
        type_rect = pygame.Rect(x, y + 40, 100, 30)
        pygame.draw.rect(surface, type_color, type_rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, type_rect, width=2, border_radius=5)
        
        type_text, type_rect = main_font.render(pokemon.type, BLACK)
        type_rect.center = type_rect.center
        surface.blit(type_text, type_rect)
        
        # Draw HP bar
        self.draw_hp_bar(surface, pokemon, x, y + 80)

    def draw(self, surface):
        # Draw background
        surface.blit(self.background, (0, 0))
        
        # Draw Pokemon
        # For player Pokemon
        player_pos = self.player.position
        computer_pos = self.computer.position
        
        # Draw legendary aura if applicable
        if isinstance(self.player, LegendaryPokemon):
            aura_pos = (player_pos[0] - 25, player_pos[1] - 25)  # Offset for aura
            surface.blit(self.player.legendary_aura, aura_pos)
            
        if isinstance(self.computer, LegendaryPokemon):
            aura_pos = (computer_pos[0] - 25, computer_pos[1] - 25)
            surface.blit(self.computer.legendary_aura, aura_pos)
        
        # Draw Pokemon with flash effect if being hit
        if self.player.is_flashing and self.player.flash_timer % 2 == 0:
            # Flash effect by not drawing the Pokemon every other frame
            pass
        else:
            surface.blit(self.player.back_image, player_pos)
            
        if self.computer.is_flashing and self.computer.flash_timer % 2 == 0:
            pass
        else:
            surface.blit(self.computer.front_image, computer_pos)
        
        # Draw Pokemon info
        self.draw_pokemon_info(surface, self.player, 50, 50, True)
        self.draw_pokemon_info(surface, self.computer, SCREEN_WIDTH - 250, 50, False)
        
        # Draw message box
        pygame.draw.rect(surface, WHITE, self.message_box, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.message_box, width=2, border_radius=10)
        
        message_text, message_rect = battle_font.render(self.message, BLACK)
        message_rect.center = self.message_box.center
        surface.blit(message_text, message_rect)
        
        # Draw move buttons if it's player's turn and choosing a move
        if self.current_turn == "player" and self.battle_state == "choosing_move":
            for button in self.move_buttons:
                button.draw(surface)

    def handle_click(self, pos):
        if self.battle_state != "choosing_move" or self.current_turn != "player":
            return
            
        for i, button in enumerate(self.move_buttons):
            if button.is_clicked(pos, True):
                if select_sound:
                    select_sound.play()
                self.player_choose_move(i)
                return

    def handle_mouse_motion(self, pos):
        for button in self.move_buttons:
            button.check_hover(pos)

    def player_choose_move(self, move_index):
        self.player_move_index = move_index
        move = self.player.moves[move_index]
        
        # Play move sound
        if move.sound:
            move.sound.play()
        
        # Update message
        self.message = f"{self.player.name} used {move.name}!"
        
        # Set battle state to animating
        self.battle_state = "animating"
        self.animation_timer = 0
        
        # Player's attack animation
        self.player.animate_attack()
        
        # After animation completes, deal damage
        pygame.time.set_timer(pygame.USEREVENT, 500)  # 500ms delay

    def computer_choose_move(self):
        self.computer_move_index = random.randint(0, len(self.computer.moves) - 1)
        move = self.computer.moves[self.computer_move_index]
        
        # Play move sound
        if move.sound:
            move.sound.play()
        
        # Update message
        self.message = f"{self.computer.name} used {move.name}!"
        
        # Set battle state to animating
        self.battle_state = "animating"
        self.animation_timer = 0
        
        # Computer's attack animation
        self.computer.animate_attack()
        
        # After animation completes, deal damage
        pygame.time.set_timer(pygame.USEREVENT, 500)

    def apply_player_move_damage(self):
        move = self.player.moves[self.player_move_index]
        damage, multiplier = move.calculate_damage(self.player, self.computer)
        
        # Apply damage
        self.computer.take_damage(damage)
        
        # Update message with effectiveness
        effectiveness = self.effectiveness_text(multiplier)
        if effectiveness:
            self.message = effectiveness
        else:
            self.message = f"{self.computer.name} took {damage} damage!"
        
        # Check if computer fainted
        if self.computer.is_fainted():
            self.battle_state = "game_over"
            self.winner = "player"
            self.message = f"{self.computer.name} fainted! You win!"
            if victory_sound:
                victory_sound.play()
        else:
            # Switch to computer's turn after a delay
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)

    def apply_computer_move_damage(self):
        move = self.computer.moves[self.computer_move_index]
        damage, multiplier = move.calculate_damage(self.computer, self.player)
        
        # Apply damage
        self.player.take_damage(damage)
        
        # Update message with effectiveness
        effectiveness = self.effectiveness_text(multiplier)
        if effectiveness:
            self.message = effectiveness
        else:
            self.message = f"{self.player.name} took {damage} damage!"
        
        # Check if player fainted
        if self.player.is_fainted():
            self.battle_state = "game_over"
            self.winner = "computer"
            self.message = f"{self.player.name} fainted! Computer wins!"
            if defeat_sound:
                defeat_sound.play()
        else:
            # Return to player's turn after a delay
            pygame.time.set_timer(pygame.USEREVENT + 2, 1500)

    def update(self):
        # Update Pokemon animations
        self.player.update_animation()
        self.computer.update_animation()

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            # Player attack animation complete, apply damage
            move = self.player.moves[self.player_move_index]
            damage, multiplier = move.calculate_damage(self.player, self.computer)
            self.computer.take_damage(damage)
            
            # Update message
            eff_text = self.effectiveness_text(multiplier)
            if eff_text:
                self.message = eff_text
            else:
                self.message = f"{self.computer.name} took {damage} damage!"
                
            # Check for win
            if self.computer.is_fainted():
                self.battle_state = "game_over"
                self.winner = "player"
                self.message = f"{self.computer.name} fainted! You win!"
                if victory_sound:
                    victory_sound.play()
            else:
                # Switch to computer's turn after delay
                pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
                
        elif event.type == pygame.USEREVENT + 1:
            # Time for computer's turn
            self.current_turn = "computer"
            # Reset the timer
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            # Choose a random move
            self.computer_move_index = random.randint(0, len(self.computer.moves) - 1)
            move = self.computer.moves[self.computer_move_index]
            self.message = f"{self.computer.name} used {move.name}!"
            if move.sound:
                move.sound.play()
            self.computer.animate_attack()
            pygame.time.set_timer(pygame.USEREVENT + 3, 500)
            
        elif event.type == pygame.USEREVENT + 3:
            # Computer attack animation complete, apply damage
            move = self.computer.moves[self.computer_move_index]
            damage, multiplier = move.calculate_damage(self.computer, self.player)
            self.player.take_damage(damage)
            
            # Update message
            eff_text = self.effectiveness_text(multiplier)
            if eff_text:
                self.message = eff_text
            else:
                self.message = f"{self.player.name} took {damage} damage!"
                
            # Check for defeat
            if self.player.is_fainted():
                self.battle_state = "game_over"
                self.winner = "computer"
                self.message = f"{self.player.name} fainted! Computer wins!"
                if defeat_sound:
                    defeat_sound.play()
            else:
                # Back to player's turn after delay
                pygame.time.set_timer(pygame.USEREVENT + 2, 1500)
                
        elif event.type == pygame.USEREVENT + 2:
            # Back to player's turn
            self.current_turn = "player"
            self.battle_state = "choosing_move"
            self.message = "Choose a move!"
            # Reset the timer
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)

# Move shortcut
def move(name, power, type_):
    return Move(name, power, type_)
# Define Pokémon pool
def create_pokemon_pool():
    return [
        Pokemon("Charizard", "Fire", 100, 30, 20, [move("Flamethrower", 40, "Fire"), move("Fire Spin", 35, "Fire")]),
        Pokemon("Blastoise", "Water", 100, 28, 22, [move("Water Gun", 35, "Water"), move("Hydro Pump", 50, "Water")]),
        Pokemon("Venusaur", "Grass", 100, 29, 21, [move("Razor Leaf", 36, "Grass"), move("Solar Beam", 50, "Grass")]),
        Pokemon("Onix", "Rock", 110, 25, 30, [move("Rock Slide", 45, "Rock"), move("Stone Edge", 55, "Rock")]),
        Pokemon("Pikachu", "Electric", 90, 35, 18, [move("Thunderbolt", 50, "Electric"), move("Thunder Shock", 30, "Electric")]),
        Pokemon("Golem", "Rock", 105, 28, 28, [move("Rock Throw", 40, "Rock"), move("Earthquake", 50, "Ground")]),
        Pokemon("Raichu", "Electric", 98, 34, 21, [move("Spark", 37, "Electric"), move("Volt Tackle", 45, "Electric")]),
        Pokemon("Magmar", "Fire", 98, 29, 19, [move("Fire Punch", 36, "Fire"), move("Lava Plume", 40, "Fire")]),
        Pokemon("Mewtwo", "Psychic", 120, 40, 25, [move("Psychic", 45, "Psychic"), move("Shadow Ball", 50, "Ghost")]),
        Pokemon("Machamp", "Fighting", 110, 35, 30, [move("Dynamic Punch", 50, "Fighting"), move("Close Combat", 45, "Fighting")]),
        Pokemon("Gengar", "Ghost", 90, 36, 18, [move("Shadow Ball", 45, "Ghost"), move("Lick", 30, "Ghost")]),
        Pokemon("Alakazam", "Psychic", 85, 37, 22, [move("Confusion", 40, "Psychic"), move("Shadow Ball", 50, "Ghost")]),
        Pokemon("Tyranitar", "Rock", 115, 30, 35, [move("Crunch", 45, "Dark"), move("Stone Edge", 50, "Rock")]),
        Pokemon("Dragonite", "Dragon", 120, 38, 28, [move("Dragon Claw", 45, "Dragon"), move("Hyper Beam", 50, "Normal")]),
        LegendaryPokemon("Lugia", "Psychic", 130, 34, 40, [move("Aeroblast", 50, "Flying"), move("Psychic", 45, "Psychic")]),
        LegendaryPokemon("Zapdos", "Electric", 130, 40, 30, [move("Thunderbolt", 50, "Electric"), move("Thunder", 60, "Electric")]),
        LegendaryPokemon("Mew", "Psychic", 130, 40, 40, [move("Psychic", 50, "Psychic"), move("Transform", 0, "Normal")]),
        LegendaryPokemon("Articuno", "Ice", 120, 35, 30, [move("Ice Beam", 50, "Ice"), move("Blizzard", 60, "Ice")]),
        LegendaryPokemon("Moltres", "Fire", 130, 40, 30, [move("Flamethrower", 50, "Fire"), move("Fire Blast", 60, "Fire")]),
        LegendaryPokemon("Regice", "Ice", 140, 30, 35, [move("Ice Beam", 50, "Ice"), move("Freeze-Dry", 60, "Ice")]),
        LegendaryPokemon("Registeel", "Steel", 140, 35, 40, [move("Iron Tail", 50, "Steel"), move("Flash Cannon", 60, "Steel")]),
        LegendaryPokemon("Groudon", "Ground", 150, 45, 45, [move("Earthquake", 55, "Ground"), move("Fissure", 70, "Ground")]),
        LegendaryPokemon("Kyogre", "Water", 150, 45, 40, [move("Water Spout", 55, "Water"), move("Hydro Pump", 70, "Water")]),
        LegendaryPokemon("Rayquaza", "Dragon", 160, 50, 45, [move("Dragon Claw", 55, "Dragon"), move("Aerial Ace", 60, "Flying")]),
    ]

class PokemonSelection:
    def __init__(self):
        self.pokemon_pool = create_pokemon_pool()
        self.selected_index = 0
        self.page = 0
        self.items_per_page = 6
        self.selected_pokemon = None
        
        # Buttons
        button_width = 200
        button_height = 60
        
        self.next_button = Button(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 100, 
                             button_width, button_height, "Next Page", BLUE, LIGHT_BLUE)
        self.prev_button = Button(50, SCREEN_HEIGHT - 100, 
                             button_width, button_height, "Prev Page", BLUE, LIGHT_BLUE)
        self.select_button = Button(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT - 100, 
                              button_width, button_height, "Select", GREEN, (100, 255, 100))
                              
        # Load selection background
        self.background = load_image("selection_background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        if not self.background:
            # Create a basic background if image not found
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(LIGHT_BLUE)
            
        # Create pokemon buttons
        self.pokemon_buttons = []
        self.create_pokemon_buttons()
        
    def create_pokemon_buttons(self):
        self.pokemon_buttons = []
        
        # Calculate grid layout
        btn_width = 300
        btn_height = 120
        padding = 30
        cols = 3
        rows = 2
        
        start_x = (SCREEN_WIDTH - (cols * (btn_width + padding) - padding)) // 2
        start_y = 150
        
        # Create buttons for current page only
        start_idx = self.page * self.items_per_page
        end_idx = min((self.page + 1) * self.items_per_page, len(self.pokemon_pool))
        
        for i in range(start_idx, end_idx):
            pokemon = self.pokemon_pool[i]
            grid_pos = i - start_idx
            row = grid_pos // cols
            col = grid_pos % cols
            
            x = start_x + col * (btn_width + padding)
            y = start_y + row * (btn_height + padding)
            
            # Use type color for the button
            type_color = type_colors.get(pokemon.type, (200, 200, 200))
            hover_color = tuple(min(c + 40, 255) for c in type_color)
            
            # Create button with Pokemon name
            legendary_star = "⭐ " if isinstance(pokemon, LegendaryPokemon) else ""
            btn_text = f"{legendary_star}{pokemon.name} ({pokemon.type})"
            
            btn = Button(x, y, btn_width, btn_height, btn_text, type_color, hover_color)
            self.pokemon_buttons.append((btn, i))
    
    def draw(self, surface):
        # Draw background
        surface.blit(self.background, (0, 0))
        
        # Draw title
        title_text, title_rect = battle_font.render("Choose Your Pokemon!", YELLOW)
        title_rect.midtop = (SCREEN_WIDTH // 2, 50)
        surface.blit(title_text, title_rect)
        
        # Draw Pokemon buttons
        for btn, _ in self.pokemon_buttons:
            btn.draw(surface)
            
        # Draw navigation buttons
        if self.page > 0:
            self.prev_button.draw(surface)
            
        total_pages = (len(self.pokemon_pool) + self.items_per_page - 1) // self.items_per_page
        if self.page < total_pages - 1:
            self.next_button.draw(surface)
            
        # Draw select button
        self.select_button.draw(surface)
        
        # Draw page counter
        page_text, page_rect = main_font.render(f"Page {self.page + 1}/{total_pages}", BLACK)
        page_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130)
        surface.blit(page_text, page_rect)
        
        # Draw Pokemon preview if one is selected
        if self.selected_index is not None and 0 <= self.selected_index < len(self.pokemon_pool):
            pokemon = self.pokemon_pool[self.selected_index]
            
            # Draw Pokemon image
            preview_x = SCREEN_WIDTH // 2 - 100
            preview_y = SCREEN_HEIGHT // 2 - 100
            surface.blit(pokemon.front_image, (preview_x, preview_y))
            
            # Draw info box
            info_x = SCREEN_WIDTH // 2 + 150
            info_y = SCREEN_HEIGHT // 2 - 100
            
            # Draw name and stats
            name_text, name_rect = battle_font.render(pokemon.name, BLACK)
            name_rect.topleft = (info_x, info_y)
            surface.blit(name_text, name_rect)
            
            # Type indicator
            type_color = type_colors.get(pokemon.type, (200, 200, 200))
            type_rect = pygame.Rect(info_x, info_y + 40, 100, 30)
            pygame.draw.rect(surface, type_color, type_rect, border_radius=5)
            pygame.draw.rect(surface, BLACK, type_rect, width=2, border_radius=5)
            
            type_text, type_rect = main_font.render(pokemon.type, BLACK)
            type_rect.center = type_rect.center
            surface.blit(type_text, type_rect)
            
            # Stats
            stats_y = info_y + 80
            stats_text = [
                f"HP: {pokemon.max_hp}",
                f"Attack: {pokemon.attack}",
                f"Defense: {pokemon.defense}"
            ]
            
            for i, text in enumerate(stats_text):
                stat_text, stat_rect = main_font.render(text, BLACK)
                stat_rect.topleft = (info_x, stats_y + i * 30)
                surface.blit(stat_text, stat_rect)
            
            # Moves
            moves_y = stats_y + 120
            move_title, move_title_rect = main_font.render("Moves:", BLACK)
            move_title_rect.topleft = (info_x, moves_y)
            surface.blit(move_title, move_title_rect)
            
            for i, m in enumerate(pokemon.moves):
                move_text, move_rect = main_font.render(f"{m.name} ({m.type}, Power: {m.power})", BLACK)
                move_rect.topleft = (info_x + 20, moves_y + (i + 1) * 30)
                surface.blit(move_text, move_rect)
                
            # Legendary indicator if applicable
            if isinstance(pokemon, LegendaryPokemon):
                legendary_text, legendary_rect = battle_font.render("⭐ LEGENDARY", YELLOW)
                legendary_rect.midtop = (SCREEN_WIDTH // 2, info_y - 50)
                surface.blit(legendary_text, legendary_rect)
        
    def handle_click(self, pos):
        # Check Pokemon buttons
        for btn, idx in self.pokemon_buttons:
            if btn.is_clicked(pos, True):
                if select_sound:
                    select_sound.play()
                self.selected_index = idx
                return
                
        # Check navigation buttons
        if self.page > 0 and self.prev_button.is_clicked(pos, True):
            if select_sound:
                select_sound.play()
            self.page -= 1
            self.create_pokemon_buttons()
            return
            
        total_pages = (len(self.pokemon_pool) + self.items_per_page - 1) // self.items_per_page
        if self.page < total_pages - 1 and self.next_button.is_clicked(pos, True):
            if select_sound:
                select_sound.play()
            self.page += 1
            self.create_pokemon_buttons()
            return
            
        # Check select button
        if self.selected_index is not None and self.select_button.is_clicked(pos, True):
            if select_sound:
                select_sound.play()
            self.selected_pokemon = self.pokemon_pool[self.selected_index]
            return
            
    def handle_mouse_motion(self, pos):
        # Update button hover states
        for btn, _ in self.pokemon_buttons:
            btn.check_hover(pos)
            
        self.next_button.check_hover(pos)
        self.prev_button.check_hover(pos)
        self.select_button.check_hover(pos)

class Game:
    def __init__(self):
        self.state = "selection"  # "selection", "battle", "game_over"
        self.selection = PokemonSelection()
        self.battle = None
        self.clock = pygame.time.Clock()
        self.running = True
        
    def run(self):
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_click(event.pos)
                        
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
                    
                elif event.type >= pygame.USEREVENT:
                    if self.battle:
                        self.battle.handle_event(event)
                        
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Exit game or return to selection from battle
                        if self.state == "battle":
                            # Stop battle music
                            mixer.music.stop()
                            self.state = "selection"
                            # Reload selection music if available
                            try:
                                mixer.music.load(os.path.join(SOUND_DIR, "selection_music.mp3"))
                                mixer.music.play(-1)
                            except:
                                pass
                        else:
                            self.running = False
            
            # Update game state
            self.update()
            
            # Draw the current state
            screen.fill(BLACK)
            self.draw(screen)
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()
        
    def update(self):
        if self.state == "battle" and self.battle:
            self.battle.update()
            
            # Check if battle is over
            if self.battle.battle_state == "game_over":
                # Set a timer to return to selection screen
                pygame.time.set_timer(pygame.USEREVENT + 10, 3000)  # 3 seconds
        
    def draw(self, surface):
        if self.state == "selection":
            self.selection.draw(surface)
        elif self.state == "battle" and self.battle:
            self.battle.draw(surface)
            
    def handle_click(self, pos):
        if self.state == "selection":
            self.selection.handle_click(pos)
            
            # Check if a pokemon was selected
            if self.selection.selected_pokemon:
                # Create computer pokemon
                player_pokemon = self.selection.selected_pokemon
                
                # If player chose a legendary, computer gets a legendary too
                if isinstance(player_pokemon, LegendaryPokemon):
                    eligible_opponents = [p for p in self.selection.pokemon_pool 
                                       if isinstance(p, LegendaryPokemon) and p != player_pokemon]
                else:
                    eligible_opponents = [p for p in self.selection.pokemon_pool 
                                       if not isinstance(p, LegendaryPokemon) and p != player_pokemon]
                
                # Choose random opponent
                computer_pokemon = random.choice(eligible_opponents)
                
                # Create battle
                self.battle = Battle(player_pokemon, computer_pokemon)
                
                # Switch to battle state
                self.state = "battle"
                
                # Reset selection for next time
                self.selection.selected_pokemon = None
                
        elif self.state == "battle" and self.battle:
            self.battle.handle_click(pos)
            
    def handle_mouse_motion(self, pos):
        if self.state == "selection":
            self.selection.handle_mouse_motion(pos)
        elif self.state == "battle" and self.battle:
            self.battle.handle_mouse_motion(pos)
            
    def handle_event(self, event):
        if event.type == pygame.USEREVENT + 10:
            # Return to selection after battle finishes
            pygame.time.set_timer(pygame.USEREVENT + 10, 0)  # Cancel timer
            self.state = "selection"
            # Stop battle music
            mixer.music.stop()
            # Play selection music if available
            try:
                mixer.music.load(os.path.join(SOUND_DIR, "selection_music.mp3"))
                mixer.music.play(-1)
            except:
                pass

if __name__ == "__main__":
    # Set icon if available
    try:
        icon = pygame.image.load(os.path.join(IMAGE_DIR, "icon.png"))
        pygame.display.set_icon(icon)
    except:
        print("Icon not found!")
    
    # Create directories if they don't exist
    for directory in [IMAGE_DIR, SOUND_DIR, FONT_DIR]:
        os.makedirs(directory, exist_ok=True)
    
    # Start the game
    game = Game()
    game.run()