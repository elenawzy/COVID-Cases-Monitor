from flask import Flask

from COVIDMonitor.main import app
from COVIDMonitor.project.routes import configure_routes

def test_monitor():
	app = Flask(__name__)
	configure_routes(app)
	response = app.test_client().get('/')

	assert response.status_code == 200

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
