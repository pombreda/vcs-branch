import os

from .task import BaseTask


class MergeTask(BaseTask):

    @property
    def paths(self):
        return [os.path.join('.vb', w) for w in self.workspaces]

    def get_branch_names(self):
        return self.workspaces  # FIXME: relax WS=BRANCH restriction

    def run(self):
        branches = self.get_branch_names()

        for (path, br) in zip(self.paths, branches):
            self.check_call(['git', 'push', self.locmain, br], cwd=path)

        self.check_call(['git', 'merge'] + branches)


task = MergeTask
