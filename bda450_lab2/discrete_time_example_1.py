import matplotlib.pyplot as plt


class BrakingSim:

    def __init__(self):
        # You might want to initialize the simulation here, but that means that you will initialize when the
        # object is created, rather than on every simulation run
        self.currentposition = 0
        self.currentvelocity = 0
        self.decelerationrate = 0
        self.brakingstarttime = 0
        self.interval = 0
        self.t = 0.
        self.timesteps = []

        self.positions = []
        self.velocities = []

    def initialize(self, startingspeed, brakingrate, brakingstarttime, timeinterval):
        self.currentposition = 0
        self.currentvelocity = startingspeed
        self.decelerationrate = brakingrate
        self.brakingstarttime = brakingstarttime
        self.interval = timeinterval
        self.t = 0.
        self.timesteps = [self.t]

        self.positions = [self.currentposition]
        self.velocities = [self.currentvelocity]

    def observe(self):
        self.positions.append(self.currentposition)
        self.velocities.append(self.currentvelocity)
        self.timesteps.append(self.t)

    def update(self):
        self.currentposition = self.currentposition + self.currentvelocity * self.interval
        if self.t > self.brakingstarttime:
            self.currentvelocity = self.currentvelocity - self.decelerationrate * self.interval
        self.t = self.t + self.interval

    def runsim(self, startingspeed, brakingrate, brakingstarttime, timeinterval):
        self.initialize(startingspeed, brakingrate, brakingstarttime, timeinterval)
        while self.currentvelocity > 0:
            self.update()
            self.observe()

        plt.figure(1)
        plt.plot(self.timesteps, self.velocities)
        plt.figure(2)
        plt.plot(self.timesteps, self.positions)
        plt.show()


if __name__ == '__main__':
    sim = BrakingSim()
    sim.runsim(28, 5, 4, .1)
