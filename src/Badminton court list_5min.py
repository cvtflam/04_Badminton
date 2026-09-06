import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

response = requests.get(os.getenv("URL"))
today_str = datetime.today().strftime("%Y-%m-%d")
time = datetime.now().strftime("%H:%M:%S")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")
# Furthest available day = 7 days from today
booking_date_max = datetime.today() + timedelta(days=7) 
booking_date_max_str = booking_date_max.strftime("%Y-%m-%d")
# Get the next weekend dates by cal days to sunday from today
weekend_delta = 6 - datetime.today().weekday()
weekend = [datetime.today() + timedelta(days=weekend_delta - 1),
           datetime.today() + timedelta(days=weekend_delta)]
weekend = [date.strftime("%Y-%m-%d") for date in weekend]


# Load data from API into df and clean df. Add record date and time columns
data = response.json()
data_pd = pd.DataFrame(data)
data_pd['Available_Courts'] = data_pd['Available_Courts'].astype(int)
data_pd['Record Date'] = datetime.today().date()
data_pd['Record Time'] = datetime.today().time()

# Filter and sort data for weekday and export to excel
data_pd_filtered = data_pd[~data_pd['Available_Date'].isin(weekend)]

record_path = f'{OUTPUT_PATH}{today_str}_{time}_badminton_record.csv'
if not os.path.exists(record_path):
    data_pd_filtered.to_csv(
        record_path, 
        index=False
    )
else:
    data_pd_filtered.to_csv(record_path, mode='a', index=False, header = False)

# Filter and sort data for weekend and export to excel
data_pd_weekend = data_pd[data_pd['Available_Date'].isin(weekend)]

record_path_weekend = f'{OUTPUT_PATH}{today_str}_{time}_badminton_weekend_record.csv'
if not os.path.exists(record_path_weekend):
    data_pd_weekend.to_csv(
        record_path_weekend, 
        index=False
    )
else:
    data_pd_weekend.to_csv(
        record_path_weekend, 
        mode='a', index=False, header = False
    )