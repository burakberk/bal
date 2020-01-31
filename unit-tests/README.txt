How to use:

  tests directory should be run as a package via python -m tests command.
  In order to execute scripts, they should be appended to given command with a dot.
  Example: python -m tests.test
  This would run test.py script.

  Why:

    This procedure allows python to import bal scripts, otherwise tests directory had
    to be an upper directory of bal directory.

Code Coverage:

	coverage run -m unittest unit-tests/test-transaction.py // python3

	or

	coverage run -m unittest unit-tests.test-transaction // python2.7

	...

	coverage report bal/transaction.py 

	// If you add the -m flag, you can see which lines are not being tested:

	coverage report -m bal/transaction.py 