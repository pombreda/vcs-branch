  $ vb
  usage: vb \[-h\] \[--log-level .*\] \[--verbose\] (re)
            {init,checkout,merge,delete,sync} ...
  vb: error: too few arguments
  [2]


Initialization

  $ vb init
  $ test -d .vb/.var


Create non-empty Git repository for test

  $ git init
  Initialized empty Git repository in * (glob)
  $ touch README.txt
  $ git add .
  $ git commit --message 'First commit' > /dev/null


Checkout

  $ vb checkout branch-a
  $ ls .vb
  branch-a
