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

        if countries != ['']:
            df = queryCountry(df, countries)

        if provinces != ['']:
            df = queryProvince(df, provinces)

        if startingDate != '':
            period = getTimePeriod(df, startingDate, endingDate)
            df = queryTime(df, period)

        self.parsed_data = df
        print(self.parsed_data)

    def refreshParsedData(self):
        self.parsed_data = self.original_data

    def exportJson(self):
        return self.parsed_data.to_json()


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


def getTimePeriod(dataframe, start, end):
    startdt = datetime.strptime(start, '%m/%d/%Y')
    if startdt < datetime.strptime('01/22/2020', '%m/%d/%Y'):
        startdt = datetime.strptime('01/22/2020', '%m/%d/%Y')
    datelist = []

    if end != '':
        enddt = datetime.strptime(end, '%m/%d/%Y')
        last_date = datetime.strptime(list(dataframe.columns)[-1], '%m/%d/%y')
        if enddt > last_date:
            enddt = last_date
        while startdt <= enddt:
            date = startdt.strftime('%m/%d/%y').lstrip("0").replace("/0", "/")
            datelist.append(date)
            startdt = startdt + timedelta(days=1)
    else:
        datelist = [startdt.strftime(
            '%m/%d/%y').lstrip("0").replace("/0", "/")]

    return datelist
