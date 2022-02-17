import matplotlib.pyplot as plt


class SimpleDTSim2:

    def __init__(self):
        # You might want to initialize the simulation here, but that means that you will initialize when the
        # object is created, rather than on every simulation run
        self.x = 0
        self.a = 0
        self.interval = 1
        self.result = []
        self.t = 0.
        self.timesteps = []

    def initialize(self, starting_x, a, timeinterval):
        self.x = starting_x
        self.a = a
        self.interval = timeinterval
        self.result = [self.x]
        self.t = 0.
        self.timesteps = [self.t]

    def observe(self):
        self.result.append(self.x)
        self.timesteps.append(self.t)

    def update(self):
        self.x = self.a * self.x
        self.t = self.t + self.interval

    def runsim(self, x, a, timeinterval, stoptime):
        self.initialize(x, a, timeinterval)
        while self.t < stoptime:
            self.update()
            self.observe()
        print(self.result)
        print(self.timesteps)


        plt.plot(self.timesteps, self.result)
        plt.show()


if __name__ == '__main__':
    sim = SimpleDTSim2()
    sim.runsim(1, 1.1, .1, 3)
