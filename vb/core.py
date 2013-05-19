import argparse


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
