from utils.plot_utils import *
from utils.table_utils import return_unique_values_of_column_from_table, filter_table_by_unique_ids
from paths import *

import numpy as np
import pandas as pd

'''
this feature should recieve two tables and columns name, and return their XCTRY,
where: XCTRY = Pr[clicked = 1 | X,Y] = #(X,Y,Clicked=1)/(X,Y)

pre: table_X will have: "ad_id" column, a feature column, a join column.
     table_Y will have the second feature column and the join column.

post: the function will return the dataframe ["ad_id",Pr[clicked = 1 | X,Y] ]
'''
#TODO: this function should support the option of printing graphs and histograms
#for a start i will try with specific columns, and later will try to make it generic.
def XCTRY(main_table,table_X,table_Y,feature_name_X,feature_name_Y,join_column,with_test=False,test_row_no=100):
    ad_and_feature_X = table_X[['ad_id',feature_name_X,join_column]]
    feature_Y = table_Y[[join_column,feature_name_Y]]
    main_table = main_table[['ad_id','clicked']]
    X_Y_and_ad = ad_and_feature_X.merge(feature_Y, on=join_column)
    X_Y_and_ad.drop([join_column],axis=1, inplace=True)

    if(with_test):
        print(feature_name_X+'_'+feature_name_Y+"_and_ad table:")
        print(X_Y_and_ad.head(test_row_no))

    #counts (X,Y) appearence, relying on the fact that each ad_id is uniqe
    X_and_Y_count = X_Y_and_ad.groupby([feature_name_X,feature_name_Y],as_index=False).agg({"ad_id":np.count_nonzero})\
        .rename(index=str, columns={"ad_id" : 'count'})
    if (with_test):
        print(feature_name_X+'_'+feature_name_Y+"_count table:")
        print(X_and_Y_count.head(test_row_no))

    #this table contains the counts of (X,Y) for each ad
    ad_and_X_Y_count = X_Y_and_ad.merge(X_and_Y_count,on=[feature_name_X,feature_name_Y])
    ad_and_X_Y_count.drop([feature_name_X,feature_name_Y],axis=1, inplace=True)
    if (with_test):
        print("ad_and_"+feature_name_X+'_'+feature_name_Y+"_count table:")
        print(ad_and_X_Y_count.head(test_row_no))

    #creates tha table with the click counts of X and Y
    X_Y_and_clicks = X_Y_and_ad.merge(main_table, on='ad_id')
    X_Y_and_clicks.drop(['ad_id'],axis=1, inplace=True)
    X_Y_and_clicks_count = X_Y_and_clicks.groupby([feature_name_X,feature_name_Y],as_index=False).agg({"clicked":np.sum})\
        .rename(index=str, columns={"clicked" : 'clicks_count'})
    if (with_test):
        print(feature_name_X+'_'+feature_name_Y+"_and_clicks_count table:")
        print(X_Y_and_clicks_count.head(test_row_no))

    ad_and_X_Y_clicks_count = X_Y_and_ad.merge(X_Y_and_clicks_count, on=[feature_name_X,feature_name_Y])
    ad_and_X_Y_clicks_count.drop([feature_name_X,feature_name_Y],axis=1, inplace=True)
    if (with_test):
        print("ad_and_"+feature_name_X+'_'+feature_name_Y+"_clicks_count table:")
        print(ad_and_X_Y_clicks_count.head(test_row_no))

    #creates the final CTR feature
    XCTRY = ad_and_X_Y_count.merge(ad_and_X_Y_clicks_count, on='ad_id')
    XCTRY[feature_name_X+'_CTR_'+feature_name_Y] = XCTRY['clicks_count']/XCTRY['count']
    if (with_test):
        print(feature_name_X+'_CTR_'+feature_name_Y+" table:")
        print(XCTRY.head(test_row_no))
    XCTRY.drop(['count','clicks_count'],axis=1, inplace=True)

    return XCTRY


main_table = pd.read_csv(MAIN_TABLE_YAIR)
promoted = pd.read_csv(PROMOTED_CONTENT_YAIR)
meta =pd.read_csv(DOC_META_YAIR)

a = XCTRY(main_table,promoted,meta,'campaign_id','publisher_id','document_id',with_test=True)
print(a.head(100))




