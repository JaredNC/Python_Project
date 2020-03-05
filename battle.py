import random
import numpy as np
import type_compare as tc
import newciv_bot as nc
import sensitive_info as si
from io import StringIO  # Python 3
import sys

creds = si.SecurityCreds()


class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        self.members, self.owner = self.grab_team(self.team_id)

    def __str__(self) -> str:
        return f"Team {self.team_id} owned by {self.owner}"

    def __len__(self):
        count = 0
        for x in self.members:
            count = count + 1 if x.hitpoints > 0 else count
        return count

    def grab_team(self, team_id):
        new = nc.NewcivLogin()
        team, name = new.get_team(team_id)
        pokemon = []
        for x in team:
            dump = x.split(',')
            pokemon.append(Pokemon(dump[0], dump[1], int(dump[2]), int(dump[3]), int(dump[4]), dump[5]))
        return pokemon, name

    def first_pokemon(self):
        return next((x for x in self.members if x.hitpoints > 0), None)

    def team_pics(self):
        string = []
        for x in self.members:
            string.append(f"[img]https://forums.novociv.org/pokemon/images/img/{x.monid}.png[/img]")
        return ''.join(string)

    def team_members(self):
        string = []
        for pokemon in self.members:
            string.append(print(pokemon))
        return string


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
        return f"{self.name}: Level {self.level}, Type {self.type}, Hitpoints: {self.hitpoints}"

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
        attack = max(attacker.strength*multiply - defender.defense, 0)
        if random.random() < 0.05:
            critical_str = "[color=orange][b]Critical Hit![/b][/color] "
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
            print(f"[color=red][b]{defender.name} fainted![/b][/color]\n")
            return False

    def fight(self, turn=0):
        alive = True
        while alive:
            turn += 1
            alive = self.attack(turn % 2)
        return turn % 2


class Battle:
    def __init__(self, team_id1, team_id2):
        self.team_1 = Team(team_id1)
        self.team_2 = Team(team_id2)

    def __str__(self) -> str:
        return f"Battle between {self.team_1} and {self.team_2}!"

    def battle(self):
        turn = 0
        while len(self.team_1) > 0 and len(self.team_2) > 0:
            fight = Fight(self.team_1.first_pokemon(), self.team_2.first_pokemon())
            turn = fight.fight(turn)
        winner = self.team_1 if len(self.team_1) > 0 else self.team_2
        print(f"Winner: {winner}!")
        return winner


class BattleBB(Battle):
    def battle_bb(self):
        # Create the in-memory "file"
        temp_out = StringIO()

        # Replace default stdout (terminal) with our stream
        sys.stdout = temp_out

        # Start Post
        print(f"[size=5]{self}[/size]")
        print(f"[url=\"https://forums.novociv.org/pokemon.php?section=team&do=view&deck={self.team_1.team_id}\"]"
              f"{self.team_1}[/url]:"
              f"{self.team_1.team_pics()}"
              f"[spoiler]")
        self.team_1.team_members()
        print("[/spoiler]")
        print(f"[url=\"https://forums.novociv.org/pokemon.php?section=team&do=view&deck={self.team_2.team_id}\"]"
              f"{self.team_2}[/url]:"
              f"{self.team_2.team_pics()}"
              f"[spoiler]")
        self.team_2.team_members()
        print("[/spoiler]")

        print("[spoiler]")
        winner = self.battle()
        print("[/spoiler]")

        print(f"The winner is "
              f"[url=\"https://forums.novociv.org/pokemon.php?section=team&do=view&deck={winner.team_id}\"]"
              f"[color=green][b]{winner}[/b][/color][/url]!")
        winner.team_members()
        # the original output stream to the terminal.
        sys.stdout = sys.__stdout__

        return temp_out.getvalue(), winner


# try:
#     battle = BattleBB(200, 16)
#     test = battle.battle_bb()
# except:
#     test = False
#
# print("output below")
# print(test)
# print("output above")