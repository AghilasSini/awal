"""  warm program clean and beatiful code   """
import random


def my_func():
    """ function for generating random value  """
    return random.randint(0, 100)


def multiply(a, b):
    """ function multiply to number """
    return a * b


## Decorator in python
## Functions are object
## Functions can be defined inside other function


def null_decorator(func):
    return func






def strong(func):
    def wrapper():
        return '<strong>'+func()+'</strong>'
    return wrapper

def emphasis(func):
    def wrapper():
        return "<em>" + func() + "</em>"
    return wrapper

@strong
@emphasis
def greet():
    return 'Hello'
