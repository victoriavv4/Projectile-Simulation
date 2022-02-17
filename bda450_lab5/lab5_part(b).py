# Based on scenario from the Law text, and based on code from the SimPy documentation

import simpy
import random
import statistics


rand = random.Random()


class MM1Sim:

    def __init__(self):
        # Aggregation of data
        self.number_delayed = 0
        self.total_delay = 0
        self.min_delay = None
        self.max_delay = None
        self.avg_list = []

    def runsim(self, number_of_customers, mean_interarrival, mean_service):
        self.number_delayed = 0
        self.total_delay = 0
        self.min_delay = None
        self.max_delay = None

        env = simpy.Environment()
        server1 = simpy.Resource(env, capacity=1)
        server2 = simpy.Resource(env, capacity=1)
        env.process(sim.source(env, server1, server2, number_of_customers, mean_interarrival, mean_service))

        env.run()

        print("Number of customers: %d" % self.number_delayed)
        print("Total delay: %0.4f" % self.total_delay)
        print("Average delay: %0.4f" % (self.total_delay / self.number_delayed))
        print("Minimum delay: %0.4f" % self.min_delay)
        print("Maximum delay: %0.4f" % self.max_delay)
        self.avg_list.append(self.total_delay / self.number_delayed)
        print(f'Average wait time per customer across {len(self.avg_list)} runs: {statistics.mean(self.avg_list):.4f}')
        print(f'Standard deviation of wait times across {len(self.avg_list)} runs: '
              f'{statistics.pstdev(self.avg_list):.4f} ')

    # Time between arrivals and service time are now random, so pass in parameters for distributions
    def source(self, env, server1, server2, number_of_customers, mean_interarrival, mean_service):
        """Source generates customers randomly"""
        for i in range(number_of_customers):
            # Wait a random amount of time before creating and scheduling customer
            yield env.timeout(rand.expovariate(1 / mean_interarrival))

            # Customer service time determined randomly
            c = self.customer(env, i + 1, rand.expovariate(1 / mean_service), server1, server2)
            env.process(c)

    def customer(self, env, id, service_time, server1, server2):
        arrival = env.now
        print("ID %d arriving at: %0.1f" % (id, arrival))

        if len(server1.queue) < len(server2.queue):

            with server1.request() as request1:
                yield request1
                self.number_delayed += 1
                wait_time = env.now - arrival
                self.total_delay += wait_time
                if self.min_delay is None or wait_time < self.min_delay:
                    self.min_delay = wait_time
                if self.max_delay is None or wait_time > self.max_delay:
                    self.max_delay = wait_time

                print("This customer joined the queue of server 1")
                print("ID %d wait time: %0.1f" % (id, wait_time))
                print("Number delayed: %d   Total wait delay: %0.2f" % (self.number_delayed, self.total_delay))
                print("ID %d started service at: %0.1f" % (id, env.now))
                yield env.timeout(service_time)
                print("ID %d finished service at: %0.1f" % (id, env.now))

        elif len(server1.queue) > len(server2.queue):

            with server2.request() as request2:
                yield request2
                self.number_delayed += 1
                wait_time = env.now - arrival
                self.total_delay += wait_time
                if self.min_delay is None or wait_time < self.min_delay:
                    self.min_delay = wait_time
                if self.max_delay is None or wait_time > self.max_delay:
                    self.max_delay = wait_time

                print("This customer joined queue of server 2")
                print("ID %d wait time: %0.1f" % (id, wait_time))
                print("Number delayed: %d   Total wait delay: %0.2f" % (self.number_delayed, self.total_delay))
                print("ID %d started service at: %0.1f" % (id, env.now))
                yield env.timeout(service_time)
                print("ID %d finished service at: %0.1f" % (id, env.now))

        else:
            rand_server = random.randint(1, 3)
            if rand_server == 1:
                with server1.request() as request1:
                    yield request1
                    self.number_delayed += 1
                    wait_time = env.now - arrival
                    self.total_delay += wait_time
                    if self.min_delay is None or wait_time < self.min_delay:
                        self.min_delay = wait_time
                    if self.max_delay is None or wait_time > self.max_delay:
                        self.max_delay = wait_time

                    print("This customer joined the queue of server 1")
                    print("ID %d wait time: %0.1f" % (id, wait_time))
                    print("Number delayed: %d   Total wait delay: %0.2f" % (self.number_delayed, self.total_delay))
                    print("ID %d started service at: %0.1f" % (id, env.now))
                    yield env.timeout(service_time)
                    print("ID %d finished service at: %0.1f" % (id, env.now))

            else:
                with server2.request() as request2:
                    yield request2
                    self.number_delayed += 1
                    wait_time = env.now - arrival
                    self.total_delay += wait_time
                    if self.min_delay is None or wait_time < self.min_delay:
                        self.min_delay = wait_time
                    if self.max_delay is None or wait_time > self.max_delay:
                        self.max_delay = wait_time

                    print("This customer joined queue of server 2")
                    print("ID %d wait time: %0.1f" % (id, wait_time))
                    print("Number delayed: %d   Total wait delay: %0.2f" % (self.number_delayed, self.total_delay))
                    print("ID %d started service at: %0.1f" % (id, env.now))
                    yield env.timeout(service_time)
                    print("ID %d finished service at: %0.1f" % (id, env.now))


if __name__ == '__main__':
    sim = MM1Sim()
    for i in range(100):
        sim.runsim(1000, 0.5, 1.5)
