import numpy as np
import pandas as pd

# Performing one-hot-encoding on the categorical platform feature


def add_platform_one_hot_encoding_feature(main_table):
    platforms_frame = main_table.groupby("display_id").first().reset_index()

    # Extracting the platform vector and creating 3 boolean vectors based on it
    platforms = platforms_frame["platform"]
    platform_is_desktop = np.array(platforms == 1, dtype=int)
    platform_is_mobile = np.array(platforms == 2, dtype=int)
    platform_is_tablet = np.array(platforms == 3, dtype=int)

    # Creating the result Dataframe
    res_frame = pd.DataFrame()
    res_frame["display_id"] = platforms_frame["display_id"]
    res_frame["platform_is_desktop"] = platform_is_desktop
    res_frame["platform_is_mobile"] = platform_is_mobile
    res_frame["platform_is_tablet"] = platform_is_tablet

    return res_frame