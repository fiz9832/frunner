__all__ = ['TaskUnit']
import frunner as fr

class TaskUnit:
    def __init__(self, name, *args, cwd=None):
        self.name = name
        self.args = args
        self.state = fr.State.PENDING
        self.prereqs = []
        self.importance = 0
        self.cwd = cwd

    def __hash__(self):
        return hash(self.name)

    def requires(self, *args):
        """Add prerequist tasks that must be completed successfully
        before this task can run."""
        self.prereqs.extend(args)
    
    def get_distance(self):
        return -1*self.importance
