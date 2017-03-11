import pandas as pd


def add_ad_count_per_display_feature(main_table):
    # Extracting the display_id's vector from main table
    displays_and_ads = main_table[["display_id"]]

    # Counting how many times every display_id appears in the vector - this equals the ad count per each display
    ad_counts = displays_and_ads.groupby("display_id").display_id.agg("count")
    ad_counts = pd.Series(ad_counts.as_matrix())

    # Extracting vector of unique displays
    displays = displays_and_ads["display_id"].unique()

    # Creating result Dataframe, containing the ad count for each display_id
    # (has only display_id and ad_count columns)
    res_frame = pd.DataFrame()
    res_frame["display_id"] = displays
    res_frame["ad_count_per_display"] = ad_counts.astype(float)

    return res_frame
