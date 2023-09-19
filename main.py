from csv_to_db import CsvToDb
from nhl_api import NhlApi
import json


def main():
    # csv_to_db = CsvToDb()
    # csv_to_db.process_all_files()
    nhl_api = NhlApi()
    # nhl_api.process_season()
    data = nhl_api.get_game('2022020110')
    my_json = (json.dumps(data, indent=4))
    with open('testdata.json', 'w') as file:
        file.write(my_json)


if __name__ == '__main__':
    main()


