import numpy as np
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta
from glob import glob
from .interface import parseDataInterface

PATH = "./resultfiles"
TEMPLATES = "./templates"


class TimeSeriesData(parseDataInterface.DataInterface):

    def __init__(self):
        super().__init__()

    def readData(self, path):
        files = glob(os.path.join(path, "*.csv"))
        files_df = (pd.read_csv(f) for f in files)
        concatenated_df = pd.concat(files_df, ignore_index=True)
        self.original_data = concatenated_df
        self.parsed_data = concatenated_df

    def queryData(self, countries=[], provinces=[], startingDate='', endingDate=''):
        df = self.parsed_data

        if countries != ['']:
            df = queryCountry(df, countries)

        if provinces != ['']:
            df = queryProvince(df, provinces)

        if startingDate != '':
            period = getTimePeriod(df, startingDate, endingDate)
            df = queryTime(df, period)

        self.parsed_data = df
        print(self.parsed_data)

    def exportJson(self):
        self.parsed_data.to_json(os.path.join(
            PATH, "json_export_time_series.json"))
        return self.parsed_data.to_json()

    def exportCsv(self):
        self.parsed_data.to_csv(os.path.join(
            PATH, "csv_export_time_series.csv"))
        return self.parsed_data.to_csv(index=False)

    def exportTxt(self):
        with open(os.path.join(PATH, 'txt_export_time_series.html'), 'w') as fo1:
            fo1.write(self.parsed_data.to_html(index=False))
        with open(os.path.join(TEMPLATES, 'txt_export_time_series.html'), 'w') as fo2:
            fo2.write(self.parsed_data.to_html(index=False))


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
