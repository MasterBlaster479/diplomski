#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request, render_template, abort

# setting up static directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/client'

app = Flask(__name__, static_folder=STATIC_DIR)
app.debug = True

# Routes
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    try:
        return app.send_static_file(path)
    except:
        return app.send_static_file('index.html')

# Generate object-database mapping

# Register views

if __name__ == '__main__':
    # Make sure each thread gets a db session
    app.run(port=3000)
