#Installing geopy and related packages for geographical plotting 
# !apt install gdal-bin python-gdal python3-gdal --quiet
# !apt install python3-rtree --quiet
# !pip install git+git://github.com/geopandas/geopandas.git --quiet
# !pip install descartes --quiet
# !pip install geopy
# !pip install plotly_express
# !pip install ipython-autotime
# !pip install tqdm==4.62
# %load_ext autotime
import pandas as pd
import numpy as np
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import matplotlib.pyplot as plt
import plotly_express as px
import tqdm
from tqdm import tqdm
from tqdm.notebook import tqdm_notebook

import os

import seaborn as sns
import string

#Loading the stinky, oil vessel and weather data into respective dataframes
url_stinky = 'https://raw.githubusercontent.com/ds5110/stinky/master/smell_data/smell_intermediary_files/df_stinky.csv'
url_vessels = 'https://raw.githubusercontent.com/ds5110/stinky/master/vessels_data/vessels_intermediary_files/df_vessels.csv'
url_weather_master = 'https://raw.githubusercontent.com/ds5110/stinky/master/weather_data/weather_intermediary_files/df_weather_master.csv'


df_stinky = pd.read_csv(url_stinky)
df_vessels = pd.read_csv(url_vessels)
df_weather_master = pd.read_csv(url_weather_master)
df_stinky.head()


def ColToStr(df,column_name):
  """
  input : df - Dataframe, column_name- Name of the column
  This function convert the column name of the dataframe into string type ans return the updated dataframe
  Output : df -Dataframe
  """
  df[column_name]=df[column_name].astype(str)
  return df
df_stinky=ColToStr(df_stinky,'date');

def PreprocessStinky(df):
  """
  input : df -Stinky dataframe
  This function preprocess the stinky dataframe by removing the data for which weather data is unavailable.
  Renaming 'Date & time (hour rounded)' to 'DateTime' and convert it to pandas Datetime object to maintain uniformity while merging with weather dataframe.
  Sorts the datadrame on the basis of DateTime object because we need sorted data to merge dataframes
  returns - updated df
  
    """
  # Removing complaints dated before 2020-09-02
  df=df[df['Date & time (hour rounded)']>'2020-09-02 11:00:00']
  df = df.rename(columns={'Date & time (hour rounded)': 'DateTime'})
  #Renaming Date time column to 'DateTime' and removing the rows where Datetime is not available as we will use this column to merge with weather data
  df=df[df['DateTime'].notnull()]
  #Converting DateTime column to panda's datetime object  
  df['DateTime'] = pd.to_datetime(df['DateTime'])
  # Sorting the dataframe on the basis of DateTime column as we need sorted dataframe to merge the data
  df = df.sort_values('DateTime')
  return df
  
df_stinky1=PreprocessStinky(df_stinky) 


def PreprocessWeather(df):
  """
  Input - Weather dataframe
  This function preprocess the Weather dataframe by renaming 'Date & time (hour rounded)' to 'DateTime' and convert it to pandas Datetime object to maintain uniformity while merging with weather dataframe.
  Sorts the datadrame on the basis of DateTime object because we need sorted data to merge dataframes
  returns - updated df
  """
  #Renaming Date time column to 'DateTime'
  df = df.rename(columns={'Date & time (hour rounded)': 'DateTime'})
  #Converting DateTime column to panda's datetime object  
  df['DateTime'] = pd.to_datetime(df['DateTime'])

  # Sorting the dataframe on the basis of DateTime column as we need sorted dataframe to merge the data
  df = df.sort_values('DateTime')

  #df_weather_master = df_weather_master.sort_values('DateTime', inplace=True)
  return df
df_weather_master= PreprocessWeather(df_weather_master)

# Merging on the basis of DateTime column, the data will be merged on the closest value available from weather data
merged_dataframe = pd.merge_asof(df_stinky1,df_weather_master, on="DateTime")

def AddPodLocations(merged_dataframe,Lat,Long):
  """
  Input - merged_dataframe (dataframe) , Lat(List of Lat that are going to be added), Long(Long of Lat that are going to be added)
  This function add a new column 'Pod/Not Pod' which contains the size, in reference to size of point in geographical plotting.
  Add new rows in the dataframe which contains the location of Pods and different size value for 'Pod/Not Pod' column value
  return- updated dataframe
  """
  #Creating a new Column which will help us in differentiating the pods from complaints while plotting
  merged_dataframe["Pod/Not Pod"]=0.01
  for i in range(len(Lat)):
    merged_dataframe = merged_dataframe.append({'Latitude' : Lat[i],'Longitude' : Long[i],'Cardinal Direction' : '0', 'Pod/Not Pod' : 0.2} , ignore_index=True)
  return merged_dataframe

Lat=[43.659321,43.638339,43.644338,43.653372,43.659877]
Long=[-70.271760,-70.269286,-70.268327,-70.234463,-70.246592]

merged_dataframe=AddPodLocations(merged_dataframe,Lat,Long)

# Merging on the basis of DateTime column, the data will be merged on the closest value available from weather data
merged_dataframe_terminal = pd.merge_asof(df_stinky1,df_weather_master, on="DateTime")
#Adding terminal location in merged dataframe 
Lat=[43.63752544238322,43.63706063528992,43.6498744275754,43.637476254815944,43.63450125967064,43.76226155616127,43.64703757317286]
Long=[-70.26858981462888,-70.28547949671125,-70.2392658465595,-70.28568138856714,-70.27563613665191,-70.14076113096043,-70.24436331996561]

def AddTerminalLocations(merged_dataframe_terminal,Lat,Long):
  """
  This function add a new column 'Terminal/Not Terminal' which contains the size, in reference to size of point in geographical plotting.
  Add new rows in the dataframe which contains the location of Terminals and different size value for 'Terminal/Not Terminal' column value
  """

  #Creating a new Column which will help us in differentiating the pods from complaints while plotting
  merged_dataframe_terminal["Terminal/Not Terminal"]=0.01
  for i in range(len(Lat)):
    merged_dataframe_terminal = merged_dataframe_terminal.append({'Latitude' : Lat[i],'Longitude' : Long[i],'Cardinal Direction' : '0', 'Terminal/Not Terminal' : 0.2} , ignore_index=True)
  return merged_dataframe_terminal

#Final Merged Dataframe
merged_dataframe_terminal=AddTerminalLocations(merged_dataframe_terminal,Lat,Long)

# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# import string

# Creating a new dataframe so that we don't make any changes in original dataframe
#Sorting rows by Average temperature 
temp_df=merged_dataframe.sort_values(by=['Temp Avg'])
# Removing rows with no temperature data
temp_df=temp_df[temp_df['Temp Avg'].notnull()]

#Calculating frequency of complaints on same dates
temp_df['freq'] = temp_df.groupby('date_y')['date_y'].transform('count')
Freq_perday=temp_df.drop_duplicates(subset=['date_y'], keep='last')

#Removing duplicates
Freq_perday.set_index(['Latitude','Longitude']).index.is_unique

#Final dataframe containing Frequency of complaint per day and average temperature of that day 
Freq_perday

print("Complaints vs temperature")

#Plotting Frequency of complains vs Temperature 
fig, ax = plt.subplots()
f=sns.barplot(data=Freq_perday,x='freq',y='Temp Avg',palette='rocket')
f.set(xlabel='Number of complaints',ylabel='Temperature ',title='Number of complaints vs Temperature');
fig.set_size_inches(10,10)

# plt.show()

# import plotly_express as px
px.set_mapbox_access_token("pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w")


def PlotGeographicalData(df,color_seq,hue_column,size_column):
  """
  This function plots the Latitude and Longitude columns of the provided dataframe, representing with different 
  color and size on the basis of values of columns hue_column and size_column respectively.
  """
  df=df.sort_values(by=[hue_column])
  return px.scatter_mapbox(df, lat="Latitude", lon="Longitude",color_discrete_sequence= color_seq , zoom=12, color=hue_column ,size=size_column)
  # box = px.scatter_mapbox(df, lat="Latitude", lon="Longitude",color_discrete_sequence= color_seq , zoom=12, color=hue_column ,size=size_column)
  # plt.show()

print("Cardinal direction")

g1 = PlotGeographicalData(merged_dataframe,px.colors.sequential.Rainbow_r,'Cardinal Direction','Pod/Not Pod')

g1.show()

PlotGeographicalData(merged_dataframe_terminal,px.colors.sequential.Rainbow_r,'Cardinal Direction','Terminal/Not Terminal')


# import plotly_express as px

# Removing complaints for which date is not available
merged_dataframe['Month']=merged_dataframe['Month'].fillna(0)
merged_dataframe=ColToStr(merged_dataframe,'Month');

#Descending the data by date for better visualization
merged_dataframe=merged_dataframe.sort_values('date_y',ascending=False)


PlotGeographicalData(merged_dataframe,px.colors.cyclical.IceFire_r,'Month','Pod/Not Pod')



PlotGeographicalData(merged_dataframe,px.colors.cyclical.mrybm_r,'Wind Direction','Pod/Not Pod')


PlotGeographicalData(merged_dataframe,px.colors.cyclical.mrybm_r,'Temp Avg','Pod/Not Pod')

# Segregation of dataframe on the basis of region

South_portland= df_stinky1[df_stinky1['South Portland/Portland']=='South Portland']
Portland=df_stinky1[df_stinky1['South Portland/Portland']!='South Portland']

#Filtering weather data on the basis of pods that we are considering for South portland and Portland
# Pods for South Portland are SMRO4,SMRO5,SMRO6
# Pods for Portland are SMRO3,SMRO4,SMRO5,SMRO7
df_weather_master_SouthP=df_weather_master[df_weather_master['Pod Name'].isin(['SMRO4','SMRO5','SMRO6']) ]
df_weather_master_Port=df_weather_master[df_weather_master['Pod Name'].isin(['SMRO3','SMRO4','SMRO5','SMRO7']) ]

#Converting DateTime column to pandas datetime object 
df_weather_master_Port['DateTime'] = pd.to_datetime(df_weather_master_Port['DateTime'])
Portland['DateTime'] = pd.to_datetime(Portland['DateTime'])

# Merging on the basis of DateTime column, the data will be merged on the closest value available from weather data
merged_dataframe_Port = pd.merge_asof(Portland,df_weather_master_Port, on="DateTime")

Lat=[43.659321,43.638339,43.644338,43.653372]
Long=[-70.271760,-70.269286,-70.268327,-70.234463]

merged_dataframe_Port=AddPodLocations(merged_dataframe_Port,Lat,Long)

#Adding pods location in merged dataframe 
merged_dataframe_Port['Cardinal Direction'] = merged_dataframe_Port['Cardinal Direction'].fillna(0)

#Drop rows which doesn't contain weather data
merged_dataframe_Port=merged_dataframe_Port.dropna(subset=['Cardinal Direction'])

#Final South Portland stinky and weather data
merged_dataframe_Port

#Converting DateTime column to pandas datetime object 
df_weather_master_SouthP['DateTime'] = pd.to_datetime(df_weather_master_SouthP['DateTime'])
South_portland['DateTime'] = pd.to_datetime(South_portland['DateTime'])
South_portland = South_portland.sort_values('DateTime')

# Merging on the basis of DateTime column, the data will be merged on the closest value available from weather data
merged_dataframe_sp = pd.merge_asof(South_portland,df_weather_master_SouthP, on="DateTime")


Lat=[43.638339,43.644338,43.653372]
Long=[-70.269286,-70.268327,-70.234463]
#Adding pods location in merged dataframe 
merged_dataframe_sp=AddPodLocations(merged_dataframe_sp,Lat,Long)

#Drop rows which doesn't contain weather data
merged_dataframe_sp=merged_dataframe_sp.dropna(subset=['Cardinal Direction'])

#Final South Portland stinky and weather data
merged_dataframe_sp


merged_dataframe_sp=ColToStr(merged_dataframe_sp,'Cardinal Direction');
PlotGeographicalData(merged_dataframe_sp,px.colors.sequential.Rainbow_r,'Cardinal Direction','Pod/Not Pod')

PlotGeographicalData(merged_dataframe_sp,px.colors.sequential.Rainbow_r,'Wind Direction','Pod/Not Pod')


PlotGeographicalData(merged_dataframe_sp,px.colors.sequential.Rainbow_r,'Temp Avg','Pod/Not Pod')

merged_dataframe_Port=ColToStr(merged_dataframe_Port,'Cardinal Direction');
PlotGeographicalData(merged_dataframe_Port,px.colors.sequential.Rainbow_r,'Cardinal Direction','Pod/Not Pod')


PlotGeographicalData(merged_dataframe_Port,px.colors.sequential.Rainbow_r,'Wind Direction','Pod/Not Pod')


PlotGeographicalData(merged_dataframe_Port,px.colors.sequential.Rainbow_r,'Temp Avg','Pod/Not Pod')

plt.show()
