import numpy as np
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta
from glob import glob


class TimeSeriesData:

    def __init__(self):
        self.original_data = pd.DataFrame()
        self.parsed_data = pd.DataFrame()

    def readData(self, path):
        files = glob(os.path.join(path, "*.csv"))
        files_df = (pd.read_csv(f) for f in files)
        concatenated_df = pd.concat(files_df, ignore_index=True)
        self.original_data = concatenated_df
        self.parsed_data = self.original_data

    def queryData(self, countries=[], provinces=[], startingDate='', endingDate=''):
        df = self.original_data

        if countries != []:
            df = queryCountry(df, countries)

        if provinces != []:
            df = queryProvince(df, provinces)

        if startingDate != '':
            if endingDate != '':
                period = getTimePeriod(startingDate, endingDate)
                df = queryTime(df, period)
            else:
                df = queryTime(df, startingDate)

        self.parsed_data = df

    def refreshParsedData(self):
        self.parsed_data = self.original_data


def queryCountry(dataframe, countries):
    queried_data = dataframe[dataframe['Country/Region'].isin(countries)]
    return queried_data


def queryProvince(dataframe, provinces):
    queried_data = dataframe[dataframe['Province/State'].isin(provinces)]
    return queried_data

# time must be in month/date/year


def queryTime(dataframe, time):
    time = ['Province/State', 'Country/Region'] + time
    queried_data = dataframe[time]
    return queried_data


def getTimePeriod(start, end):
    startdt = datetime.strptime(start, '%m/%d/%y')
    enddt = datetime.strptime(end, '%m/%d/%y')
    datelist = []

    while startdt < enddt:
        date = startdt.strftime('%m/%d/%y').lstrip("0").replace("/0", "/")
        datelist.append(date)
        startdt = startdt + timedelta(days=1)

    return datelist
