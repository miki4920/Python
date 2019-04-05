from sklearn.linear_model import LinearRegression
import datetime
import pandas
from nltk.stem.porter import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import numpy as np


class Prediction(object):
    def __init__(self, data, days):
        # Creates variables
        self.data = data
        self.days = days
        self.new_dataframe = pandas.DataFrame()
        # Stores date in a separate variable as prediction won't handle strings
        self.date = self.data.pop("Date")
        self.tweets = []

    def machine_learning_prediction(self):
        # Iterate through columns
        for column in self.data:
            # Make x a single column
            x = self.data.drop(column, 1)
            # Store rest of the columns in y
            y = self.data[column]
            # Create a linear regression class
            predictor = LinearRegression(n_jobs=-1)
            # Trains the predictor
            predictor.fit(x, y)
            # Predicts n days into future
            self.new_dataframe[column] = predictor.predict(x)[0:self.days+1]

    def date_generator(self):
        # Convert the first date to datetime object
        first_date = datetime.datetime.strptime(self.date[0], "%m/%d/%y")
        # Creates a list to store future dates
        future_date = []
        # Iterates through n days, creates a date in format mm/dd/yy for each date
        for day in range(self.days+1):
            future_date.append((first_date+datetime.timedelta(days=day)).strftime("%m/%d/%y"))
        # Creates a column called date, and fills it with created dates
        self.new_dataframe["Date"] = future_date

    def manage_dataframe(self):
        # Inverts the dataframe
        self.new_dataframe = self.new_dataframe.iloc[::-1]
        # Puts the date column back into the dataframe
        self.data["Date"] = self.date
        # Joins dataframes together
        self.new_dataframe = self.new_dataframe.append(self.data)
        # Resets indexes and sorts items
        self.new_dataframe.reset_index(inplace=True)
        # Returns the new dataframe
        return self.new_dataframe

    def sentiment_analysis_prediction(self, tokens):
        # Simplifies words
        stemmer = PorterStemmer()
        # stemming
        self.tweets = tokens.apply(lambda x: [stemmer.stem(i) for i in x])
        # Counts words
        self.tweets = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
        # bag-of-words feature matrix
        bow = self.tweets.fit_transform(self.tweets)
        for column in self.data:
            predictor = LogisticRegression()
            # training the model
            predictor.fit(bow, self.data[column])
            # Predicting prices
            self.new_dataframe[column] = predictor.predict(bow)[0:self.days + 1]

