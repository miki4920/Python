import quandl


class StockExchange(object):
    def __init__(self, api):
        quandl.ApiConfig.api_key = api

    @staticmethod
    def get_data_between_dates(name, date_one, date_two):
        data = quandl.get(f'EURONEXT/{name}', start_date=date_one, end_date=date_two)
        data = data.drop(["Turnover", "Volume"], axis=1)
        data.rename(columns={"Last": "Close"}, inplace=True)
        data = data[["Open", "Close", "Low", "High"]]
        return data


print(StockExchange("mNniGYUeXUex5kz3yQHE").get_data_between_dates("ADYEN", "2020-05-13", '2020-05-15'))