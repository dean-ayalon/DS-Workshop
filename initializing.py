# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 18:50:58 2016
initializing
@author: Eran
"""
import numpy as np
import pandas as pd
##import seaborn as sns



#importing documents_topics.csv
topics = pd.read_csv(r"C:\Users\Eran\Desktop\2017\info\documents_topics.csv")

#slicing topics to isolate document_id and conf level, and the combining
#rows so each document appears once with average conf level
topics = topics[["document_id", "confidence_level","topic_id"]]
##topics.columns = ["topic_id", "document_id","confidence_level"]


#importing first 1000000 rows of clicks_train.csv
clicks = pd.read_csv(r"C:\Users\Eran\Desktop\2017\info\clicks_train.csv", nrows=1000000)
promoted = pd.read_csv(r"C:\Users\Eran\Desktop\2017\info\promoted_content.csv", nrows=1000000)
events = pd.read_csv(r"C:\Users\Eran\Desktop\2017\info\events.csv")


##according to the flowchart from 30/11
events1 = events[["document_id","display_id"]]
##renaming to doc_out
events1.rename(columns={'document_id':'doc_out'}, inplace=True)
#doc_out = events1["]
stage2 = events1.merge(clicks, on="display_id")
##replacing ad_id with doc_id to use the topics table
stage3 = stage2.merge(promoted, on="ad_id")
final_without_topics = stage3[["doc_out","clicked","document_id"]]
sorted_by_doc_out = final_without_topics.sort('doc_out')
##getting the confidence match array
a = adding_attr1(sorted_by_doc_out,topics)
b = adding_attr2(sorted_by_doc_out,entities)
c = adding_attr3(sorted_by_doc_out,entities)

with_attributes = sorted_by_doc_out
##adding it as attribute
with_attributes["topic"] = a
with_attributes["category"] = b
with_attributes["entity"] = c

