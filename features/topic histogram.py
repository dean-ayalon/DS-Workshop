import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
##import seaborn as sns
import statsmodels.api as sm

#------------------------------Topic per clicks Histogram----------------------

promoted = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/promoted_content.csv",
                       usecols=["document_id", "ad_id"])

clicks = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv",
                     nrows=1000000, usecols = ["ad_id", "clicked"])

topics = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/documents_topics.csv",
                     usecols=["document_id", "confidence_level", "topic_id"])


topic_histogram = promoted.merge(clicks, on="ad_id").merge(topics,on = "document_id")

topic_histogram = topic_histogram.groupby(["topic_id"],as_index=False).agg({"clicked":np.sum})

topicArr = np.array(topic_histogram[["topic_id"]])
#topicArr += [1]
clicksArr = np.array(topic_histogram[["clicked"]])
fig = plt.figure()
fig.suptitle('Clicks Per Topic', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("Topic_ID")
ax.set_ylabel("Number of clicks")
plt.bar(left=topicArr, height=clicksArr)
plt.show()


#-----------------------Topic per Document Histogram------------------------

top_doc_hist = topics.groupby(["topic_id"],as_index=False).agg({"document_id":np.count_nonzero})

topic_ids = np.array(top_doc_hist[["topic_id"]])
number_of_documents = np.array(top_doc_hist[["document_id"]])
fig = plt.figure()
fig.suptitle('Documents Per Topic', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("Topic_ID")
ax.set_ylabel("Number of Documents")
plt.bar(left=topic_ids, height=number_of_documents)
plt.show()