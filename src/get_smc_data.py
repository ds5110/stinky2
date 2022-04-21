import csv
import datetime
import math
import time

import requests


URL = "https://api.smellpittsburgh.org/api/v2/smell_reports"

PARAMS = {
    "format": "json",
    "zipcodes": "4101,4102,4106,4107,4103,4108,4124",
    "start_time": "1577836800", # Jan 1 2020 12:00 AM
    "end_time": int(time.time()), # right meow
    "timezone_string": "America%2FNew_York"
}

OUTPUT_FILES = ["./output_data/smc_data.csv", "./website/static/data/smc_data.csv"]


header_written = False

# Addresses found in Maine DEP report
# https://www.protectsouthportland.com/_files/ugd/6281f2_699328196df94c75a61f58fd4824abc2.pdf

# Lat long found using https://www.latlong.net/convert-address-to-lat-long.html

tank_coord_deg = {
    "sprague": (43.637210, -70.286400),
    "portland_pipeline": (43.629500, -70.271290),
    "south_portland_terminal": (43.635930, -70.285290),
    "gulf_oil": (43.650240, -70.239670),
    "global": (43.634410, -70.284430),
    "citgo": (43.637009, -70.267303)
}

for of in OUTPUT_FILES:
    with open(of, "w", newline='') as data_file:
        try:
            resp = requests.get(url=URL, params=PARAMS)
        except Exception as exc:
            print(f"An exception occurred on GET: {exc}")
            raise
        csv_writer = csv.writer(data_file)

        raw_smc_data = resp.json()

        filtered_smc_data = []

        for complaint in raw_smc_data:
            # For some reason the API will include other zip codes including NoneType and boolean values
            if complaint["zipcode"] and len(complaint["zipcode"]) <= 5 and int(complaint["zipcode"]) in [4101, 4102, 4106, 4107, 4103, 4108, 4124]:
                complaint["epoch time"] = complaint["observed_at"]
                complaint["date & time"] = time.ctime(complaint["observed_at"])
                complaint["date"] = datetime.datetime.fromtimestamp(complaint["observed_at"]).strftime('%x')
                complaint.pop("observed_at")
                lat1 = complaint["latitude"] / (180 / math.pi)
                lon1 = complaint["longitude"] / (180 / math.pi)
                for tank, coord in tank_coord_deg.items():
                    lat2 = float(coord[0]) / (180 / math.pi)
                    lon2 = float(coord[1]) / (180 / math.pi)
                    dist = 3963 * math.acos((math.sin(lat1)*math.sin(lat2)) + math.cos(lat1)*math.cos(lat2)*math.cos(lon2 - lon1))
                    complaint[tank + "_miles"] = dist

                filtered_smc_data.append(complaint)

        for row in filtered_smc_data:
            if not header_written:
                header = row.keys()
                csv_writer.writerow(header)
                header_written = True

            csv_writer.writerow(row.values())