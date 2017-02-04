import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.plot_utils import *


#how many times an ad appeared:
adAppearance = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv",
                     nrows=1000000, usecols=["ad_id"])

adAppearance["appearance"] = adAppearance["ad_id"]
adAppearance = adAppearance.groupby(["ad_id"],as_index=False).agg({"appearance":np.count_nonzero})

adArr = np.array(adAppearance["ad_id"])
aprArr = np.array(adAppearance["appearance"])

create_simple_histogram(adArr,aprArr,'Number of time ad appearded',"ad_ID","Appearances","ad_appearance.png")


#how many times an ad got a click

adClicks = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv",
                     nrows=1000000, usecols=["ad_id","clicked"])
adClicks = adClicks.groupby(["ad_id"],as_index=False).agg({"clicked":np.sum})
adArr = np.array(adClicks["ad_id"])
clicksArr = np.array(adClicks[["clicked"]])

create_simple_histogram(adArr,clicksArr,'Number of time ad got clicked',"Ad_ID","Clicks","clicks_per_ad.png")


#a plot which shows per ad_id: #appearance - (#appearances-#clicks) assume #appearnces>=#clicks

aprClkArr = [0 for x in range(len(clicksArr))]
for i in range(len(clicksArr)):
    aprClkArr[i] = clicksArr[i]/aprArr[i]
aprClkArr = np.array(aprClkArr)

create_simple_histogram(adArr,aprClkArr,'Clicks/Appearances per ad',"Ad_ID","Clicks/Appearances","Clicks_Appearances_per_ad.png")

'''
sum0 = 0
for x in aprClkArr:
    if x==0:
        sum0 += 1

sum1 = 0
for x in aprClkArr:
    if x==1:
        sum1 += 1
'''

