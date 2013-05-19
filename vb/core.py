import argparse


class BaseApplication(object):

    def add_arguments(self, parser):
        raise NotImplementedError

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
