import os

from .base import MultiBranchTask
from .checkout import GitBranches


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
        branches = GitBranches().load()
        current = branches.current()

        for (path, br) in zip(self.paths, self.get_branch_names()):
            self.call(['git', 'pull', '--ff', self.locmain, br], cwd=path)
            # FIXME: warn when git pull failed.
            if current.branch == br:
                self.call(['git', 'pull', '--ff', path, br])
                # FIXME: warn when git pull failed.
            else:
                self.check_call(['git', 'push', self.locmain, br], cwd=path)

        runner = self.check_call if self.fg else self.call_bg
        runner(['git', 'relink'] + self.paths + ['.'])


task = SyncTask
