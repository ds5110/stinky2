
get_data:
	python3 -B src/get_smc_data.py
	python3 -B src/get_weather_data.py

merge_data:
	python3 -B src/merge_weather_and_smc.py
	python3 -B src/merge_for_east_end.py
	python3 -B src/merge_for_east_sopo.py
	python3 -B src/merge_for_west_sopo.py

scatterplot:
	python3 -B src/scatter.py

histogram:
	python3 -B src/histogram_east_end.py
	python3 -B src/histogram_east_sopo.py
	python3 -B src/histogram_west_sopo.py
	python3 -B src/histogram_temp_east_end.py
	python3 -B src/histogram_temp_east_sopo.py
	python3 -B src/histogram_temp_west_sopo.py

regression:
	python3 -B src/sopo_regression.py
