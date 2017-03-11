import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from paths import *
from utils.table_utils import get_clicks_per_advertiser_or_campaign, get_ads_per_feat
from features.geo_features import filter_countries_by_size

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

def create_simple_pie_chart(count_arr,labels,pie_title,do_save=False,file_name=''):
    fig1, ax1 = plt.subplots()
    fig1.suptitle(pie_title, fontsize=14, fontweight='bold')
    colors = ['blue', 'green', 'red', 'skyblue', 'purple', 'yellow', 'black', 'white', 'lightcoral',
              'pink', 'darkgreen', 'yellow', 'grey']
    patches, texts = ax1.pie(count_arr, shadow=True, colors=colors, startangle=90)
    ax1.axis('equal')

    percent = 100. * count_arr / count_arr.sum()
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(labels, percent)]
    plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.22, 0.5),
               fontsize=10)
    if(do_save):
        plt.savefig(file_name)

#creates a platform with two types of bars, mostly use to compare amount of clicks
#against the amount of some feature_ids, in order to see their popularity.
def create_two_bars_histogram(sample_size,feature_count,clicks,feature_ids,title,x_label,y_label,legend_prop_name):
    place_on_chart = np.dot(np.arange(sample_size),2)
    width = 0.5
    fig, ax = plt.subplots()
    prop_cnt_bars = ax.bar(place_on_chart,feature_count,width,color="r")
    clicks_cnt_bars = ax.bar(place_on_chart+width,clicks,width)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(place_on_chart + width / 2)
    ax.set_xticklabels(feature_ids, rotation=90, rotation_mode="anchor", ha="right",size=7)
    ax.legend((prop_cnt_bars[0],clicks_cnt_bars[0]),(legend_prop_name,'clicks'),loc='center left',bbox_to_anchor=(1, 0.5))

    #plt.savefig("testRand1.png")

#creates the histogram of the platforms
def plot_platform_histogram(main_table):
    platforms_count = main_table[["platform_is_desktop", "platform_is_mobile", "platform_is_tablet"]]
    platforms_count = np.array(platforms_count.sum())
    platforms_names = np.array(["Desktop", "Mobile", "Tablet"])
    fig = plt.figure()
    fig.suptitle("Amount of clicks ", fontsize=14, fontweight='bold')
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
    fig1, ax1 = plt.subplots()
    fig1.suptitle("Percentage of display sizes in the sample", fontsize=14, fontweight='bold')
    colors = ['blue','green', 'red','skyblue','purple', 'yellow','black', 'white', 'lightcoral', 'pink']#, 'darkgreen', 'yellow', 'grey', 'violet', 'magenta', 'cyan']
    patches, texts = ax1.pie(disp_size_count_arr,colors=colors,
            shadow=True, startangle=90)
    ax1.axis('equal')
    percent = 100. * disp_size_count_arr / disp_size_count_arr.sum()
    labels = ['{0} ads - {1:1.2f} %'.format(i, j) for i, j in zip(disp_size_type, percent)]
    plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.22, 0.5),
               fontsize=10)
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
                              adv_or_camp,"Count","ads")


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

def create_similarity_histograms(main_table,ads_no,sim_name,sim_name_for_title):
    ad_and_sim = main_table[["ad_id",sim_name]]
    indexes = np.random.RandomState(0).permutation(len(ad_and_sim))[:ads_no]
    ad_id = np.array(ad_and_sim["ad_id"])[indexes]
    sim_rate = np.array(ad_and_sim[sim_name])[indexes]
    create_simple_histogram(ad_id,sim_rate,sim_name_for_title+" similarity for "+str(ads_no)+" random ads",
                            "Ad id",sim_name_for_title+" similarity rate")#,sim_name_for_title+"_sim.png",do_print=True)

def create_countries_pie_chart(disp_geo,size):
    countries = filter_countries_by_size(disp_geo,size)
    country_name = np.array(countries["country"])
    country_count = np.array(countries["country_count"])
    create_simple_pie_chart(country_count, country_name,
                            "Countries Which are at least " + str(100/size) +"% from all countries")
                            #,do_save=True, file_name='countries_pie'+str(1/size)+'.png')

#here will be plots we have to create and upload as an image, since we can't upload
#their tables
#disp_geo = pd.read_csv(DISPLAY_GEO_YAIR)
#create_countries_pie_chart(disp_geo,100)
#create_countries_pie_chart(disp_geo,1000)



#tests: TODO delete later
#create_similarity_histograms(main_table,1000,"topic_sim","Topics")
#create_similarity_histograms(main_table,1000,"entities_sim","Entities")
#create_similarity_histograms(main_table,100,"categories_sim","Categories")