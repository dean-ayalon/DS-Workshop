# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 18:50:07 2017

@author: Eran
"""
'''
from utils.plot_utils import *
from utils.table_utils import return_unique_values_of_column_from_table, filter_table_by_unique_ids
from paths import *
'''

import numpy as np
import pandas as pd

# Similar to advertiser_freq, returns a mapping of ads and their campaign's "frequency"
# That is, num. of ads belonging to same campaign

#promoted = pd.read_csv(r"C:\Users\Dean\Documents\Semester G\Data Science Workshop\Outbrain Data\promoted_content.csv")
#promoted = pd.read_csv()

def campaign_freq(promoted):
    # Loading the relevant tables
    ad_campaigns = promoted[["ad_id", "campaign_id"]]
    # Counting the number of times an advertiser appeared:
    ad_per_campaign = ad_campaigns.groupby(["campaign_id"], as_index=False).agg({"ad_id": np.count_nonzero})\
        .rename(index=str, columns={"ad_id": "ads_per_campaign"})
    campaign_freq_per_ad = ad_campaigns.merge(ad_per_campaign, on="campaign_id", copy=False)
    campaign_freq_per_ad.drop(['campaign_id'], axis=1, inplace=True)
    return campaign_freq_per_ad


'''
##in order to add the pop_vector to the main_table
campaign_freq = advertiser_freq(main_table,promoted)
df = pandas.DataFrame(campaign_freq,columns = ["ad_id","campaign_freq"])
main_table.merge(df)
'''
