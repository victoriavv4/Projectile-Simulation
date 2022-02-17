import matplotlib.pyplot as plt


class SimpleDTSim:

    def __init__(self):
        # You might want to initialize the simulation here, but that means that you will initialize when the
        # object is created, rather than on every simulation run
        self.x = 0
        self.a = 0
        self.result = []

    def initialize(self, starting_x, a):
        self.x = starting_x
        self.a = a
        self.result = [self.x]

    def observe(self):
        self.result.append(self.x)

    def update(self):
        self.x = self.a * self.x

    def runsim(self, x, a, steps):
        self.initialize(x, a)
        for t in range(steps):
            self.update()
            self.observe()

        plt.plot(self.result)
        plt.show()


if __name__ == '__main__':
    sim = SimpleDTSim()
    sim.runsim(1, 1.1, 30)
