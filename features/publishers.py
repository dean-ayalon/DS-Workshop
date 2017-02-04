import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('Agg')
from utils.plot_utils import *

#ads per publishers. each ad is connected to a publisher through the document it is leading to.
ad_doc = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/promoted_content.csv",
                     usecols=["ad_id","document_id"],iterator = True, chunksize = 20000)

doc_publisher = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/documents_meta.csv",
                            usecols=["document_id","publisher_id"],iterator = True, chunksize = 20000)

clicks = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv",
                     usecols=["ad_id","clicked","display_id"],iterator = True, chunksize = 20000)

#returns a block of relavent docs, ads and displays
#TODO: create a function create_uniqe_column_from_table
relavent_docs = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/fifth_merge_w_top_sim.csv",
                           usecols = ["document_id_y"])
relavent_docs = pd.Series(np.array(relavent_docs.document_id_y)).unique() #TODO what does this do?

relavent_ad = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/fifth_merge_w_top_sim.csv",
                           usecols = ["ad_id"])
relavent_ad = pd.Series(np.array(relavent_ad.ad_id)).unique()

relavent_disp = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/fifth_merge_w_top_sim.csv",
                           usecols = ["display_id"])
relavent_disp = pd.Series(np.array(relavent_disp.display_id)).unique()


#returns filtered tables of doc_publisher, clicks and ad_doc by document_id, display_id and ad_id
#TODO: create function filter_table_by_uniqe_ids
relavent_doc_publisher = pd.concat([chunk[chunk['document_id'].isin(relavent_docs)]for chunk in doc_publisher]) #return all the relevant docs from doc_publisher
#TODO: why does the second one takes so long??
relavent_clicks = pd.concat([chunk[chunk['display_id'].isin(relavent_disp)]for chunk in clicks]) #return all the relevant displayes in clicks
relavent_ad = pd.concat([chunk[chunk['ad_id'].isin(relavent_disp)]for chunk in ad_doc]) #return all the relevant ads in ad_doc


#creates number of ads per publisher dataframe
ad_publisher = relavent_ad.merge(relavent_doc_publisher, on="document_id") #merge relevant ads with relevant docs
ad_publisher.drop(['document_id'],axis=1,inplace=True)
ad_publisher_g = ad_publisher.groupby(["publisher_id"],as_index=False).agg({"ad_id":np.count_nonzero})
publishers = np.array(ad_publisher_g["publisher_id"])
ads_count = np.array(ad_publisher_g["ad_id"])

create_simple_histogram(publishers,ads_count,'ads per publisher',"Publishers","Ads","ads_per_publishers.png")

#now clicks per publisher
#we need to agragate first in order to prevent multiplies (many ads in different displays)
clicks_g = relavent_clicks.groupby(["ad_id"], as_index = False).agg({"clicked":np.sum})
clicks_publishers = ad_publisher.merge(clicks_g,on = "ad_id")
clicks_publishers = clicks_publishers.drop("ad_id",1)
clicks_publishers_g = clicks_publishers.groupby(["publisher_id"], as_index = False).agg({"clicked":np.sum})

clks = np.array(clicks_publishers_g["clicked"])
pblshs = np.array(clicks_publishers_g["publisher_id"])

create_simple_histogram(pblshs,clks,'clicks per publisher',"Publishers","Clicks","clicks_per_publishers.png")

#finelly creates the feature: publisher popularity, which is (#clicks_per_publisher)/(#ads per publisher)
publishers_popularity = clicks_publishers_g.merge(ad_publisher_g, on="publisher_id")
publishers_popularity["publisher_popularity"] = publishers_popularity["clicked"] / publishers_popularity["ad_id"] #number of clicks/number of ads
publishers_popularity.drop(publishers_popularity.columns[[1,2]],axis=1,inplace=True)

ad_publisher_pop = publishers_popularity.merge(ad_publisher, on="publisher_id")
ad_publisher_pop.drop(['publisher_id'],axis=1,inplace=True)



#remarks:
#some document_id's who appears in doc_meta does not appear on promoted content, and the opposite.