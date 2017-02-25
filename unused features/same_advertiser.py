# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 15:18:04 2017

@author: Eran
"""
import pandas as pd
def same_advertiser(main_table,promoted_content):
    '''
    input: main table and promoted content
    output: main table with same_value attribute for doc and ad
    '''
    # Slicing only necessary columns
    promoted_doc = pd.DataFrame(promoted_content)
    promoted_ad = pd.DataFrame(promoted_content)
    promoted_doc.drop(["ad_id","campaign_id"],axis=1,inplace=True)
    promoted_ad.drop(["document_id","campaign_id"],axis=1,inplace=True)
    ##if advertiser of ad == advertiser of document put 1, else 0.
    ##two tables, one for ad advertiser and one for doc advertiser
    advertiser_doc = pd.merge(main_table,promoted_doc,on="document_id")
    advertiser_ad = pd.merge(main_table,promoted_ad, on="ad_id")
    ##removing unnecessary document_id from ad
    advertiser_ad.drop("document_id",axis=1,inplace=True)
    ##get rid of unnecessary rows, that already exist in the advertiser_ad table
    advertiser_doc = advertiser_doc.rename(index=str,columns={"advertiser_id":"advertiser_doc_id"})
    advertiser_doc.drop(["clicked","display_id"],axis=1,inplace=True)
    advertiser_ad = advertiser_ad.rename(index=str,columns={"advertiser_id":"advertiser_ad_id"})
    joined = pd.merge(advertiser_doc,advertiser_ad,on="ad_id")
    ##True False attribute
    joined["advertiser_ad_id"] = (joined["advertiser_doc_id"] == joined["advertiser_ad_id"])
    joined = joined.rename(index=str,columns={"advertiser_ad_id":"same_advertiser"})
    ##dropping unnecessary columns
    joined.drop("advertiser_doc_id",axis=1,inplace=True)
    return joined
    
    
"""
##to return only ad and attribute add after 28th line:
advertiser_ad.drop(["clicked","display_id"],axis=1,inplace=True) 
##for notebook: this is the count of true and false.
pd.value_counts(joined["same_advertiser"])
##results not that optimistic: less than 1/1000 have same advertiser
"""