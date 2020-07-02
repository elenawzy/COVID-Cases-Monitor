import numpy as np
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta
from glob import glob
from .interface import parseDataInterface

PATH = "./resultfiles"
TEMPLATES = "./templates"


class DailyReportData(parseDataInterface.DataInterface):

    def __init__(self):
        super().__init__()

    def readData(self, path):
        files = glob(os.path.join(path, "*.csv"))
        files_df = (pd.read_csv(f) for f in files)
        concatenated_df = pd.concat(files_df, ignore_index=True)
        concatenated_df['Last_Update'] = pd.to_datetime(
            concatenated_df['Last_Update'], format='%Y-%m-%d %H:%M:%S').dt.normalize()
        columns = ['Province_State', 'Country_Region', 'Last_Update',
                   'Confirmed', 'Deaths', 'Recovered', 'Active', 'Combined_Key']
        concatenated_df = concatenated_df[columns]
        self.original_data = concatenated_df
        self.parsed_data = concatenated_df

    def queryData(self, countries=[], provinces=[], combined=[], startingDate='', endingDate='', data_content=''):
        df = self.original_data
        if countries != ['']:
            df = queryCountry(df, countries)

        if provinces != ['']:
            df = queryProvince(df, provinces)

        if combined != ['']:
            df = queryCombined_Key(df, combined)

        if startingDate != '':
            df = queryTime(df, startingDate, endingDate)

        if data_content != '':
            if data_content == 'deaths':
                df = queryDeaths(df)
            elif data_content == 'confirmed':
                df = queryConfirmed(df)
            elif data_content == 'recovered':
                df = queryRecovered(df)
            else:
                df = queryActive(df)
        self.parsed_data = df

    def exportJson(self, path=PATH):
        time_changed = self.parsed_data
        time_changed['Last_Update'] = time_changed['Last_Update'].dt.strftime(
            '%m/%d/%Y')
        time_changed.to_json(os.path.join(
            path, "json_export_daily_report.json"))
        return time_changed.to_json()

    def exportCsv(self, path=PATH):
        time_changed = self.parsed_data
        time_changed['Last_Update'] = time_changed['Last_Update'].dt.strftime(
            '%m/%d/%Y')
        time_changed.to_csv(os.path.join(
            path, "csv_export_daily_report.csv"), index=False)
        return time_changed.to_csv(index=False)

    def exportTxt(self, path=PATH, temp=TEMPLATES):
        time_changed = self.parsed_data
        time_changed['Last_Update'] = time_changed['Last_Update'].dt.strftime(
            '%m/%d/%Y')
        with open(os.path.join(path, 'txt_export_daily_report.html'), 'w') as fo1:
            fo1.write(time_changed.to_html(index=False))
        if temp != '':
            with open(os.path.join(temp, 'txt_export_daily_report.html'), 'w') as fo2:
                fo2.write(time_changed.to_html(index=False))


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


def queryTime(dataframe, start, end):
    start = start + " 00:00:00"
    startdt = datetime.strptime(start, '%m/%d/%Y %H:%M:%S')
    if end != '':
        end = end + " 00:00:00"
        enddt = datetime.strptime(end, '%m/%d/%Y %H:%M:%S')
        mask = (dataframe['Last_Update'] >= startdt) & (
            dataframe['Last_Update'] <= enddt)
        queried_data = dataframe.loc[mask]
    else:
        queried_data = dataframe[dataframe['Last_Update'] == startdt]
    return queried_data
