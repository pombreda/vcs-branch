from .core import RootApp, TaskRunnerApp


class InitializeApp(TaskRunnerApp):

    command = 'init'


class CheckoutApp(TaskRunnerApp):

    command = 'checkout'

    def add_arguments(self, parser):
        parser.add_argument('branch')
        parser.add_argument(
            '--existing', '-e', action='store_true', help="""
            Use existing BRANCH instead of creating the new one.
            """)
        parser.add_argument(
            '--fg', help="""
            Run ``git remote add -f ...`` at foreground after
            ``git clone ...`` is finished.  Otherwise, these are done
            at background in parallel.
            """)


class MergeApp(TaskRunnerApp):

    command = 'merge'

    def add_arguments(self, parser):
        parser.add_argument(
            'workspaces', metavar='workspace', nargs='+')


class DeleteApp(TaskRunnerApp):

    command = 'delete'

    def add_arguments(self, parser):
        parser.add_argument('branch')


class VBApp(RootApp):

    subappclasses = [InitializeApp, CheckoutApp, MergeApp, DeleteApp]

    def __init__(self):
        self.subapps = [c() for c in self.subappclasses]
        self._command_app_map = dict((c.command, c) for c in self.subapps)

    def add_arguments(self, parser):
        super(VBApp, self).add_arguments(parser)
        subparsers = parser.add_subparsers()
        for subapp in self.subapps:
            subp = subparsers.add_parser(subapp.command)
            subp.set_defaults(command=subapp.command)
            subapp.add_arguments(subp)

    def do_run(self, command, **kwds):
        kwds = super(VBApp, self).do_run(**kwds)
        self.current_app = self._command_app_map[command]
        return self.current_app.do_run(**kwds)
