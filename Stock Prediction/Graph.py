import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MONDAY
from mpl_finance import candlestick_ohlc
import datetime


class Graph(object):
    def __init__(self, stock_name, data):
        # Imports a style
        plt.style.use("seaborn")
        # Creates a figure (window) for the graph
        self.fig = plt.figure()
        # Creates an axis
        self.axis = plt.subplot2grid((1, 1), (0, 0))
        # Formats date to DD-MM-YYYY format
        self.axis.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        # Identifies months and mondays, ensuring apprioprate ticks would be created
        self.months = mdates.MonthLocator(range(1, 13), bymonthday=1, interval=1)
        self.mondays = mdates.WeekdayLocator(MONDAY)
        # Sets ticks
        self.axis.xaxis.set_major_locator(self.months)
        self.axis.xaxis.set_minor_locator(self.mondays)

        # Creates variables to store data
        self.stock_name = stock_name
        self.data = data
        self.date = []
        # Creates an arrow pointing to the last price
        self.bbox_props = dict(boxstyle='larrow', fc='w', ec='k', lw=1)

    def convert_dates(self):
        # Iterates through dates
        for day in self.data["Date"]:
            # Converts dates into datetime format
            self.date.append(mdates.date2num(datetime.datetime.strptime(day, "%m/%d/%y")))
        # Removes dates column from the main data frame
        self.data.drop(["Date"], axis=1, inplace=True)

    def linear_graph(self):
        # Iterates through data columns
        for column in self.data:
            # Plots each column, creating a legend as well
            plt.plot_date(self.date, self.data[column], "-", label=column)
            # Annotates it with an arrow, regarding the last price
            self.axis.annotate(str(round(self.data[column][0], 2)), (self.date[0], self.data[column][0]),
                               xytext=(self.date[0] + round(len(self.date)/20), self.data[column][0]), bbox=self.bbox_props)

    def candle_graph(self):
        # Creates a candlestick graph
        candlestick_ohlc(self.axis, zip(self.date,
                         self.data[' Open'], self.data[' High'],
                         self.data[' Low'], self.data[' Close']), width=0.6, colorup='g')
        # Creates an arrow point to the last price
        self.axis.annotate(str(round(self.data[' Close'][0], 2)), (self.date[0], self.data[' Close'][0]),
                           xytext=(self.date[0] + round(len(self.date) / 20), self.data[' Close'][0]),
                           bbox=self.bbox_props)

    def bar_graph(self):
        # Create bars with low and high prices,
        plt.bar(self.date, 10, width=1, bottom=self.data[' High'].apply(lambda x: x-10), label='High')
        plt.bar(self.date, 10, width=1, bottom=self.data[' Low'].apply(lambda x: x-10), label='Low')
        # Annotates it with an arrow, regarding the last price
        self.axis.annotate(str(round(self.data[' High'][0], 2)), (self.date[0], self.data[' High'][0]),
                           xytext=(self.date[0] + round(len(self.date)/20), self.data[' High'][0]), bbox=self.bbox_props)

    def area_graph(self):
        # Fills the area between low price line and high price line
        plt.fill_between(self.date, self.data[' High'], self.data[' Low'], label="High-Low")
        # Annotates the last high price
        self.axis.annotate(str(round(self.data[' High'][0], 2)), (self.date[0], self.data[' High'][0]),
                           xytext=(self.date[0] + round(len(self.date) / 20), self.data[' High'][0]),
                           bbox=self.bbox_props)

    def scatter_graph(self):
        for column in self.data:
            # Plots each column, creating a legend as well
            plt.scatter(self.date, self.data[column], s=2, label=column)
            # Annotates it with an arrow, regarding the last price
            self.axis.annotate(str(round(self.data[column][0], 2)), (self.date[0], self.data[column][0]),
                               xytext=(self.date[0] + round(len(self.date)/20), self.data[column][0]), bbox=self.bbox_props)

    def start_graph(self):
        # Gets all x axis labels
        for label in self.axis.xaxis.get_ticklabels():
            # Rotates them by 45 degrees
            label.set_rotation(45)
        # Scales the window
        self.axis.autoscale_view()
        # Sets a grid up
        self.axis.grid(True)
        # Sets up legend
        plt.legend()
        # Creates a title for the graph
        plt.title(self.stock_name)
        # Opens the graph window
        plt.show()
