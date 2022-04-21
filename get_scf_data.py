import csv

import requests


URL = "https://seeclickfix.com/api/v2/issues"

PARAMS = {
    "min_lat": "43.62737788219894",
    "min_lng": "-70.35352706909181",
    "max_lat": "43.67780454967293",
    "max_lng": "-70.17808914184572",
    "search": "smell",
    "status": "open%2Cacknowledged%2Cclosed",
    "fields%5Bissue%5D": "id%2Csummary%2Cdescription%2Cstatus%2Clat%2Clng%2Caddress%2Cmedia%2Ccreated_at%2Cacknowledged_at%2Cclosed_at",
    "page": 1
}

OUTPUT_FILE = "./output_data/scf_data.csv"


header_written = False
new_results = True
page = 1

# while new_results:
#     with open(OUTPUT_FILE, "w") as data_file:
#         try:
#             resp = requests.get(url=URL, params=PARAMS)
#         except Exception as exc:
#             print(f"An exception occurred on GET: {exc}")
#             raise
#         csv_writer = csv.writer(data_file)
# 
#         if issues := resp.json().get("issues", []):
#             # print(issues)
#             for row in issues.copy():
#                 # print(f"row: {row}")
#                 if not header_written:
#                     header = row.keys()
#                     csv_writer.writerow(header)
#                     header_written = True
# 
#                 csv_writer.writerow(row.values())
#                 # data_file.flush()
#         else:
#             new_results = False
# 
#         print(f"Page {page}")
#         page += 1
#         PARAMS["page"] = page

data_file = open(OUTPUT_FILE, "w")

while new_results:
    try:
        resp = requests.get(url=URL, params=PARAMS)
    except Exception as exc:
        print(f"An exception occurred on GET: {exc}")
        raise
    csv_writer = csv.writer(data_file)

    if issues := resp.json().get("issues", []):
        # print(issues)
        for row in issues:
            # print(f"row: {row}")
            if not header_written:
                header = row.keys()
                csv_writer.writerow(header)
                header_written = True

            csv_writer.writerow(row.values())
            # data_file.flush()
    else:
        new_results = False
        data_file.flush()
        data_file.close()

    print(f"Page {page}")
    page += 1
    PARAMS["page"] = page
