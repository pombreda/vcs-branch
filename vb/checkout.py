import os
import collections

from .task import Launchable, BaseTask


def parse_git_remote_v(output):
    r"""
    Parse output of ``git remote -v``

    >>> list(parse_git_remote_v('''\
    ... origin\tgit://github.com/ipython/ipython.git (fetch)
    ... origin\tgit://github.com/ipython/ipython.git (push)
    ... tkf\tgit@github.com:tkf/ipython.git (fetch)
    ... tkf\tgit@github.com:tkf/ipython.git (push)
    ... '''))                               #doctest: +NORMALIZE_WHITESPACE
    [('origin', 'git://github.com/ipython/ipython.git', 'fetch'),
     ('origin', 'git://github.com/ipython/ipython.git', 'push'),
     ('tkf', 'git@github.com:tkf/ipython.git', 'fetch'),
     ('tkf', 'git@github.com:tkf/ipython.git', 'push')]

    """
    for line in output.splitlines():
        (remote, url, fop) = line.split()
        yield (remote, url, fop.strip('()'))


class GitBranches(Launchable):

    _Branch = collections.namedtuple(
        'Branch', ['mark', 'branch', 'rbranch', 'remote'])

    def current(self):
        for item in self.parsed:
            if item == '*':
                return item

    def remote(self, branch):
        for item in self.parsed:
            if item.branch == branch:
                return item

    def load(self):
        output = self.check_output(['git', 'branch', '-vv'])
        self.parsed = list(self._Branch(*i) for i in self.parse(output))
        return self

    @staticmethod
    def parse(output):
        r"""
        Parse output of ``git branch -vv``.

        >>> list(GitBranches.parse('''\
        ... * B1  d7cab8a [r1/b1] commit message
        ...   B2  17b657c [r2/b2] commit message
        ...   B3  203ff99 [r3/b3] commit message
        ... '''))                           #doctest: +NORMALIZE_WHITESPACE
        [('*', 'B1', 'r1/b1', 'r1'),
         ('',  'B2', 'r2/b2', 'r2'),
         ('',  'B3', 'r3/b3', 'r3')]

        """
        for line in output.splitlines():
            if line.startswith('*'):
                line = line.lstrip('*')
                mark = '*'
            else:
                mark = ''
            line = line.lstrip()
            str.split
            words = line.split(None, 4)
            (branch, sha) = words[:2]
            rbranch = remote = ''
            if len(words) > 2:
                w2 = words[2]
                if w2[0] == '[' and w2[-1] == ']':
                    rbranch = w2[1:-1]
                    if '/' in rbranch:
                        remote = rbranch.split('/', 1)[0]
            yield (mark, branch, rbranch, remote)

    def __contains__(self, item):
        return self.remote(item) is not None


class CheckoutTask(BaseTask):

    def get_remotes(self):
        output = self.check_output(['git', 'remote', '-v'])
        return dict((l[0], l[1]) for l in parse_git_remote_v(output))

    @staticmethod
    def get_branches():
        return GitBranches().load()

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
            rbranch = rmitem.rbranch
            url = remotes.pop(rbranch)
        except (AttributeError, KeyError):
            pass
        else:
            self.call_at_clone(['git', 'remote', 'add', '-f', rbranch, url])
            self.call(['git', 'branch', '--set-upstream',
                             self.branch, rmitem.rbranch],
                            cwd=self.path)

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
