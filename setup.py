from distutils.core import setup

import vb

setup(
    name='vb',
    version=vb.__version__,
    packages=['vb', 'vb.tasks'],
    author=vb.__author__,
    author_email='aka.tkf@gmail.com',
    url='https://github.com/tkf/vcs-branch',
    license=vb.__license__,
    description='VB - VCS branching utility',
    long_description=vb.__doc__,
    keywords='VCS, Git, branch, CLI',
    classifiers=[
        "Development Status :: 3 - Alpha",
        # see: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': ['vb = vb.cli:main'],
    },
)
