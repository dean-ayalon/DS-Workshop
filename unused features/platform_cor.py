import numpy as np
import pandas as pd
from paths import *
import seaborn as sns
sns.set(color_codes=True)


#import events:
events = pd.read_csv(EVENTS_YAIR , usecols=["platform","display_id"],nrows=100000)
#events = events[["platform","display_id"]] #what does that syntax means?

#import click train
clicks = pd.read_csv(CLICKS_YAIR, usecols=["display_id","clicked"],nrows=100000)

#merge
merged = events.merge(clicks, on = "display_id")
merged = merged.drop("display_id",axis = 1) #what does axis means?
merged = merged.groupby(["platform"],as_index=False).agg({"clicked":np.sum})


#a test i did...
#sns.pairplot(merged)


