import numpy as np
import pandas as pd
from paths import *

print("Beginning building of main table...")
# Randomly Sampling a sixteenth of displays in the entire dataset (clicks_train.csv)

# Importing display_id's from clicks.csv
clicks = pd.read_csv(CLICKS_DEAN, usecols=["display_id"])

del clicks  # No longer needed

unique_displays = clicks.display_id.unique()
l = len(unique_displays)

sampled_displays = np.random.RandomState(0).choice(unique_displays, size=527331, replace=False)

# Generating a new dataframe from events.csv containing only the sampled displays
reading_chunks_iterator = pd.read_csv(EVENTS_DEAN, iterator=True, chunksize=20000,
                                      usecols=["display_id", "document_id", "timestamp", "platform", "geo_location"])
sampled_events = pd.concat([chunk[chunk['display_id'].isin(sampled_displays)] for chunk in reading_chunks_iterator])
print("Finished filtering events.csv")
# Generating a new dataframe from clicks_train.csv containing only the sampled displays
reading_chunks_iterator = pd.read_csv(CLICKS_DEAN, iterator=True, chunksize=20000)
sampled_clicks = pd.concat([chunk[chunk['display_id'].isin(sampled_displays)] for chunk in reading_chunks_iterator])
print("Finished filtering clicks.csv")

# Converting current timestamps to real timestamps in seconds instead of ms
current_timestamps = sampled_events["timestamp"]
real_timestamps = np.array(current_timestamps + 1465876799998) // 1000
sampled_events["timestamp"] = real_timestamps


# First Merge
initial_merge = sampled_clicks.merge(sampled_events, on="display_id")
initial_merge.rename(index=str, columns={"timestamp": "click_tstamp"}, inplace=True)

#initial_merge = pd.read_csv(r"C:\Users\Dean\Documents\Semester G\Data Science "
#                            r"Workshop\Repo\DS-Workshop\initial_merge_2.csv")

from features import platform_one_hot_encoding
from features import event_time
from features import is_weekend
from features import ad_count_per_display
from features import updated_clicks_per_appearances
from features import advertiser_freq
from features import campaign_freq

# Merging Features
per_display_features = [event_time.add_event_time_bin_feature,
                        platform_one_hot_encoding.add_platform_one_hot_encoding_feature,
                        is_weekend.add_is_weekend_feature,
                        ad_count_per_display.add_ad_count_per_display_feature]

for feature in per_display_features:
    print("Now adding " + str(feature.__name__))
    feature_frame = feature(initial_merge)
    initial_merge = initial_merge.merge(feature_frame, on="display_id", how="left", copy=False)

initial_merge.drop(["click_tstamp", "platform"], axis=1, inplace=True)


promoted = pd.read_csv(PROMOTED_CONTENT_DEAN)

advertiser_freq_frame = advertiser_freq.advertiser_freq(promoted)
campaign_freq_frame = campaign_freq.campaign_freq(promoted)


promoted.drop(["advertiser_id", "campaign_id"], axis=1, inplace=True)

initial_merge = initial_merge.merge(advertiser_freq_frame, on="ad_id", how="left", copy=False)
initial_merge = initial_merge.merge(campaign_freq_frame, on="ad_id", how="left", copy=False)
initial_merge = initial_merge.merge(promoted, on="ad_id", how="left", copy=False)

del promoted

per_ad_features = [updated_clicks_per_appearances.add_clicks_per_appearances_ratio_feature]
for feature in per_ad_features:
    print("Now adding " + str(feature.__name__))
    feature_frame = feature(initial_merge)
    initial_merge = initial_merge.merge(feature_frame, on="ad_id", how="left", copy=False)



# In order to filter the relevant dataframes to include only relevant documents,
# We first create an array containing only the document_id's appearing in the sampled displays
docs_out = np.array(initial_merge.document_id_x)
docs_in = np.array(initial_merge.document_id_y)
all_docs = np.concatenate((docs_out, docs_in))
all_docs = pd.Series(all_docs).unique()


# Creating filtered versions of document attributes tables to include only relevant displays,
# This makes calculations down the road much quicker
reading_chunks_iterator = pd.read_csv(DOC_TOPICS_DEAN, iterator=True, chunksize=20000)
topics = pd.concat([chunk[chunk['document_id'].isin(all_docs)] for chunk in reading_chunks_iterator])

print("Finished filtering topics.csv")

reading_chunks_iterator = pd.read_csv(DOC_CATEGORIES_DEAN, iterator=True, chunksize=20000)
categories = pd.concat([chunk[chunk['document_id'].isin(all_docs)] for chunk in reading_chunks_iterator])

print("Finished filtering categories.csv")

reading_chunks_iterator = pd.read_csv(DOC_ENTETIES_DEAN, iterator=True, chunksize=20000)
entities = pd.concat([chunk[chunk['document_id'].isin(all_docs)] for chunk in reading_chunks_iterator])

print("Finished filtering entities.csv")


# Adding Topic, Entities and Categories Similarity Features

topic_similarities = []
entities_similarities = []
categories_similarities = []

from features.find_similarity import find_similarity
counter = 0
for row in initial_merge.itertuples():
    if not counter % 27247:
        print("Adding similarity features: passed through " + (str(round(counter * 100 / 2724795))) + "% of rows")
    doc_out = row.document_id_x
    doc_in = row.document_id_y

    topic_similarity = find_similarity(topics, doc_out, doc_in, "topic_id")
    topic_similarities.append(topic_similarity)

    categories_similarity = find_similarity(categories, doc_out, doc_in, "category_id")
    categories_similarities.append(categories_similarity)

    entities_similarity = find_similarity(entities, doc_out, doc_in, "entity_id")
    entities_similarities.append(entities_similarity)

    #print("for doc_out " + str(doc_out) + ", for doc_in " + str(doc_in))
    #print("       top_sim = " + str(topic_similarity) + ", cat_sim=" + str(categories_similarity) + ", ent_sim = " +
    #     str(entities_similarity))
    counter += 1

# Creating the final table

initial_merge["topic_sim"] = topic_similarities
initial_merge["entities_sim"] = entities_similarities
initial_merge["categories_sim"] = categories_similarities










