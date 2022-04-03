import csv

import requests


URL = "https://api.smellpittsburgh.org/api/v2/smell_reports"

PARAMS = {
    "format": "json",
    "zipcodes": "4101,4102,4106,4107,4103,4108,4124",
    "start_time": "1644037200",
    "end_time": "1646715599",
    "timezone_string": "America%2FNew_York"
}

OUTPUT_FILE = "smc_data.csv"


header_written = False


with open(OUTPUT_FILE, "w") as data_file:
    try:
        resp = requests.get(url=URL, params=PARAMS)
    except Exception as exc:
        print(f"An exception occurred on GET: {exc}")
        raise
    csv_writer = csv.writer(data_file)

    for row in resp.json():
        if not header_written:
            header = row.keys()
            csv_writer.writerow(header)
            header_written = True

        csv_writer.writerow(row.values())
