import re

import pandas as pd

import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import matplotlib.pyplot as plt
import plotly_express as px
import tqdm
from tqdm import tqdm
from tqdm.notebook import tqdm_notebook

# load SMC data
url_all_zips = 'https://raw.githubusercontent.com/ds5110/stinky/master/smell_data/smell_raw_data/smc.csv'
df_smc = pd.read_csv(url_all_zips)
print(df_smc.shape)

# the first rows of df_smc look like this
df_smc.head()

# Check for NA values
df_smc.isna().sum()

# get number of reports by zipcode (look at values in columns with 0 NA values)
df_smc.groupby('zipcode').count()

# add column for city name
df_smc['South Portland/Portland'] = 'Portland'
df_smc.loc[df_smc['zipcode'].isin([4106, 4107]), 'South Portland/Portland'] = "South Portland"

# find out number of Portland vs S Portland rows
df_smc.groupby('South Portland/Portland').count()

def separate_datecols(df, datetime_col):
  # create separate columns for day, month, year, hour and month name
  df['Day'] = col.dt.day
  df['Month'] = col.dt.month
  df['Year'] = col.dt.year
  df['Hour'] = col.dt.hour
  df['Month_name'] = pd.to_datetime(df['Month'], format='%m').dt.month_name().str.slice(stop=3)

  # Create a date and hour column
  df['Date & time (hour rounded)'] = col.dt.strftime("%Y-%m-%d %H:00:00")

# change the date and time column to datetime format
df_smc['date & time'] = df_smc['date & time'].str[0:20]
df_smc['date & time'] = pd.to_datetime(df_smc['date & time'])

# create separate columns for date and time
df_smc['date'] = [d.date() for d in df_smc['date & time']]
df_smc['time'] = [d.time() for d in df_smc['date & time']]

# create separate columns for day, month, year, hour and month name
col = df_smc['date & time']
separate_datecols(df_smc, col)

# rename columns
df_smc.rename(columns={'skewed latitude':'Latitude', 'skewed longitude':'Longitude'}, inplace=True)

# load SCF data
url = 'https://raw.githubusercontent.com/ds5110/stinky/master/smell_data/smell_raw_data/scf.csv'
df_scf=pd.read_csv(url)
print(df_scf.shape)

# the first rows of df_scf look like this
df_scf.head()

# check for NA values 
df_scf.isnull().sum()

# change the date and time column to datetime format
df_scf['Created at local']=pd.to_datetime(df_scf['Created at local'])
df_scf['Closed at local']=pd.to_datetime(df_scf['Closed at local'])

# create separate columns for date and time
df_scf['date'] = [d.date() for d in df_scf['Created at local']]
df_scf['time'] = [d.time() for d in df_scf['Created at local']]

# create separate columns for day, month, year, hour and month name
col = df_scf['Created at local']
separate_datecols(df_scf, col)

# rename columns
df_scf.rename(columns={'Description':'smell description', 'Lat':'Latitude', 'Lng':'Longitude'}, inplace=True)

# We used Google's geocoding API to determine the city of odor reports in df_scf, which contains only addresses (number and street name) and lat/long. 
# This is in case future SCF data includes reports from South Portland.
# More information about the approach in the code below can be found here: 
# https://towardsdatascience.com/the-art-of-geofencing-in-python-e6cc237e172d

# install packages for google geocoding API
# !apt install gdal-bin python-gdal python3-gdal --quiet
# !apt install python3-rtree --quiet
# !pip install git+git://github.com/geopandas/geopandas.git --quiet
# !pip install descartes --quiet
# !pip install geopy
# !pip install plotly_express
# !pip install ipython-autotime
# !pip install tqdm==4.62
# %load_ext autotime
# import pandas as pd

# import geopandas as gpd
# import geopy
# from geopy.geocoders import Nominatim
# from geopy.extra.rate_limiter import RateLimiter

# import matplotlib.pyplot as plt
# import plotly_express as px
# import tqdm
# from tqdm import tqdm
# from tqdm.notebook import tqdm_notebook

# THIS CELL TAKES ~2.5 minutes to run (with 295 rows of data)


# Breaks due to 403s

# create column "address" from lat and long
df_scf["geom"] =  df_scf["Latitude"].map(str)  + ',' + df_scf['Longitude'].map(str)
# locator = Nominatim(user_agent="myGeocoder", timeout=10)
locator = Nominatim(user_agent="stinky", timeout=10)
rgeocode = RateLimiter(locator.reverse, min_delay_seconds=0.001)
tqdm.pandas()
df_scf['address'] = df_scf['geom'].progress_apply(rgeocode)

# create 'South Portland/Portland' column and filter out any South Portland entries
# import re
df_scf['South Portland/Portland'] = 'Portland'
df_scf.loc[df_scf['address'].str.contains('South Portland', na=False), 'South Portland/Portland'] = "South Portland"

# Merge two datasets
df_stinky = df_scf.append(df_smc, sort=False)

# the first rows of df_stinky look like this
df_stinky.head()

# there are 350 reports for 2019, 1802 for 2020, and 755 for 2021
df_stinky.groupby('Year').count()

# check that common columns were correctly merged
df_stinky.isnull().sum()

# look into missing 'smell description' data to check there were no merge errors
print('SCF has {} null smell description rows'.format(df_scf['smell description'].isnull().sum()))
print('SMC has {} null smell description rows'.format(df_smc['smell description'].isnull().sum()))
print('Merged df has {} null smell description rows'.format(df_stinky['smell description'].isnull().sum()))

# download tidied df_stinky
# from google.colab import files
df_stinky.to_csv('df_stinky.csv', index=False) 
# files.download('df_stinky.csv')
