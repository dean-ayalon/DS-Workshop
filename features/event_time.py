import numpy as np
import pandas as pd


# This feature corrects click timestamps for timezone differences
# in the 4 most common countries in the data: US, Canada, Great Britain and Australia.
# After this correction is applied, the resulting times are "binned" into
# 5 different periods using boolean vectors:
# Morning - 7:00 to 11:59
# Noon - 12:00 to 15:59
# Afternoon - 16:00 to 19:59
# Evening - 20:00 to 23:59
# Night - 00:00 to 06:59


def add_event_time_bin_feature(main_table):
    working_table = main_table.groupby("display_id").first().reset_index()

    relevant_countries = ["CA", "US", "AU", "GB"]
    hours = list(range(24))  # Used to make hour calculations in modulo 24

    click_timestamps = working_table["click_tstamp"]
    geolocations = working_table["geo_location"].apply(str)

    # Timezone correction for the 4 most common countries in the data
    localized_hours = []
    for i in range(len(geolocations)):
        country = geolocations[i][:2]
        timezone_correction = 0
        if country in relevant_countries:
            if country == "GB":
                timezone_correction = 1
            elif country == "CA" or country == "US":
                timezone_correction = -5
            elif country == "AU":
                timezone_correction = 10
        timestamp = click_timestamps[i]
        as_datetime64 = np.datetime64(int(timestamp), 's')
        as_datetime = pd.to_datetime(as_datetime64)
        corrected_hour = as_datetime.hour + timezone_correction
        if corrected_hour > 23:
            corrected_hour -= 24
        localized_hour = hours[corrected_hour]
        localized_hours.append(localized_hour)


    # Creating boolean vectors for "binning" the hours
    localized_hours = pd.Series(localized_hours)
    is_morning = np.zeros(shape=len(working_table))
    is_noon = np.zeros(shape=len(working_table))
    is_afternoon = np.zeros(shape=len(working_table))
    is_evening = np.zeros(shape=len(working_table))
    is_night = np.zeros(shape=len(working_table))

    for i in range(len(localized_hours)):
        if 7 <= localized_hours[i] < 12:
            is_morning[i] = 1
        elif 12 <= localized_hours[i] < 16:
            is_noon[i] = 1
        elif 16 <= localized_hours[i] < 20:
            is_afternoon[i] = 1
        elif 20 <= localized_hours[i] < 24:
            is_evening[i] = 1
        elif 0 <= localized_hours[i] < 7:
            is_night[i] = 1

    res_table = pd.DataFrame()
    res_table["display_id"] = working_table["display_id"]
    res_table["is_morning"] = is_morning
    res_table["is_noon"] = is_noon
    res_table["is_afternoon"] = is_afternoon
    res_table["is_evening"] = is_evening
    res_table["is_night"] = is_night

    return res_table
