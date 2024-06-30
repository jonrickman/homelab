from typing import List
from itertools import chain, product
import math


class Die:
    sides: int
    adv: str
    roll_count: int

    def __init__(self, sides: int, adv: str = '') -> None:
        self.sides = sides
        self.adv = adv
        self.roll_count = self.sides if not self.adv else math.pow(self.sides, 2)

    def __str__(self):
        return f"d{self.sides}, advantage:{self.adv}"


def parse_die_str(die_str: str) -> List[Die]:
    # defensive against empty string
    if not die_str:
        return

    # create a list to hold die
    dice: List[Die] = []

    # split the die terms  i.e.(1d4 2d6 1d20)
    terms = die_str.split(" ")
    for term in terms:
        (qty, sides) = term.split("d")

        # case: 1d4+
        if len(sides.split('+')) > 1:
            dice.append([Die(int(sides[:-1]), '+') for i in range(int(qty))])
            continue

        # case: 1d20-
        if len(sides.split('-')) > 1:
            dice.append([Die(int(sides[:-1]), '-') for i in range(int(qty))])
            continue

        # case: 2d8
        dice.append([Die(int(sides)) for i in range(int(qty))])

    # flatten the list and return
    return list(chain.from_iterable(dice))


def gen_adv_rolls(die: Die):
    return [max(roll) for roll in (product(*(range(1, die.sides+1), range(1, die.sides+1))))]


def gen_dis_rolls(die: Die):
    return [min(roll) for roll in (product(*((range(1, die.sides+1), range(1, die.sides+1)))))]


def gen_rolls(die: Die):
    return list(range(1, die.sides+1))


# https://stackoverflow.com/a/64938679
def flatten(data):
    if isinstance(data, tuple):
        for x in data:
            yield from flatten(x)
    else:
        yield data


def calculate_odds(die_str: str, target: int) -> float:

    # parse the die string
    dice = parse_die_str(die_str)

    total_combinations = 1
    for d in dice:
        total_combinations *= d.roll_count

    favorable_outcomes = 0

    # Generate all possible outcomes of rolling the dice
    adv_dice = list(product(*(gen_adv_rolls(die) for die in dice if die.adv == "+"))) or [0]
    dis_dice = list(product(*(gen_dis_rolls(die) for die in dice if die.adv == "-"))) or [0]
    neutral_dice = list(product(*(gen_rolls(die) for die in dice if not die.adv))) or [0]

    rolls = [[(i, j, k) for k in adv_dice] for j in dis_dice for i in neutral_dice]
    for roll in rolls:
        for die in roll:
            if sum(flatten(die)) >= target:
                favorable_outcomes += 1

    # Calculate the probability
    probability = favorable_outcomes / total_combinations

    print(f"{total_combinations=}, {favorable_outcomes=}")

    return probability, favorable_outcomes, total_combinations


if __name__ == "__main__":

    res = calculate_odds("1d4+ 1d8+ 1d20+", 5)
    print(res)
