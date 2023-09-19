import unittest
import test_nhl_api

loader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTests(loader.loadTestsFromModule(test_nhl_api))

runner = unittest.TextTestRunner(verbosity=4)
result = runner.run(suite)
