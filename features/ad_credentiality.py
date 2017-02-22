# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:41:30 2017

@author: Eran
"""
import numpy as np
import pandas as pd

'''
this function is general and can be used to acquire all kinds of elements. 
this is the code for adding a general credentiality measure (sum of creds for all elements)
topic_cred = calculate_credentiality(table,topics,promoted)
entity_cred = calculate_credentiality(table,entities,promoted)
category_cred = calculate_credentiality(table,categories,promoted)

'''
def calculate_credentiality(main_table,elements,promoted_content):
    '''
    input: standard table and one of the entities, categories and topics tables
    output: a credentiality factor for each ad
    the formula for the credentiality is the sum of all confidences.
    '''
    # Slicing only necessary columns
    ad_table = main_table[["ad_id", "clicked"]]
    ##changing ad_id to document_id using the promoted_content table
    with_doc = ad_table.merge(promoted_content, on="ad_id")
    ##summing up all elements confidence levels for all docs
    doc_cred = elements.groupby(["document_id"],as_index=False).agg({"confidence_level":np.sum})
    #return what's relevant for main_table, that is, only ad and new attribute
    attribute = pd.merge(with_doc, doc_cred, on="document_id")
    return attribute[["ad_id", "confidence_level"]]
    
