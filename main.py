from __future__ import print_function, unicode_literals
# from collections.abc import Mapping
from PyInquirer import prompt, print_json
import numpy as np
import csv as csv
import time as time
from typing import List, Set

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

questions = [
    {
        'name': 'recipe',
        'type': 'list',
        'message': 'What recipe would you like to make?',
        'choices': [{'name': r.Name(), 'value': r, } for r in recipes],
    },
    {
        'type': 'input',
        'name': 'max_ingredients',
        'message': 'What\'s the max number of ingredients?',
        'default': '7',
        'validate': lambda val: int(val) > 0 or 'Must be greater than 0',
        'filter': lambda val: int(val),
    },
    {
        'type': 'checkbox',
        'message': 'Select values to optimize for',
        'name': 'optimize_values',
        'choices': [{'name': str(v), 'value': v} for v in special_values if v % np.sum(recipes[0].recipe()) == 0],
    }
]

answers = prompt(questions)

inventor = Inventor(answers['optimize_values'], answers['max_ingredients'])
for p in inventor.Invent(answers['recipe'], range(0, 10000), ingredients):
    print(p)
