# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 12:09:00 2017

@author: Eran
"""
'''
from utils.plot_utils import *
from utils.table_utils import return_unique_values_of_column_from_table, filter_table_by_unique_ids
from paths import *
'''
import numpy as np
import pandas as pd

# Returns a map of ads and the number of times their advertiser published an ad.


def advertiser_freq(promoted):
    # Loading the relevant tables
    ad_advertisers = promoted[["ad_id", "advertiser_id"]]
    # Counting the number of times an advertiser appeared:
    ad_per_advertiser = ad_advertisers.groupby(["advertiser_id"], as_index=False).agg({"ad_id": np.count_nonzero})\
        .rename(index=str, columns={"ad_id": "ads_per_advertiser"})
    advertiser_freq_per_ad = ad_advertisers.merge(ad_per_advertiser, on="advertiser_id")
    advertiser_freq_per_ad.drop(['advertiser_id'], axis=1, inplace=True)
    return advertiser_freq_per_ad
'''

a = advertiser_freq(promoted)
##printing first 100 results
print(a.head(100))
##join with main_table:
main_table.merge(a)
'''