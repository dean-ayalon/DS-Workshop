from utils.plot_utils import *
from utils.table_utils import *
from paths import *
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_ad_appearance(main_table,squared = False,onlyClicks=False):
    #how many times an ad appeared:
    '''
    #this code filters clicks by ad_id. seems to be unnecessary
    clicks = pd.read_csv(CLICKS_YAIR, usecols=['ad_id','clicked'],iterator = True, chunksize = 20000)
    relevant_ads = return_unique_values_of_column_from_table('ad_id',MAIN_TABLE_YAIR)
    filtered_clicks = filter_table_by_unique_ids(relevant_ads,'ad_id',clicks)
    '''
    clicks = pd.read_csv(MAIN_TABLE_YAIR, usecols=['ad_id','clicked'])

    adAppearance = clicks.drop(['clicked'],axis=1)
    adAppearance["appearance"] = adAppearance["ad_id"]
    adAppearance = adAppearance.groupby(["ad_id"],as_index=False).agg({"appearance":np.count_nonzero})

    '''
    adArr = np.array(adAppearance["ad_id"])
    aprArr = np.array(adAppearance["appearance"])

    create_simple_histogram(adArr,aprArr,'Number of time ad appearded',"ad_ID","Appearances","ad_appearance.png")
    '''

    #how many times an ad got a click
    adClicks = clicks.groupby(["ad_id"],as_index=False).agg({"clicked":np.sum})

    #clicks in relation to appearence
    #TODO: we did NOT gave any weight to the apearance, means ad who appeared once and got click will
    #TODO: get the same rate as an ad who appeared 127 times and got 127 clicks. is that right?
    #TODO: maybe it is better just to count clicks? or to power the clicks values by 2? should try.

    clicks_r_appearance = adAppearance.merge(adClicks,on = "ad_id")
    clicks_r_appearance['clicks_per_appearance'] = clicks_r_appearance['clicked']/clicks_r_appearance['appearance']
    clicks_r_appearance.drop(clicks_r_appearance.columns[[1,2]],axis=1,inplace=True)
    return adAppearance

T = create_ad_appearance("")
print(T.head(10))

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

