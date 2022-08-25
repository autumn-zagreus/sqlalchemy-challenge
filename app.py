from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


app = Flask(__name__)

# connect to database
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# home route
@app.route("/")
def home():
    return(
        f"Hello and welcome to the Climate App API!"
        f"Choose one of the following routes: "
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

# first route - /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precip():
    # return previous year's precipitation as json
    # Calculate the date one year from the last date in data set.
    prevDate = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #prevDate

    # Perform a query to retrieve the data and precipitation scores
    precScore = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prevDate).all()

    session.close()
    # dictionary with date as key and precipitation as value
    precipitation = {date: prcp for date, prcp in results}
    # convert to json
    return jsonify(precipitation)

# second route - /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    # list the stations
    # Perform a query to retrieve the station names
    precScore = session.query(Station.station).all()
    session.close()

    stationLs = list(np.ravel(results))

    # convert to json and return
    return jsonify(stationLs)

# third route - /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    # return the previous year's temperatures
    # return previous year's precipitation as json
    # Calculate the date one year from the last date in data set.
    prevDate = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #prevDate

    # Perform a query to retrieve the temperatures from the most active station from the previous year
    results = session.query(Measurement.tobs).filter(Measurement.station =='USC00519281').filter(Measurement.date >= prevDate).all()
    session.close()
    
    tempLs = list(np.ravel(results))

    # return the jsonified list of temps
    return jsonify(tempLs)

# fourth route - /api/v1.0/<start>/ and /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):
    # do the sql
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    if not end:

        startDate = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*selection).filter(Measurement.date >= startDate)
        session.close()

        tempLs = list(np.ravel(results))

        # return the jsonified list of temps
        return jsonify(tempLs)
    else:
        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")
        results = session.query(*selection).filter(Measurement.date >= startDate).filter(Measurement.date <= endDate)
        session.close()

        tempLs = list(np.ravel(results))

        # return the jsonified list of temps
        return jsonify(tempLs)




## app launcher
if __name__ == '__main__':
    app.run()

