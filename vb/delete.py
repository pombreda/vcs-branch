import os
import shutil

from .task import BaseTask


class DeleteTask(BaseTask):

    def run(self):
        super(DeleteTask, self).run()

        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        else:
            self.logger.warn(
                '{0} does not exist.  ignoring...'.format(self.path))

        self.check_call(['git', 'branch', '-d', self.branch])


task = DeleteTask
