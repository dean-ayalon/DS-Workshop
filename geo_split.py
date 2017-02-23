import numpy as np
import pandas as pd
from paths import *



print("start read events")
events = pd.read_csv(EVENTS_YAIR, iterator=True, chunksize=100000)
print("end read events")
#print("this is Events row number: "+str(len(events)))


print("start split")
geo = pd.concat(chunk['geo_location'].str.split('>',expand = True)\
                .rename(index=int, columns={0: 'country', 1 : 'state',2 : 'DMA'}) for chunk in events)
#geo = events['geo_location'].str.split('>',expand = True).rename(index=int, columns={0: 'country', 1 : 'state',2 : 'DMA'})
print("end split")

print("start restart iterator")
events = pd.read_csv(EVENTS_YAIR, iterator=True, chunksize=100000)
print("end restart iterator")

print("start adding doc_ids")
doc = pd.concat(pd.DataFrame(chunk['document_id']) for chunk in events)
print("end adding doc_ids")
geo['document_id'] = doc['document_id']
print(geo.head(10))

print("start export to file")
geo.to_csv("doc_geo.csv", index=False)
print("end export to file")

#pd.concat([chunk[chunk['display_id'].isin(sampled_displays)] for chunk in reading_chunks_iterator])