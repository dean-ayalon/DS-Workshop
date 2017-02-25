import numpy as np
import pandas as pd
##import seaborn as sns
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression


# Importing documents_topics.csv
topics = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/documents_topics.csv",
                     usecols=["document_id", "confidence_level", "topic_id"])


# importing first 1000000 rows of clicks_train.csv
clicks = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv",
                     nrows=1000000)
# import promoted_content.csv and clean, leave only doc_id and ad_id
promoted = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/promoted_content.csv",
                       usecols=["document_id", "ad_id"])
# importing events.csv
events = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/events.csv",
                     nrows=1000000, usecols=["document_id", "display_id"])


# According to the flowchart from 30/11
stage2 = events.merge(clicks, on="display_id")


stage3 = stage2.merge(promoted, on="ad_id")
final_without_topics = stage3[["document_id_x", "clicked", "document_id_y"]]
final_without_topics.columns = ["doc_out", "clicked", "document_id"]

final = final_without_topics.merge(topics, on="document_id")
final.columns = ["document_id", "clicked", "doc_in", "topic_in", "conf_in"]

final = final.merge(topics, on="document_id")
final.columns = ["doc_out", "clicked", "doc_in", "topic_in", "conf_in", "topic_out", "conf_out"]
final.head()

final["topics_match"] = (final["topic_in"] == final["topic_out"])
final.head()

# Checking correlation between topics matching and clicking - apparently positive but very small
# Perhaps can be part of the model anyway
np.corrcoef(final["clicked"], final["topics_match"])


# Checking for correlation with category_id confidence
categories = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/documents_categories.csv",
                         usecols=["document_id", "confidence_level"])


final2 = stage2.merge(categories, on="document_id")
final2.head()

# Performing logistic regression to determine strength of correlation
logit = sm.Logit(final2["clicked"], final2["confidence_level"])
res = logit.fit()
print(res.summary())
# Very significant negative coefficient - the higher the confidence in category the less likely the click



#Checking for correlation between topics and entities conf. levels and clicks

# Importing document_entities.csv
entities = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/documents_entities.csv",
                       usecols=["document_id", "confidence_level"])
entities = entities.groupby(["document_id"], as_index=False).mean()
entities.columns = ["document_id", "average_entities_conf"]

topics_grouped = topics.groupby(by="document_id", as_index=False).mean()
topics_grouped = topics_grouped[["document_id", "confidence_level"]]
topics_grouped.columns = ["document_id", "average_topics_conf"]

merged1 = topics_grouped.merge(entities, on="document_id")
merged1 = merged1.merge(promoted, on="document_id")
merged1.head()

merged1 = merged1.merge(clicks, on="ad_id")
merged1.head()

#extracting relevant vectors
topic_conf = merged1["average_topics_conf"]
entities_conf = merged1["average_entities_conf"]
clicked = merged1["clicked"]


# Checking correlation between average topic confidence and clicks = negative and very significant
logit = sm.Logit(clicked, topic_conf)
res = logit.fit()
print(res.summary())


# Checking correlation between average entities confidence and clicks = negative and very significant
logit = sm.Logit(clicked, entities_conf)
res = logit.fit()
print(res.summary())