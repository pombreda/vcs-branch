import os
import logging
import argparse

_unspecified = object()

_logger = None
LOG_LEVEL_NAMES = [
    'FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'NOTSET']


def get_logger():
    return _logger


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
        self.logger.setLevel(logging.NOTSET)
        self.set_log_stderr_handler()
        self.set_log_file_handler()

        global _logger
        _logger = self.logger

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
            self.logfilehandler.setLevel(0)
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

    def do_run(self, **kwds):
        taskclass = self.get_taskclass()
        self.task = taskclass(**kwds)
        self.task.run()
