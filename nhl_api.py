import requests
from requests.exceptions import HTTPError
import yaml
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine
import pandas as pd
import traceback


class NhlApi:

    def __init__(self):
        with open('config.yaml', 'r') as file:
            configs = yaml.safe_load(file)
        self.base_url = configs['base_api']
        self.user = configs['db_info'].get('user')
        self.pw = configs['db_info'].get('pw')
        self.db = configs['db_info'].get('db')
        self.db_engine = create_engine(url="mysql+pymysql://{user}:{pw}@localhost/{db}"
                                           .format(user=self.user, pw=self.pw,
                                                   db=self.db))

    def get_game(self, game_id):
        try:
            response = requests.get(self.base_url+'game/'+game_id+'/feed/live')
        except HTTPError:
            return "Encountered HTTPError"
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return game_id

    def extract_game_teams_stats(self, data):
        game_id = data['gamePk']
        away_team_id = data['gameData']['teams']['away']['id']
        home_team_id = data['gameData']['teams']['home']['id']
        away_keys_list = data['liveData']['boxscore']['teams']['away']['players'].keys()
        home_keys_list = data['liveData']['boxscore']['teams']['home']['players'].keys()
        winning_starter = data['liveData']['decisions']['winner']['id']
        if 'ID'+str(winning_starter) in away_keys_list:
            away_result = True
            home_result = False
        if 'ID'+str(winning_starter) in home_keys_list:
            home_result = True
            away_result = False
        settled_in = data['liveData']['linescore']['currentPeriodOrdinal']
        away_coach = data['liveData']['boxscore']['teams']['away']['coaches'][0]['person']['fullName']
        home_coach = data['liveData']['boxscore']['teams']['home']['coaches'][0]['person']['fullName']
        away_stats = data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']
        home_stats = data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']
        away_team_skater_stats = away_stats['goals'], away_stats['shots'], away_stats['hits'], away_stats['pim'], away_stats['powerPlayOpportunities'], away_stats['powerPlayGoals'], away_stats['faceOffWinPercentage'], away_stats['giveaways'], away_stats['takeaways'], away_stats['blocked']
        home_team_skater_stats = home_stats['goals'], home_stats['shots'], home_stats['hits'], home_stats['pim'], home_stats['powerPlayOpportunities'], home_stats['powerPlayGoals'], home_stats['faceOffWinPercentage'], home_stats['giveaways'], home_stats['takeaways'], home_stats['blocked']
        columns = ["game_id","team_id","HoA","won","settled_in","head_coach","goals","shots","hits","pim","powerPlayOpportunities","powerPlayGoals","faceOffWinPercentage","giveaways","takeaways","blocked"]
        away_values = [game_id, away_team_id, 'away', away_result, settled_in, away_coach, away_team_skater_stats[0], away_team_skater_stats[1], away_team_skater_stats[2], away_team_skater_stats[3], away_team_skater_stats[4], away_team_skater_stats[5], away_team_skater_stats[6], away_team_skater_stats[7], away_team_skater_stats[8], away_team_skater_stats[9]]
        home_values = [game_id, home_team_id, 'home', home_result, settled_in, home_coach, home_team_skater_stats[0], home_team_skater_stats[1], home_team_skater_stats[2], home_team_skater_stats[3], home_team_skater_stats[4], home_team_skater_stats[5], home_team_skater_stats[6], home_team_skater_stats[7], home_team_skater_stats[8], home_team_skater_stats[9]]
        away_df = pd.DataFrame([away_values], [0], columns)
        home_df = pd.DataFrame([home_values], [0], columns)
        try:
            away_df.to_sql('game_teams_stats_api', con=self.db_engine, if_exists='append', index=False)
            home_df.to_sql('game_teams_stats_api', con=self.db_engine, if_exists='append', index=False)
            return "Successfully processed game_teams_stats for game {}".format(game_id)
        except Exception:
            traceback.print_exc()
            return game_id

    def extract_game_skater_stats(self, data):
        game_id = data['gamePk']
        away_team_id = data['gameData']['teams']['away']['id']
        home_team_id = data['gameData']['teams']['home']['id']
        columns = ["game_id","player_id","name","team_id","timeOnIce","assists","goals","shots","hits","powerPlayGoals","powerPlayAssists","penaltyMinutes","faceOffWins","faceoffTaken","takeaways","giveaways","shortHandedGoals","shortHandedAssists","blocked","plusMinus","evenTimeOnIce","shortHandedTimeOnIce","powerPlayTimeOnIce"]
        away_keys_list = data['liveData']['boxscore']['teams']['away']['players'].keys()
        home_keys_list = data['liveData']['boxscore']['teams']['home']['players'].keys()
        for player_id in away_keys_list:
            try:
                agss = data['liveData']['boxscore']['teams']['away']['players'][player_id]['stats']['skaterStats']
                name = data['liveData']['boxscore']['teams']['away']['players'][player_id]['person']['fullName']
                away_values = [game_id, player_id[2:], name, away_team_id, agss.get('timeOnIce'), agss.get('assists'), agss.get('goals'), agss.get('shots'), agss.get('hits'), agss.get('powerPlayGoals'), agss.get('powerPlayAssists'), agss.get('penaltyMinutes'), agss.get('faceOffWins'), agss.get('faceoffTaken'), agss.get('takeaways'), agss.get('giveaways'), agss.get('shortHandedGoals'), agss.get('shortHandedAssists'), agss.get('blocked'), agss.get('plusMinus'), str(agss.get('evenTimeOnIce')), str(agss.get('powerPlayTimeOnIce')), str(agss.get('shortHandedTimeOnIce'))]
                away_values[4], away_values[20], away_values[21], away_values[22] = self.convert_string_time_seconds(away_values[4]), self.convert_string_time_seconds(away_values[20]), self.convert_string_time_seconds(away_values[21]), self.convert_string_time_seconds(away_values[22])
                away_df = pd.DataFrame([away_values], [0], columns)
                away_df.to_sql('game_skater_stats_api', con=self.db_engine, if_exists='append', index=False)
            except KeyError:
                pass
            except Exception:
                traceback.print_exc()
                return game_id
        for player_id in home_keys_list:
            try:
                hgss = data['liveData']['boxscore']['teams']['home']['players'][player_id]['stats']['skaterStats']
                name = data['liveData']['boxscore']['teams']['home']['players'][player_id]['person']['fullName']
                home_values = [game_id, player_id[2:], name, home_team_id, hgss.get('timeOnIce'), hgss.get('assists'), hgss.get('goals'), hgss.get('shots'), hgss.get('hits'), hgss.get('powerPlayGoals'), hgss.get('powerPlayAssists'), hgss.get('penaltyMinutes'), hgss.get('faceOffWins'), hgss.get('faceoffTaken'), hgss.get('takeaways'), hgss.get('giveaways'), hgss.get('shortHandedGoals'), hgss.get('shortHandedAssists'), hgss.get('blocked'), hgss.get('plusMinus'), hgss.get('evenTimeOnIce'), hgss.get('powerPlayTimeOnIce'), hgss.get('shortHandedTimeOnIce')]
                home_values[4], home_values[20], home_values[21], home_values[22] = self.convert_string_time_seconds(home_values[4]), self.convert_string_time_seconds(home_values[20]), self.convert_string_time_seconds(home_values[21]), self.convert_string_time_seconds(home_values[22])
                home_df = pd.DataFrame([home_values], [0], columns)
                home_df.to_sql('game_skater_stats_api', con=self.db_engine, if_exists='append', index=False)
            except KeyError:
                pass
            except Exception:
                return game_id
        return "Successfully processed game_skater_stats for game {}".format(game_id)

    def extract_game_table(self, data):
        game_id = data['gamePk']
        away_team_id = data['gameData']['teams']['away']['id']
        home_team_id = data['gameData']['teams']['home']['id']
        date = data['gameData']['datetime']['dateTime'][0:10]
        away_goals = data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']
        home_goals = data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']
        winner = 'home' if home_goals > away_goals else 'away'
        columns = ['game_id', 'home_id', 'away_id', 'game_date', 'winner', 'away_goals', 'home_goals']
        values = [game_id, home_team_id, away_team_id, date, winner, away_goals, home_goals]
        try:
            game_df = pd.DataFrame([values], [0], columns)
            game_df.to_sql('game_api', con=self.db_engine, if_exists='append', index=False)
        except Exception:
            return game_id

    def extract_game_goalie_stats(self, data):
        game_id = data['gamePk']
        away_team_id = data['gameData']['teams']['away']['id']
        home_team_id = data['gameData']['teams']['home']['id']
        columns = ["game_id","name","player_id","team_id","timeOnIce","assists","goals","pim","shots","saves","powerPlaySaves","shortHandedSaves","evenSaves","shortHandedShotsAgainst","evenShotsAgainst","powerPlayShotsAgainst","decision","savePercentage"]
        away_keys_list = data['liveData']['boxscore']['teams']['away']['players'].keys()
        home_keys_list = data['liveData']['boxscore']['teams']['home']['players'].keys()
        for player_id in away_keys_list:
            try:
                aggs = data['liveData']['boxscore']['teams']['away']['players'][player_id]['stats']['goalieStats']
                name = data['liveData']['boxscore']['teams']['away']['players'][player_id]['person']['fullName']
                away_stats = [game_id, name, player_id[2:], away_team_id, self.convert_string_time_seconds(aggs.get('timeOnIce')), aggs.get('assists'), aggs.get('goals'), aggs.get('pim'), aggs.get('shots'), aggs.get('saves'), aggs.get('powerPlaySaves'), aggs.get('shortHandedSaves'), aggs.get('evenSaves'), aggs.get('shortHandedShotsAgainst'), aggs.get('evenShotsAgainst'), aggs.get('powerPlayShotsAgainst'), aggs.get('decision'), aggs.get('savePercentage')]
                away_df = pd.DataFrame([away_stats], [0], columns)
                away_df.to_sql('game_goalie_stats_api', con=self.db_engine, if_exists='append', index=False)
            except KeyError:
                pass
            except Exception as e:
                traceback.print_exc()
                return game_id
        for player_id in home_keys_list:
            try:
                hggs = data['liveData']['boxscore']['teams']['home']['players'][player_id]['stats']['goalieStats']
                name = data['liveData']['boxscore']['teams']['home']['players'][player_id]['person']['fullName']
                home_stats = [game_id, name, player_id[2:], home_team_id, self.convert_string_time_seconds(hggs.get('timeOnIce')), hggs.get('assists'), hggs.get('goals'), hggs.get('pim'), hggs.get('shots'), hggs.get('saves'), hggs.get('powerPlaySaves'), hggs.get('shortHandedSaves'), hggs.get('evenSaves'), hggs.get('shortHandedShotsAgainst'), hggs.get('evenShotsAgainst'), hggs.get('powerPlayShotsAgainst'), hggs.get('decision'), hggs.get('savePercentage')]
                home_df = pd.DataFrame([home_stats], [0], columns)
                home_df.to_sql('game_goalie_stats_api', con=self.db_engine, if_exists='append', index=False)
            except KeyError:
                pass
            except Exception as e:
                traceback.print_exc()
                return game_id


    def run_all_operations(self, game_id):
        try:
            # data = self.get_game(game_id)
            # self.extract_game_teams_stats(data)
            # self.extract_game_skater_stats(data)
            # self.extract_game_table(data)
            # self.extract_game_goalie_stats(data)
            print("Successfully processed game {}".format(game_id))
            return "Successfully processed game {}".format(game_id)
        except Exception:
            print("EXCEPTION IN GAME {}".format(game_id))
            return game_id

    def insert_json(self, game_id):
        try:
            df = pd.read_json(self.base_url+'game/'+game_id+'/feed/live')
            df = df.applymap(str)
            print(df.columns.values)
            df.to_sql('game_json', con=self.db_engine, if_exists='append', index=False)
            print("Successfully processed game {}".format(game_id))
        except Exception:
            traceback.print_exc()
            print("EXCEPTION IN GAME {}".format(game_id))


    def convert_string_time_seconds(self, time):
        time_seconds = 0
        time_seconds += int(time.split(':')[0]) * 60
        time_seconds += int(time.split(':')[1])
        return time_seconds

    def process_season(self):
        season_code = '202202'
        num_games = 1312
        with ThreadPoolExecutor() as ex:
            futures = [ex.submit(self.run_all_operations, season_code + "{:04d}".format(game_id)) for game_id in range(1, num_games+1)]
        return futures
