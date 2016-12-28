import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#ads per publishers. each ad is connected to a publisher through the document it is leading to.
ad_doc = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/promoted_content.csv",
                     nrows=1000000, usecols=["ad_id","document_id"])

doc_publisher = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/documents_meta.csv",
                     nrows=1000000, usecols=["document_id","publisher_id"])

clicks = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv",
                     nrows=1000000, usecols=["ad_id","clicked"])

ad_publisher = ad_doc.merge(doc_publisher, on="document_id")
ad_publisher = ad_publisher.drop("document_id",1)
ad_publisher_g = ad_publisher.groupby(["publisher_id"],as_index=False).agg({"ad_id":np.count_nonzero})

publishers = np.array(ad_publisher_g["publisher_id"])
ads = np.array(ad_publisher_g["ad_id"])

fig = plt.figure()
fig.suptitle('ads per publisher', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("Publishers")
ax.set_ylabel("Ads")
plt.bar(left=publishers, height=ads)
plt.show()

#now clicks per publisher
#we need to agragate first in order to prevent multiplies (many ads in different displays)
clicks_g = clicks.groupby(["ad_id"], as_index = False).agg({"clicked":np.sum})
clicks_publishers = clicks_g.merge(ad_publisher,on = "ad_id")
clicks_publishers = clicks_publishers.drop("ad_id",1)
clicks_publishers_g = clicks_publishers.groupby(["publisher_id"], as_index = False).agg({"clicked":np.sum})

clks = np.array(clicks_publishers_g["clicked"])
pblshs = np.array(clicks_publishers_g["publisher_id"])

fig = plt.figure()
fig.suptitle('clicks per publisher', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("Publishers")
ax.set_ylabel("Clicks")
plt.bar(left=pblshs, height=clks)
plt.show()



#remarks:
#some document_id's who appears in doc_meta does not appear on promoted content, and the opposite.