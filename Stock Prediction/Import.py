import pandas as pd
import datetime
import csv
import tweepy
import string
from nltk.corpus import stopwords


class Import(object):
    def __init__(self, stock_name, start_date, end_date):
        self.stock_name = stock_name
        self.start_date = start_date
        self.end_date = end_date
        self.stock_data = []

    def stock_check(self):
        # Creates API URL, tries to import 10 prices between 2000 and current year
        full_stock_address = 'http://quotes.wsj.com/' +\
                             self.stock_name + \
                             '/historical-prices/download?num_rows=10&range_' \
                             'days=10&startDate=01/01/2000&endDate=' + datetime.datetime.today().strftime('%m-%d-%Y')
        # Try-except statement
        try:
            # Tries to import data, if URL is wrong, assume that user's input is incorrect
            stock_data = pd.read_csv(full_stock_address, encoding="utf-8")
            # Returns True if imported file is not empty (.empty by default returns False, hence "not"
            return not stock_data.empty
        # If URL is wrong or internet is down, return False
        except:
            return False

    def import_data(self):
        # Creates an API URL for data
        address = "http://quotes.wsj.com/" + \
                  self.stock_name + "/historical-prices/download?num_rows=10000" \
                  "&range_days=10000&startDate=" + self.start_date + \
                  "&endDate=" + self.end_date
        # Imports data
        stock_data = pd.read_csv(address, encoding="utf-8")
        # Drops the volume column, as it is not required
        stock_data.drop([' Volume'], axis=1, inplace=True)
        # Returns data
        return stock_data

    def import_tweets(self):
        consumer_key = 'cpb1Zvr97wbcb3SeUVmUtbCrM'
        consumer_secret = '2H2r7nwu5Etcw8zKgGEws4iPpHMXnVitigyNvK6fbLZss8OYYt'
        access_token = '1093225935678119936-NOBRzYTivsiDMl3OVCmu49K463MEIw'
        access_token_secret = 'bHfu9Qdb4A4lIKda9Uvz4wmSjN7HdErBTQcLnsP7jEDto'
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        # Clears the file
        f = open("tweets.csv", "w+")
        f.truncate()
        f.close()
        # Open/Create a file to append data
        csv_file = open('tweets.csv', 'a')
        # Use csv Writer
        csv_writer = csv.writer(csv_file)
        # Iterates through tweets, saves ones containing stock name and being created after the start date
        for tweet in tweepy.Cursor(api.search, q="#"+self.stock_name, count=1000,
                                   lang="en",
                                   since=
                                        datetime.datetime.strptime(self.start_date, '%m/%d/%Y')
                                        .strftime('%Y-%m-%d'))\
                                        .items():
            csv_writer.writerow([tweet.created_at, tweet.text.encode('utf-8')])

    def clean_tweets(self):
        # open the file as read only
        file = open("tweets.csv", 'r')
        # read all text
        text = file.read()
        # close the file
        file.close()
        # split into tokens by white space
        tokens = text.split()
        # remove punctuation from each token
        table = str.maketrans('', '', string.punctuation)
        tokens = [w.translate(table) for w in tokens]
        # remove remaining tokens that are not alphabetic
        tokens = [word for word in tokens if word.isalpha()]
        # filter out stop words
        stop_words = set(stopwords.words('english'))
        tokens = [w for w in tokens if not w in stop_words]
        # filter out short tokens
        tokens = [word for word in tokens if len(word) > 1]
        return tokens
