import random
import matplotlib.pyplot as plt

rand = random.Random()


def flipcoin():
    coin = rand.randint(1, 2)
    return coin


def playround(n):
    # print("---\nStart.")
    coinflip = flipcoin()
    # print(firstroll)
    if coinflip == 1:
        flipcoin()
        return True

    return False






def runtrial(numgames):
    wintotal = 0
    for gamenum in range(numgames):
        if playround():
            wintotal += 1

    return wintotal / numgames


def singletrial(numgames):
    winproportion = runtrial(numgames)

    print('Win proportion: %0.3f' % winproportion)


def sample_of_trials(numsamples, numgames):
    samples = []
    for x in range(numsamples):
        print(x)
        samples.append(runtrial(numgames))

    plt.hist(samples)
    plt.show()


if __name__ == '__main__':
    num_games = 500
    singletrial(num_games)
