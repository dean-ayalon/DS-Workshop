# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:41:30 2017

@author: Eran
"""
import numpy as np

'''
this function is general and can be used to acquire all kinds of elements. 
this is the code for adding a general credentiality measure (sum of creds for all elements)
topic_cred = calculate_credentiality(table,topics,promoted)
entity_cred = calculate_credentiality(table,entities,promoted)
category_cred = calculate_credentiality(table,categories,promoted)

'''
def calculate_credentiality(main_table, elements,promoted_content):
    '''
    input: standard table and one of the entities, categories and topics tables
    output: a credentiality factor for each ad
    the formula for the credentiality is the sum of all confidences.
    '''
    # Slicing only necessary columns
    ad_table = main_table[["ad_id", "clicked"]]
    ##changing ad_id to document_id by the promoted_content table
    with_doc = ad_table.merge(promoted_content, on="ad_id")
    table = with_doc[["clicked","document_id"]]
    credentiality_array = []
    ##for row in clicks:
    for i in range(len(table.index)):
        ##this is the doc_out
        doc = table.iloc[i]["document_id"]
        credentiality_array.append(find_cred(elements,doc))
    ##now returns just the norman python similarity array
    return credentiality_array
    

def find_cred(elements,doc):
    ##all the elements of doc
    doc_elements = elements.loc[elements["document_id"] == doc]
    cred = 0
    ##for every element, calculating the sum of confidence levels
    for i in range(len(doc_elements.index)):
        cred += doc_elements.iloc[i]["confidence_level"]
    return cred
    
