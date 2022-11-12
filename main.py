from __future__ import print_function, unicode_literals
# from collections.abc import Mapping
from PyInquirer import prompt, print_json
import numpy as np
import csv as csv
import time as time
from typing import List, Set
import sys

from potionomics.model import Recipe, Ingredient
from potionomics.potion_generator import Inventor


# Read csv and create arrays

name_array = []
ingredient_array = []
potion_array = []
special_values = []


included: Set[str] = set()
with open('filter.txt', 'r') as f:
    included = set(line.lower().strip() for line in f)


ingredients: List[Ingredient] = []
with open('potionomics.csv', 'r') as f:
    reader = csv.reader(f)
    for row in [r for r in reader if r[0].lower() in included]:
        ingredients.append(Ingredient(
            row[0].lower(),
            int(row[14]),
            int(row[4]),
            int(row[5]),
            int(row[6]),
            int(row[7]),
            int(row[8]),
            [t for t in row[9:14] if t != ""]
        ))


recipes: List[Recipe] = []
with open('potion_recipes.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        recipes.append(Recipe(row[0], row[1], int(row[2]), int(
            row[3]), int(row[4]), int(row[5]), int(row[6])))

special_values: List[int] = []
with open('special_amounts.txt', 'r') as f:
    for row in f:
        special_values.append(int(row))

default_recipe = recipes[0]
minimum = 100
maximum = 200
max_ingredients = 8
shown = 10
output = None

# Read flags from command line
for flag in sys.argv:
    switch = flag.split("=")
    if switch[0] == "--recipe":
        recipes = [r for r in recipes if r.name == switch[1]]
    if switch[0] == "--min":
        minimum = int(switch[1])
    if switch[0] == "--max":
        maximum = int(switch[1])
    if switch[0] == "--ingredients":
        max_ingredients = int(switch[1])
    if switch[0] == "--show":
        shown = int(switch[1])
    if switch[0] == "--out":
        output = switch[1]
        


questions = [
    {
        'name': 'recipe',
        'type': 'list',
        'message': 'What recipe would you like to make?',
        'choices': [{'name': r.Name(), 'value': r, } for r in recipes],
        'default': default_recipe
    },
    {
        'type': 'input',
        'name': 'max_ingredients',
        'message': 'What\'s the max number of ingredients?',
        'default': str(max_ingredients),
        'validate': lambda val: int(val) > 0 or 'Must be greater than 0',
        'filter': lambda val: int(val),
    },
    {
        'type': 'input',
        'name': 'minimum',
        'message': 'What\'s the minimum value?',
        'default': str(minimum),
        'validate': lambda val: int(val) > 0 or 'Must be greater than 0',
        'filter': lambda val: int(val),
    },
    {
        'type': 'input',
        'name': 'maximum',
        'message': 'What\'s the minimum value?',
        'default': str(maximum),
        'validate': lambda val: int(val) > 0 or 'Must be greater than 0',
        'filter': lambda val: int(val),
    }
]

answers = prompt(questions)

# inventor = Inventor(answers['optimize_values'], answers['max_ingredients'])
inventor = Inventor(answers['max_ingredients'])

# List of the 10 ceapest potions
cheapest_potions = []
cheapest_potion = None

UP = "\x1B[10A"
CLR = "\x1B[0K"
print("Inventing potions...")

inventions = inventor.Invent(answers['recipe'], range(answers['minimum'], answers['maximum']), ingredients)

if output is not None:
    with open(output, 'w') as f:
        for potion in inventions:
            f.write(potion.note() + "\n")
    exit()

for p in inventor.Invent(answers['recipe'], range(answers['minimum'], answers['maximum']), ingredients):
    if len(cheapest_potions) >= shown and p.cost() > cheapest_potions[-1].cost():
        continue
    else:
        if len(cheapest_potions) < shown:
            cheapest_potions.append(p)
        else:
            cheapest_potions[-1] = p
        cheapest_potions.sort(key=lambda x: x.cost())
        for i in range(0, len(cheapest_potions)):
            print(f"{CLR}{i}. {cheapest_potions[i]}")
        up = f"\x1B[{len(cheapest_potions)+1}A"
        print(f"{up}")

for cp in cheapest_potions:
    print()

# for p in cheapest_potions:
#     print(p)
