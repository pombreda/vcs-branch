import os


def make_dir_if_not_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def quote_command(command):
    """
    Quote command

    >>> quote_command(['cat', 'file name with space.txt'])
    "cat 'file name with space.txt'"

    :type command: [str]

    """
    return ' '.join(repr(c) if ' ' in c else c for c in command)


def import_item(name):
    """
    Import and return `bar` given the string ``'foo.bar'``.

    >>> import_item('os.path.join')                    # doctest: +ELLIPSIS
    <function join at 0x...>
    >>> import_item('datetime')                        # doctest: +ELLIPSIS
    <module 'datetime' from '...'>

    Copied from: IPython/utils/importstring.py

    """
    package = '.'.join(name.split('.')[0:-1])
    obj = name.split('.')[-1]

    if package:
        module = __import__(package, fromlist=[obj])
        try:
            pak = module.__dict__[obj]
        except KeyError:
            raise ImportError('No module named %s' % obj)
        return pak
    else:
        return __import__(obj)
