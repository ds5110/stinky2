import csv
import datetime
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

OUTPUT_FILE = "./sample_data/smc_data.csv"


header_written = False


with open(OUTPUT_FILE, "w", newline='') as data_file:
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

            filtered_smc_data.append(complaint)

    for row in filtered_smc_data:
        if not header_written:
            header = row.keys()
            csv_writer.writerow(header)
            header_written = True

        csv_writer.writerow(row.values())