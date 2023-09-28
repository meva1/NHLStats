from csv_to_db import CsvToDb
from nhl_api import NhlApi


def main():
    # csv_to_db = CsvToDb()
    # csv_to_db.process_all_files()
    nhl_api = NhlApi()
    # results = nhl_api.process_season()
    # for result in results:
    #     if result.result()[0:7] != "Success":
    #         print("Unable to process game {}".format(result.result()))
    nhl_api.insert_json('2022021012')


if __name__ == '__main__':
    main()


