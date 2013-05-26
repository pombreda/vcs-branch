=======
 Merge
=======

Initialize Git repository and VB for test::

  $ git init
  Initialized empty Git repository in * (glob)
  $ touch README.txt
  $ git add .
  $ git commit --message 'First commit' > /dev/null
  $ vb init
  $ git branch first  # for later use

Do some edit at branch-a::

  $ vb checkout branch-a
  $ cd .vb/branch-a
  $ echo 'edit (a)' > file-a.txt
  $ git add .
  $ git commit --message 'Second commit' > /dev/null
  $ cd ../..

Do some edit at branch-b, also::

  $ vb checkout branch-b
  $ cd .vb/branch-b
  $ echo 'edit (b)' > file-b.txt
  $ git add .
  $ git commit --message 'Different second commit' > /dev/null
  $ cd ../..

Merging two branches::

  $ vb merge branch-a branch-b
  $ cat file-*.txt
  edit (a)
  edit (b)

Let's do some edit at branch-a::

  $ cd .vb/branch-a
  $ echo 'changed (a)' > file-a.txt
  $ git commit --all --message 'Third commit' > /dev/null
  $ cd ../..

... and then merge again::

  $ vb merge branch-a branch-b
  $ cat file-*.txt
  changed (a)
  edit (b)

At this point, you have commit tree like this::

  $ git log --graph  --pretty='format:%s%d'
  *   Merge branches 'branch-a' and 'branch-b' (HEAD, master)
  |\  
  | * Third commit (branch-a)
  * |   Merge branches 'branch-a' and 'branch-b'
  |\ \  
  | |/  
  |/|   
  | * Different second commit (branch-b)
  * | Second commit
  |/  
  * First commit (first) (no-eol)

Running ``vb merge`` again and again could make the branch full of merge
commits.  To avoid that, you can run ``vb merge --reset REFSPEC`` to
reset the branch to the point specified by ``REFSPEC``::

  $ vb merge --reset first branch-a branch-b
  $ git log --graph  --pretty='format:%s%d'
  *   Merge branches 'branch-a' and 'branch-b' (HEAD, master)
  |\  
  | * Different second commit (branch-b)
  * | Third commit (branch-a)
  * | Second commit
  |/  
  * First commit (first) (no-eol)

If ``vb merge --reset`` creates different result comparing to simple
``vb merge``, the branch created by ``vb merge`` locates at ``BRANCH.old``
so that you can examine it before completely removing it::

  $ echo 'change' > README.txt
  $ git commit --all --message 'Forth commit' > /dev/null
  $ vb merge --reset first branch-a branch-b
  WARNING Re-merging produces different result.
  Check: git diff master.old
  $ git diff master.old
  diff --git a/README.txt b/README.txt
  index * (glob)
  --- a/README.txt
  +++ b/README.txt
  @@ -1 +0,0 @@
  -change
