import numpy as np
import time as time
from potionomics.model import Ingredient, Potion
from typing import List


def GeneratePotions(ingredients: List[Ingredient], max_ingredients: int, desired: np.array):
    A = np.array([i.spec() for i in ingredients], dtype=int).transpose()
    candidates = [x for x in prune(A, np.identity(
        len(ingredients), dtype=int), desired)]
    for v in generateVectors(candidates, A, max_ingredients, desired):
        yield Potion(dict([(ingredients[i], v[i]) for i in range(len(v)) if v[i] > 0]))


def generateVectors(candidates, A, r, desired):
    if isZeroes(desired):
        yield np.zeros(len(A[0]), dtype=int)
        # Implies that desired is not 0 and we have no more room
    elif r == 0 or testIsNegative(desired):
        return  # Return nothing as we have no solution in this branch
    else:  # Recursive case
        for i in range(0, len(candidates)):  # For each candidate
            # Reduce desire to the rest
            rest = np.subtract(desired, np.dot(A, candidates[i]))
            # Generate all vectors that sum to the rest
            for v in generateVectors(candidates[i:], A, r-1, rest):
                # Add the candidate to the vector
                yield np.add(v, candidates[i])


def prune(A, id, desired):
    for i in id:
        l = np.subtract(desired, np.dot(A, i))
        if testIsNegative(l):
            continue
        else:
            yield i


def testIsNegative(array):
    for x in array:
        if x < 0:
            return True
    return False


def isZeroes(array):
    for x in array:
        if x != 0:
            return False
    return True


def Performance():
    A = np.array([1, 2, 3, 4, 5], dtype=int)

    # for i in range(1, 1000000):
    #     testIsPositive(A)

    start = time.time()
    for i in range(1, 1000000):
        isZeroes(A)
    print("isZeroes ", time.time() - start)

    start = time.time()
    for i in range(1, 1000000):
        np.array_equal(np.zeros(len(A)), A)
    print("array_equal ", time.time() - start)
