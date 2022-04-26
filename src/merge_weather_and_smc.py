import time

import numpy as np
import pandas as pd
from sklearn import preprocessing

OUTPUT_FILES = ["./output_data/merged_data.csv", "./website/static/data/merged_data.csv"]


DISTANCES = ["sprague_miles", "portland_pipeline_miles", "south_portland_terminal_miles", "gulf_oil_miles", "global_miles", "citgo_miles"]
# DIRECTIONS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
DIRECTIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

# From https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f 
def calculate_bearing(d):
	ix = int(round(d / (360. / len(DIRECTIONS))))
	return DIRECTIONS[ix % len(DIRECTIONS)]


complaints_df = pd.read_csv("./output_data/smc_data.csv")
weather_df = pd.read_csv("./output_data/weather_data.csv")

complaints_df["date"] = [time.strftime("%Y-%m-%d", time.strptime(dt, "%c")) for dt in complaints_df["date & time"]]

# For South Portland
# complaints_df = complaints_df[complaints_df["zipcode"] > 4105]

# print(weather_df["WDF5"].value_counts())
weather_df["wind_direction"] = weather_df.apply(lambda x: calculate_bearing(x["WDF5"]), axis=1)
print(weather_df["wind_direction"].value_counts())

df = pd.DataFrame()

df["latitude"] = complaints_df["latitude"]
df["longitude"] = complaints_df["longitude"]

df["date"] = weather_df["date"]

for field in DISTANCES:
	df[field] = complaints_df[field]

daily_complaints = pd.DataFrame(complaints_df["date"].value_counts()).reset_index()
daily_complaints.columns = ["date", "daily complaints"]

df = df.merge(daily_complaints, on="date")

df = df.merge(weather_df, on="date")

# 52 rows with inf/NA miles
df = df.dropna()

df["wind_direction"] = df.apply(lambda x: calculate_bearing(x["WDF5"]), axis=1)

enc = preprocessing.OneHotEncoder()

categorical = pd.DataFrame(enc.fit_transform(df[["wind_direction"]]).toarray())

categorical.columns = DIRECTIONS

df = df.join(categorical)

df = df.fillna(0)

for of in OUTPUT_FILES:
	df.to_csv(of, index=False)
