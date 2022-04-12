import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm


complaints_df = pd.read_csv("smc_data.csv")
weather_df = pd.read_csv("weather_data.csv")

complaints_df["date"] = [time.strftime("%Y-%m-%d", time.strptime(dt, "%c")) for dt in complaints_df["date & time"]]

df = pd.DataFrame()

df["date"] = weather_df["date"]

daily_complaints = pd.DataFrame(complaints_df["date"].value_counts()).reset_index()
daily_complaints.columns = ["date", "daily complaints"]

df = df.merge(daily_complaints, on="date")
df = df.merge(weather_df, on="date")

g = sns.scatterplot(x="average_wind", y="daily complaints", data=df)

plt.show()