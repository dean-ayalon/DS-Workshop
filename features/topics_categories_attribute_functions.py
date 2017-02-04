#!/usr/bin/env python
# -*- coding: utf-8 -
import numpy as np
import pandas as pd
##import seaborn as sns
import statsmodels.api as sm


##defining a function to create the topics attribute
def adding_attr1(clicks,topics):
    '''
    the input is:
        cul1 doc_out
        cul2 clicked? 0/1
        cul3 doc_in
        AND
        topics table
    the outout:
        an additional colunm which is a new attribute of similarity between topics.
        formula:
            sum of multiplication of confidence levels of common topics
    '''
    final = clicks
    similarity_array = []
    ##for row in clicks:
    for i in range(len(final.index)):
        ##this is the doc_out
        doc_out = clicks.iloc[i]["doc_out"]
        ##doc in 
        doc_in = clicks.iloc[i]["document_id"]
        similarity_array.append(find_similarity(topics,doc_out,doc_in))
    ##now returns just the norman python similarity array
    return similarity_array
        
    
def find_similarity(topics,doc_out,doc_in):
    ##all the topics of the doc_out
    out_topics = topics.loc[topics["document_id"] == doc_out]
    ##all the topics of the doc_in
    in_topics = topics.loc[topics["document_id"] == doc_in]
    ##getting similarity
    similarity = 0
    ##for every out_topic
    for i in range(len(out_topics.index)):
        topic = out_topics.iloc[i]["topic_id"]
        ##if the other doc has indeed the topic
        if (topic in in_topics.values):
            ##using the formula stated in adding attr1
            s1 = out_topics.iloc[i]["confidence_level"]
            s2 = in_topics.loc[in_topics["topic_id"] == topic].iloc[0]["topic_id"]
            similarity += s1*s2
    return similarity
    
##defining a function to create the topics attribute
def adding_attr2(clicks,categories):
    '''
    the input is:
        cul1 doc_out
        cul2 clicked? 0/1
        cul3 doc_in
        AND
        categories table
    the outout:
        an additional colunm which is a new attribute of similarity between categories.
        formula:
            sum of multiplication of confidence levels of common categories
    '''
    final = clicks
    similarity_array = []
    ##for row in clicks:
    for i in range(len(final.index)):
        ##this is the doc_out
        doc_out = clicks.iloc[i]["doc_out"]
        ##doc in 
        doc_in = clicks.iloc[i]["document_id"]
        similarity_array.append(find_similarity2(categories,doc_out,doc_in))
    ##now returns just the norman python similarity array
    return similarity_array
        
    
def find_similarity2(categories,doc_out,doc_in):
    ##all the docs of the doc_out
    out_docs = categories.loc[categories["document_id"] == doc_out]
    ##all the docs of the doc_in
    in_docs = categories.loc[categories["document_id"] == doc_in]
    ##getting similarity
    similarity = 0
    ##for every out_topic
    for i in range(len(out_docs.index)):
        cat = out_docs.iloc[i]["category_id"]
        ##if the other doc has indeed the topic
        if (cat in in_docs.values):
            ##using the formula stated in adding attr1
            s1 = out_docs.iloc[i]["confidence_level"]
            s2 = in_docs.loc[in_docs["category_id"] == cat].iloc[0]["category_id"]
            similarity += s1*s2
    return similarity
    

   
##defining a function to create the topics attribute
def adding_attr3(clicks,entities):
    '''
    the input is:
        cul1 doc_out
        cul2 clicked? 0/1
        cul3 doc_in
        AND
        categories table
    the outout:
        an additional colunm which is a new attribute of similarity between categories.
        formula:
            sum of multiplication of confidence levels of common categories
    '''
    final = clicks
    similarity_array = []
    ##for row in clicks:
    for i in range(len(final.index)):
        ##this is the doc_out
        doc_out = clicks.iloc[i]["doc_out"]
        ##doc in 
        doc_in = clicks.iloc[i]["document_id"]
        similarity_array.append(find_similarity3(entities,doc_out,doc_in))
    ##now returns just the norman python similarity array
    return similarity_array
        
    
def find_similarity3(entities,doc_out,doc_in):
    ##all the docs of the doc_out
    out_ents = entities.loc[entities["entity_id"] == doc_out]
    ##all the docs of the doc_in
    in_ents = entities.loc[entities["entity_id"] == doc_in]
    ##getting similarity
    similarity = 0
    ##for every out_topic
    for i in range(len(out_ents.index)):
        cat = out_ents.iloc[i]["entity_id"]
        ##if the other doc has indeed the topic
        if (cat in in_ents.values):
            ##using the formula stated in adding attr1
            s1 = out_ents.iloc[i]["confidence_level"]
            s2 = in_ents.loc[in_ents["entity_id"] == cat].iloc[0]["entity_id"]
            similarity += s1*s2
    return similarity

    
    
    
    
##another suggestion for attributes - common values between doc out and doc_in
##another suggestion for topics - getting a topics similarity table by connectivity, and then getting a better idea about topics match.
##because now it has only mached topics

##problems: entities too slow, and maybe all of them.
##scales are not mached. the specific formular for "similarity" are not yet decided, and are now a little random.