# Create views for the html page
from app import app
import json
from operator import itemgetter
from flask import Flask, render_template, redirect, url_for, request, jsonify, json
from cassie_utils import CassieUtilities
import csv
import time
from datetime import datetime, timedelta
import time
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map

CUtils = CassieUtilities('52.26.135.59', 'bikeshare')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/maps')
def maps():
    return render_template('index.html')

@app.route('/batch')
def batch():
    return render_template('batch.html')

@app.route('/bikecount/<stationid>')
def bikecount(stationid):
    count = CUtils.fetch_bikecount(stationid)
    return jsonify(count=count)

@app.route('/realtime')
def realtime():
    bikes = [CUtils.fetch_data(i) for i in xrange(1,11)]

    return jsonify(bikes=bikes)

@app.route('/location')
def locations():
    bikecount = []
    locations = [CUtils.fetch_location(i) for i in xrange(1,11)]

    return jsonify(locations=locations)
