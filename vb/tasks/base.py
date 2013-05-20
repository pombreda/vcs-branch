import os
import sys

from ..core import Launchable
from ..vcs import parse_git_remote_v, GitBranches


class BaseTask(Launchable):

    def __init__(self, logger, locmain='locmain', **kwds):
        super(BaseTask, self).__init__(logger)

        self.locmain = locmain
        for (k, v) in kwds.items():
            setattr(self, k, v)

    @property
    def path(self):
        # FIXME: defining `path` for all tasks is not good because
        #        some task operate against multiple branches.
        return os.path.join('.vb', self.branch)

    def check_init(self):
        if not os.path.isdir('.vb'):
            raise RuntimeError('Not initialized')

    def run(self):
        self.check_init()

    def fail(self, message=None):
        print(message)
        sys.exit(1)

    def get_all_workspaces(self):
        return [w for w in os.listdir('.vb') if w != '.var']

    def get_remotes(self):
        output = self.check_output(['git', 'remote', '-v'])
        return dict((l[0], l[1]) for l in parse_git_remote_v(output))

    def get_branches(self):
        return GitBranches(self.logger).load()


class MultiBranchTask(BaseTask):

    def ws_to_path(self, workspace):
        """
        Convert workspace (branch) to file system path.
        """
        return os.path.join('.vb', workspace)

    @property
    def paths(self):
        return list(map(self.ws_to_path, self.workspaces))

    def get_branch_names(self):
        return self.workspaces  # FIXME: relax WS=BRANCH restriction
