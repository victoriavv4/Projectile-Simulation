import matplotlib.pyplot as plt
import random

rand = random.Random()


class BrakingSim:

    def __init__(self):

        # State for 3 separate cars
        self.position1 = 0
        self.position2 = 0
        self.position3 = 0
        self.velocity1 = 0
        self.velocity2 = 0
        self.velocity3 = 0
        self.brakingstarttime1 = 0
        self.brakingstarttime2 = 0
        self.brakingstarttime3 = 0
        self.isbreaking1 = False
        self.isbreaking2 = False
        self.isbraking3 = False
        self.crash = False

        self.decelerationrate = 0  # Braking rate the same for each car
        self.reactiontime = 0  # Only applies to second and 3rd driver who react to its predecessor car braking

        self.interval = 0
        self.t = 0.
        self.timesteps = []

        # Keeping of position/speed records for each car, for each interval
        self.pos1 = []
        self.pos2 = []
        self.pos3 = []
        self.veloc1 = []
        self.veloc2 = []
        self.veloc3 = []

    def initialize(self, gaplength, startingspeed, brakingrate, car1_start_braking_time, minreactiontime,
                   maxreactiontime, timeinterval):

        # Setting cars positions relative to gaplength
        self.position1 = 2 * gaplength
        self.position2 = gaplength
        self.position3 = 0

        self.velocity1 = startingspeed
        self.velocity2 = startingspeed
        self.velocity3 = startingspeed
        self.decelerationrate = brakingrate  # constant among all 3 cars

        self.brakingstarttime1 = car1_start_braking_time  # Breaking time of the first car set in advance
        self.brakingstarttime2 = None  # wait until car 1 brakes and let driver 2 react
        self.brakingstarttime3 = None  # wait until car 2 brakes and let driver 3 react

        # reaction time is random for car 2 and 3
        self.reactiontime = rand.uniform(minreactiontime, maxreactiontime)

        # setting flags
        self.isbreaking1 = False
        self.isbreaking2 = False
        self.isbraking3 = False
        self.crash = False

        # Initialize time, and all data tracking lists to initial state
        self.interval = timeinterval
        self.t = 0.
        self.timesteps = [self.t]

        self.pos1 = [self.position1]
        self.pos2 = [self.position2]
        self.pos3 = [self.position3]
        self.veloc1 = [self.velocity1]
        self.veloc2 = [self.velocity2]
        self.veloc3 = [self.velocity3]

    def observe(self):
        self.pos1.append(self.position1)
        self.pos2.append(self.position2)
        self.pos3.append(self.position3)
        self.veloc1.append(self.velocity1)
        self.veloc2.append(self.velocity2)
        self.veloc3.append(self.velocity3)
        self.timesteps.append(self.t)

    def update(self):

        # setting temporary variables to store old positions to detect crash
        oldpos1 = self.position1
        oldpos2 = self.position2
        oldpos3 = self.position3

        # setting temporary variables to store the new positions and average new positions
        newpos1 = self.position1 + self.velocity1 * self.interval
        newpos2 = self.position2 + self.velocity2 * self.interval
        newpos3 = self.position3 + self.velocity3 * self.interval

        bounce_proportion = 0.1

        if oldpos1 > oldpos2 and newpos1 < newpos2:
            self.crash = True
            print(f'Crash: Car 2 into Car 1!')

            net_impact_speed1 = self.velocity2 - self.velocity1
            print("Time of impact: %0.3f" % self.t)
            print("Net impact speed: %0.3f" % net_impact_speed1)

            avg_pos = (newpos1 + newpos2) / 2
            newpos1 = avg_pos
            newpos2 = avg_pos
            avg_velocity = (self.velocity1 + self.velocity2) / 2
            self.velocity1 = avg_velocity + bounce_proportion * net_impact_speed1
            self.velocity2 = avg_velocity - bounce_proportion * net_impact_speed1

        elif oldpos3 > oldpos2 and newpos2 < newpos3:
            self.crash = True
            print(f'Crash: Car 3 into Car 2! ')
            net_impact_speed2 = self.velocity3 - self.velocity2
            print("Time of impact: %0.3f" % self.t)
            print("Net impact speed: %0.3f" % net_impact_speed2)

            avg_pos2 = (newpos2 + newpos3) / 2
            newpos2 = avg_pos2
            newpos3 = avg_pos2
            avg_velocity = (self.velocity2 + self.velocity3) / 2
            self.velocity2 = avg_velocity + bounce_proportion * net_impact_speed2
            self.velocity3 = avg_velocity - bounce_proportion * net_impact_speed2

        # isbreaking flags used to ensure braking process only starts once
        # if the car is not already braking, and the time is greater than the braking time set, then car1 will start
        # braking
        if not self.isbreaking1 and self.t > self.brakingstarttime1:
            self.isbreaking1 = True

            # When car 1 brakes, determine time that car 2 will start braking
            # the braking start time determined by the time at the given time step + the random reaction time generated
            self.brakingstarttime2 = self.t + self.reactiontime

        # now we can turn on car 2 brakes by ensuring that car 2 is not already braking, that the brake start time
        # is not none (and it's not since we just set the braking start time above ^) and that the current time step is
        # greater than the braking start time for car 2
        if not self.isbreaking2 and self.brakingstarttime2 and self.t > self.brakingstarttime2:
            self.isbreaking2 = True

            # when car 2 brakes (braking is turned on above ^) the braking start time for car 3 is set. Identical
            # to setting the brake start time for car 2
            self.brakingstarttime3 = self.t + self.reactiontime

        # now we can turn on car 3 brakes by ensuring that car 3 is not already braking, that the brake start time has
        # been set, an the current time step is greater than braking start time for car 3
        if not self.isbraking3 and self.brakingstarttime3 and self.t > self.brakingstarttime3:
            self.isbraking3 = True

        # Update positions
        self.position1 = newpos1
        self.position2 = newpos2
        self.position3 = newpos3

        # If braking, apply deceleration
        # these lines of code are to ensure that the velocity is not < 0. A velocity > 0 indicates that the car is
        # travelling backwards
        if self.isbreaking1:
            self.velocity1 = max(self.velocity1 - self.decelerationrate * self.interval, 0)
        if self.isbreaking2:
            self.velocity2 = max(self.velocity2 - self.decelerationrate * self.interval, 0)
        if self.isbraking3:
            self.velocity3 = max(self.velocity3 - self.decelerationrate * self.interval, 0)
        self.t = self.t + self.interval

    def runsim(self, gaplength, startingspeed, brakingrate, car1_start_braking_time, minreactiontime,
               maxreactiontime, timeinterval):
        self.initialize(gaplength, startingspeed, brakingrate, car1_start_braking_time, minreactiontime,
                        maxreactiontime, timeinterval)

        # Run while either car has positive velocity
        while self.velocity1 > 0 or self.velocity2 > 0 or self.velocity3 > 0:
            self.update()
            self.observe()

        plt.figure(1)
        plt.plot(self.timesteps, self.veloc1)
        plt.plot(self.timesteps, self.veloc2)
        plt.plot(self.timesteps, self.veloc3)
        plt.figure(2)
        plt.plot(self.timesteps, self.pos1)
        plt.plot(self.timesteps, self.pos2)
        plt.plot(self.timesteps, self.pos3)
        plt.show()


if __name__ == '__main__':
    sim = BrakingSim()
    sim.runsim(10, 28, 12, 2, .5, 1.25, .1)
