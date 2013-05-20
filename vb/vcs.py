import collections

from .core import Launchable


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
            if item.mark == '*':
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
        ...   B2  17b657c [r2/b2: ahead 1] commit message
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
            words = line.split(None, 4)
            (branch, sha) = words[:2]
            rbranch = remote = ''
            if len(words) > 2:
                w2 = words[2]
                if w2[0] == '[':
                    rbranch = w2[1:].rstrip(':]')
                    if '/' in rbranch:
                        remote = rbranch.split('/', 1)[0]
            yield (mark, branch, rbranch, remote)

    def __contains__(self, item):
        return self.remote(item) is not None
