Git does not let you to commit unless user.name and user.email are set.
Let's check that they are correctly set and commit works.  These values are
set in ``../tox.ini`` using ``$GIT_AUTHOR_NAME`` and ``$GIT_AUTHOR_EMAIL``.

  $ git init
  Initialized empty Git repository in * (glob)
  $ echo 'edit' > README.txt
  $ git add .
  $ git commit --message 'First commit' > /dev/null
  $ git log --format=short
  commit * (glob)
  Author: Test <test@mail.com>
  
      First commit
