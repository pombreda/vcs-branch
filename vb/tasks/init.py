import os

from .. import utils
from .base import BaseTask


class InitializeTask(BaseTask):

    def run(self):
        utils.make_dir_if_not_exist(os.path.join('.vb', '.var'))


task = InitializeTask
