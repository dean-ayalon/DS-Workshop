import numpy as np

# This feature calculated the popularity of a publisher, where
# popularity = #clicks/#ads per publisher.
# we discarded this feature because around hald of the ads had no publisher.

def create_publishers_popularity_feature(main_table,promoted,meta):
    #ads per publishers. each ad is connected to a publisher through the document it is leading to.
    ad_doc = promoted[["ad_id","document_id"]]
    doc_publisher =meta[["document_id","publisher_id"]]
    main_table = main_table[["ad_id","clicked","display_id"]]


    #creates number of ads per publisher dataframe
    ad_publisher = ad_doc.merge(doc_publisher, on="document_id") #merge relevant ads with relevant docs
    ad_publisher.drop(['document_id'],axis=1,inplace=True)
    ad_publisher_g = ad_publisher.groupby(["publisher_id"],as_index=False).agg({"ad_id":np.count_nonzero})


    #now clicks per publisher
    #we need to agragate first in order to prevent multiplies (many ads in different displays)
    clicks_g = main_table.groupby(["ad_id"], as_index = False).agg({"clicked":np.sum})
    clicks_publishers = ad_publisher.merge(clicks_g,on = "ad_id")
    clicks_publishers = clicks_publishers.drop("ad_id",1)
    clicks_publishers_g = clicks_publishers.groupby(["publisher_id"], as_index = False).agg({"clicked":np.sum})


    #finally creates the feature: publisher popularity, which is (#clicks_per_publisher)/(#ads per publisher)
    publishers_popularity = clicks_publishers_g.merge(ad_publisher_g, on="publisher_id")
    publishers_popularity["publisher_popularity"] = publishers_popularity["clicked"] / publishers_popularity["ad_id"] #number of clicks/number of ads
    publishers_popularity.drop(publishers_popularity.columns[[1,2]],axis=1,inplace=True)

    ad_publisher_pop = publishers_popularity.merge(ad_publisher, on="publisher_id")
    ad_publisher_pop.drop(['publisher_id'],axis=1,inplace=True)

    return ad_publisher_pop