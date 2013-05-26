from .base import MultiBranchTask


class MergeTask(MultiBranchTask):

    def run(self):
        branches = self.get_branch_names()

        for (path, br) in zip(self.paths, branches):
            self.check_call(['git', 'push', self.locmain, br], cwd=path)

        self.check_call(['git', 'merge'] + branches)

        if self.reset or self.reset_to_remote:
            self.remerge(branches)

    def remerge(self, branches):
        current = self.get_branches().current()
        if self.reset_to_remote:
            self.reset = current.rbranch

        tmp_branch = self.old_branch_format.format(current.branch)
        self.check_call(['git', 'branch', tmp_branch])

        self.check_call(['git', 'reset', '--hard', self.reset])
        self.check_call(['git', 'merge'] + branches)
        diff = self.check_output(['git', 'diff', tmp_branch])
        if diff.strip():
            self.logger.warn(
                'Re-merging produces different result.\n'
                'Check: git diff %s', tmp_branch)
        else:
            self.logger.info('Remove %s', tmp_branch)
            self.check_call(['git', 'branch', '-D', tmp_branch])


task = MergeTask
