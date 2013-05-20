import os
import logging
import argparse
import subprocess

from . import utils

_unspecified = object()

LOG_LEVEL_NAMES = [
    'FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'NOTSET']


class BaseApplication(object):

    def add_arguments(self, parser):
        pass

    def get_description(self):
        import textwrap
        doc = self.__doc__
        if doc:
            return textwrap.dedent(doc)

    def get_short_help(self):
        for line in (self.__doc__ or '').splitlines():
            line = line.strip()
            if line:
                return line

    def get_parser(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=self.get_description())
        self.add_arguments(parser)
        return parser

    def parse_args(self, args=None):
        parser = self.get_parser()
        return vars(parser.parse_args(args))

    def run(self):
        try:
            self.do_run(**self.parse_args())
        finally:
            self.after_run()

    def do_run(self, **kwds):
        return kwds

    def after_run(self):
        pass


class RootApp(BaseApplication):

    def add_arguments(self, parser):
        parser.add_argument(
            '--log-level', default=_unspecified, choices=LOG_LEVEL_NAMES,
            help="Set logging level. (default: WARN)")
        parser.add_argument(
            '--verbose', '-v', action='count',
            help="""
            Alias for --log-level.  -v: INFO; -vv: DEBUG; -vvv: NOTSET
            """)

    logfilehandler = None
    logfile = None

    def set_logger(self):
        self.logger = logging.getLogger('vb')
        self.logger.setLevel(logging.DEBUG)
        self.set_log_stderr_handler()
        self.set_log_file_handler()

    def set_log_stderr_handler(self):
        self.logstderrhandler = hndlr = logging.StreamHandler()
        hndlr.setLevel(0)
        formatter = logging.Formatter("%(levelname)s %(message)s")
        hndlr.setFormatter(formatter)
        self.logger.addHandler(hndlr)

    def set_log_file_handler(self):
        vardir = os.path.join('.vb', '.var')
        if os.path.isdir(vardir):
            self.logfile = open(os.path.join(vardir, 'app.log'), 'w')
            formatter = logging.Formatter(logging.BASIC_FORMAT)
            self.logfilehandler = logging.StreamHandler(self.logfile)
            self.logfilehandler.setLevel(logging.DEBUG)
            self.logfilehandler.setFormatter(formatter)
            self.logger.addHandler(self.logfilehandler)

    def do_run(self, log_level, verbose, **kwds):
        if log_level is _unspecified:
            if verbose:
                log_level = {1: 'INFO', 2: 'DEBUG'}.get(verbose, 0)
            else:
                log_level = 'WARN'
        self.set_logger()
        self.logstderrhandler.setLevel(log_level)
        return super(RootApp, self).do_run(**kwds)

    def after_run(self):
        if self.logfile:
            self.logfile.close()


class TaskRunnerApp(BaseApplication):

    @property
    def command(self):
        raise NotImplementedError

    @property
    def taskclass(self):
        return 'vb.tasks.{0}.task'.format(self.command)

    def get_taskclass(self):
        from .utils import import_item
        return import_item(self.taskclass)

    def do_run(self, logger, **kwds):
        taskclass = self.get_taskclass()
        self.task = taskclass(logger, **kwds)
        self.task.run()


def wrap_popen(func, annotation=''):
    def wrapper(self, *args, **kwds):
        self.logger.debug(
            '{0}(*{1!r}, **{2!r})'.format(func.__name__, args, kwds))
        return func(*args, **kwds)
    return wrapper


class Launchable(object):

    def __init__(self, logger):
        self.logger = logger

    sp = subprocess
    _Popen = subprocess.Popen
    Popen = wrap_popen(subprocess.Popen)
    check_output = wrap_popen(subprocess.check_output)

    def call_bg(self, *args, **kwds):
        with open(os.devnull, 'w') as devnull:
            outfile = devnull
            return self.Popen(
                *args, stdin=devnull, stdout=outfile, stderr=self.sp.PIPE,
                **kwds)

    def _wrap_call(func):
        def wrapper(self, *args, **kwds):
            self.logger.debug('{0}(*{1!r}, **{2!r})'.format(name, args, kwds))
            return func(self, *args, **kwds)
        name = func.__name__
        return wrapper

    def _call(self, command, *args, **kwds):
        show_failed_stdout = kwds.pop('show_failed_stdout', False)
        proc = self._Popen(
            command, *args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            **kwds)
        (stdout, _) = proc.communicate()
        level = logging.DEBUG
        if show_failed_stdout and proc.returncode:
            level = logging.WARN
        self.logger.debug('code = %s', proc.returncode)
        self.logger.log(level, """Failed: %s
stdout:
%s""", utils.quote_command(command), stdout)
        return (proc, stdout)

    @_wrap_call
    def call(self, *args, **kwds):
        return self._call(*args, **kwds)[0].returncode

    @_wrap_call
    def check_call(self, cmd, *args, **kwds):
        (proc, stdout) = self._call(cmd, *args, **kwds)
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, cmd, stdout)
