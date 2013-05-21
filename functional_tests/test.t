Test that test environment is setup as expected.

  $ git config user.name
  Test
  $ git config user.email
  test@mail.com


This user setting must be used when committing etc.

  $ git init
  Initialized empty Git repository in * (glob)
  $ echo 'edit' > README.txt
  $ git add .
  $ git commit --message 'First commit' > /dev/null
  $ git log --format=short
  commit * (glob)
  Author: Test <test@mail.com>
  
      First commit
