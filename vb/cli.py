from .core import RootApp, TaskRunnerApp


class InitializeApp(TaskRunnerApp):

    """
    Create ``.vb`` directory.
    """

    command = 'init'


class CheckoutApp(TaskRunnerApp):

    """
    Create branch and working copy at ``.vb/BRANCH``.
    """

    command = 'checkout'

    def add_arguments(self, parser):
        parser.add_argument('branch')
        parser.add_argument(
            '--existing', '-e', action='store_true', help="""
            Use existing BRANCH instead of creating the new one.
            """)
        parser.add_argument(
            '--fg', action='store_true', help="""
            Run ``git remote add -f ...`` at foreground after
            ``git clone ...`` is finished.  Otherwise, these are done
            at background in parallel.
            """)


class MergeApp(TaskRunnerApp):

    """
    Merge branch(es) to the root repository.
    """

    command = 'merge'

    def add_arguments(self, parser):
        parser.add_argument(
            'workspaces', metavar='workspace', nargs='+')


class DeleteApp(TaskRunnerApp):

    """
    Delete branch and corresponding working directory.
    """

    command = 'delete'

    def add_arguments(self, parser):
        parser.add_argument('branch')


class SyncApp(TaskRunnerApp):

    """
    Synchronize git DB in root and branches.

    1. Run ``git fetch LOCMAIN`` in specified BRANCHes
    2. Run ``git push LOCMAIN BRANCH`` [#]_
    3. Run ``git relink`` to save disk consumption

    .. [#]  If currently checked out branch at LOCMAIN is BRANCH, then
            ``git pull --ff`` is used instead.

    """

    command = 'sync'

    def add_arguments(self, parser):
        parser.add_argument('workspaces', metavar='workspace', nargs='*')
        parser.add_argument(
            '--fg', action='store_true', help="""
            Run ``git relink ...`` at foreground after ``git fetch LOCMAIN``
            is finished.  Otherwise, these are done at background in parallel.
            """)
        parser.add_argument(
            '--force', '-f', action='store_true', help="""
            Do force push for `.vb/BRANCH`-to-`LOCMAIN` synchronization.
            When this option is specified, branch in LOCMAIN is discarded.
            """)


class VBApp(RootApp):

    subappclasses = [InitializeApp, CheckoutApp, MergeApp, DeleteApp, SyncApp]

    def __init__(self):
        self.subapps = [c() for c in self.subappclasses]
        self._command_app_map = dict((c.command, c) for c in self.subapps)

    def add_arguments(self, parser):
        import argparse
        super(VBApp, self).add_arguments(parser)
        subparsers = parser.add_subparsers()
        for subapp in self.subapps:
            subp = subparsers.add_parser(
                subapp.command,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                help=subapp.get_short_help(),
                description=subapp.get_description())
            subp.set_defaults(command=subapp.command)
            subapp.add_arguments(subp)

    def do_run(self, command, **kwds):
        kwds = super(VBApp, self).do_run(**kwds)
        self.current_app = self._command_app_map[command]
        return self.current_app.do_run(self.logger, **kwds)
