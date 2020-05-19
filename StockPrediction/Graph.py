import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MONDAY
import mplfinance as mpf


class Graph(object):
    def __init__(self, stock_name, data):
        # Imports a style
        plt.style.use("seaborn")
        # Creates a figure (window) for the graph
        self.fig = plt.figure()
        # Creates an axis
        self.axis = plt.subplot2grid((1, 1), (0, 0))
        # Formats date to DD-MM-YYYY format
        self.axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
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

    def linear_graph(self):
        # Iterates through data columns
        for column in self.data:
            # Plots each column, creating a legend 0as well
            plt.plot_date(self.data.index, self.data[column], "-", label=column)

    def candle_graph(self):
        # Creates a candlestick graph
        mc = mpf.make_marketcolors(up='g', down='r')
        s = mpf.make_mpf_style(marketcolors=mc)
        mpf.plot(self.data, type="candle", style=s, title=self.stock_name, ylabel='OHLC Candles')

    def bar_graph(self):
        # Create bars with low and high prices,
        plt.bar(self.data.index, 10, width=1, bottom=self.data['High'].apply(lambda x: x-10), label='High')
        plt.bar(self.data.index, 10, width=1, bottom=self.data['Low'].apply(lambda x: x-10), label='Low')

    def area_graph(self):
        # Fills the area between low price line and high price line
        plt.fill_between(self.data.index, self.data['High'], self.data['Low'], label="High-Low")

    def scatter_graph(self):
        for column in self.data:
            # Plots each column, creating a legend as well
            plt.scatter(self.data.index, self.data[column], s=2, label=column)

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
