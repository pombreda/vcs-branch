from .task import MultiBranchTask


class MergeTask(MultiBranchTask):

    def run(self):
        branches = self.get_branch_names()

        for (path, br) in zip(self.paths, branches):
            self.check_call(['git', 'push', self.locmain, br], cwd=path)

        self.check_call(['git', 'merge'] + branches)


task = MergeTask
