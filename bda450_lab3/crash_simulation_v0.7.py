import matplotlib.pyplot as plt
import random

rand = random.Random()


class BrakingSim:

    def __init__(self):

        # State for two separate cars
        self.position1 = 0
        self.position2 = 0
        self.velocity1 = 0
        self.velocity2 = 0
        self.brakingstarttime1 = 0
        self.brakingstarttime2 = 0
        self.isbreaking1 = False
        self.isbreaking2 = False
        self.crash = False

        self.decelerationrate = 0  # Braking rate the same for both cars
        self.reactiontime = 0  # Only applies to second driver who reacts to the first braking

        self.interval = 0
        self.t = 0.
        self.timesteps = []

        # Keeping of position/speed records for each car, for each interval
        self.pos1 = []
        self.pos2 = []
        self.veloc1 = []
        self.veloc2 = []

    def initialize(self, gaplength, startingspeed, brakingrate, car1_start_braking_time, minreactiontime,
                   maxreactiontime, timeinterval):

        # Setting the following car to be at position 0, and the position of the first car to be gaplength ahead
        self.position1 = gaplength
        self.position2 = 0

        self.velocity1 = startingspeed
        self.velocity2 = startingspeed
        self.decelerationrate = brakingrate

        self.brakingstarttime1 = car1_start_braking_time  # Breaking time of the first car set in advance
        self.brakingstarttime2 = None  # Let's wait until it happens, and let driver 2 react!

        self.reactiontime = 1 # rand.uniform(minreactiontime, maxreactiontime)

        self.isbreaking1 = False
        self.isbreaking2 = False
        self.crash = False

        # Initialize time, and all data tracking lists to initial state
        self.interval = timeinterval
        self.t = 0.
        self.timesteps = [self.t]

        self.pos1 = [self.position1]
        self.pos2 = [self.position2]
        self.veloc1 = [self.velocity1]
        self.veloc2 = [self.velocity2]

    def observe(self):
        self.pos1.append(self.position1)
        self.pos2.append(self.position2)
        self.veloc1.append(self.velocity1)
        self.veloc2.append(self.velocity2)
        self.timesteps.append(self.t)

    def update(self):

        # DETECT IMPACT
        # CAN'T SIMPLY TEST FOR POSITION BEING THE SAME.  BECAUSE OF DISCRETE TIME, CARS MAY PASS EACH OTHER FROM
        # ONE TIME STEP THE NEXT, AND NEVER BE ON EXACTLY THE SAME POSITION IN THE SAME TIME STEP.
        # INSTEAD, WE TEST IF THEY 'PASS' EACH OTHER DURING THE TIME STEP.  SINCE THE CAN'T 'PASS' (BECAUSE THEY
        # ARE ONE BEHIND THE OTHER), THE 'PASSING' OF POSITION INDICATES A CRASH.
        oldpos1 = self.position1
        oldpos2 = self.position2

        # The original code (up to v0.6) contained an error.  In each time step, we would update the position based on the
        # velocity, and then check (below) if the positions of the cars had 'passed', indicating a crash during the
        # time interval.  But there are (at least) a couple of problems here!:
        #
        # -Specifically, even though we said that cars couldn't pass each other, in the event of a crash (detected
        # by the latter car's position moving ahead of the former), we left the new positions in place!  This placed
        # the latter car ahead of the former (even if just for a short period of time)!
        # -More generally, we violated the idea of calculating our values at time t based on those from time t-1.
        #
        # A couple of changes were made to improve this.
        # - Calculate the projected new positions in temporary variables, before updating our state.
        # - Update the positions only after all of the other calculations had been done.
        #
        # There are still issues with how we deal with the position itself at the time of collision.  If the cars would
        # otherwise 'pass' from time t-1 to t (meaning a crash occurred between t-1 and t), what should their positions
        # be at time t?
        # -If we set them to the new positions (as we did in earlier versions), then car2 will be ahead of car1!
        # -If we set them to the old positions, then effectively the cars don't move at all from t-1 to t, which
        # is an unusual pause in the motion!
        #
        # Clearly, the new positions of the cars should be somewhere between the old position and the new position, and
        # car1 should not be behind car2.  But what should the positions be?  Ideally, we should be able to calculate
        # what happens in the interval _between_ steps... But that's not how discrete time generally works, and is, in
        # fact, one of the drawbacks of it!  Two approaches can be useful here:
        # -Use a reasonable assumption/calculation (and also test if it works).  Here, I have assumed in the event of a crash, the
        # new positions of both cars will be the same, equal to the average of the projected new positions for the time
        # step.
        # -These problems crop up because of things that happen in the intervals of steps.  To reduce the impact
        # of these issues, and get more accurate results, reduce the length of the time interval!  In fact, for something
        # that happens as quickly as a car crash, 0.1 second intervals are very long.  Try in interval like 0.01 seconds.

        newpos1 = self.position1 + self.velocity1 * self.interval
        newpos2 = self.position2 + self.velocity2 * self.interval

        if oldpos1 > oldpos2 and newpos1 < newpos2:
            self.crash = True

            # NOT REALISTIC TO HAVE THE TWO CARS SIMPLY MOVE TOGETHER AFTER IMPACT.  IN REALITY, THERE IS SOME
            # 'ELASTIC' FORCE, AS THE CARS 'BOUNCE' OFF EACH OTHER A LITTLE BIT.  WE DON'T HAVE THE PHYSICS
            # EXPERTISE TO BUILD A PHYSICS MODEL FOR THIS.  INSTEAD, WE WILL TRY TO COME UP WITH SOMETHING THAT
            # PROVIDES A REALISTIC RESULT.  IT CAN BE REFINED AS WE LEARN MORE.
            # WE WILL STILL COMPUTE THE AVERAGE VELOCITY AS THE STARTING POINT, BUT WE WILL APPLY A 'BOUNCE' FACTOR,
            # SOME PROPORTION OF THE IMPACT VELOCITY THAT IS ADDED TO THE FIRST CAR, AND SUBTRACTED FROM THE SECOND.

            net_impact_speed = self.velocity2 - self.velocity1
            print("Time of impact: %0.3f" % self.t)
            print("Net impact speed: %0.3f" % net_impact_speed)

            # New positions for both cars are the average of the original newpositions
            avg_pos = (newpos1 + newpos2) / 2
            newpos1 = avg_pos
            newpos2 = avg_pos

            bounce_proportion = 0.1

            avg_velocity = (self.velocity1 + self.velocity2)/2
            self.velocity1 = avg_velocity + bounce_proportion * net_impact_speed
            self.velocity2 = avg_velocity - bounce_proportion * net_impact_speed

        # Wait until the first car has braked to apply reaction/braking to car 2, to allow more
        # flexibility/sophistication possibilities in the future

        # isbreaking flags used to ensure braking process only starts once
        if not self.isbreaking1 and self.t > self.brakingstarttime1:
            self.isbreaking1 = True

            # When car 1 brakes, determine time that car 2 will start braking
            self.brakingstarttime2 = self.t + self.reactiontime

        if not self.isbreaking2 and self.brakingstarttime2 and self.t > self.brakingstarttime2:
            self.isbreaking2 = True

        #Update positions
        self.position1 = newpos1
        self.position2 = newpos2

        # If braking, apply deceleration
        # Velocity floor via braking is zero
        if self.isbreaking1:
            self.velocity1 = max(self.velocity1 - self.decelerationrate * self.interval, 0)
        if self.isbreaking2:
            self.velocity2 = max(self.velocity2 - self.decelerationrate * self.interval, 0)
        self.t = self.t + self.interval

    def runsim(self, gaplength, startingspeed, brakingrate, car1_start_braking_time, minreactiontime,
                   maxreactiontime, timeinterval):
        self.initialize(gaplength, startingspeed, brakingrate, car1_start_braking_time, minreactiontime,
                   maxreactiontime, timeinterval)

        # Run while either car has positive velocity
        while self.velocity1 > 0 or self.velocity2 > 0:
            self.update()
            self.observe()

        plt.figure(1)
        plt.plot(self.timesteps, self.veloc1)
        plt.plot(self.timesteps, self.veloc2)
        plt.figure(2)
        plt.plot(self.timesteps, self.pos1)
        plt.plot(self.timesteps, self.pos2)
        plt.show()


if __name__ == '__main__':
    sim = BrakingSim()
    sim.runsim(10, 28, 12, 2, .5, 1.25, .01)
