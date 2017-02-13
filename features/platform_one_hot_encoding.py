import numpy as np
import pandas as pd

# Performing one-hot-encoding on the categorical platform feature


def platform_one_hot_encoding(main_table):

    # Extracting the platform vector and creating 3 boolean vectors based on it
    platforms = main_table["platform"]
    platform_is_desktop = platforms == 1
    platform_is_mobile = platforms == 2
    platform_is_tablet = platforms == 3

    # Creating the result Dataframe
    res_frame = pd.DataFrame()
    res_frame["display_id"] = main_table["display_id"]
    res_frame["platform_is_desktop"] = platform_is_desktop
    res_frame["platform_is_mobile"] = platform_is_mobile
    res_frame["platform_is_tablet"] = platform_is_tablet

    return res_frame
