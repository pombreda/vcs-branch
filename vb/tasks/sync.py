from .base import MultiBranchTask


class SyncTask(MultiBranchTask):

    def run(self):
        if not self.workspaces:
            self.workspaces = self.get_all_workspaces()
            if not self.workspaces:
                self.logger.warn('No workspace exists.')
                return
            self.logger.info(
                'No workspace is specified.  Running for all\n%s',
                self.workspaces)
        branches = self.get_branches()
        current = branches.current()

        self.failures = 0
        for br in self.get_branch_names():

            self.logger.info('Sync: {0} -> locmain'.format(br))
            if current.branch == br:
                to_locmain = self.pull_from_branch
            else:
                to_locmain = self.push_to_locmain
            if to_locmain(br) != 0:
                continue

            self.logger.info('Sync: locmain -> {0}'.format(br))
            self.pull_from_locmain(br)

        runner = self.check_call if self.fg else self.call_bg
        runner(['git', 'relink'] + self.paths + ['.'])

        if self.failures != 0:
            self.fail('{0} failures during sync'.format(self.failures))

    def call_with_fail_count(self, msgfmt, *args, **kwds):
        returncode = self.call(*args, show_failed_stdout=True, **kwds)
        if returncode != 0:
            self.logger.warn(msgfmt.format(code=returncode))
            self.failures += 1
        return returncode

    def pull_from_locmain(self, branch):
        base = ['git', 'pull', '--ff-only']
        return self.call_with_fail_count(
            'Pulling locmain to {0} failed with code {{code}}'.format(branch),
            base + [self.locmain, branch],
            cwd=self.ws_to_path(branch))

    def pull_from_branch(self, branch):
        base = ['git', 'pull', '--ff-only']
        return self.call_with_fail_count(
            'Pulling {0} to locmain failed with code {{code}}'.format(branch),
            base + [self.ws_to_path(branch), branch])

    def push_to_locmain(self, branch):
        base = ['git', 'push']
        if self.force:
            self.logger.info('Using --force for pushing from %s', branch)
            base += ['--force']
        return self.call_with_fail_count(
            'Pushing {0} to locmain failed with code {{code}}'.format(branch),
            base + [self.locmain, branch],
            cwd=self.ws_to_path(branch))


task = SyncTask
