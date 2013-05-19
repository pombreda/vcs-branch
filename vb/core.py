import logging
import argparse

_unspecified = object()

_logger = None
LOG_LEVEL_NAMES = [
    'FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'NOTSET']


def get_logger():
    global _logger
    if _logger is None:
        hndlr = logging.StreamHandler()
        hndlr.setLevel(0)

        formatter = logging.Formatter("%(levelname)s %(message)s")
        hndlr.setFormatter(formatter)

        _logger = logging.getLogger('vb')
        _logger.addHandler(hndlr)
    return _logger


class BaseApplication(object):

    def add_arguments(self, parser):
        pass

    def get_parser(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=self.__doc__)
        self.add_arguments(parser)
        return parser

    def parse_args(self, args=None):
        parser = self.get_parser()
        return vars(parser.parse_args(args))

    def run(self):
        self.do_run(**self.parse_args())

    def do_run(self, **kwds):
        return kwds


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

    def do_run(self, log_level, verbose, **kwds):
        if log_level is _unspecified:
            if verbose:
                log_level = {1: 'INFO', 2: 'DEBUG'}.get(verbose, 0)
            else:
                log_level = 'WARN'
        logger = get_logger()
        logger.setLevel(log_level)
        return super(RootApp, self).do_run(**kwds)


class TaskRunnerApp(BaseApplication):

    @property
    def command(self):
        raise NotImplementedError

    @property
    def taskclass(self):
        return 'vb.{0}.task'.format(self.command)

    def get_taskclass(self):
        from .utils import import_item
        return import_item(self.taskclass)

    def do_run(self, **kwds):
        taskclass = self.get_taskclass()
        self.task = taskclass(**kwds)
        self.task.run()
