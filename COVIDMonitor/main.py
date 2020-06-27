from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

CSV_FOLDER = "csvfiles"
TIME_SERIES_FOLDER = "timeseries"
DAILY_REPORT_FOLDER = "dailyreports"

app = Flask("Assignment 2")
app.debug = True
app.config["ROOT_PATH"] = app.root_path

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
				else:
					file.save(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, TIME_SERIES_FOLDER, filename))
					print("time series file saved!")
			# daily report file
			else:
				filename = secure_filename(file.filename)
				# if file already exists
				if filename in os.listdir(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER)):
					print('updating daily report file')
					os.remove(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER, filename))
					file.save(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER, filename))
					print('updated daily report file')
				else:
					file.save(os.path.join(app.config["ROOT_PATH"], CSV_FOLDER, DAILY_REPORT_FOLDER, filename))
					print("time daily report saved!")
			return redirect('/')
	return render_template('monitor.html')
if __name__ == "__main__":
	app.run(debug = True)
