import time
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

complaints_df = pd.read_csv("./output_data/smc_data.csv")
weather_df = pd.read_csv("./output_data/weather_data.csv")

complaints_df["date"] = [time.strftime("%Y-%m-%d", time.strptime(dt, "%c")) for dt in complaints_df["date & time"]]

complaints_df = complaints_df[complaints_df["zipcode"].isin([4101, 4102])]

df = complaints_df.copy()

df = df.merge(weather_df, on="date")

sns.histplot(df, x = "average_temp", shrink=1, bins=100).set(title="Average temperature vs number of complaints (West South Portland)")
plt.show() 
