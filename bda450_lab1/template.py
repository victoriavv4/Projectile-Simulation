import random
import matplotlib.pyplot as plt

rand = random.Random()

def rolldice():
    d1 = rand.randint(1, 6)
    d2 = rand.randint(1, 6)
    # print("%d + %d = %d" % (d1, d2, d1 + d2))
    return d1 + d2


def playround():
    # print("---\nStart.")
    firstroll = rolldice()
    # print(firstroll)
    if firstroll == 7 or firstroll == 11:
        # print('Win')
        return True
    elif firstroll in {2, 3, 12}:
        # print('Lose')
        return False
    else:
        pass
        # print('Point number: %d' % firstroll)
    while True:
        nextroll = rolldice()
        # print(nextroll)
        if nextroll == 7:
            # print('Lose')
            return False
        if nextroll == firstroll:
            # print('Win')
            return True


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
    num_games = 10
    singletrial(num_games)
