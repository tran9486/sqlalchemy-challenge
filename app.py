import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year = dt.datetime.strptime(str(recent), "%Y-%m-%d") - dt.timedelta(days = 365)
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > one_year).all()
    
    prcp_list = list(np.ravel(prcp_query))
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_names = session.query(Station.station).all()
    
    station_list = list(np.ravel(station_names))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year = dt.datetime.strptime(str(recent), "%Y-%m-%d") - dt.timedelta(days = 365)
    temp_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > one_year)\
                .filter(Measurement.station == 'USC00519281').all()
    
    temp_list = list(np.ravel(temp_query))
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    start_date = dt.datetime.strptime(str(start), "%Y-%m-%d")
    TMIN = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).all()[0]
    TAVG = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()[0]
    TMAX = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()[0]
    
    TMIN_list = list(np.ravel(TMIN))
    TAVG_list = list(np.ravel(TAVG))
    TMAX_list = list(np.ravel(TMAX))
    return (
        f'Minimum Temperature: {TMIN_list}</br>'
        f'Average Temperature: {TAVG_list}</br>'
        f'Maximum Temperature: {TMAX_list}'
    )

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    session = Session(engine)
    start_date = dt.datetime.strptime(str(start), "%Y-%m-%d")
    end_date = dt.datetime.strptime(str(end), "%Y-%m-%d")
    TMIN = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    TAVG = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    TMAX = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    TMIN_list = list(np.ravel(TMIN))
    TAVG_list = list(np.ravel(TAVG))
    TMAX_list = list(np.ravel(TMAX))
    return (
        f'Minimum Temperature: {TMIN_list}</br>'
        f'Average Temperature: {TAVG_list}</br>'
        f'Maximum Temperature: {TMAX_list}'
    )
    
if __name__ == "__main__":
    app.run(debug=True)