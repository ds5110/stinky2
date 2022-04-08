import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import string

weather = pd.read_csv('WeatherData-2020-2022.csv')
complaints = pd.read_csv('smc_data.csv', encoding = 'ISO-8859-1')


def PreprocessWeather(df):
  #Renaming Date time column to 'DateTime'
  df = df.rename(columns={'DATE': 'DATE & TIME'})
  df['DATE & TIME'] = pd.to_datetime(df['DATE & TIME'])

  df=df[df['DATE & TIME'].notnull()]
  # Sorting based on Date & Time column to merge dataframes
  df = df.sort_values('DATE & TIME')
  return df

weather= PreprocessWeather(weather)
weather.head()

def PreprocessComplaints(df):
  # Update to consistent column name
  df = df.rename(columns={'date & time': 'DATE & TIME'})
  df['DATE & TIME'] = pd.to_datetime(df['DATE & TIME'])

  df=df[df['DATE & TIME'].notnull()]
  # Sorting the dataframe on the basis of Date & Time column as we need sorted dataframe to merge the data
  df = df.sort_values('DATE & TIME')
  return df

complaints= PreprocessComplaints(complaints)
complaints.head()


#Merging weather data with complaints data on "DATE & TIME"
merged_dataframe = pd.merge_asof(weather, complaints, on="DATE & TIME")
merged_dataframe.head()

#Merging weather data with complaints data
merged_dataframe = pd.merge_asof(weather, complaints, on="DATE & TIME")
merged_dataframe.to_csv('mergedWeatherAndComplaints.csv')

"""
def AddPodLocations(merged_dataframe,Lat,Long):
  merged_dataframe["Pod/Not Pod"] = 0.01
  for i in range(len(Lat)):
    merged_dataframe = merged_dataframe.append({'Latitude' : Lat[i],'Longitude' : Long[i],'Cardinal Direction' : '0', 'Pod/Not Pod' : 0.2} , ignore_index=True)
  return merged_dataframe

Lat=[43.659321,43.638339,43.644338,43.653372,43.659877]
Long=[-70.271760,-70.269286,-70.268327,-70.234463,-70.246592]

merged_dataframe=AddPodLocations(merged_dataframe,Lat,Long)
merged_dataframe.head()


#Temperature and Frequency of complaints
temp_df = weather.sort_values(by=['TMP'])
temp_df = temp_df[temp_df['TMP'].notnull()]

temp_df['freq'] = temp_df.groupby('DATE & TIME')['DATE & TIME']
Freq = temp_df.drop_duplicates(subset=['DATE & TIME'], keep='last')
Freq.set_index(['LATITUDE','LONGITUDE']).index.is_unique

#Visualizing Frequency of complains vs Temperature 
fig, ax = plt.subplots()
f=sns.barplot(data=Freq,x='freq',y='TMP',palette='rocket')
f.set(xlabel='Number of complaints',ylabel='Temperature ',title='Number of complaints vs Temperature');

temp_df.head()
"""
