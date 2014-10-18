from simpy import Container
from errors import ResourceException
from random import gauss
from logger import simlog, INFO
from constants import QUEUEING_MEAN, QUEUING_STD

class DCI(Container):

    def __init__(self, env, name, cores):
        self.name = name
        self.env = env
        super(DCI, self).__init__(env, cores, init=0)
        simlog(INFO, "Initializing DCI '%s' with %d cores." % (name, cores), self.env)

    def submit_job(self, job, cores):
        if cores > self.capacity:
            raise ResourceException("Can't get more than capacity allows.")

        queuing_delay = int(gauss(QUEUEING_MEAN, QUEUING_STD))
        if queuing_delay < 0:
            queuing_delay = 0

        simlog(INFO, "Waiting for %d seconds on job request of size %d." % (queuing_delay, cores), self.env)
        yield self.env.timeout(queuing_delay)

        simlog(INFO, "Job launching on %s with %d cores at %d." % (self.name, cores, self.env.now), self.env)
        yield job.put(cores)