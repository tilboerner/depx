from fake_module.another_module import oh_nice
import random


def pick_a_number():
    print(oh_nice())
    return random.randint(1, 10)
