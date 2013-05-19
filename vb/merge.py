import os
import subprocess


class MergeTask(object):

    def __init__(self, workspaces, locmain='locmain'):
        self.workspaces = workspaces
        self.paths = [os.path.join('.vb', w) for w in workspaces]
        self.locmain = locmain

    def get_branch_names(self):
        return self.workspaces  # FIXME: relax WS=BRANCH restriction

    def run(self):
        for path in self.paths:
            subprocess.check_call(['git', 'push', self.locmain], cwd=path)

        branches = self.get_branch_names()
        subprocess.check_call(['git', 'merge'] + branches)
