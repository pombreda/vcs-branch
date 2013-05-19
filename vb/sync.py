import os

from .task import MultiBranchTask


class SyncTask(MultiBranchTask):

    def run(self):
        if not self.workspaces:
            self.workspaces = os.listdir('.vb')
            if not self.workspaces:
                self.logger.warn('No workspace exists.')
                return
            self.logger.info(
                'No workspace is specified.  Running for all\n%s',
                self.workspaces)
        branches = self.get_branch_names()

        for (path, br) in zip(self.paths, branches):
            self.check_call(['git', 'fetch', self.locmain], cwd=path)

        runner = self.check_call if self.fg else self.call_bg
        runner(['git', 'relink'] + self.paths + ['.'])


task = SyncTask
