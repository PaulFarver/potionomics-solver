import numpy as np
from potionomics.model import Recipe, Ingredient, Potion
from potionomics.solver import GeneratePotions
from typing import List


class Inventor:
    def __init__(self, special_values, max_ingredients):
        self.special_values = special_values
        self.max_ingredients = max_ingredients

    def Invent(self, recipe: Recipe, values: range, ingredients: List[Ingredient]) -> List[Potion]:
        optimals = optimalValues(recipe, self.special_values, values)
        for o in optimals:
            for p in GeneratePotions(ingredients, self.max_ingredients, o, True):
                yield p


def optimalValues(recipe: Recipe, special_values: List[int], values: range):
    s = np.sum(recipe.recipe())
    for v in pickFactor(special_values, s, values.start, values.stop):
        yield np.multiply(recipe.recipe(), v, dtype=int)


def pickFactor(special_values, ratio_sum, min_value, max_value):
    for v in special_values:
        if v % ratio_sum == 0 and v <= max_value and v >= min_value:
            yield int(v/ratio_sum)
