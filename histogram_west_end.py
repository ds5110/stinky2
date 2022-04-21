import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DIRECTIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

# From https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f 
def calculate_bearing(d):
	ix = int(round(d / (360. / len(DIRECTIONS))))
	return DIRECTIONS[ix % len(DIRECTIONS)]


complaints_df = pd.read_csv("./output_data/smc_data.csv")
weather_df = pd.read_csv("./output_data/weather_data.csv")

complaints_df["date"] = [time.strftime("%Y-%m-%d", time.strptime(dt, "%c")) for dt in complaints_df["date & time"]]

complaints_df = complaints_df[complaints_df["zipcode"].isin([4101, 4102])]

df = complaints_df.copy()

df = df.merge(weather_df, on="date")
df["wind_direction"] = df.apply(lambda x: calculate_bearing(x["WDF5"]), axis=1)

# Sort the histogram by sorting the dataframe
df["wind_direction"] = pd.Categorical(df["wind_direction"], DIRECTIONS)

sns.histplot(df, x="wind_direction").set(title="Wind direction vs number of complaints (West End)")
plt.show()