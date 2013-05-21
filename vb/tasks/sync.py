from .base import MultiBranchTask


class SyncTask(MultiBranchTask):

    def run(self):
        if not self.workspaces:
            self.workspaces = self.get_all_workspaces()
            if not self.workspaces:
                self.logger.warn('No workspace exists.')
                return
            self.logger.info(
                'No workspace is specified.  Running for all %s workspace(s)',
                len(self.workspaces))
        branches = self.get_branches()
        current = branches.current()

        self.failures = 0
        for br in self.get_branch_names():

            if current.branch != br:
                self.logger.info(
                    'Sync ({0}): locmain -> {1}'.format(current.branch, br))
                self.fetch_from_locmain(current.branch, br)

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
            self.fail('{0} failure(s) during sync'.format(self.failures))

    def call_with_fail_count(self, msgfmt, command, *args, **kwds):
        act = '{0}ing'.format(command[0].title())  # Pulling/Pushing/Fetching
        returncode = self.call(command, *args, show_failed_stdout=True, **kwds)
        if returncode != 0:
            self.logger.warn(msgfmt.format(act=act, code=returncode))
            self.failures += 1
        return returncode

    @staticmethod
    def _msgfmt(frm, to):
        return '{{act}} {0} to {1} failed with code {{code}}'.format(frm, to)

    def fetch_from_locmain(self, branch, ws=None):
        return self.pull_from_locmain(branch, ws, ['fetch'])

    def pull_from_locmain(self, branch, ws=None, cmd=['pull', '--ff-only']):
        msgfmt = self._msgfmt('locmain', branch)
        command = ['git'] + cmd + [self.locmain, branch]
        cwd = self.ws_to_path(branch if ws is None else ws)
        return self.call_with_fail_count(msgfmt, command, cwd=cwd)

    def pull_from_branch(self, branch):
        msgfmt = self._msgfmt(branch, 'locmain')
        command = ['git', 'pull', '--ff-only', self.ws_to_path(branch), branch]
        return self.call_with_fail_count(msgfmt, command)

    def push_to_locmain(self, branch):
        if self.force:
            self.logger.info('Using --force for pushing from %s', branch)
            force = ['--force']
        else:
            force = []
        msgfmt = self._msgfmt(branch, 'locmain')
        command = ['git', 'push'] + force + [self.locmain, branch]
        cwd = self.ws_to_path(branch)
        return self.call_with_fail_count(msgfmt, command, cwd=cwd)


task = SyncTask
