import unittest
from unittest.mock import patch, MagicMock
from csv_to_db import CsvToDb
import pandas as pd


class TestCsvToDb(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.csv_to_db = CsvToDb()

    @patch('pandas.read_csv')
    def test_read_csv_generator_mock_read(self, mock_read):
        filename = 'valid.csv'
        for chunk in self.csv_to_db.read_csv_generator(filename, 100000):
            pass
        mock_read.assert_called_once_with(filename, chunksize=100000)
        self.assertRaises(Exception, self.csv_to_db.read_csv_generator('invalid.txt', 1))

    @patch('pandas.DataFrame.to_sql')
    def test_process_chunk(self, mock_db):
        chunk = pd.DataFrame([{'one: 1'}, {'two': 2}])
        mock_db.return_value = 'chunk of some_table successfully processed'
        actual_result = self.csv_to_db.process_chunk(chunk, 'some_table')
        self.assertEqual('chunk of some_table successfully processed', actual_result)
        mock_db.assert_called_once()
        mock_db.side_effect = Exception
        actual_result = self.csv_to_db.process_chunk(chunk, 'some_table')
        self.assertEqual("Failed to write chunk to database", actual_result)


if __name__ == '__main__':
    unittest.main()
