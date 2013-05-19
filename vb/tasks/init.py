from . import utils


class InitializeTask(object):

    def run(self):
        utils.make_dir_if_not_exist('.vb')


task = InitializeTask
