import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#how many times an ad appeared:
adAppearance = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv",
                     nrows=1000000, usecols=["ad_id"])

adAppearance["appearance"] = adAppearance["ad_id"]
adAppearance = adAppearance.groupby(["ad_id"],as_index=False).agg({"appearance":np.count_nonzero})

adArr = np.array(adAppearance["ad_id"])
aprArr = np.array(adAppearance["appearance"])

fig = plt.figure()
fig.suptitle('Number of time ad appearded', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("ad_ID")
ax.set_ylabel("Appearances")
plt.bar(left=adArr, height=aprArr)
plt.show()


#how many times an ad got a click

adClicks = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv",
                     nrows=1000000, usecols=["ad_id","clicked"])
adClicks = adClicks.groupby(["ad_id"],as_index=False).agg({"clicked":np.sum})
adArr = np.array(adClicks["ad_id"])
clicksArr = np.array(adClicks[["clicked"]])

fig = plt.figure()
fig.suptitle('Number of time ad got clicked', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("Ad_ID")
ax.set_ylabel("Clicks")
plt.bar(left=adArr, height=clicksArr)
plt.show()

#a plot which shows per ad_id: #appearance - (#appearances-#clicks) assume #appearnces>=#clicks

aprClkArr = [0 for x in range(len(clicksArr))]
for i in range(len(clicksArr)):
    aprClkArr[i] = clicksArr[i]/aprArr[i]
aprClkArr = np.array(aprClkArr)
fig = plt.figure()
fig.suptitle('Clicks/Appearances per ad', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel("Ad_ID")
ax.set_ylabel("Clicks/Appearances")
plt.bar(left=adArr, height=aprClkArr)
plt.show()

sum0 = 0
for x in aprClkArr:
    if x==0:
        sum0 += 1

sum1 = 0
for x in aprClkArr:
    if x==1:
        sum1 += 1

