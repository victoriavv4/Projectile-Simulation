import simpy

class DeterministicServerSim:

    def __init__(self):
        self.number_delayed = 0
        self.total_delay = 0

    def runsim(self, arrival_times, serve_times):
        self.number_delayed = 0
        self.total_delay = 0
        env = simpy.Environment()
        server = simpy.Resource(env, capacity=1)
        env.process(sim.source(env, arrival_times, serve_times, server))
        env.run()


    def source(self, env, arrival_times, serve_times, server):
        """Source generates customers randomly"""
        for i in range(len(arrival_times)):
            yield env.timeout(arrival_times[i])
            c = self.customer(env, i+1, serve_times[i], server)
            env.process(c)

    def customer(self, env, id, service_time, server):
        arrival = env.now
        print("ID %d arriving at: %0.1f" % (id, arrival))

        with server.request() as request:
            yield request
            self.number_delayed += 1
            wait_time = env.now - arrival
            self.total_delay += wait_time
            print("ID %d wait time: %0.1f" % (id, wait_time ))
            print("Number delayed: %d   Total wait delay: %0.2f" % (self.number_delayed, self.total_delay))
            print("ID %d started service at: %0.1f" % (id, env.now))
            yield env.timeout(service_time)
            print("ID %d finished service at: %0.1f" % (id, env.now))


if __name__ == '__main__':
    arrival_times = [0.4, 1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9]
    serve_times = [2.0, 0.7, 0.2, 1.1, 3.7, 0.6, 99, 99, 99]

    sim = DeterministicServerSim()
    sim.runsim(arrival_times, serve_times)

