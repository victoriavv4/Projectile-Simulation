import random
import matplotlib.pyplot as plt

rand = random.Random()


def flipcoin():
    coin = rand.randint(1, 2)
    return coin


def playround(inputlist, n=6):
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
            inputlist.append(flip_num)

            break


def runtrial(numgames, inputlist):
    for x in range(numgames):
        playround(inputlist)
    print(f"\nThe average number of flips to reach 'n' heads in a row is: {sum(inputlist) / numgames:.2f}")
    plt.hist(inputlist, bins=10)
    plt.show()


def main():
    flip_list = []

    runtrial(500, flip_list)
    print(flip_list)


if __name__ == "__main__":
    main()
