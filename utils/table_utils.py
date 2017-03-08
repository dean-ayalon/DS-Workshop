import numpy as np
import pandas as pd


#given a table name and a column name - returns only unique appearences of value from that column
def return_unique_values_of_column_from_table(column_name,table_name):
    unique_column = pd.Series(np.array(table_name[column_name])).unique()
    return unique_column

#this function gets an ITERATOR, which is table_to_filter
def filter_table_by_unique_ids(filter_column,column_to_filter,table_to_filter):
    table_itr = pd.read_csv(table_to_filter, iterator=True, chunksize=1000000)
    filtered_table = pd.concat([chunk[chunk[column_to_filter].isin(filter_column)] for chunk in table_itr])
    return filtered_table

#this function returns a Dataframe with the number of clicks each advertiser or campaign got.
def get_clicks_per_advertiser_or_campaign(main_table,promoted,adv_or_camp):
    advertisers = promoted[["ad_id",adv_or_camp]]
    clicks = main_table[["ad_id","clicked"]]
    adv_clicks = advertisers.merge(clicks,on="ad_id")
    adv_clicks = adv_clicks.groupby([adv_or_camp], as_index=False).agg({"clicked": np.sum})\
        .rename(index=str, columns={"clicked": "clicks"})
    return adv_clicks

#returns the number of ads each advertiser or campagin has.
def get_ads_per_feat(promoted,adv_or_camp):
    # Counting the number of times an advertiser appeared:
    ad_per_advertiser = promoted.groupby([adv_or_camp], as_index=False).agg({"ad_id": np.count_nonzero})\
        .rename(index=str, columns={"ad_id": "ads_per_advertiser"})
    return ad_per_advertiser

#returns a DataFrame, which for eac feature id counts the feature appearance in the table.
def count_feature(table,feature_name):
    # Extracting the display_id's vector from main table
    feature_to_count = table[[feature_name]]

    # Counting how many times every display_id appears in the vector - this equals the ad count per each display
    ad_counts = displays_and_ads.groupby(feature_name).feature_name.agg("count")
    ad_counts = pd.Series(ad_counts.as_matrix())

    # Extracting vector of unique displays
    displays = displays_and_ads["display_id"].unique()

    # Creating result Dataframe, contaning the ad count for each display_id
    # (has only display_id and ad_count columns)
    res_frame = pd.DataFrame()
    res_frame["display_id"] = displays
    res_frame["ad_count_per_display"] = ad_counts.astype(int)

    return res_frame

