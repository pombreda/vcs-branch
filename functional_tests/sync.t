Initialize Git repository

  $ git init
  Initialized empty Git repository in * (glob)
  $ touch README.txt
  $ git add .
  $ git commit --message 'First commit' > /dev/null


Prepare vb

  $ vb init
  $ vb checkout branch-a
  $ vb checkout branch-b


Test

  $ echo 'edit' > README.txt
  $ git commit --all --message 'Second commit' > /dev/null
  $ vb sync
  $ cd .vb/branch-a
  $ git log --all | grep 'Second commit' > /dev/null
  $ cd ..
