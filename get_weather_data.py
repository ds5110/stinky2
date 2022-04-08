# From https://towardsdatascience.com/getting-weather-data-in-3-easy-steps-8dc10cc5c859

from datetime import datetime
import json

import pandas as pd
import numpy as np
import requests


TOKEN = ""
STATION = "GHCND:USW00014764"

URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"

# https://docs.opendata.aws/noaa-ghcn-pds/readme.html
# Available at PWM:
# AWND - Average daily wind speed (tenths of meters per second)
# PRCP - Precipitation (tenths of mm)
# SNOW - Snowfall
# SNWD - Snow depth
# TAVG - Average temperature (tenths of degrees C)
# TMAX - Max temp
# TMIN - Min temp
# WDF2 - Direction of fastest 2-minute wind (degrees)
# WDF5 - Direction of fastest 5-minute wind (degrees)
# WSF2 - Fastest 2-minute wind speed (tenths of meters per second)
# WSF5 - Fastest 5-minute wind speed (tenths of meters per second)

# No humidity?!

# DATA_TYPES = ["TAVG", "AWND", "PRCP"]

PARAMS = {
	"datasetid": "GHCND",
	"limit": 1000,
	"stationid": STATION,
	"startdate": "",
	"enddate": ""
}

HEADERS = {
	"token": TOKEN
}

dates = []
avg_temps = []

df = pd.DataFrame()

for year in [2020, 2021, 2022]:
	print(f"Getting TAVG data for {year}")

	start = f"{year}-01-01"
	end = f"{year}-12-31"

	PARAMS["startdate"] = start
	PARAMS["enddate"] = end
	
	PARAMS["datatypeid"] = "TAVG"

	r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
	d = r.json()

	dates.extend([item["date"] for item in d["results"] if item["datatype"] == "TAVG"])
	avg_temps.extend([item["value"] for item in d["results"] if item["datatype"] == "TAVG"])

df["date"] = [str(date[0:10]).strip() for date in dates]
df["average_temp"] = [float(value)/10.0*1.8 + 32 for value in avg_temps]

dates = []
avg_winds = []

df_wind = pd.DataFrame()

for year in [2020, 2021, 2022]:
	print(f"Getting AWND data for {year}")

	start = f"{year}-01-01"
	end = f"{year}-12-31"

	PARAMS["startdate"] = start
	PARAMS["enddate"] = end
	
	PARAMS["datatypeid"] = "AWND"

	r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
	d = r.json()

	dates.extend([item["date"] for item in d["results"] if item["datatype"] == "AWND"])
	avg_winds.extend([item["value"] for item in d["results"] if item["datatype"] == "AWND"])

df_wind["date"] = [str(date[0:10]).strip() for date in dates]
df_wind["average_temp"] = [value for value in avg_winds]

dates = []
precips = []

df_prec = pd.DataFrame()

for year in [2020, 2021, 2022]:
	print(f"Getting PRCP data for {year}")

	start = f"{year}-01-01"
	end = f"{year}-12-31"

	PARAMS["startdate"] = start
	PARAMS["enddate"] = end
	
	PARAMS["datatypeid"] = "PRCP"

	r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
	d = r.json()

	results = [item for item in d["results"] if item["datatype"] == "PRCP"]

	dates.extend([item["date"] for item in d["results"] if item["datatype"] == "PRCP"])
	precips.extend([item["value"] for item in d["results"] if item["datatype"] == "PRCP"])

df_prec["date"] = [str(date[0:10]).strip() for date in dates]
df_prec["precipitation"] = [value for value in precips]

df = df.merge(df_wind, on="date")
df = df.merge(df_prec, on="date")

df.to_csv("weather_data.csv", index=False)
