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
#load relavent tables
page_views = pd.read_csv(PAGE_VIEWS_YAIR, usecols=["uuid","document_id"])
main = pd.read_csv(MAIN_TABLE_YAIR, usecols=["ad_id","document_id_y","clicked"])
main = main.rename(index=str, columns={"document_id_y" : "document_id"})

#create views per add
views_per_doc = page_views.groupby(["document_id"],as_index=False).agg({"uuid":np.count_nonzero})
views_per_add = views_per_doc.merge(main, on="document_id").drop(['document_id','clicked'],axis=1).drop_duplicates()\
    .rename(index=str, columns={"uuid" : "views_per_ad"})

#create_simple_histogram(np.array(views_per_add.ad_id),np.array(views_per_add.views_per_ad),"Views per ad","Ad-id","Views","views_per_ad.png")

clicks_per_ad = main.groupby(["ad_id"],as_index=False).agg({"clicked":np.sum})

#create_simple_histogram(np.array(clicks_per_ad.ad_id),np.array(clicks_per_ad.clicked),"Clicks per Ad","Ad-id","Clicks","clicks_per_ad.png")


