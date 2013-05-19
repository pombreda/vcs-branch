import subprocess

from .core import get_logger


def wrap_popen(func):
    def wrapper(self, command, *args, **kwds):
        self.logger.debug(
            'Calling {0}({1!r}, ...)'.format(func.__name__, command))
        return func(command, *args, **kwds)
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
