from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import sys
import pandas as pd
try:
    from project import routes
except ImportError:
    from . import project
    from .project import routes

template_folder_path = os.path.join(sys.path[0], "templates")
app = Flask("Assignment 2", template_folder=template_folder_path)
app.debug = True
app.config["ROOT_PATH"] = app.root_path

routes.configure_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
