import random
import matplotlib.pyplot as plt

rand = random.Random()


def store_flips():
    flip_list = []
    return flip_list


def flipcoin():
    coin = rand.randint(1, 2)
    return coin


def playround(n=6):
    heads = 0
    flip_num = 0
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
            store_flips().append(flip_num)

            break

def find_average(func):
    store_flips()

def runtrial(numgames):
    for x in range(numgames):
        playround()
    print(f"\nThe average number of flips to reach 'n' heads in a row is: {sum(store_flips()) / numgames:.2f}")


def show_histogram():
    plt.hist(store_flips(), bins=10)
    plt.show()


def main():
    runtrial(500)
    show_histogram()


if __name__ == "__main__":
    main()
