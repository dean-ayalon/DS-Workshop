# Adapted from https://www.kaggle.com/clustifier/outbrain-click-prediction/pandas-is-cool-lb-0-63714/code

import numpy as np
import pandas as pd

# Currently without any regularization - an ad that appeared 350 times and got clicked 350 times,
# is evaluated the same way as an ad that appeared once and got clicked once


# Accepts the main table as an argument (already as a Pandas object)
def calculate_clicks_per_appearances_ratio(main_table):
    # Slicing only necessary columns
    table = main_table[["ad_id", "clicked"]]
    # Calculating clicks/appearances ratio
    click_ratio_frame = table.groupby("ad_id").clicked.agg(["mean"]).reset_index()

    click_ratio_frame.rename(index=str, columns={"mean": "clicks_appearances_ratio"}, inplace=True)

    # At this point, we have a dataframe with clicks/appearances ratio for each ad in the main table
    # We return it, so it can be merged with the main table in the main procedure for building it
    return click_ratio_frame
