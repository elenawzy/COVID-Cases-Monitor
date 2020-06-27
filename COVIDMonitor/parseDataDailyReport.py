import numpy as np
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta
from glob import glob


class DailyReportData:

    def __init__(self):
        self.original_data = pd.DataFrame()
        self.parsed_data = pd.DataFrame()

    def readData(self, path):
        files = glob(os.path.join(path, "*.csv"))
        files_df = (pd.read_csv(f) for f in files)
        concatenated_df = pd.concat(files_df, ignore_index=True)
        concatenated_df['Last_Update'] = pd.to_datetime(
            concatenated_df['Last_Update'], format='%Y-%m-%d %H:%M:%S').dt.date
        columns = ['Province_State', 'Country_Region', 'Last_Update',
                   'Confirmed', 'Deaths', 'Recovered', 'Active', 'Combined_Key']
        concatenated_df = concatenated_df[columns]
        self.original_data = concatenated_df
        self.parsed_data = self.original_data

    def queryData(self, countries=[], provinces=[], startingDate='', endingDate=''):
        df = self.original_data
        if countries != []:
            df = queryCountry(df, countries)

        if provinces != []:
            df = queryProvince(df, provinces)

        if startingDate != '':
            df = queryTime(startingDate, endingDate)

        self.parsed_data = df

    def refreshParsedData(self):
        self.parsed_data = self.original_data


def queryCountry(dataframe, countries):
    queried_data = dataframe[dataframe['Country_Region'].isin(countries)]
    return queried_data


def queryProvince(dataframe, provinces):
    queried_data = dataframe[dataframe['Province_State'].isin(provinces)]
    return queried_data


def queryCombined_Key(dataframe, combined_keys):
    queried_data = dataframe[dataframe['Combined_Key'].isin(combined_keys)]
    return queried_data


def queryConfirmed(dataframe):
    columns = ['Province_State', 'Country_Region',
               'Last_Update', 'Confirmed', 'Combined_Key']
    queried_data = dataframe[columns]
    return queried_data


def queryDeaths(dataframe):
    columns = ['Province_State', 'Country_Region',
               'Last_Update', 'Deaths', 'Combined_Key']
    queried_data = dataframe[columns]
    return queried_data


def queryRecovered(dataframe):
    columns = ['Province_State', 'Country_Region',
               'Last_Update', 'Recovered', 'Combined_Key']
    queried_data = dataframe[columns]
    return queried_data


def queryActive(dataframe):
    columns = ['Province_State', 'Country_Region',
               'Last_Update', 'Active', 'Combined_Key']
    queried_data = dataframe[columns]
    return queried_data

# time must be in month/date/year


def queryTime(dataframe, start, end=''):
    startdt = datetime.strptime(start, '%m/%d/%y')
    if enddt != '':
        enddt = datetime.strptime(end, '%m/%d/%y')
        queried_data = dataframe[startdt <= dataframe['Last_Update'] <= enddt]
    else:
        queried_data = dataframe[dataframe['Last_Update'] == startdt]
    return queried_data
