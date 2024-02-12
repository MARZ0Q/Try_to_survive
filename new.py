import sys
import random 

def randomeChooser():
    return random.randint(1,2)


while True:
    if randomeChooser() == 1 and True:
        sys.exit()
    else:
        print('not working')