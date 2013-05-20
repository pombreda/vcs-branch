import os

from .base import BaseTask


class CheckoutTask(BaseTask):

    def run(self):
        super(CheckoutTask, self).run()
        if os.path.isdir(self.path):
            print("{0} already exists".format(self.path))
            return

        remotes = self.get_remotes()
        branches = self.get_branches()
        rmitem = branches.remote(self.branch)

        if self.existing:
            if self.branch not in branches:
                raise RuntimeError(
                    "Branch '{0}' does not exist".format(self.branch))
        else:
            self.call_at_main(['git', 'branch', self.branch])
        self.call_at_main(['git', 'clone', '.', self.path])
        self.call_at_clone(['git', 'checkout', self.branch])

        self.call_at_clone(['git', 'remote', 'rename', 'origin', self.locmain])

        try:
            remote = rmitem.remote
            url = remotes.pop(remote)
        except (AttributeError, KeyError):
            pass
        else:
            self.call_at_clone(['git', 'remote', 'add', '-f', remote, url])
            self.call_at_clone(['git', 'branch', '--set-upstream',
                                self.branch, rmitem.rbranch])

        commands = list(
            ['git', 'remote', 'add', '-f', remote, url]
            for (remote, url) in remotes.items())
        runner = self.run_commands_fg if self.fg else self.run_commands_bg
        runner(commands)

    def run_commands_bg(self, commands):
        with open(os.devnull, 'w') as devnull:
            outfile = devnull
            for args in commands:
                self.Popen(
                    args, cwd=self.path,
                    stdin=devnull, stdout=outfile, stderr=self.sp.PIPE)

    def run_commands_fg(self, commands):
        for args in commands:
            self.check_call(args, cwd=self.path)

    def call_at_main(self, *args, **kwds):
        self.check_call(*args, **kwds)

    def call_at_clone(self, *args, **kwds):
        self.check_call(*args, cwd=self.path, **kwds)


task = CheckoutTask
