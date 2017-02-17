from utils.plot_utils import *
from utils.table_utils import return_unique_values_of_column_from_table, filter_table_by_unique_ids
from paths import *

import numpy as np
import pandas as pd

'''
this feature will measure the number of views each doc had - and each ad related to doc

1) count views per doc
2) connect those views to ads.
also:
3) check in relation to clicks
'''

def create_clicks_views_ratio_feature(main_table,page_views):
    #load relavent tables
    page_views = page_views[["uuid","document_id"]]
    main = main_table[["ad_id","document_id_y","clicked"]]
    main = main.rename(index=str, columns={"document_id_y" : "document_id"})

    #create views per add

    #len: 59849
    views_per_doc = page_views.groupby(["document_id"],as_index=False).agg({"uuid":np.count_nonzero})
    #len: 1331
    views_per_add = views_per_doc.merge(main, on="document_id").drop(['document_id','clicked'],axis=1).drop_duplicates()\
        .rename(index=str, columns={"uuid" : "views_per_ad"})

    #create_simple_histogram(np.array(views_per_add.ad_id),np.array(views_per_add.views_per_ad),"Views per ad","Ad-id","Views","views_per_ad.png")

    #len: 148393
    clicks_per_ad = main.groupby(["ad_id"],as_index=False).agg({"clicked":np.sum})

    #TODO: you can see that different ads of the same doc got different ammount of clicks. maybe we should consider that.
    #TODO for eample - for each doc, check what was the most popular ad.
    clicks_views_ratio = views_per_add.merge(clicks_per_ad,on="ad_id")

    clicks_views_ratio["clicks/views"] = clicks_views_ratio["clicked"]/clicks_views_ratio["views_per_ad"]
    clicks_views_ratio.drop(['views_per_ad','clicked'],axis=1, inplace=True)

    #create_simple_histogram(np.array(clicks_views_ratio.ad_id),np.array(clicks_views_ratio["clicks/views"]),"Clicks/views per ad","ad_id","clicks/views","clicks_views_ratio.png")
    return clicks_views_ratio

'''
#test:
main_table = pd.read_csv(MAIN_TABLE_YAIR)
page_views = pd.read_csv(PAGE_VIEWS_YAIR)
a = create_clicks_views_ratio_feature(main_table,page_views)
print(a.head())
'''


