import pandas as pd
import yaml
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine


class CsvToDb:

    def __init__(self):
        with open('config.yaml', 'r') as file:
            configs = yaml.safe_load(file)
        self.files_list = configs['csv_file_names']
        self.user = configs['db_info'].get('user')
        self.pw = configs['db_info'].get('pw')
        self.db = configs['db_info'].get('db')
        self.db_engine = create_engine(url="mysql+pymysql://{user}:{pw}@localhost/{db}"
                                           .format(user=self.user, pw=self.pw,
                                                   db=self.db))

    @staticmethod
    def read_csv_generator(file_name):
        try:
            for chunk in pd.read_csv(file_name, chunksize=100000):
                yield chunk
        except IOError:
            return 'Encountered an IOError'

    def process_chunk(self, chunk, table_name):
        try:
            chunk.to_sql(table_name, con=self.db_engine, if_exists='append', index=False)
            return 'chunk of {} successfully processed'.format(table_name)
        except Exception:
            return "Failed to write chunk to database"

    def process_all_files(self):
        with ThreadPoolExecutor() as ex:
            many_futures = []
            for file_name in self.files_list:
                futures = [ex.submit(self.process_chunk, chunk, file_name.split('.')[0])
                           for chunk in self.read_csv_generator('RawData/{}'.format(file_name))]
                many_futures.append(futures)
            return many_futures


