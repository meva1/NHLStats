import unittest
import test_nhl_api
import test_csv_to_db

loader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTests(loader.loadTestsFromModule(test_nhl_api))
suite.addTests(loader.loadTestsFromModule(test_csv_to_db))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
