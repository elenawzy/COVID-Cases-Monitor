from flask import Flask, render_template

app = Flask("Assignment 2")

@app.route('/monitor')
def welcome_monitor():
	return render_template('monitor.html')

if __name__ == "__main__":
	app.run()