======
 Sync
======

Initialize Git repository::

  $ git init
  Initialized empty Git repository in * (glob)
  $ touch README.txt
  $ git add .
  $ git commit --message 'First commit' > /dev/null


Prepare vb::

  $ vb init
  $ vb checkout branch-a
  $ vb checkout branch-b


You can use `vb sync` to propagate changes in the root repository to
workspaces::

  $ echo 'edit' > README.txt
  $ git commit --all --message 'Second commit' > /dev/null
  $ vb sync
  $ git --git-dir .vb/branch-a/.git log --all | grep 'Second commit'
  * Second commit (glob)

This is like `git fetch`, so, `.git` in the workspaces are updated even
though it can't be fast-forwarded::

  $ git reset --hard HEAD^
  HEAD is now at * (glob)
  $ echo 'different edit' > README.txt
  $ git commit --all --message 'Second commit (redo)' > /dev/null
  $ vb sync
  $ git --git-dir .vb/branch-a/.git log --all | grep 'Second commit'
  * Second commit (redo) (glob)
