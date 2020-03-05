import random
import numpy as np
import type_compare as tc
import newciv_bot as nc
import sensitive_info as si
from datetime import datetime
import time

creds = si.SecurityCreds()


class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        self.members = self.grab_team(self.team_id)

    def __str__(self) -> str:
        return f"Team {self.team_id}"

    def grab_team(self, team_id):
        new = nc.NewcivLogin()
        team = new.get_team(team_id)
        pokemon = []
        for x in team:
            dump = x.split(',')
            pokemon.append(Pokemon(dump[0], dump[1], int(dump[2]), int(dump[3]), int(dump[4]), dump[5]))
        return pokemon


class Pokemon:
    last_id = 0

    def __init__(self, monid, name, level, friend, indv_item_id, type):
        Pokemon.last_id += 1
        self.indv_id = Pokemon.last_id
        self.monid = monid
        self.name = name
        self.level = level
        self.friend = friend
        self.indv_item_id = indv_item_id
        self.type = type
        self.hitpoints = self.calc_hitpoints(self.level)
        self.strength = self.calc_strength(self.level)
        self.defense = self.calc_defense(self.level, self.friend)

    def __str__(self) -> str:
        return f"{self.name}: Level {self.level}, Pokemon #{self.monid}, Type {self.type}, Hitpoints: {self.hitpoints}"

    def calc_hitpoints(self, level):
        hitpoints = (level*2) + (np.floor(level/10)+1)*2
        return hitpoints

    def calc_strength(self, level):
        strength = level
        return strength

    def calc_defense(self, level, friend):
        defense = np.floor((level/2) * min((friend/400), 1))
        return defense

    def remove_hitpoints(self, damage):
        self.hitpoints = max(0, self.hitpoints - damage)
        return self.hitpoints


class Fight:
    last_id = 0

    def __init__(self, pokemon_1, pokemon_2):
        Fight.last_id += 1
        self.fight_id = Fight.last_id
        self.pokemon_1 = pokemon_1
        self.pokemon_2 = pokemon_2

    def attack(self, turn):
        attacker = self.pokemon_1 if turn == 1 else self.pokemon_2
        defender = self.pokemon_2 if turn == 1 else self.pokemon_1
        multiply = tc.compare(attacker.type, defender.type)
        attack = attacker.strength*multiply - defender.defense
        if random.random() < 0.05:
            critical_str = "Critical Hit! "
            attack = np.floor(attack*1.5)
        else:
            critical_str = ""

        print(f"{critical_str}{attacker.name} attacks for {attack}! (ATK: {attacker.strength} TC: {multiply} DEF: {defender.defense})")
        defender.remove_hitpoints(attack)
        remaining = defender.hitpoints
        print(f"{remaining} hitpoints remaining on {defender.name}!")
        if remaining > 0:
            return True
        else:
            print(f"{defender.name} fainted!")
            return False

    def fight(self):
        turn = 0
        alive = True
        while alive:
            turn += 1
            alive = self.attack(turn % 2)


team1 = Team(2)
print(team1)

for pokemon in team1.members:
    print(pokemon)

# team2 = Team(200)
# team3 = Team(2000)

# a = Pokemon(1, "Bulbasaur", 30, 41, 0, "Grass")
# b = Pokemon(7, "Squirtle", 50, 400, 0, "Water")
#
# print(a)
# print(b)
#
# fight = Fight(a, b)
# fight.fight()
#
# print(a)
# print(b)



