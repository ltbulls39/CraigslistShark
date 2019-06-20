from craigslist import CraigslistResumes
from craigslist import CraigslistForSale
import numpy as np
import sqlite3
from sqlite3 import Error
import os


# TODO Note
# When starting a new query we might want to
# default to filtering out the data

class Shark:
    def __init__(self, query=None):
        prev = os.path.dirname(os.getcwd())
        db = os.path.join(prev, 'database', 'craigslist_results.db')
        self.conn = self.connect_db(db)
        if query is not None:
            self.craig = CraigslistForSale(site='sandiego', filters={'query' : query})

            # Fill db with queried items now

            self.sql_init(query)


    def close_db(self):
        '''
        Closes the connection to the DB
        :return:
        '''
        try:
            self.conn.close()
        except Error as e:
            print(e)


    def sql_init(self, query):
        '''
        Initializes all the sql functions to their initial state
        :return:
        '''
        result_set = self.get_query(limit=50)
        for result in result_set:
            self.insert_db(result, query)

        data = self.select_price_from_db()
        # print(data)
        outliers = self.filter_data(data)
        self.remove_filtered_from_db(outliers)


    def connect_db(self, db_file):
        '''
        Make a connection to our DB
        :param db_file:
        :return: conn object or None
        '''
        try:
            conn = sqlite3.connect(db_file)
            x = conn.execute('pragma journal_mode=wal')
            return conn
        except Error as e:
            print(e)

        return None

    def insert_db(self, item, query):
        '''
        Updates DB and inserts new items into it
        :param item: Item to be inserted
        :param query: User input, will be hashed into a query ID for distinction between queries
        :return:
        '''
        id = int(item['id'])
        name = item['name']
        url = item['url']
        time = item['datetime']
        price = int(item['price'][1:])
        q_id = str(hash(query))
        insert_stmt = 'INSERT or IGNORE INTO computers (id, name, url, time, price, query_id) ' \
                      'VALUES (?, ?, ?, ?, ?, ?)'
        entry = (id, name, url, time, price, q_id)

        try:
            c = self.conn.cursor()
            with self.conn:
                c.execute(insert_stmt, entry)
        except Error as e:
            print(e)

    def remove_filtered_from_db(self, outliers):
        '''
        Removes all outliers from the DB
        :param outliers:
        '''
        cur = self.conn.cursor()
        for item in outliers:
            cur.execute('DELETE FROM computers WHERE price = ?', item)

    def select_all_from_db(self):
        '''
        Fetches all items from db
        :param conn:
        :return: rows -> all rows from db
        '''
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM computers')

        rows = cur.fetchall()
        return rows

    def select_price_from_db(self):
        cur = self.conn.cursor()
        cur.execute('SELECT price FROM computers')

        rows = cur.fetchall()
        return rows

    def price_with_query(self, query):
        h = str(hash(query))
        cur = self.conn.cursor()
        cur.execute('SELECT price FROM computers WHERE query_id = ?', (query,))

        rows = cur.fetchall()
        return rows

    def select_by_hash_from_db(self, item):
        h = hash(item)
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM computers WHERE query_id = ?', (str(h),))

        rows = cur.fetchall()
        return rows


    def get_query(self, limit=0, year=None):
        '''
        Gets results back from web search
        :param limit:
        :param year:
        :return:
        '''
        results = []
        for result in self.craig.get_results(limit=limit):
            if year is not None:
                if year in result['name']:
                    results.append(result)
            else:
                results.append(result)
        return results

    def filter_data(self, data):
        '''
        Filters out values that are too low to be valid electronics
        :param data: list of data to filter
        :return outliers:
        '''
        # TODO Fix so it actually filters data with a better algorithm
        mean = np.mean(data)
        std = np.std(data)
        outliers = []

        for item in data:
            if item < (mean - std):
                outliers.append(item)

        return outliers