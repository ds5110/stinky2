import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DIRECTIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']


# From https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f 
def calculate_bearing(d):
	ix = int(round(d / (360. / len(DIRECTIONS))))
	return DIRECTIONS[ix % len(DIRECTIONS)]


weather_df = pd.read_csv("./output_data/weather_data.csv")

weather_df["wind_direction"] = weather_df.apply(lambda x: calculate_bearing(x["WDF5"]), axis=1)

df = weather_df.copy()

df["wind_direction"] = pd.Categorical(df["wind_direction"], DIRECTIONS)

sns.histplot(df, x="wind_direction").set(title="Number of days the strongest 5-minute wind blew from each direction")

plt.show()