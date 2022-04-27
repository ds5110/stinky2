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

complaints_df = complaints_df[complaints_df["zipcode"] == 4106]
complaints_df = complaints_df[complaints_df["longitude"] < -70.26]

df = complaints_df.copy()

df = df.merge(weather_df, on="date")
df["wind_direction"] = df.apply(lambda x: calculate_bearing(x["WDF5"]), axis=1)

# Sort the histogram by sorting the dataframe
df["wind_direction"] = pd.Categorical(df["wind_direction"], DIRECTIONS)

sns.histplot(df, x="wind_direction").set(title="Wind direction vs number of complaints (West SoPo)")
plt.show()

weather_df["wind_direction"] = weather_df.apply(lambda x: calculate_bearing(x["WDF5"]), axis=1)
complaints_by_wd_df = pd.DataFrame(df["wind_direction"].value_counts()).reset_index()
wd_freq_df = pd.DataFrame(weather_df["wind_direction"].value_counts()).reset_index()

complaints_by_wd_df.columns = ["wind_direction", "num_complaints"]
wd_freq_df.columns = ["wind_direction", "num_days"]

merged_df = pd.merge(complaints_by_wd_df, wd_freq_df, on="wind_direction")

merged_df["freq"] = merged_df["num_complaints"]/merged_df["num_days"]

merged_df.drop("num_complaints", axis=1, inplace=True)
merged_df.drop("num_days", axis=1, inplace=True)

merged_df["wind_direction"] = pd.Categorical(merged_df["wind_direction"], DIRECTIONS)

print(merged_df)

ax = sns.histplot(data=merged_df, x="wind_direction", weights="freq")

ax.set(title="Frequency of complaints by wind direction (West SoPo)")

plt.show()