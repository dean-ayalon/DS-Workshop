import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from paths import *
from utils.table_utils import get_clicks_per_advertiser_or_campaign, get_ads_per_feat

#main_table = pd.read_csv(MAIN_TABLE_YAIR)
#promoted = pd.read_csv(PROMOTED_CONTENT_YAIR)

#TODO: consider change this to be like in the platform histogram
def create_simple_histogram(categoryArr,countArr,title,x_label,y_label,file_name='',
                            do_print=False):
    fig = plt.figure()
    fig.suptitle(title,fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.bar(left=categoryArr, height=countArr)
    if(do_print):
        plt.savefig(file_name)
    #plt.show()

#creates a platform with two types of bars, mostly use to compare amount of clicks
#against the amount of some feature_ids, in order to see their popularity.
def create_two_bars_histogram(sample_size,feature_count,clicks,feature_ids,title,x_label,y_label):
    place_on_chart = np.dot(np.arange(sample_size),2)
    width = 0.5
    fig, ax = plt.subplots()
    adv_cnt_bars = ax.bar(place_on_chart,feature_count,width,color="r")
    clicks_cnt_bars = ax.bar(place_on_chart+width,clicks,width)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(place_on_chart + width / 2)
    ax.set_xticklabels(feature_ids, rotation=90, rotation_mode="anchor", ha="right",size=7)
    ax.legend((adv_cnt_bars[0],clicks_cnt_bars[0]),('ads','clicks'),loc='center left',bbox_to_anchor=(1, 0.5))

    #plt.savefig("testRand1.png")


#creates the histogram of the platforms
def plot_platform_histogram(main_table):
    platforms_count = main_table[["platform_is_desktop","platform_is_mobile","platform_is_tablet"]]
    platforms_count = np.array(platforms_count.sum())
    platforms_names = np.array(["Desktop","Mobile","Tablet"])
    fig = plt.figure()
    fig.suptitle("Amount of platforms",fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel("Platform type")
    ax.set_ylabel("Amount")
    width = 0.3
    bins = list(map(lambda x: x - width / 2, range(1, len(platforms_count) + 1)))
    ax.bar(bins, platforms_count, width=width)
    ax.set_xticks(list(map(lambda x: x, range(1, len(platforms_count) + 1))))
    ax.set_xticklabels(platforms_names)

    #plt.bar(left=platforms_names, height=platforms_count)
    #plt.savefig("test.png")
    #plt.show()

#creates a pie chart which show the amount of each display from some size,
#where size is the number of ads in it.
def create_disp_number_piechart(main_table):
    disp_size = main_table[["display_id","ad_id"]]
    disp_size = disp_size.groupby(["display_id"],as_index=False).agg({"ad_id":np.count_nonzero})\
        .rename(index=str, columns={"ad_id" : 'disp_size'})
    disp_size_count = disp_size.groupby(["disp_size"],as_index=False).agg({"display_id":np.count_nonzero})\
        .rename(index=str, columns={"display_id" : 'disp_size_count'})
    disp_size_count_arr = np.array(disp_size_count['disp_size_count'])
    disp_size_type = np.array(disp_size_count['disp_size'])

    #now create the pie chart
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    fig1, ax1 = plt.subplots()
    ax1.pie(disp_size_count_arr, labels=disp_size_type, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    #plt.savefig('test.png')

#create two bar type histogram of advertiser and campaign
def create_advertiser_or_campaign_pop_histogram(main_table,promoted,adv_or_camp,title):
    adv_no=50
    adv_clicks = get_clicks_per_advertiser_or_campaign(main_table,promoted,adv_or_camp)
    ad_per_feat = get_ads_per_feat(promoted,adv_or_camp)
    data = adv_clicks.merge(ad_per_feat,on=adv_or_camp)

    indexes = np.random.RandomState(1).permutation(len(data))[:adv_no]
    adv_cnt = np.array(data["ads_per_feature"][indexes])
    clicks = np.array(data["clicks"][indexes])
    adv_id = np.array(data[adv_or_camp][indexes])

    #ploting:
    create_two_bars_histogram(adv_no,adv_cnt,clicks,adv_id,title,
                              adv_or_camp,"Count")


def create_ads_clicks_histogram(main_table,create_ad_appearance = False):
    pd.options.mode.chained_assignment = None  # default='warn'
    #prepare data to plot:
    ads = main_table[["ad_id"]]
    ads["amount"] = main_table["ad_id"].copy()
    ads = ads.groupby(["ad_id"], as_index=False).agg({"amount": np.count_nonzero})
    clicks = main_table.groupby(["ad_id"], as_index=False).agg({"clicked": np.sum})

    indexes = np.random.RandomState(1).permutation(len(ads))[:30000]
    ads_id = np.array(ads["ad_id"])[indexes]
    ads_count = np.array(ads["amount"])[indexes]
    clicks_count = np.array(clicks["clicked"])[indexes]
    if(create_ad_appearance):
        create_simple_histogram(ads_id,ads_count, "Number of times an ad appeared",
                                "Ad id","Ad count")#,"ad_appearance.png",do_print=True)
    else:
        create_simple_histogram(ads_id,clicks_count,"Number of times an ad got clicked",
                                "Ad id","Click count")#,"ad_clicks.png",do_print=True)

    '''
    indexes = np.random.RandomState(100).permutation(len(ads))[:ad_no]
    ad_count = np.array(ads["amount"])[indexes]
    clicks_count = np.array(clicks["clicked"])[indexes]
    ad_ids = np.array(ads["ad_id"])[indexes]

    #plot:
    create_two_bars_histogram(ad_no,ad_count,clicks_count,ad_ids,
                              "Ad apearence vs the clicks it got","Ad_id","count")
    '''

def create_clicks_per_ad_histogram(main_table):
    clicks = main_table.groupby(["ad_id"], as_index=False).agg({"clicked": np.sum})
