import random

class Pokemon:
    def __init__(self, name, type, hp, attack, defense, moves):
        self.name = name
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.moves = moves

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

# Type effectiveness chart
type_chart = {
    "Fire": {"Water": 0.5, "Grass": 2.0, "Rock": 0.5, "Electric": 1.0, "Fire": 1.0},
    "Water": {"Fire": 2.0, "Grass": 0.5, "Rock": 2.0, "Electric": 0.5, "Water": 1.0},
    "Grass": {"Fire": 0.5, "Water": 2.0, "Rock": 2.0, "Electric": 1.0, "Grass": 1.0},
    "Rock": {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Electric": 1.0, "Rock": 1.0},
    "Electric": {"Water": 2.0, "Rock": 0.5, "Grass": 0.5, "Fire": 1.0, "Electric": 1.0},
}

class Move:
    def __init__(self, name, power, type):
        self.name = name
        self.power = power
        self.type = type

    def calculate_damage(self, attacker, defender):
        base_damage = (self.power * (attacker.attack / defender.defense))
        type_multiplier = type_chart.get(self.type, {}).get(defender.type, 1.0)
        return int(base_damage * type_multiplier)

class Battle:
    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

    def turn(self, attacker, defender, move):
        damage = move.calculate_damage(attacker, defender)
        defender.take_damage(damage)
        effectiveness = type_chart.get(move.type, {}).get(defender.type, 1.0)
        
        effectiveness_text = ""
        if effectiveness > 1:
            effectiveness_text = "It's super effective!"
        elif effectiveness < 1:
            effectiveness_text = "It's not very effective..."
        
        print(f"{attacker.name} used {move.name}! {effectiveness_text} {defender.name} took {damage} damage. (HP: {defender.hp})")

    def start(self):
        while self.pokemon1.hp > 0 and self.pokemon2.hp > 0:
            move1 = random.choice(self.pokemon1.moves)
            self.turn(self.pokemon1, self.pokemon2, move1)
            if self.pokemon2.hp == 0:
                print(f"{self.pokemon2.name} fainted! {self.pokemon1.name} wins!")
                break
            
            move2 = random.choice(self.pokemon2.moves)
            self.turn(self.pokemon2, self.pokemon1, move2)
            if self.pokemon1.hp == 0:
                print(f"{self.pokemon1.name} fainted! {self.pokemon2.name} wins!")
                break

pokemon_list = [
    # Fire-type Pokémon
    Pokemon("Charizard", "Fire", 100, 30, 20, [Move("Flamethrower", 40, "Fire"), Move("Fire Spin", 35, "Fire")]),
    Pokemon("Arcanine", "Fire", 105, 32, 22, [Move("Fire Fang", 38, "Fire"), Move("Heat Wave", 42, "Fire")]),
    Pokemon("Magmar", "Fire", 98, 29, 19, [Move("Fire Punch", 36, "Fire"), Move("Lava Plume", 40, "Fire")]),
    Pokemon("Flareon", "Fire", 95, 31, 21, [Move("Ember", 34, "Fire"), Move("Flame Burst", 37, "Fire")]),
    
    # Water-type Pokémon
    Pokemon("Blastoise", "Water", 100, 28, 22, [Move("Water Gun", 35, "Water"), Move("Hydro Pump", 50, "Water")]),
    Pokemon("Vaporeon", "Water", 110, 27, 24, [Move("Aqua Tail", 39, "Water"), Move("Surf", 45, "Water")]),
    Pokemon("Gyarados", "Water", 102, 31, 23, [Move("Waterfall", 42, "Water"), Move("Rain Dance", 38, "Water")]),
    Pokemon("Kingdra", "Water", 105, 30, 25, [Move("Bubble Beam", 37, "Water"), Move("Dragon Pulse", 44, "Water")]),
    
    # Grass-type Pokémon
    Pokemon("Venusaur", "Grass", 100, 29, 21, [Move("Razor Leaf", 36, "Grass"), Move("Solar Beam", 50, "Grass")]),
    Pokemon("Tangela", "Grass", 95, 28, 22, [Move("Vine Whip", 34, "Grass"), Move("Giga Drain", 40, "Grass")]),
    Pokemon("Torterra", "Grass", 110, 30, 23, [Move("Leaf Storm", 42, "Grass"), Move("Wood Hammer", 46, "Grass")]),
    Pokemon("Ludicolo", "Grass", 102, 27, 24, [Move("Energy Ball", 38, "Grass"), Move("Leech Seed", 35, "Grass")]),
    
    # Rock-type Pokémon
    Pokemon("Onix", "Rock", 110, 25, 30, [Move("Rock Slide", 45, "Rock"), Move("Stone Edge", 55, "Rock")]),
    Pokemon("Golem", "Rock", 105, 28, 28, [Move("Rock Throw", 40, "Rock"), Move("Earthquake", 50, "Rock")]),
    Pokemon("Tyranitar", "Rock", 115, 35, 32, [Move("Rock Smash", 44, "Rock"), Move("Crunch", 46, "Rock")]),
    Pokemon("Kabutops", "Rock", 100, 29, 27, [Move("Ancient Power", 38, "Rock"), Move("Aqua Jet", 35, "Rock")]),
    
    # Electric-type Pokémon
    Pokemon("Pikachu", "Electric", 90, 35, 18, [Move("Thunderbolt", 50, "Electric"), Move("Thunder Shock", 30, "Electric")]),
    Pokemon("Jolteon", "Electric", 95, 33, 20, [Move("Discharge", 40, "Electric"), Move("Thunder Fang", 38, "Electric")]),
    Pokemon("Electivire", "Electric", 100, 36, 22, [Move("Wild Charge", 42, "Electric"), Move("Thunder Punch", 39, "Electric")]),
    Pokemon("Raichu", "Electric", 98, 34, 21, [Move("Spark", 37, "Electric"), Move("Volt Tackle", 45, "Electric")])
]


# Player selects Pokémon
print("Choose your Pokémon:")
for i, pokemon in enumerate(pokemon_list):
    print(f"{i + 1}. {pokemon.name} ({pokemon.type})")

player_choice = int(input("Enter the number of your Pokémon: ")) - 1
player_pokemon = pokemon_list[player_choice]
computer_pokemon = random.choice(pokemon_list)
print(f"You chose {player_pokemon.name}! The computer chose {computer_pokemon.name}!")

battle = Battle(player_pokemon, computer_pokemon)
battle.start()
