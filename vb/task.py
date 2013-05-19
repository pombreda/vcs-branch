import subprocess

from .core import get_logger


def wrap_popen(func, annotation=''):
    def wrapper(self, *args, **kwds):
        self.logger.debug(
            '{0}(*{1!r}, **{2!r})'.format(func.__name__, args, kwds))
        return func(*args, **kwds)
    return wrapper


class Launchable(object):

    def __init__(self):
        self.logger = get_logger()

    sp = subprocess
    Popen = wrap_popen(subprocess.Popen)
    check_call = wrap_popen(subprocess.check_call)
    check_output = wrap_popen(subprocess.check_output)
    call = wrap_popen(subprocess.call)


class BaseTask(Launchable):

    def __init__(self, locmain='locmain', **kwds):
        super(BaseTask, self).__init__()

        self.locmain = locmain
        for (k, v) in kwds.items():
            setattr(self, k, v)
