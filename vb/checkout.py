import os
import subprocess


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


class CheckoutTask(object):

    def __init__(self, branch, locmain='locmain'):
        self.branch = branch
        self.path = os.path.join('.vb', branch)
        self.locmain = locmain

    def check_init(self):
        if not os.path.isdir('.vb'):
            raise RuntimeError('Not initialized')

    def run(self):
        self.check_init()
        if os.path.isdir(self.path):
            print("{0} already exists".format(self.path))
            return

        output = subprocess.check_output(['git', 'remote', '-v'])
        remotes = dict((l[0], l[1]) for l in parse_git_remote_v(output))

        self.call_at_main(['git', 'clone', '.', self.branch])
        self.call_at_clone(['git', 'checkout', self.branch])

        self.call_at_clone(['git', 'remote', 'rename', 'origin', self.locmain])
        for (remote, url) in remotes.items():
            self.call_at_clone(['git', 'remote', 'add', '-f', remote, url])
        # FIXME: use "git branch -vv" to find appropriate remote
        subprocess.call(['git', 'branch', '--set-upstream',
                         self.branch, 'origin/{0}'.format(self.branch)],
                        cwd=self.path)

    def call_at_main(self, *args, **kwds):
        subprocess.check_call(*args, **kwds)

    def call_at_clone(self, *args, **kwds):
        subprocess.check_call(*args, cwd=self.path, **kwds)
