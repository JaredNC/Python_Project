"""
I grabbed this from https://code.sololearn.com/cDJV706Ec466/#py and modified it. --Jared
"""


class Type:
    def __init__(self, own_type, enemy_type):
        self.own_type = own_type
        self.enemy_type = enemy_type
        self.null = {"Normal": 1, "Fighting": 1, "Flying": 1, "Poison": 1, "Ground": 1, "Rock": 1, "Bug": 1, "Ghost": 1, "Steel": 1,
                "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Psychic": 1, "Ice": 1, "Dragon": 1, "Dark": 1, "Fairy": 1}
        self.normal = {"Normal": 1, "Fighting": 2, "Flying": 1, "Poison": 1, "Ground": 1, "Rock": 1, "Bug": 1, "Ghost": 0,
                  "Steel": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Psychic": 1, "Ice": 1, "Dragon": 1, "Dark": 1,
                  "Fairy": 1}
        self.fighting = {"Normal": 1, "Fighting": 1, "Flying": 2, "Poison": 1, "Ground": 1, "Rock": 0.5, "Bug": 0.5, "Ghost": 1,
                    "Steel": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Psychic": 2, "Ice": 1, "Dragon": 1,
                    "Dark": 0.5, "Fairy": 2}
        self.flying = {"Normal": 1, "Fighting": 0.5, "Flying": 1, "Poison": 1, "Ground": 0, "Rock": 2, "Bug": 0.5, "Ghost": 1,
                  "Steel": 1, "Fire": 1, "Water": 1, "Grass": 0.5, "Electric": 2, "Psychic": 1, "Ice": 2, "Dragon": 1,
                  "Dark": 1, "Fairy": 1}
        self.poison = {"Normal": 1, "Fighting": 0.5, "Flying": 1, "Poison": 0.5, "Ground": 2, "Rock": 1, "Bug": 0.5, "Ghost": 1,
                  "Steel": 1, "Fire": 1, "Water": 1, "Grass": 0.5, "Electric": 1, "Psychic": 2, "Ice": 1, "Dragon": 1,
                  "Dark": 1, "Fairy": 0.5}
        self.ground = {"Normal": 1, "Fighting": 1, "Flying": 1, "Poison": 0.5, "Ground": 1, "Rock": 0.5, "Bug": 1, "Ghost": 1,
                  "Steel": 1, "Fire": 1, "Water": 2, "Grass": 2, "Electric": 0, "Psychic": 1, "Ice": 2, "Dragon": 1, "Dark": 1,
                  "Fairy": 1}
        self.rock = {"Normal": 0.5, "Fighting": 2, "Flying": 0.5, "Poison": 0.5, "Ground": 2, "Rock": 1, "Bug": 1, "Ghost": 1,
                "Steel": 2, "Fire": 0.5, "Water": 2, "Grass": 0.5, "Electric": 1, "Psychic": 1, "Ice": 1, "Dragon": 1,
                "Dark": 1, "Fairy": 1}
        self.bug = {"Normal": 1, "Fighting": 0.5, "Flying": 2, "Poison": 1, "Ground": 0.5, "Rock": 2, "Bug": 1, "Ghost": 1,
               "Steel": 1, "Fire": 2, "Water": 1, "Grass": 0.5, "Electric": 1, "Psychic": 1, "Ice": 1, "Dragon": 1, "Dark": 1,
               "Fairy": 1}
        self.ghost = {"Normal": 0, "Fighting": 0, "Flying": 1, "Poison": 0.5, "Ground": 1, "Rock": 1, "Bug": 0.5, "Ghost": 2,
                 "Steel": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Psychic": 1, "Ice": 1, "Dragon": 1, "Dark": 2,
                 "Fairy": 1}
        self.steel = {"Normal": 0.5, "Fighting": 2, "Flying": 0.5, "Poison": 0, "Ground": 2, "Rock": 0.5, "Bug": 0.5, "Ghost": 1,
                 "Steel": 0.5, "Fire": 2, "Water": 1, "Grass": 0.5, "Electric": 1, "Psychic": 0.5, "Ice": 0.5, "Dragon": 0.5,
                 "Dark": 1, "Fairy": 0.5}
        self.fire = {"Normal": 1, "Fighting": 1, "Flying": 1, "Poison": 1, "Ground": 2, "Rock": 2, "Bug": 0.5, "Ghost": 1,
                "Steel": 0.5, "Fire": 0.5, "Water": 2, "Grass": 0.5, "Electric": 1, "Psychic": 1, "Ice": 0.5, "Dragon": 1,
                "Dark": 1, "Fairy": 0.5}
        self.water = {"Normal": 1, "Fighting": 1, "Flying": 1, "Poison": 1, "Ground": 1, "Rock": 1, "Bug": 1, "Ghost": 1,
                 "Steel": 0.5, "Fire": 0.5, "Water": 0.5, "Grass": 2, "Electric": 2, "Psychic": 1, "Ice": 0.5, "Dragon": 1,
                 "Dark": 1, "Fairy": 1}
        self.grass = {"Normal": 1, "Fighting": 1, "Flying": 2, "Poison": 2, "Ground": 0.5, "Rock": 1, "Bug": 2, "Ghost": 1,
                 "Steel": 1, "Fire": 2, "Water": 0.5, "Grass": 0.5, "Electric": 0.5, "Psychic": 1, "Ice": 2, "Dragon": 1,
                 "Dark": 1, "Fairy": 1}
        self.electric = {"Normal": 1, "Fighting": 1, "Flying": 0.5, "Poison": 1, "Ground": 2, "Rock": 1, "Bug": 1, "Ghost": 1,
                    "Steel": 0.5, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 0.5, "Psychic": 1, "Ice": 1, "Dragon": 1,
                    "Dark": 1, "Fairy": 1}
        self.psychic = {"Normal": 1, "Fighting": 0.5, "Flying": 1, "Poison": 1, "Ground": 1, "Rock": 1, "Bug": 2, "Ghost": 2,
                   "Steel": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Psychic": 0.5, "Ice": 1, "Dragon": 1,
                   "Dark": 2, "Fairy": 1}
        self.ice = {"Normal": 1, "Fighting": 2, "Flying": 1, "Poison": 1, "Ground": 1, "Rock": 2, "Bug": 1, "Ghost": 1, "Steel": 2,
               "Fire": 2, "Water": 1, "Grass": 1, "Electric": 1, "Psychic": 1, "Ice": 0.5, "Dragon": 1, "Dark": 1, "Fairy": 1}
        self.dragon = {"Normal": 1, "Fighting": 1, "Flying": 1, "Poison": 1, "Ground": 1, "Rock": 1, "Bug": 1, "Ghost": 1,
                  "Steel": 1, "Fire": 0.5, "Water": 0.5, "Grass": 0.5, "Electric": 0.5, "Psychic": 1, "Ice": 2, "Dragon": 2,
                  "Dark": 1, "Fairy": 2}
        self.dark = {"Normal": 1, "Fighting": 2, "Flying": 1, "Poison": 1, "Ground": 1, "Rock": 1, "Bug": 2, "Ghost": 0.5,
                "Steel": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Psychic": 0, "Ice": 1, "Dragon": 1, "Dark": 0.5,
                "Fairy": 2}
        self.fairy = {"Normal": 1, "Fighting": 0.5, "Flying": 1, "Poison": 2, "Ground": 1, "Rock": 1, "Bug": 0.5, "Ghost": 1,
                 "Steel": 2, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Psychic": 1, "Ice": 1, "Dragon": 0, "Dark": 0.5,
                 "Fairy": 1}
        self.result = self.type_effect()

    def type_effect(self):
        first = self.enemy_type
        if first == "Normal":
            first = self.normal
        elif first == "Fighting":
            first = self.fighting
        elif first == "Flying":
            first = self.flying
        elif first == "Poison":
            first = self.poison
        elif first == "Ground":
            first = self.ground
        elif first == "Rock":
            first = self.rock
        elif first == "Bug":
            first = self.bug
        elif first == "Ghost":
            first = self.ghost
        elif first == "Steel":
            first = self.steel
        elif first == "Fire":
            first = self.fire
        elif first == "Water":
            first = self.water
        elif first == "Grass":
            first = self.grass
        elif first == "Electric":
            first = self.electric
        elif first == "Psychic":
            first = self.psychic
        elif first == "Ice":
            first = self.ice
        elif first == "Dragon":
            first = self.dragon
        elif first == "Dark":
            first = self.dark
        elif first == "Fairy":
            first = self.fairy
        elif first == "Null":
            first = self.null
        else:
            raise Exception("Invalid Entry; type does not exist. Please try again.")

        # print(first)
        return first[self.own_type]


def compare(a, b):
    return Type(a, b).result

