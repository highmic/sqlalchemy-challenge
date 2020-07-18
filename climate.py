import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Surfs Up Hawaii Vacation Weather API <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"********************************<br/>"
        f"Enter start date format yyyy-mm-dd:<br/>"
        f"/api/v1.0/2016-07-04<br/>"
        f"********************************<br/>"
        f"Enter specific start-end dates format yyyy-mm-dd:<br/>"
        f"/api/v1.0/2016-07-04/2016-07-14"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Design a query to retrieve the last 12 months of precipitation data"""
    # Query for precipitaion data
    year_ago = dt.date(2016, 8, 23)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago)\
    .order_by(Measurement.date).all()

    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_data.append(precipitation_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

#     # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)
    

@app.route("//api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

#     """Query the dates and temperature observations of the most active station for the last year of data"""
    year_ago = dt.date(2016, 8, 23)
    active_station = "USC00519281"

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.\
    station == active_station).filter(Measurement.date >= year_ago).all()

    session.close()

    tobs_data = list(np.ravel(results))

    return jsonify(tobs_data)

@app.route("//api/v1.0/<start_date>")
def start_temps(start_date):
     # Create our session (link) from Python to the DB
    session = Session(engine)
    #Return a JASON of TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),\
    func.max(Measurement.tobs)]
    """TMIN, TAVG, and TMAX for all dates greater than a specific start date. 
    Args:
        start_date (string): A date string in the format %Y-%m-%d     
    Returns:
        TMIN, TAVE, and TMAX
    """
  
    results = session.query(*sel).filter(Measurement.date >= start_date).group_by(Measurement.date).all()

    session.close()

    start_temp_data = []
    for data in results:
        start_tobs_dict = {}
        start_tobs_dict["date"] = data[0]
        start_tobs_dict["TMIN"] = data[1]
        start_tobs_dict["TAVG"] = data[2]
        start_tobs_dict["TMAX"] = data[3]
        start_temp_data.append(start_tobs_dict)
    
    return jsonify(start_temp_data)


@app.route("//api/v1.0/<start_date>/<end_date>")
def start_end_temps(start_date, end_date):
     # Create our session (link) from Python to the DB
    session = Session(engine)
    #Return a JASON of TMIN, TAVG, and TMAX for all dates between the start and end dates 
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),\
    func.max(Measurement.tobs)]
    """TMIN, TAVG, and TMAX for all dates greater than a specific start date. 
    Args:
        start_date (string): A date string in the format %Y-%m-%d 
        end_date (string): A date string in the format %Y-%m-%d    
    Returns:
        TMIN, TAVE, and TMAX
    """
    results = session.query(*sel).filter(Measurement.date >= start_date).filter(Measurement.date <=end_date)\
              .group_by(Measurement.date).all()

    session.close()

    start_temp_data = []
    for data in results:
        start_tobs_dict = {}
        start_tobs_dict["date"] = data[0]
        start_tobs_dict["TMIN"] = data[1]
        start_tobs_dict["TAVG"] = data[2]
        start_tobs_dict["TMAX"] = data[3]
        start_temp_data.append(start_tobs_dict)
    
    return jsonify(start_temp_data)

if __name__ == '__main__':
    app.run(debug=True)
