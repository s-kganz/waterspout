#!/bin/python

from flask import Flask, render_template, request
import json
import pandas as pd
from pyproj import Proj, transform
from dbfread import DBF

from config import maps_key, data_dir, filenames
from saga_util import Saga_cmd
app = Flask(__name__)
saga = Saga_cmd()

def generate_polygon(lat=42.73, lon=-73.68):
    # First, convert lat/lon to epsg26918 for call to upslope area
    inproj = Proj(init="epsg:4326") # 4326 GPS coord system as of 1984
    outproj = Proj(init="epsg:26918") # 26918 NAD stateplane NY North

    x,y = transform(inproj, outproj, lon, lat)

    # 1. Calculate upslope area
    saga.upslope_area(x, y, filenames['dem'], filenames['upslope_area'])

    # 2. Reclassify grid
    saga.reclassify_grid(filenames["upslope_area"],
                         filenames["upslope_area"])
    
    # 3. Vectorize grid class
    saga.vectorize_grid_class(filenames["upslope_area"],
                              filenames["upslope_shape"])
    
    # 4. Simplify geometry
    saga.simplify_lines(filenames["upslope_shape"], filenames["upslope_shape"])

    # 5. Generate points from polygon
    saga.polygon_to_points(filenames["upslope_shape"], filenames["area_points"])

    # 6. Add lat/lon coordinates to points
    saga.add_coords_points(filenames["area_points"], filenames["area_points"])

    return home(lat=lat, lon=lon)

@app.route("/submit", methods=["POST"])
def submit():
    # Get lat/lon from form and start generation process
    lat = float(request.form.get("latitude"))
    lon = float(request.form.get("longitude"))

    generate_polygon(lat=lat, lon=lon)
    return home(lat=lat, lon=lon)


@app.route('/')
def home(lat=-99999, lon=-99999):
    # Read in boundary shpfile
    bound_df = list()
    bound_df = list(DBF(filenames["boundary_db"]))
    # convert to dataframe and transform to list of dicts
    bound_df = pd.DataFrame(bound_df)
    bound_df = bound_df.rename(columns = {"LON": "lng", "LAT": "lat"})
    bound_points = filter(lambda x: x["ID_PART"] == 0, bound_df.to_dict(orient="records"))
    # Dummy catchment points in case read fails
    catchment = list()
    try:
        df = list(DBF(filenames["points_db"], load=True))
        df = pd.DataFrame(df)
        df = df.rename(columns = {"LON":"lng", "LAT":'lat'})
        catchment = filter(lambda x: x["ID_PART"] == 0, df.to_dict(orient="records"))
    except Exception as e:
        catchment = list()
        print(e)
    return render_template("home.html", 
                           maps_key=maps_key, 
                           points=catchment, 
                           boundary=bound_points) 


if __name__ == "__main__":
    # Send it
    app.run(port=5000, debug=True)
    