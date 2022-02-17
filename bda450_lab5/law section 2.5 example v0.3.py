import simpy
import random

rand = random.Random()


# A subclass of the simpy Resource with monitoring code added to update stats every time it is requested or released.
# You can use this code as a model when you want to monitor a resource. (Based on code in the SimPy docs.)
class MonitoredCPU(simpy.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elapsed_time = 0  # Time since beginning of the simulation
        self.last_update_time = 0  # Time of last stat update, used to determine interval for the current values
        self.total_busy_time = 0  # Time CPU has been in use
        self.total_queue_time = 0  # Total amount of time spent in queue by users

    def request(self, *args, **kwargs):
        self.update_stats()
        return super().request(*args, **kwargs)

    def release(self, *args, **kwargs):
        self.update_stats()
        return super().release(*args, **kwargs)

    def update_stats(self):
        time_interval = self._env.now - self.last_update_time
        self.elapsed_time = self._env.now
        self.last_update_time = self._env.now
        self.total_busy_time += len(self.users) * time_interval
        self.total_queue_time += len(self.queue) * time_interval


class SharedCPUSim:

    def runsim(self, number_of_users, mean_think_time, mean_job_time, max_quantum, swap_time):
        env = simpy.Environment()
        cpu = MonitoredCPU(env, capacity=1) #Use the subclass in which we added monitoring capabilities
        env.process(sim.source(env, number_of_users, mean_think_time, mean_job_time, max_quantum, swap_time, cpu))
        env.run(until=500)

        print("Average utilization: %0.4f" % (cpu.total_busy_time / cpu.elapsed_time))
        print("Average queue length: %0.4f" % (cpu.total_queue_time / cpu.elapsed_time))

    def source(self, env, number_of_users, mean_think_time, mean_job_time, max_quantum, swap_time, cpu):
        """Source generates customers randomly"""
        yield env.timeout(0)  # To act as a generator, this function must yield something.  However, each user
                              # Individually yields based on wait time.  Thus, added a trivial yield.
        for i in range(number_of_users):
            u = self.user(env, i + 1, mean_think_time, mean_job_time, max_quantum, swap_time, cpu)
            env.process(u)

    def user(self, env, id, mean_think_time, mean_job_time, max_quantum, swap_time, cpu):

        while True:
            # Initial think time
            think_time = rand.expovariate(1 / mean_think_time)
            print("ID %d  Think time: %0.4f" % (id, think_time))
            yield env.timeout(think_time)

            #
            # Simple implementation -- we will calculate how much processor time we get in advance, and then
            # give up the CPU after that amount of time and reschedule the rest of the job, rather than using
            # a pre-emptive interrupt approach
            #

            # Determine total job time
            required_job_time = rand.expovariate(1 / mean_job_time)

            # Store the remaining CPU time required to complete the job; at beginning, is entire job time
            remaining_job_time = required_job_time

            # Keep grabbing shares of the CPU until job is done
            while remaining_job_time > 0:
                # Wait for the CPU
                wait_start = env.now
                print("ID %d  Start waiting at: %0.4f  Job time required: %0.4f" % (id, env.now, required_job_time))
                with cpu.request() as request:
                    yield request

                    waiting_time = env.now - wait_start
                    if waiting_time > 0:
                        #Print more noteworthy message when job actually had to wait
                        print("**ID %d  Wait time for CPU: %0.4f." % (id, waiting_time))
                    job_time_to_compute = min(remaining_job_time, max_quantum) # Run time capped at maximum quantum
                    print("ID %d  Got CPU at %0.4f.  Remaining time required: %0.4f  Slice to take: %0.4f" % (
                        id, env.now, remaining_job_time, job_time_to_compute))

                    # Occupying the CPU for the time period (implemented as a time delay while 'owning' the CPU),
                    # plus context switching time
                    yield env.timeout(job_time_to_compute + swap_time)

                    remaining_job_time -= job_time_to_compute
                    print("ID %d  Giving up CPU at %0.4f.  Remaining time required: %0.4f" % (
                        id, env.now, remaining_job_time))

if __name__ == '__main__':
    sim = SharedCPUSim()
    sim.runsim(20, 25, 0.8, 0.1, 0.015)
