# Import the dependencies.

import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare a Base using `automap_base()`

Base = automap_base()

# Use the Base class to reflect the database tables

Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data for the last year"""
# Query the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').all()

# Convert the query results to a dictionary
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
# Query all stations
    results = session.query(Station.station, Station.name).all()

# Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations for the last year"""
# Query the last 12 months of temperature observation data
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()

# Convert list of tuples into normal list
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return the min, max, and avg temperatures from the start date to the end of the dataset."""
# Query the min, max, and avg temperatures
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

# Convert list of tuples into normal list
    temps_list = list(np.ravel(results))

    return jsonify(temps_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return the min, max, and avg temperatures for the given date range."""
# Query the min, max, and avg temperatures
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

# Convert list of tuples into normal list
    temps_list = list(np.ravel(results))

    return jsonify(temps_list)

if __name__ == '__main__':
    app.run(debug=True)