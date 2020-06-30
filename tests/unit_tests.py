from COVIDMonitor.main import app
from COVIDMonitor.project import parseDataDailyReport
from COVIDMonitor.project import parseDataTimeSeries
from COVIDMonitor.project.routes import configure_routes
from io import BytesIO
import pandas as pd
import os
from datetime import datetime
from flask import Flask


def test_monitor():
    app = Flask(__name__)
    configure_routes(app)
    response = app.test_client().get('/')

    assert response.status_code == 200

def test_post_add_file_daily():
    app = Flask(__name__)
    configure_routes(app)
    response = app.test_client().post('/addfile',
    data={"file": (BytesIO(b'content'), "06-05-2020.csv")}
    )
    # check for redirect
    assert response.status_code == 302

def test_post_add_file_time_series():
    app = Flask(__name__)
    configure_routes(app)
    response = app.test_client().post('/addfile',
    data={"file": (BytesIO(b'content'), "time_series_covid19_confirmed_global.csv")}
    )
    # check for redirect
    assert response.status_code == 302

def test_post_no_file_sent():
    app = Flask(__name__)
    configure_routes(app)
    response = app.test_client().post('/addfile')
    # check for redirect
    assert response.status_code == 302

def test_get_add_file():
    app = Flask(__name__)
    configure_routes(app)
    response = app.test_client().get('/addfile')

    assert response.status_code == 403

def test_filter_daily():
    app = Flask(__name__)
    configure_routes(app)
    response = app.test_client().get('/filter-daily')

    assert response.status_code == 200

def test_filter_time_series():
    app = Flask(__name__)
    configure_routes(app)
    response = app.test_client().get('/filter-time-series')

    assert response.status_code == 200

def test_post_return_daily_data():
    app = Flask(__name__)
    configure_routes(app)
    data_dict = dict([("province", ""), ("country", "Canada"),
    ("combined", ''), ("start-date", '06/06/2020'), ("end-date", ''),
    ("data-content", 'active'), ("data-format", "csv")])

    data_dictt = {"province": "", "country": "Canada", "combined": "",
                "start-date": '06/06/2020', "end-date": '',
                "data-content": 'active', "data-format": "csv"}
    response = app.test_client().post(
        '/return-daily-data', content_type='multipart/form-data', buffered=True,
        data=data_dictt)
    assert response.status_code == 200

def test_post_return_time_series_data():
    app = Flask(__name__)
    configure_routes(app)
    data_dict = dict([("province", ''), ("country", "Canada"),
    ("start-date", '06/05/2020'), ("end-date", '06/10/2020'), ("data-format", "csv")])
    response = app.test_client().post('/return-time-series-data', buffered=True,
        content_type='multipart/form-data', data=data_dict)
    assert response.status_code == 200

def test_get_return_daily_data():
    app = Flask(__name__)
    configure_routes(app)
    response = app.test_client().get('/return-daily-data')

    assert response.status_code == 403

def test_get_return_time_series_data():
    app = Flask(__name__)
    configure_routes(app)
    response = app.test_client().get('/return-time-series-data')

    assert response.status_code == 403

def test_daily_initial_data():
    daily_report = parseDataDailyReport.DailyReportData()

    assert daily_report.original_data.empty
    assert daily_report.parsed_data.empty


def test_daily_read_data():
    daily_report = parseDataDailyReport.DailyReportData()
    daily_report.readData(os.path.join(
        os.getcwd(), "tests", "test_csv", "test_daily"))
    check_equal = pd.DataFrame(
        {"Province_State": ["South Carolina"], "Country_Region": ["US"], "Last_Update": [datetime(2020, 6, 25, 0, 0, 0)], "Confirmed": [91], "Deaths": [0], "Recovered": [0], "Active": [91], "Combined_Key": ["Abbeville, South Carolina, US"]})

    assert daily_report.original_data.equals(check_equal)
    assert daily_report.parsed_data.equals(check_equal)


def test_daily_query_data():
    daily_report = parseDataDailyReport.DailyReportData()
    daily_report.readData(os.path.join(
        os.getcwd(), "tests", "test_csv", "test_daily"))
    daily_report.queryData(["US"], [
                           "South Carolina"], ["Abbeville, South Carolina, US"], "01/01/2020", "09/01/2020", "confirmed")
    check_equal_original = pd.DataFrame(
        {"Province_State": ["South Carolina"], "Country_Region": ["US"], "Last_Update": [datetime(2020, 6, 25, 0, 0, 0)], "Confirmed": [91], "Deaths": [0], "Recovered": [0], "Active": [91], "Combined_Key": ["Abbeville, South Carolina, US"]})
    check_equal_parsed = pd.DataFrame(
        {"Province_State": ["South Carolina"], "Country_Region": ["US"], "Last_Update": [datetime(2020, 6, 25, 0, 0, 0)], "Confirmed": [91], "Combined_Key": ["Abbeville, South Carolina, US"]})

    assert daily_report.original_data.equals(check_equal_original)
    assert daily_report.parsed_data.equals(check_equal_parsed)


def test_daily_export_json():
    daily_report = parseDataDailyReport.DailyReportData()
    daily_report.readData(os.path.join(
        os.getcwd(), "tests", "test_csv", "test_daily"))
    daily_report.queryData(["US"], [
                           "South Carolina"], ["Abbeville, South Carolina, US"], "01/01/2020", "09/01/2020", "confirmed")
    json = daily_report.exportJson(
        os.path.join(os.getcwd(), "tests", "test_result"))

    assert os.path.isfile(os.path.join(
        os.getcwd(), "tests", "test_result", "json_export_daily_report.json"))


def test_daily_export_csv():
    daily_report = parseDataDailyReport.DailyReportData()
    daily_report.readData(os.path.join(
        os.getcwd(), "tests", "test_csv", "test_daily"))
    daily_report.queryData(["US"], [
                           "South Carolina"], ["Abbeville, South Carolina, US"], "01/01/2020", "09/01/2020", "confirmed")
    csv = daily_report.exportCsv(
        os.path.join(os.getcwd(), "tests", "test_result"))

    assert os.path.isfile(os.path.join(
        os.getcwd(), "tests", "test_result", "csv_export_daily_report.csv"))


def test_daily_export_txt():
    daily_report = parseDataDailyReport.DailyReportData()
    daily_report.readData(os.path.join(
        os.getcwd(), "tests", "test_csv", "test_daily"))
    daily_report.queryData(["US"], [
                           "South Carolina"], ["Abbeville, South Carolina, US"], "01/01/2020", "09/01/2020", "confirmed")
    daily_report.exportTxt(os.path.join(
        os.getcwd(), "tests", "test_result"), '')

    assert os.path.isfile(os.path.join(
        os.getcwd(), "tests", "test_result", "txt_export_daily_report.html"))


def test_daily_query_deaths():
    data = pd.DataFrame(
        {"Province_State": ["South Carolina"], "Country_Region": ["US"], "Last_Update": [datetime(2020, 6, 25, 0, 0, 0)], "Confirmed": [91], "Deaths": [0], "Recovered": [0], "Active": [91], "Combined_Key": ["Abbeville, South Carolina, US"]})
    result = parseDataDailyReport.queryDeaths(data)
    compare = pd.DataFrame(
        {"Province_State": ["South Carolina"], "Country_Region": ["US"], "Last_Update": [datetime(2020, 6, 25, 0, 0, 0)], "Deaths": [0], "Combined_Key": ["Abbeville, South Carolina, US"]})

    assert result.equals(compare)


def test_daily_query_recovered():
    data = pd.DataFrame(
        {"Province_State": ["South Carolina"], "Country_Region": ["US"], "Last_Update": [datetime(2020, 6, 25, 0, 0, 0)], "Confirmed": [91], "Deaths": [0], "Recovered": [0], "Active": [91], "Combined_Key": ["Abbeville, South Carolina, US"]})
    result = parseDataDailyReport.queryRecovered(data)
    compare = pd.DataFrame(
        {"Province_State": ["South Carolina"], "Country_Region": ["US"], "Last_Update": [datetime(2020, 6, 25, 0, 0, 0)], "Recovered": [0], "Combined_Key": ["Abbeville, South Carolina, US"]})

    assert result.equals(compare)


def test_daily_query_active():
    data = pd.DataFrame(
        {"Province_State": ["South Carolina"], "Country_Region": ["US"], "Last_Update": [datetime(2020, 6, 25, 0, 0, 0)], "Confirmed": [91], "Deaths": [0], "Recovered": [0], "Active": [91], "Combined_Key": ["Abbeville, South Carolina, US"]})
    result = parseDataDailyReport.queryActive(data)
    compare = pd.DataFrame(
        {"Province_State": ["South Carolina"], "Country_Region": ["US"], "Last_Update": [datetime(2020, 6, 25, 0, 0, 0)], "Active": [91], "Combined_Key": ["Abbeville, South Carolina, US"]})

    assert result.equals(compare)


def test_daily_query_time():
    data = pd.DataFrame(
        {"Province_State": ["South Carolina"], "Country_Region": ["US"], "Last_Update": [datetime(2020, 6, 25, 0, 0, 0)], "Confirmed": [91], "Deaths": [0], "Recovered": [0], "Active": [91], "Combined_Key": ["Abbeville, South Carolina, US"]})

    result1 = parseDataDailyReport.queryTime(data, "01/01/2020", '')
    assert result1.empty

    result2 = parseDataDailyReport.queryTime(data, "06/25/2020", '')
    assert result2.equals(data)

    result3 = parseDataDailyReport.queryTime(data, "09/20/2020", '10/20/2020')
    assert result3.empty

# parseDataTimeSeries Tests


def test_time_initial_data():
    time_series = parseDataTimeSeries.TimeSeriesData()

    assert time_series.original_data.empty
    assert time_series.parsed_data.empty


def test_time_read_data():
    time_series = parseDataTimeSeries.TimeSeriesData()
    time_series.readData(os.path.join(
        os.getcwd(), "tests", "test_csv", "test_time"))
    check_equal = pd.DataFrame(
        {"Province/State": ["Ontario"], "Country/Region": ["Canada"], "Lat": [33], "Long": [65], "1/22/20": [0], "1/23/20": [0], "1/24/20": [0], "1/25/20": [0], "1/26/20": [0], "1/27/20": [0]})

    assert time_series.original_data.equals(check_equal)
    assert time_series.parsed_data.equals(check_equal)


def test_time_query_data():
    time_series = parseDataTimeSeries.TimeSeriesData()
    time_series.readData(os.path.join(
        os.getcwd(), "tests", "test_csv", "test_time"))
    time_series.queryData(["Canada"], [
        "Ontario"], "01/01/2020", "01/23/2020")
    check_equal_original = pd.DataFrame(
        {"Province/State": ["Ontario"], "Country/Region": ["Canada"], "Lat": [33], "Long": [65], "1/22/20": [0], "1/23/20": [0], "1/24/20": [0], "1/25/20": [0], "1/26/20": [0], "1/27/20": [0]})
    check_equal_parsed = pd.DataFrame(
        {"Province/State": ["Ontario"], "Country/Region": ["Canada"], "1/22/20": [0], "1/23/20": [0]})

    assert time_series.original_data.equals(check_equal_original)
    assert time_series.parsed_data.equals(check_equal_parsed)


def test_time_export_json():
    time_series = parseDataTimeSeries.TimeSeriesData()
    time_series.readData(os.path.join(
        os.getcwd(), "tests", "test_csv", "test_time"))
    time_series.queryData(["Canada"], [
        "Ontario"], "01/01/2020", "01/23/2020")
    json = time_series.exportJson(
        os.path.join(os.getcwd(), "tests", "test_result"))

    assert os.path.isfile(os.path.join(
        os.getcwd(), "tests", "test_result", "json_export_time_series.json"))


def test_time_export_csv():
    time_series = parseDataTimeSeries.TimeSeriesData()
    time_series.readData(os.path.join(
        os.getcwd(), "tests", "test_csv", "test_time"))
    time_series.queryData(["Canada"], [
        "Ontario"], "01/01/2020", "01/23/2020")
    csv = time_series.exportCsv(
        os.path.join(os.getcwd(), "tests", "test_result"))

    assert os.path.isfile(os.path.join(
        os.getcwd(), "tests", "test_result", "csv_export_time_series.csv"))


def test_time_export_txt():
    time_series = parseDataTimeSeries.TimeSeriesData()
    time_series.readData(os.path.join(
        os.getcwd(), "tests", "test_csv", "test_time"))
    time_series.queryData(["Canada"], [
        "Ontario"], "01/01/2020", "01/23/2020")
    time_series.exportTxt(os.path.join(
        os.getcwd(), "tests", "test_result"), '')

    assert os.path.isfile(os.path.join(
        os.getcwd(), "tests", "test_result", "txt_export_time_series.html"))


def test_time_get_time_period():
    data = pd.DataFrame({"Province/State": ["Ontario"], "Country/Region": ["Canada"], "Lat": [33], "Long": [
                        65], "1/22/20": [0], "1/23/20": [0], "1/24/20": [0], "1/25/20": [0], "1/26/20": [0], "1/27/20": [0]})

    result1 = parseDataTimeSeries.getTimePeriod(data, "09/06/2019", "")
    assert result1 == []

    result2 = parseDataTimeSeries.getTimePeriod(
        data, "09/06/2019", "09/08/2019")
    assert result2 == []

    result3 = parseDataTimeSeries.getTimePeriod(
        data, "01/01/2020", "01/23/2020")
    assert result3 == ["1/22/20", "1/23/20"]

    result4 = parseDataTimeSeries.getTimePeriod(
        data, "01/24/2020", "01/25/2020")
    assert result4 == ["1/24/20", "1/25/20"]
