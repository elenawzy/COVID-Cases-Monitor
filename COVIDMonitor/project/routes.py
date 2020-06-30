from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from werkzeug.utils import secure_filename
import os
import sys
import pandas as pd
try:
    import parseDataDailyReport
    import parseDataTimeSeries
except ImportError:
    from . import parseDataDailyReport
    from . import parseDataTimeSeries

CSV_FOLDER = "csvfiles"
TIME_SERIES_FOLDER = "timeseries"
DAILY_REPORT_FOLDER = "dailyreports"

timeSeries_df = parseDataTimeSeries.TimeSeriesData()
dailyReport_df = parseDataDailyReport.DailyReportData()


def configure_routes(app):
    class InvalidUsage(Exception):
        status_code = 400

        def __init__(self, message, status_code=None, payload=None):
            Exception.__init__(self)
            self.message = message
            if status_code is not None:
                self.status_code = status_code
            self.payload = payload

        def to_dict(self):
            rv = dict(self.payload or ())
            rv['message'] = self.message
            return rv

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.route('/')
    def welcome_monitor():
        return render_template('monitor.html')

    @app.route('/addfile', methods=["GET", "POST"])
    def add_file():
        if request.method == "POST":
            if 'data-file' not in request.files:
                print('no data file sent')
                return redirect('/')
            if "data-file" in request.files:
                file = request.files["data-file"]
                # check for empty file
                if file.filename == '':
                    print('empty file')
                    return redirect('/')
                # time series file
                elif "time_series" in file.filename:
                    filename = secure_filename(file.filename)
                    # if file already exists
                    if filename in os.listdir(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER)):
                        print('updating time series file')
                        os.remove(os.path.join(
                            app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER, filename))
                        file.save(os.path.join(
                            app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER, filename))
                        print('updated time series file')
                        timeSeries_df.readData(os.path.join(
                            app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER))
                        print(timeSeries_df.parsed_data)
                    else:
                        file.save(os.path.join(
                            app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER, filename))
                        print("time series file saved!")
                        timeSeries_df.readData(os.path.join(
                            app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER))
                        print(timeSeries_df.parsed_data)
                # daily report file
                else:
                    filename = secure_filename(file.filename)
                    # if file already exists
                    if filename in os.listdir(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER)):
                        print('updating daily report file')
                        os.remove(os.path.join(
                            app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER, filename))
                        file.save(os.path.join(
                            app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER, filename))
                        print('updated daily report file')
                        dailyReport_df.readData(os.path.join(
                            app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER))
                        print(dailyReport_df.parsed_data)
                    else:
                        file.save(os.path.join(
                            app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER, filename))
                        print("time daily report saved!")
                        dailyReport_df.readData(os.path.join(
                            app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER))
                        print(dailyReport_df.parsed_data)
                return redirect('/')
        if request.method == "GET":
            raise InvalidUsage('This url is only for POST methods, please go back and add a file', status_code=403)

    @app.route('/filter-time-series', methods=["GET", "POST"])
    def filter_time_series():
        return render_template('filter-time-series.html')

    @app.route('/filter-daily', methods=["GET", "POST"])
    def filter_daily():
        return render_template('filter-daily.html')

    @app.route('/return-time-series-data', methods=["GET", "POST"])
    def return_time_series_data():
        if request.method == "POST":
            print(request.form["province"])
            print(request.form["country"])
            print(request.form["start-date"])
            if request.form["end-date"] == '':
                print("end-date empty string")
            else:
                print(request.form["end-date"])
            print(request.form["data-format"])

            countries = request.form["country"].split(";")
            provinces = request.form["province"].split(";")

            timeSeries_df.queryData(
                countries, provinces, request.form["start-date"], request.form["end-date"])

            if request.form["data-format"] == "json":
                export_data = timeSeries_df.exportJson()
                return export_data
            elif request.form["data-format"] == "csv":
                export_data = timeSeries_df.exportCsv()
                return export_data
            else:
                timeSeries_df.exportTxt()
                return render_template('txt_export_time_series.html')
        if request.method == "GET":
            raise InvalidUsage('This url is only for POST methods, please go back and add your filters', status_code=403)

    @app.route('/return-daily-data', methods=["GET", "POST"])
    def return_daily_data():
        if request.method == "POST":
            print(request.form["province"])
            print(request.form["country"])
            print(request.form["start-date"])
            if request.form["end-date"] == '':
                print("end-date empty string")
            else:
                print(request.form["end-date"])
            print(request.form["data-content"])
            print(request.form["data-format"])

            countries = request.form["country"].split(";")
            provinces = request.form["province"].split(";")
            combined_keys = request.form["combined"].split(";")

            dailyReport_df.queryData(
                countries, provinces, combined_keys, request.form["start-date"], request.form["end-date"], request.form["data-content"])

            if request.form["data-format"] == "json":
                export_data = dailyReport_df.exportJson()
                return export_data
            elif request.form["data-format"] == "csv":
                export_data = dailyReport_df.exportCsv()
                return export_data
            else:
                dailyReport_df.exportTxt()
                return render_template('txt_export_daily_report.html')
        if request.method == "GET":
            raise InvalidUsage('This url is only for POST methods, please go back and add your filters', status_code=403)
