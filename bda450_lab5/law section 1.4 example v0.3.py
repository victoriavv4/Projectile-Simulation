#Based on scenario from the Law text, and based on code from the SimPy documentation

import simpy

class DeterministicServerSim:

    def __init__(self):
        self.number_delayed = 0
        self.total_delay = 0

    def runsim(self, arrival_times, serve_times):
        self.number_delayed = 0
        self.total_delay = 0
        env = simpy.Environment()  # Simulation environment
        server = simpy.Resource(env, capacity=1) # Server is shared resource
        env.process(sim.source(env, arrival_times, serve_times, server)) # Create a source, and add it to schedule
        env.run()


    def source(self, env, arrival_times, serve_times, server):
        """Source generates customers randomly"""
        for i in range(len(arrival_times)):

            #Schedule an event (wait a certain time), to resume after the timeout
            yield env.timeout(arrival_times[i])

            #Create each customer, and schedule
            c = self.customer(env, i+1, serve_times[i], server)
            env.process(c)

    def customer(self, env, id, service_time, server):
        arrival = env.now
        print("ID %d arriving at: %0.1f" % (id, arrival))

        # Set up 'request' as an attempt to make use of the server
        with server.request() as request:

            #Wait until we successfully obtain the server; yield will resume once that takes place
            yield request

            #We now have the server
            self.number_delayed += 1
            wait_time = env.now - arrival
            self.total_delay += wait_time
            print("ID %d wait time: %0.1f" % (id, wait_time ))
            print("Number delayed: %d   Total wait delay: %0.2f" % (self.number_delayed, self.total_delay))
            print("ID %d started service at: %0.1f" % (id, env.now))

            # Now that we have the server, waiting for a period of time simulates the transaction.  The yield:
            # allows the timeout to be scheduled/take place starting now; stops execution of this function, so
            # that other events can take place; resumes execution at this point when the timeout has elapsed.
            yield env.timeout(service_time)
            print("ID %d finished service at: %0.1f" % (id, env.now))


if __name__ == '__main__':
    arrival_times = [0.4, 1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9]
    serve_times = [2.0, 0.7, 0.2, 1.1, 3.7, 0.6, 99, 99, 99]

    sim = DeterministicServerSim()
    sim.runsim(arrival_times, serve_times)

