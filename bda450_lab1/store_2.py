import random
import matplotlib.pyplot as plt

rand = random.Random()





def flipcoin():
    coin = rand.randint(1, 2)
    return coin


def playround(n=6):
    heads = 0
    flip_num = 0
    flip_list = []
    while True:
        coinflip = flipcoin()
        flip_num += 1

        # print(coinflip)
        if coinflip == 1:
            heads += 1
        if coinflip == 2:
            heads = 0
        elif heads == n:
            print(f'It took {flip_num} flips to reach 6 heads in a row')
            flip_list.append(flip_num)
            return flip_list

def runtrial(numgames):
    for x in range(numgames):
        playround()

def print_list():
    print(playround())

playround()
runtrial(10)
print_list()


