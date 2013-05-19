import logging
import argparse

_logger = None
LOG_LEVEL_NAMES = [
    'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET']


def get_logger():
    global _logger
    if _logger is None:
        hndlr = logging.StreamHandler()
        hndlr.setLevel(0)

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

    def do_run(self, **_):
        pass


class RootApp(BaseApplication):

    def add_arguments(self, parser):
        parser.add_argument(
            '--log-level', default='INFO', choices=LOG_LEVEL_NAMES)

    def do_run(self, log_level, **kwds):
        level = getattr(logging, log_level.upper(), log_level)
        logger = get_logger(level)
        logger.setLevel()
        super(RootApp, self).do_run(**kwds)


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
