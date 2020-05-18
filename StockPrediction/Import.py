import pandas as pd
import datetime
import csv
import tweepy
import string
from nltk.corpus import stopwords
import quandl


class Import(object):
    def __init__(self, stock_name, start_date, end_date):
        self.stock_name = stock_name
        self.start_date = start_date
        self.end_date = end_date
        self.stock_data = []
        quandl.ApiConfig.api_key = 'mNniGYUeXUex5kz3yQHE'

    def stock_check(self):
        try:
            data = quandl.get(f'EURONEXT/{self.stock_name}', start_date='2000-01-01', end_date=datetime.datetime.today().strftime('%Y-%m-%d'), limit=10)
            return True
        except quandl.NotFoundError:
            return False

    def import_data(self):
        # Imports data
        stock_data = quandl.get(f'EURONEXT/{self.stock_name}', start_date=self.start_date, end_date=self.end_date)
        stock_data = stock_data.drop(['Volume', 'Turnover'], axis=1, inplace=True)
        return stock_data
