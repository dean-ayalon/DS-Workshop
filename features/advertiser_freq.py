# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 12:09:00 2017

@author: Eran
"""

from utils.plot_utils import *
from utils.table_utils import return_unique_values_of_column_from_table, filter_table_by_unique_ids
from paths import *

import numpy as np
import pandas as pd

#TODO: why do we need main here? the ad_ids are in promoted. can't we just use them?
def advertiser_freq(main_table,promoted):
    #loading the relevant tables
    ad_advertisers = promoted[["ad_id","advertiser_id"]]

    #TODO: this replaces PART 1
    #counting the number of times an advertiser appeared:
    ad_per_acvertiser = ad_advertisers.groupby(["advertiser_id"],as_index=False).agg({"ad_id":np.count_nonzero})\
        .rename(index=str, columns={"ad_id" : "ads_per_advertiser"})
    #TODO: replace PART 2
    advertiser_freq_per_ad = ad_advertisers.merge(ad_per_acvertiser, on="advertiser_id")
    advertiser_freq_per_ad.drop(['advertiser_id'],axis=1, inplace=True)
    return advertiser_freq_per_ad

    '''
    PART 1:
    #generates a tuple array of (ad_id,advertiser_freq)
    advertisers = promoted["advertiser_id"]
    ##creating a dict for number of times a campain appears
    advertiser_map = {}
    for advertiser in advertisers:
        ##if action was not yet done
        if advertiser not in advertiser_map:
            ##add the sum of appearences of a specific campaign in campaigns
            advertiser_map[advertiser] = (advertisers == advertiser).sum()
    '''

    '''
    ads = main_table["ad_id"]
    pop_vector = [] ##the popularity vector for each ad in main_table
    #adding all popularity measures obtained from the dict
    for ad in ads:
        ##the campaign of the ad
        ad_advertiser = promoted.loc[promoted['ad_id'] == ad]["advertiser_id"]
        if ad_advertiser.empty: ##if there is no campaign for this add in campaigns
            pop_vector.append((ad,0))
            continue
        ad_advertiser = ad_advertiser.iat[0] ##converting value to int
        if ad_advertiser in advertiser_map:
            pop_vector.append((ad,advertiser_map[ad_advertiser])) ##appending popularity measure for ad
        else:
            pop_vector.append((ad,0))
    ##returns the popularity vector for the main table
    return pop_vector
    '''
    
    
'''
##in order to add the pop_vector to the main_table
advertisers_freq = advertiser_freq(main_table,promoted)
df = pandas.DataFrame(advertisers_freq,columns = ["ad_id","advertiser_freq"])
main_table.merge(df)
'''

main_table = pd.read_csv(MAIN_TABLE_YAIR)
promoted = pd.read_csv(PROMOTED_CONTENT_YAIR)
a = advertiser_freq(main_table,promoted)
print(a.head(100))