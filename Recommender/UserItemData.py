import pandas
from datetime import datetime as dt
class UserItemData:
    def __init__(self, path, start_date='1.1.1970', end_date='12.12.2090', min_ratings=None):
        self.data = list()
        self.path = path
        self.start_date = start_date
        self.end_date = end_date
        self.min_ratings = min_ratings
        if(start_date != None and end_date != None and min_ratings != None):
            self.start_date = dt.strptime(start_date,'%d.%m.%Y')
            self.end_date = dt.strptime(end_date,'%d.%m.%Y')
            self.min_ratings = min_ratings
        self.ReadData()

    def ReadData(self):
        self.FormatData()
        if(self.start_date != None and self.end_date != None and self.min_ratings != None ):
            self.FilterData()

    def FormatData(self):
        self.data = pandas.read_csv(self.path, sep='\t', encoding='ISO-8859-1', usecols=["userID", "movieID", "rating", "date_day", "date_month", "date_year"])
        self.data['date'] = self.data['date_year'].astype(str) + '-' + self.data['date_month'].astype(str) + '-' + self.data['date_day'].astype(str)
        self.data['date'] = pandas.to_datetime(self.data['date'])
        self.data.drop(["date_day", "date_month", "date_year"], inplace=True, axis=1)

    def NRatings(self):
        return self.data.shape[0]

    def FilterData(self):
        df1 = self.data[(self.data.date >= self.start_date) & (self.data.date < self.end_date)]
        df2 = df1.groupby('movieID')
        self.data = df2.filter(lambda x: len(x) > self.min_ratings)