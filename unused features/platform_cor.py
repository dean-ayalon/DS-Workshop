import numpy as np
import pandas as pd
import seaborn as sns
sns.set(color_codes=True)

#import events:
events = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/events.csv", nrows=1000000)
#some kind of warning is here.
#answer to this: http://stackoverflow.com/questions/33469277/pandas-read-table-reads-mixed-type-reading-string-as-hexadecimal
events = events[["platform","display_id"]] #what does that syntax means?
#events.columns = ["platform","display_id","disp2"]

#import click train
clicks = pd.read_csv("C:/Users/Yair/Desktop/Data Science Workshop/Outbrain Competition/clicks_train.csv",nrows=1000000)
clicks = clicks[["display_id","clicked"]]

#merge
merged = events.merge(clicks, on = "display_id")
merged = merged.drop("display_id",axis = 1) #what does axis means?
merged = merged.groupby(["platform"],as_index=False).agg({"clicked":np.sum})


#a test i did...
#sns.pairplot(merged)
