import unittest


# This function starts all the unit tests (test*.py files) in parent folder
def start_tests():
    print('Application unit tests have started')
    loader = unittest.TestLoader()
    start_dir = '.'
    # Discovering all the test files in start directory
    suite = loader.discover(start_dir)

    # Setting up a detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
