from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from parseDataTimeSeries import TimeSeriesData
from parseDataDailyReport import DailyReportData
import pandas as pd

CSV_FOLDER = "csvfiles"
TIME_SERIES_FOLDER = "timeseries"
DAILY_REPORT_FOLDER = "dailyreports"

app = Flask("Assignment 2")
app.debug = True
app.config["ROOT_PATH"] = app.root_path

timeSeries_df = TimeSeriesData()
dailyReport_df = DailyReportData()


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
			# time series file
			elif "time_series" in file.filename:
				filename = secure_filename(file.filename)
				# if file already exists
				if filename in os.listdir(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER)):
					print('updating time series file')
					os.remove(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER, filename))
					file.save(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER, filename))
					print('updated time series file')
          			timeSeries_df.readData(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER))
          			print(timeSeries_df.parsed_data)
				else:
					file.save(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER, filename))
					print("time series file saved!")
          			timeSeries_df.readData(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER))
          			print(timeSeries_df.parsed_data)
			# daily report file
			else:
				filename = secure_filename(file.filename)
				# if file already exists
				if filename in os.listdir(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER)):
					print('updating daily report file')
					os.remove(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER, filename))
					file.save(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER, filename))
					print('updated daily report file')
          			dailyReport_df.readData(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER))
          			print(dailyReport_df.parsed_data)
				else:
					file.save(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER, filename))
					print("time daily report saved!")
          			dailyReport_df.readData(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER))
          			print(dailyReport_df.parsed_data)
			return redirect('/')
	return render_template('monitor.html')

@app.route('/filter-time-series', methods=["GET", "POST"])
def filter_time_series():
	return render_template('filter-time-series.html')

@app.route('/filter-daily', methods=["GET", "POST"])
def filter_daily():
	return render_template('filter-daily.html')

@app.route('/return-time-series-data', methods=["GET", "POST"])
def return_time_series_data():
	if request.method == "POST":
		# check that there isn't any empty data inputs for any of the options (probably will not happen)
		if (all(x in request.files for x in ["province", "country", "start-date", "end-date", "data-format"])):
			print('missing one or more filter options')
			return redirect('/filter-time-series')
	return "time series data"

@app.route('/return-daily-data', methods=["GET", "POST"])
def return_daily_data():
	if request.method == "POST":
		# check that there isn't any empty data inputs for any of the options (probably will not happen)
		if (all(x in request.files for x in ["province", "country", "start-date", "end-date", "data-content", "data-format"])):
			print('missing one or more filter options')
			return redirect('/filter-daily')
	return "daily report data"

if __name__ == "__main__":
    app.run(debug=True)
