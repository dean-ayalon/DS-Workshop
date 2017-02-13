import numpy as np
import pandas as pd


def is_weekend(main_table):

    # Extracting relevant columns from main table
    table = main_table[["display_id", "click_tstamp"]]
    timestamps = table["click_tstamp"]
    # Initializing empty is_weekend array
    is_weekend_boolean = np.zeros(shape=len(timestamps))

    for i in range(len(timestamps)):
        # Format conversions to allow use of is_busday function
        as_datetime64 = np.datetime64(int(timestamps[i]), 's')
        as_datetime = pd.to_datetime(as_datetime64)

        # Using the is_busday function to return an is_weekend boolean - True for Saturday and Sunday, False otherwise
        boolean = np.is_busday(as_datetime, weekmask='0000011')
        is_weekend_boolean[i] = boolean

    # Creating result Dataframe with two columns - display_id and is_weekend
    res_frame = pd.DataFrame()
    res_frame["display_id"] = table["display_id"]
    res_frame["is_weekend"] = is_weekend_boolean

    return res_frame
