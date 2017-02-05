from utils.plot_utils import *
from utils.table_utils import *
from paths import *
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_ad_appearance(main_table):
    #how many times an ad appeared:
    clicks = pd.read_csv(CLICKS_YAIR, usecols=['ad_id','clicked'])
    relevant_ads = return_unique_values_of_column_from_table('ad_id',main_table)
    filtered_clicks = filter_table_by_unique_ids(relevant_ads,'ad_id',clicks)

    adAppearance = filtered_clicks.drop(['clicked'],axis=1)
    adAppearance["appearance"] = adAppearance["ad_id"]
    adAppearance = adAppearance.groupby(["ad_id"],as_index=False).agg({"appearance":np.count_nonzero})

    '''
    adArr = np.array(adAppearance["ad_id"])
    aprArr = np.array(adAppearance["appearance"])

    create_simple_histogram(adArr,aprArr,'Number of time ad appearded',"ad_ID","Appearances","ad_appearance.png")
    '''

    #how many times an ad got a click

    adClicks = filtered_clicks.groupby(["ad_id"],as_index=False).agg({"clicked":np.sum})
    adAppearance = adAppearance.merge(adClicks,on = "ad_id")
    adAppearance['clicks_per_appearance'] = adAppearance['clicked']/adAppearance['appearance']
    adAppearance.drop(adAppearance.columns[[1,2]],axis=1,inplace=True)
    return adAppearance

'''
adArr = np.array(adClicks["ad_id"])
clicksArr = np.array(adClicks[["clicked"]])

#TODO from some reason on Yairs computer runs get stuck, be carful if you ren this.
create_simple_histogram(adArr,clicksArr,'Number of time ad got clicked',"Ad_ID","Clicks","clicks_per_ad.png")

#a plot which shows per ad_id: #appearance - (#appearances-#clicks) assume #appearnces>=#clicks

aprClkArr = [0 for x in range(len(clicksArr))]
for i in range(len(clicksArr)):
    aprClkArr[i] = clicksArr[i]/aprArr[i]
aprClkArr = np.array(aprClkArr)

create_simple_histogram(adArr,aprClkArr,'Clicks/Appearances per ad',"Ad_ID","Clicks/Appearances","Clicks_Appearances_per_ad.png")
'''

