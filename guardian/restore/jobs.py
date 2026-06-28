from guardian.restore.status import RestoreStatus

status = RestoreStatus()


class RestoreJobs:

    def get(self, filename):
        return status.get(filename)

    def create(self, filename):
        return status.create(filename)

    def update(self, filename, state):
        status.update(filename, state)

    def fail(self, filename, error):
        status.fail(filename, error)
