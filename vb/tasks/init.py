import os

from .. import utils


class InitializeTask(object):

    def run(self):
        utils.make_dir_if_not_exist(os.path.join('.vb', '.var'))


task = InitializeTask
