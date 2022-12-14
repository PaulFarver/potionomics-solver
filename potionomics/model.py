import numpy as np


class Recipe:
    def __init__(self, name, type, A, B, C, D, E):
        self.name = name
        self.type = type
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E

    def __str__(self):
        return self.name + " " + self.type + " " + str(self.A) + "A " + str(self.B) + "B " + str(self.C) + "C " + str(self.D) + "D " + str(self.E) + "E"

    def Name(self):
        return self.name + " " + self.type

    def code(self):
        s = ""
        if self.A > 0:
            s += "A" + str(self.A)
        if self.B > 0:
            s += "B" + str(self.B)
        if self.C > 0:
            s += "C" + str(self.C)
        if self.D > 0:
            s += "D" + str(self.D)
        if self.E > 0:
            s += "E" + str(self.E)
        return s + " " + self.name + " " + self.type

    def recipe(self):
        return np.array([self.A, self.B, self.C, self.D, self.E], dtype=int)


class Ingredient:
    def __init__(self, name, base_price, A, B, C, D, E, traits):
        self.name = name
        self.base_price = base_price
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E
        self.traits = traits

    def spec(self):
        return np.array([self.A, self.B, self.C, self.D, self.E], dtype=int)

    def __str__(self):
        return self.name

class Potion:
    def __init__(self, ingredients: dict):
        self.ingredients = ingredients

    def cost(self):
        c = 0
        for i, v in self.ingredients.items():
            c += i.base_price * v
        return c

    def traits(self):
        t = set()
        for i, v in self.ingredients.items():
            for trait in i.traits:
                
                if trait.__contains__("positive"):
                    t.add(trait.replace("positive", "").replace(" ", "").replace("Trait", ""))
        return t

    def note(self):
        s = str(self.cost()) + "g " 
        s += str(np.sum([i.spec() * v for i, v in self.ingredients.items()])) + " "
        for t in self.traits():
            s += f"{t} "
        for i, v in self.ingredients.items():
            s += f"[{str(v)}x {i.name}] "
        return s

    def __str__(self):
        # return str(self.ingredients)
        # Print gold in color
        s = "\033[33m" + str(self.cost()) + "g\033[0m " 
        s += str(np.sum([i.spec() * v for i, v in self.ingredients.items()])) + " "
        for t in self.traits():
            s += f"{t} "
        for i, v in self.ingredients.items():
            # Print ingredients in grey
            s += "\033[90m["  + str(v) + "x " + i.name + "]\033[0m "
            # s += str(v) + "x " + str(i) + ", "
        return s