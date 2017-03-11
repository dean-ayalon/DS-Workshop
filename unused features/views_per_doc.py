import numpy as np

#unique docs in page view: 59849
#unique docs in main table: 60484

# This feature counts the number of views each doc got and calculates
# its ratio with the amount of clicks it got.
# we discarded this feature because most of the docs in page_views
# did not appear in our sample (this feature was created on the full page_views table)
def create_clicks_views_ratio_feature(main_table,page_views):
    #load relavent tables
    page_views = page_views[["uuid","document_id"]]
    main = main_table[["ad_id","document_id_y","clicked"]]
    main = main.rename(index=str, columns={"document_id_y" : "document_id"})

    #create views per add

    #len: 59849
    views_per_doc = page_views.groupby(["document_id"],as_index=False).agg({"uuid":np.count_nonzero})
    #len: 1331, without drop 9515
    views_per_add = views_per_doc.merge(main, on="document_id").drop(['document_id','clicked'],axis=1)\
        .rename(index=str, columns={"uuid" : "views_per_ad"})

    #calculates clicks per ad

    #len: 148393
    clicks_per_ad = main.groupby(["ad_id"],as_index=False).agg({"clicked":np.sum})

    #calculates the ratio between the views and the clicks

    clicks_views_ratio = views_per_add.merge(clicks_per_ad,on="ad_id")
    clicks_views_ratio["clicks/views"] = clicks_views_ratio["clicked"]/clicks_views_ratio["views_per_ad"]
    clicks_views_ratio.drop(['views_per_ad','clicked'],axis=1, inplace=True)

    return clicks_views_ratio



