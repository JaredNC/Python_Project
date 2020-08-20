import random
import numpy as np
import type_compare as tc
import newciv_bot as nc
import sensitive_info as si
from io import StringIO  # Python 3
import sys
import pandas as pd

data = pd.read_csv(r'pokemon.csv')
df = pd.DataFrame(data, columns=['attack',
                                 'defense',
                                 'hp',
                                 'name',
                                 'sp_attack',
                                 'sp_defense',
                                 'speed',
                                 'is_legendary'])

creds = si.SecurityCreds()


class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        self.members, self.owner, self.user_id = self.grab_team(self.team_id)

    def __str__(self) -> str:
        if str(self.team_id).split("*")[0] == "Random":
            return f"Random Team owned by {self.owner}"
        elif str(self.team_id).split("*")[0] == "Gym":
            return f"Team owned by Gym Leader {self.owner}"
        else:
            return f"Team {self.team_id} owned by {self.owner}"

    def __len__(self):
        count = 0
        for x in self.members:
            count = count + 1 if x.hitpoints > 0 else count
        return count

    def grab_team(self, team_id):
        new = nc.NewcivLogin()
        team, name, user_id = new.get_team(team_id)
        pokemon = []
        for x in team:
            dump = x.split(',')
            pokemon.append(Pokemon(dump[0], dump[1], int(dump[2]), int(dump[3]), int(dump[4]), dump[5]))
        return pokemon, name, user_id

    def first_pokemon(self):
        return next((x for x in self.members if x.hitpoints > 0), None)

    def team_pics(self):
        string = []
        for x in self.members:
            string.append(f"[url=\"https://forums.novociv.org/pokemon.php?section=pokemon&do=view&pokemon={x.monid}\"]"
                          f"[img]https://forums.novociv.org/pokemon/images/img/{x.monid}.png[/img][/url]")
        return ''.join(string)

    def team_members(self):
        string = []
        for pokemon in self.members:
            string.append(print(pokemon))
        return string

    def analyze(self):
        lvl = 0
        min_lvl = 0
        count = 0
        for pokemon in self.members:
            if pokemon.legendary == 1:
                min_lvl = max(min_lvl, pokemon.level * 1.6)
                lvl += pokemon.level * 1.5
            else:
                min_lvl = max(min_lvl, pokemon.level*1.2)
                lvl += pokemon.level*0.75
            count += 1
        return round((min_lvl + lvl/count)*.50)


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
        self.legendary = df['is_legendary'].values[int(self.monid) - 1]
        self.hitpoints = self.calc_hitpoints(self.level)
        self.strength = self.calc_strength(self.level)
        self.defense = self.calc_defense(self.level, self.friend)
        self.sp_attack = self.calc_sp_attack(self.level)
        self.sp_defense = self.calc_sp_defense(self.level, self.friend)

    def __str__(self) -> str:
        return f"{self.name}: Level {self.level}, Type {self.type}, Hitpoints: {self.hitpoints}"

    def calc_hitpoints(self, level):
        base = df['hp'].values[int(self.monid) - 1]
        hitpoints = int(base) * (1+level/50) + (np.floor(level/10)+1)*2
        return np.floor(hitpoints)

    def calc_strength(self, level):
        base = df['attack'].values[int(self.monid)-1]
        strength = int(base) * (1+level/50)
        return np.floor(strength)

    def calc_defense(self, level, friend):
        base = df['defense'].values[int(self.monid) - 1]
        defense = int(base) * (1 + level / 50)
        return np.floor(defense/2) + np.floor((defense/4) * min((friend/400), 1))

    def calc_sp_attack(self, level):
        base = df['sp_attack'].values[int(self.monid)-1]
        strength = int(base) * (1+level/50)
        return np.floor(strength)

    def calc_sp_defense(self, level, friend):
        base = df['sp_defense'].values[int(self.monid) - 1]
        defense = int(base) * (1 + level / 50)
        return np.floor(defense/2) + np.floor((defense/4) * min((friend/400), 1))

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
        atk = attacker.strength - defender.defense
        sp_atk = attacker.sp_attack - defender.sp_defense
        if atk > sp_atk:
            form = 'SP_'
            attack = max(atk * multiply, np.floor(attacker.strength * 0.25 * multiply))
        else:
            form = ''
            attack = max(sp_atk * multiply, np.floor(attacker.sp_attack * 0.25 * multiply))

        if random.random() < 0.05:
            critical_str = "[color=orange][b]Critical Hit![/b][/color] "
            attack = np.floor(attack*1.5)
        else:
            critical_str = ""

        print(f"{critical_str}{attacker.name} attacks for {attack}! ({form}ATK: {attacker.strength} TC: {multiply} {form}DEF: {defender.defense})")
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
        if team_id1 == team_id2:
            self.team_1 = 0

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