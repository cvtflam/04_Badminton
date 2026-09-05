import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

response = requests.get(os.getenv("URL"))
today_str = datetime.today().strftime("%Y-%m-%d")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")
# Furthest available day = 7 days from today
booking_date_max = datetime.today() + timedelta(days=7) 
booking_date_max_str = booking_date_max.strftime("%Y-%m-%d")
# Get the next weekend dates by cal days to sunday from today
weekend_delta = 6 - datetime.today().weekday()
weekend = [datetime.today() + timedelta(days=weekend_delta - 1),
           datetime.today() + timedelta(days=weekend_delta)]
weekend = [date.strftime("%Y-%m-%d") for date in weekend]
# Configure districts for weekday and weekend
districts_weekday = ['中西區', '灣仔區', '油尖旺區']
districts_weekend = ['中西區', '灣仔區', '油尖旺區', 
                     '觀塘區', '九龍城區', '西貢區']

# Load data from API into df and clean df
data = response.json()
data_pd = pd.DataFrame(data)
data_pd = data_pd.drop(columns=['District_Name_EN', 'Venue_Name_EN', 
                                'Facility_Type_Name_EN', 'Venue_Address_EN',
                                'Venue_Address_TC', 'Venue_Phone_No.',
                                'Venue_Longitude', 'Venue_Latitude',
                                'Facility_Location_Name_EN',
                                'Facility_Location_Name_TC'])
data_pd['Available_Courts'] = data_pd['Available_Courts'].astype(int)

# Filter and sort data for weekday and export to excel
data_pd_filtered = data_pd[
    (data_pd['District_Name_TC'].isin(districts_weekday)) &
    (data_pd['Available_Courts'] > 0) &
    (data_pd['Available_Date'] != booking_date_max_str) &
    (~data_pd['Available_Date'].isin(weekend))
]

data_pd_filtered_sorted = data_pd_filtered.sort_values(
    by=['Available_Date', 'Venue_Name_TC', 'Session_Start_Time'], 
    ascending = True
)

data_pd_filtered_sorted.to_excel(
    f'{OUTPUT_PATH}{today_str}_badminton_filtered.xlsx', 
    index=False
)

# Filter and sort data for weekend and export to excel
data_pd_weekend = data_pd[
    (data_pd['District_Name_TC'].isin(districts_weekend)) &
    (data_pd['Available_Courts'] > 0) &
    (data_pd['Available_Date'].isin(weekend))
]

data_pd_weekend_sorted = data_pd_weekend.sort_values(
    by=['Available_Date', 'Venue_Name_TC', 'Session_Start_Time'],
    ascending = True
)

data_pd_weekend_sorted.to_excel(
    f'{OUTPUT_PATH}{today_str}_badminton_weekend.xlsx', 
    index=False
)