from nhl_api import NhlApi
from requests import exceptions
import unittest
from unittest.mock import patch, MagicMock
import responses
import json


class TestNhlApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nhl_api = NhlApi()

    @patch('requests.get')
    def test_get_game_get_request_http_error(self, mock_get):
        game_id = 'imaginary_game'
        mock_get.side_effect = exceptions.HTTPError
        actual_result = self.nhl_api.get_game(game_id)
        self.assertEqual("Encountered HTTPError", actual_result)

    @patch('requests.get')
    def test_get_game_get_request_not_found(self, mock_get):
        game_id = '2022029999'
        mock_get.return_value.status_code = 404
        actual_result = self.nhl_api.get_game(game_id)
        self.assertEqual(game_id, actual_result)
        mock_get.assert_called_once_with(self.nhl_api.base_url+'game/'+game_id+'/feed/live')

    @patch('requests.get')
    def test_get_game_get_request_good_request(self, mock_get):
        game_id = '2022020777'
        mock_response = MagicMock()
        mock_response.status_code = 200
        expected = {'gameId': game_id, 'somekey': 'somevalue'}
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response
        actual_result = self.nhl_api.get_game(game_id)
        self.assertEqual(expected, actual_result)
        mock_get.assert_called_once_with(self.nhl_api.base_url+'game/'+game_id+'/feed/live')

    @responses.activate
    def test_get_game_get_request_good_request_responses(self):
        game_id = '2022020777'
        expected = {'gameId': game_id, 'somekey': 'somevalue'}
        responses.get(url=self.nhl_api.base_url+'game/'+game_id+'/feed/live', json=expected, status=200)
        self.assertEqual(self.nhl_api.get_game(game_id), expected)

    @patch('pandas.DataFrame.to_sql')
    def test_extract_game_teams_stats(self, mock_db):
        with open('testdata.json', 'r') as file:
            data = json.loads(file.read())
        game_id = data['gamePk']
        mock_db.return_value = "Successfully processed game_teams_stats for game {}".format(game_id)
        actual_result = self.nhl_api.extract_game_teams_stats(data)
        self.assertEqual("Successfully processed game_teams_stats for game {}".format(game_id), actual_result)
        self.assertEqual(mock_db.call_count, 2)
        mock_db.side_effect = Exception
        actual_result = self.nhl_api.extract_game_teams_stats(data)
        self.assertEqual(game_id, actual_result)

    @patch('pandas.DataFrame.to_sql')
    def test_extract_game_skater_stats(self, mock_db):
        with open('testdata.json', 'r') as file:
            data = json.loads(file.read())
        game_id = data['gamePk']
        mock_db.return_value = "Successfully processed game_skater_stats for game {}".format(game_id)
        actual_result = self.nhl_api.extract_game_skater_stats(data)
        self.assertEqual("Successfully processed game_skater_stats for game {}".format(game_id), actual_result)
        self.assertEqual(mock_db.call_count, 36)
        mock_db.side_effect = KeyError
        actual_result = self.nhl_api.extract_game_skater_stats(data)
        self.assertEqual("Successfully processed game_skater_stats for game {}".format(game_id), actual_result)
        mock_db.side_effect = Exception
        actual_result = self.nhl_api.extract_game_skater_stats(data)
        self.assertEqual(game_id, actual_result)

    @patch('nhl_api.NhlApi.get_game')
    @patch('nhl_api.NhlApi.extract_game_skater_stats')
    @patch('nhl_api.NhlApi.extract_game_teams_stats')
    def test_run_all_operations(self, mock_teams, mock_skaters, mock_game):
        game_id = '2022020777'
        mock_game.return_value = "test input"
        mock_teams.return_value = "something"
        mock_skaters.return_value = "something else"
        actual_result = self.nhl_api.run_all_operations(game_id)
        self.assertEqual("Successfully processed game {}".format(game_id), actual_result)
        mock_teams.assert_called_once_with("test input")
        mock_skaters.assert_called_once_with("test input")
        mock_game.assert_called_once_with(game_id)
        mock_teams.side_effect = Exception
        actual_result = self.nhl_api.run_all_operations(game_id)
        self.assertEqual(game_id, actual_result)
        mock_skaters.side_effect = Exception
        actual_result = self.nhl_api.run_all_operations(game_id)
        self.assertEqual(game_id, actual_result)

if __name__ == '__main__':
    unittest.main()
