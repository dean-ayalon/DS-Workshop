#!/usr/bin/env python
# -*- coding: utf-8 -
import numpy as np
import pandas as pd
##import seaborn as sns
import statsmodels.api as sm




#importing documents_topics.csv
topics = pd.read_csv(r"C:\Users\Eran\Desktop\University2017\info\documents_topics.csv")

#slicing topics to isolate document_id and conf level, and the combining
#rows so each document appears once with average conf level
topics = topics[["document_id", "confidence_level","topic_id"]]
##topics.columns = ["topic_id", "document_id","confidence_level"]


#importing first 1000000 rows of clicks_train.csv
clicks = pd.read_csv(r"C:\Users\Eran\Desktop\University2017\info\clicks_train.csv", nrows=1000000)
#import and clean, leave only doc_id and ad_id
promoted_content = pd.read_csv(r"C:\Users\Eran\Desktop\University2017\info\promoted_content.csv")
promoted = promoted_content[["document_id","ad_id"]]
#importing events
events = pd.read_csv(r"C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/events.csv")


##according to the flowchart from 30/11
events1 = events[["document_id","display_id"]]
#doc_out = events1["]
stage2 = events1.merge(clicks, on="display_id")


stage3 = stage2.merge(promoted, on="ad_id")
final_without_topics = stage3[["document_id_x","clicked","document_id_y"]]
final_without_topics.columns = ["doc_out","clicked","doc_in"]


"""


#extracting relevant vectors
topic_conf = np.array(merged3["topic_conf"])
entities_conf = np.array(merged3["entities_conf"])
topic_conf = np.array(merged3["topic_conf"])
clicked = np.array(merged3["clicked"])


#performing logistic regression
logit = sm.Logit(clicked, topic_conf)
res = logit.fit()
print (res.summary())
"""
