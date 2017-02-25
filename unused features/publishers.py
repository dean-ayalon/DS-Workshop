from utils.plot_utils import *
from utils.table_utils import return_unique_values_of_column_from_table, filter_table_by_unique_ids
from paths import *

import numpy as np
import pandas as pd

def create_publishers_popularity_feature(main_table,promoted,meta):
    #ads per publishers. each ad is connected to a publisher through the document it is leading to.
    #TODO: all the tables and the filtered tables should be later passed as an arguments to this pocedure!
    ad_doc = promoted[["ad_id","document_id"]]
    doc_publisher =meta[["document_id","publisher_id"]]
    main_table = main_table[["ad_id","clicked","display_id"]]

    '''
    #returns single columns of relavent docs, ads and displays
    relavent_docs = return_unique_values_of_column_from_table("document_id_y",main_table)
    relavent_ad = return_unique_values_of_column_from_table("ad_id",main_table)
    relavent_disp = return_unique_values_of_column_from_table("display_id",main_table)


    #returns filtered tables of doc_publisher, clicks and ad_doc by document_id, display_id and ad_id
    relavent_doc_publisher = filter_table_by_unique_ids(relavent_docs,'document_id',doc_publisher) #return all the relevant docs from doc_publisher
    relavent_clicks = filter_table_by_unique_ids(relavent_disp,'display_id',clicks) #return all the relevant displayes in clicks
    relavent_ad = filter_table_by_unique_ids(relavent_ad,'ad_id',ad_doc) #return all the relevant ads in ad_doc

    '''

    #creates number of ads per publisher dataframe
    ad_publisher = ad_doc.merge(doc_publisher, on="document_id") #merge relevant ads with relevant docs
    ad_publisher.drop(['document_id'],axis=1,inplace=True)
    ad_publisher_g = ad_publisher.groupby(["publisher_id"],as_index=False).agg({"ad_id":np.count_nonzero})

    '''
    #this code creates ads_per_publisher histogram
    publishers = np.array(ad_publisher_g["publisher_id"])
    ads_count = np.array(ad_publisher_g["ad_id"])

    create_simple_histogram(publishers,ads_count,'ads per publisher',"Publishers","Ads","ads_per_publishers.png")
    '''

    #now clicks per publisher
    #we need to agragate first in order to prevent multiplies (many ads in different displays)
    clicks_g = main_table.groupby(["ad_id"], as_index = False).agg({"clicked":np.sum})
    clicks_publishers = ad_publisher.merge(clicks_g,on = "ad_id")
    clicks_publishers = clicks_publishers.drop("ad_id",1)
    clicks_publishers_g = clicks_publishers.groupby(["publisher_id"], as_index = False).agg({"clicked":np.sum})

    '''
    #this code creates clicks_per_publisher histogram
    clks = np.array(clicks_publishers_g["clicked"])
    pblshs = np.array(clicks_publishers_g["publisher_id"])

    create_simple_histogram(pblshs,clks,'clicks per publisher',"Publishers","Clicks","clicks_per_publishers.png")
    '''

    #finelly creates the feature: publisher popularity, which is (#clicks_per_publisher)/(#ads per publisher)
    publishers_popularity = clicks_publishers_g.merge(ad_publisher_g, on="publisher_id")
    publishers_popularity["publisher_popularity"] = publishers_popularity["clicked"] / publishers_popularity["ad_id"] #number of clicks/number of ads
    publishers_popularity.drop(publishers_popularity.columns[[1,2]],axis=1,inplace=True)

    ad_publisher_pop = publishers_popularity.merge(ad_publisher, on="publisher_id")
    ad_publisher_pop.drop(['publisher_id'],axis=1,inplace=True)

    return ad_publisher_pop

promoted = pd.read_csv(PROMOTED_CONTENT_YAIR)
meta = pd.read_csv(DOC_META_YAIR)
main_table = pd.read_csv(MAIN_TABLE_YAIR)
ppf = create_publishers_popularity_feature(main_table,promoted,meta)
print(ppf.head(10))



#remarks:
#some document_id's who appears in doc_meta does not appear on promoted content, and the opposite.

#TODO: half of the ads has no publisher! does it worth the sacrefice?