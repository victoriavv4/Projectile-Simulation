import matplotlib.pyplot as plt


class CreditSim:

    def __init__(self):
        self.amountOwing = 0
        self.interestRate = 0.
        self.payment = 0
        self.t = 0.
        self.debt = 0
        self.interval = 1
        self.timeSteps = []
        self.result = []

    def initialize(self, owing, interestRate, monthlyPayment, timeInterval):
        self.amountOwing = owing
        self.interestRate = interestRate
        self.payment = monthlyPayment
        self.debt = 0
        self.interval = timeInterval
        self.result = [self.amountOwing]
        self.t = 0.
        self.timeSteps = [self.t]

    def observe(self):
        self.result.append(self.amountOwing)
        self.timeSteps.append(self.t)

    def update(self):
        self.debt = (self.amountOwing - self.payment)
        self.amountOwing = (self.debt * (self.interestRate / 12)) + self.debt
        self.t = self.t + self.interval

    def runSim(self, owing, interestRate, monthlyPayment, timeInterval):
        self.initialize(owing, interestRate, monthlyPayment, timeInterval)
        while self.t < 60:
            self.update()
            self.observe()

        for i in range(len(self.result)):
            print(i, end=" ")
            print(f'{self.result[i]:.2f}')

        plt.plot(self.timeSteps, self.result)
        plt.show()


def main():
    sim = CreditSim()
    sim.runSim(10000, 0.07, 50, 1.0)


if __name__ == '__main__':
    main()
