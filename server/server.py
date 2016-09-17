#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request, render_template, abort, send_from_directory, url_for
# Import db models and generate
import models
# Import model views
import views

# setting up static directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/client'
app = Flask(__name__, static_folder=STATIC_DIR)
# Set debugging mode in flask for on change compiling of code
app.debug = False
app.config["ERROR_404_HELP"] = False
# Routes
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/lib/<path:path>')
def static_lib(path):
    try:
        return app.send_static_file('lib/'+ path)
    except:
        print path
        abort(404)

@app.route('/js/<path:path>')
def static_js(path):
    print path
    try:
        return app.send_static_file('js/' + path)
    except:
        print path
        abort(404)

@app.route('/css/<path:path>')
def static_css(path):
    print path
    try:
        return app.send_static_file('css/' + path)
    except:
        print path
        abort(404)

@app.route('/partials/<path:path>')
def static_partials(path):
    print path
    try:
        return app.send_static_file('partials/' + path)
    except:
        return app.send_static_file('index.html')

if __name__ == '__main__':
    # Generate object-database mapping
    models.register.register_models(app)
    # Register views
    views.register.register_resources(app, '/api')
    app.run(port=3000)
