import numpy as np
from potionomics.model import Recipe, Ingredient, Potion
from potionomics.solver import GeneratePotions
from typing import List


class Inventor:
    def __init__(self, max_ingredients):
        self.max_ingredients = max_ingredients

    def Invent(self, recipe: Recipe, values: range, ingredients: List[Ingredient]) -> List[Potion]:
        optimals = optimalValues2(recipe, values)
        for o in optimals:
            for p in GeneratePotions(ingredients, self.max_ingredients, o):
                yield p

def optimalValues2(recipe: Recipe, values: range):
    s = np.sum(recipe.recipe())
    for v in pickFactor2(s, values):
        yield np.multiply(recipe.recipe(), v, dtype=int)

def pickFactor2(ratio_sum, r):
    for v in r:
        if v % ratio_sum == 0:
            yield int(v/ratio_sum)

def optimalValues(recipe: Recipe, special_values: List[int], values: range):
    s = np.sum(recipe.recipe())
    for v in pickFactor(special_values, s, values.start, values.stop):
        yield np.multiply(recipe.recipe(), v, dtype=int)


def pickFactor(special_values, ratio_sum, min_value, max_value):
    for v in special_values:
        if v % ratio_sum == 0 and v <= max_value and v >= min_value:
            yield int(v/ratio_sum)
