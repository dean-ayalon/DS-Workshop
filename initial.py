import numpy as np
import pandas as pd
import seaborn as sns
sns.set(color_codes=True)
import statsmodels.api as sm



#importing promoted_content.csv
promoted = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/promoted_content.csv")

promoted = promoted[["ad_id", "document_id"]]
promoted = promoted.groupby(["document_id"], as_index=False).first()



#importing documents_topics.csv
topics = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/documents_topics.csv")


#slicing topics to isolate document_id and conf level, and the combining
#rows so each document appears once with average conf level
topics = topics[["document_id", "confidence_level"]]
topics = topics.groupby(["document_id"], as_index=False).mean()
topics.columns = ["document_id", "topic_conf"]



#importing document_entities.csv
entities = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/documents_entities.csv")
#slicing entities just like topics
entities = entities[["document_id", "confidence_level"]]
entities = entities.groupby(["document_id"], as_index=False).mean()
entities.columns = ["document_id", "entities_conf"]

#merging all of the existing tables
merged = topics.merge(entities, on="document_id")
merged2 = merged.merge(promoted, on="document_id")


#importing first 1000000 rows of clicks_train.csv
clicks = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv", nrows=1000000)
clicks = clicks[["ad_id", "clicked"]]

#merging clicks with existing data
merged3 = merged2.merge(clicks, on="ad_id")
#showing first 10 rows of final table
merged3.head(10)


#extracting relevant vectors
topic_conf = np.array(merged3["topic_conf"])
entities_conf = np.array(merged3["entities_conf"])
topic_conf = np.array(merged3["topic_conf"])
clicked = np.array(merged3["clicked"])


#performing logistic regression
logit = sm.Logit(clicked, topic_conf)
res = logit.fit()
print (res.summary())




















#nonsense



"""
fig = plt.figure()
plt.plot(topic_conf, clicked, 'bo')
axes = plt.gca()
axes.set_ylim([-0.1, 1.1])

np.corrcoef(entities_conf, clicked)
sns.distplot(topic_conf)

sns.regplot(y='clicked', x='entities_conf', data=merged3, logistic=True)

"""
