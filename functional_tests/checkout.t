Initialize Git repository and VB for test::

  $ git init
  Initialized empty Git repository in * (glob)
  $ touch README.txt
  $ git add .
  $ git commit --message 'First commit' > /dev/null
  $ vb init

``vb checkout`` creates a branch and make a clone repository to work
with it.  Working copy of the root repository is not changed.
``vb checkout`` takes argument like ``git branch``::

  $ vb checkout branch-a
  $ git branch
    branch-a
  * master
  $ cd .vb/branch-a
  $ git branch
  * branch-a
    master
  $ git remote
  locmain
  $ cd ../..

Branch to be based on is default to the currently checked out one.
But it can be specified::

  $ echo 'edit' > README.txt
  $ git commit --all --message 'Second commit' > /dev/null
  $ vb checkout branch-b --based-on branch-a
  $ git branch
    branch-a
    branch-b
  * master
  $ git log --format=oneline
  * Second commit* (glob)
  * First commit* (glob)
  $ cd .vb/branch-b
  $ git branch
  * branch-b
    master
  $ git log --format=oneline
  * First commit* (glob)
  $ cd ../..

Existing branch can be used.  In that case, repository is just checked
out in ``.vb/BRANCH``::

  $ git branch branch-c
  $ vb checkout --existing branch-c
  $ cd .vb/branch-c
  $ git branch
  * branch-c
    master
  $ cd ../..

Passing ``--existing`` for non-existing branch fails::

  $ vb checkout --existing non-existing-branch
  Branch 'non-existing-branch' does not exist
  [1]

If repository at ``.vb/BRANCH`` already exist, it does not do anything::

  $ vb checkout branch-a
  .vb/branch-a already exists
  $ vb checkout --existing branch-c
  .vb/branch-c already exists
