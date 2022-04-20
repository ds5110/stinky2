# stinky2
Turning stinky into a production site

## Local development

Install requirements via `pip3 install -r requirements.txt`.

Navigate to `/website` and run `run_site.py`.

## Generating data

To create CSV files for smell complaints and weather, run `get_smc_data.py` and `get_weather_data.py`.

Retrieving weather data requires an [API token](https://www.ncdc.noaa.gov/cdo-web/token). 

## EDA results

<img src="img/scatter_temp_vs_complaints.png" width="500px">

<img src="img/scatter_wind_vs_complaints.png" width="500px">

<img src="img/wc_hist_east_sopo.png" width="500px">

<img src="img/wc_hist_west_sopo.png" width="500px">

<img src="img/wc_hist_west_end.png" width="500px">
