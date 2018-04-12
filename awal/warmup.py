"""  warm program clean and beatiful code   """
import random


def my_func():
    """ function for generating random value  """
    return random.randint(0, 100)


def multiply(a, b):
    """ function multiply to number """
    return a * b


print(multiply(my_func(), my_func()))
