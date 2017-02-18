# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 18:50:07 2017

@author: Eran
"""

from utils.plot_utils import *
from utils.table_utils import return_unique_values_of_column_from_table, filter_table_by_unique_ids
from paths import *

import numpy as np
import pandas as pd


def campaign_freq(main_table,promoted):
    campaigns = promoted["campaign_id"]
    ##creating a dict for number of times a campain appears
    campaign_map = {}
    for campaign in campaigns:
        ##if action was not yet done
        if campaign not in campaign_map: 
            ##add the sum of appearences of a specific campaign in campaigns
            campaign_map[campaign] = (campaigns == campaign).sum()
    ads = main_table["ad_id"]
    pop_vector = [] ##the popularity vector for each ad in main_table
    #adding all popularity measures obtained from the dict
    for ad in ads:
        ##the campaign of the ad
        ad_campaign = promoted.loc[promoted['ad_id'] == ad]["campaign_id"]
        if ad_campaign.empty: ##if there is no campaign for this add in campaigns
            pop_vector.append((ad,0))
            continue
        ad_campaign = ad_campaign.iat[0] ##converting value to int
        if ad_campaign in campaign_map:
            pop_vector.append((ad,campaign_map[ad_campaign])) ##appending popularity measure for ad
        else:
            pop_vector.append((ad,0))
    ##returns the popularity vector for the main table
    return pop_vector
    

'''
##in order to add the pop_vector to the main_table
campaign_freq = advertiser_freq(main_table,promoted)
df = pandas.DataFrame(campaign_freq,columns = ["ad_id","campaign_freq"])
main_table.merge(df)
'''

main_t = pd.read_csv(MAIN_TABLE_YAIR)
promoted = pd.read_csv(PROMOTED_CONTENT_YAIR)

a = campaign_freq(main_t[:100],promoted[:100])
print(a)