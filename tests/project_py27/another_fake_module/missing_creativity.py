from fake_module.another_module import oh_nice
import random

# Force Python2 syntax
print "This is python2 only", 1000L

def pick_a_number():
    print(oh_nice())
    return random.randint(1, 10)
