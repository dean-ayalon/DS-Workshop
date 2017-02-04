import numpy as np
import pandas as pd
import time

# Sampling a fourth of displays in the entire dataset (clicks_train.csv)

# Importing display_id's from clicks.csv
clicks = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/clicks_train.csv", usecols=["display_id"])

unique_displays = clicks.display_id.unique()
l = len(unique_displays)

sampled_displays = np.random.RandomState(0).choice(unique_displays, size=4218648)

# Generating a new dataframe from events.csv containing only the sampled displays
reading_chunks_iterator = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                                      "Data/events.csv", usecols=["display_id", "document_id", "timestamp"],
                                      iterator=True, chunksize=20000)
sampled_events = pd.concat([chunk[chunk['display_id'].isin(sampled_displays)] for chunk in reading_chunks_iterator])
sampled_events.to_csv("sampled_events.csv", index=False)

print("saved sampled_events")
# Generating a new dataframe from clicks_train.csv containing only the sampled displays
reading_chunks_iterator = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/clicks_train.csv", iterator=True, chunksize=20000)
sampled_clicks = pd.concat([chunk[chunk['display_id'].isin(sampled_displays)] for chunk in reading_chunks_iterator])
sampled_clicks.to_csv("sampled_clicks.csv", index=False)
print("saved sampled_clicks")


####Reset / Clear Memory ####


# Reloading the sampled tables
clicks = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/sampled_clicks.csv")

events = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/sampled_events.csv")


# Beginning preprocessing
# Turning current click timestamps to real timestamps by adding 1465876799998 and dividing by 1000 to get timestamp in
# seconds instead of ms
current_timestamps = events["timestamp"]

real_timestamps = np.array(current_timestamps + 1465876799998) // 1000

events["timestamp"] = real_timestamps

# Initial merging
initial_merge = clicks.merge(events, on="display_id")

initial_merge.rename(index=str, columns={"timestamp": "click_tstamp"}, inplace=True)

initial_merge.to_csv("initial_merge.csv", index=False)


####Reset / Clear Memory ####


# Reloading initial merge
initial_merge = pd.read_csv('C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain '
                   'Data/initial_merge.csv')

# Loading promoted_content.csv and documents_meta.csv
promoted = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/promoted_content.csv", usecols=["document_id", "ad_id"])

meta = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/documents_meta.csv", usecols=["document_id", "publish_time"])


# Merging with promoted
merged_with_promoted = initial_merge.merge(promoted, on='ad_id', how='left', sort=False)
merged_with_promoted.head()

# Merging with meta
meta.rename(index=str, columns={"document_id": "document_id_y"}, inplace=True)
merged_with_meta = merged_with_promoted.merge(meta, on="document_id_y", how='left')
merged_with_meta.to_csv("merged_with_meta.csv", index=False)

# Now we need to filter out displays that contain invalid publish timestamps -
# Either before 1971 or after 28.6.2016, or contain a null publish timestamp

# Finding displays with invalid timestamps
counter = 0
problem_displays = []
for row in merged_with_meta.itertuples():
    if not counter % 1926862:
        print("passed through " + str(round(counter*100/19268603)) + "% of rows")
    if type(row[-1]) != str:
            problem_displays.append(row[1])
    else:
        time_struct = time.strptime(row[-1], "%Y-%m-%d %H:%M:%S")
        year = time_struct.tm_year
        month = time_struct.tm_mon
        day = time_struct.tm_mday
        if not 1971 <= year <= 2016:
            problem_displays.append(row[1])
        elif year == 2016:
            if not ((month == 6 and day <= 28) or month <= 5):
                problem_displays.append(row[1])
    counter += 1

problem_displays = pd.Series(problem_displays).unique()
all_displays = merged_with_meta.display_id.unique()
good_displays = []

# Creating a new array, containing only "good" displays - containing valid publish timestamps
current_bad_display_index = 0
current_bad_display = problem_displays[0]
for i in range(len(all_displays)):
    current_disp = all_displays[i]
    current_bad_display = problem_displays[current_bad_display_index]
    if current_disp != current_bad_display:
        good_displays.append(current_disp)
    else:
        current_bad_display_index += 1
good_displays = pd.Series(good_displays)

# Generating a new dataframe containing only displays with valid timestamps
reading_chunks_iterator = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/merged_with_meta.csv", iterator=True, chunksize=20000)
merged_with_meta_only_good_displays = pd.concat([chunk[chunk['display_id'].isin(good_displays)] for chunk in reading_chunks_iterator])

merged_with_meta_only_good_displays.to_csv("merged_with_meta_only_good_displays.csv", index=False)


#### Reset / Clear Memory ####


# Loading 4th merged table

merged_with_meta_only_good_displays = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/merged_with_meta_only_good_displays.csv")

from ad_age_calculator import ad_age_calculator
# Adding first feature ->  "ad age" = click_timestamp - publish_timestamp in days
publish_times = merged_with_meta_only_good_displays.publish_time
click_times = merged_with_meta_only_good_displays.click_tstamp
ad_ages_in_days = ad_age_calculator(publish_times, click_times)

merged_with_meta_only_good_displays["ad_age_in_days"] = ad_ages_in_days

# Dropping click timestamps and publish timestamps - no longer needed
merged_with_meta_only_good_displays.drop(["click_tstamp", "publish_time"], axis=1, inplace=True)

merged_with_meta_only_good_displays.to_csv("merged_with_meta_only_good_displays_with_ad_age.csv", index=False)


#### Reset / Clear Memory ####

merged_with_meta_only_good_displays = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/merged_with_meta_only_good_displays_with_ad_age.csv")

# In order to filter the relevant dataframes to include only relevant documents,
# We first create an array containing only the document_id's appearing in the sampled displays
docs_out = np.array(merged_with_meta_only_good_displays.document_id_x)
docs_in = np.array(merged_with_meta_only_good_displays.document_id_y)
all_docs = np.concatenate((docs_out, docs_in))
all_docs = pd.Series(all_docs).unique()


# Creating filtered versions of document attributes tables to include only relevant displays,
# This makes calculations down the road much quicker
reading_chunks_iterator = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/documents_topics.csv", iterator=True, chunksize=20000)
topics = pd.concat([chunk[chunk['document_id'].isin(all_docs)] for chunk in reading_chunks_iterator])

print("finished topics")

reading_chunks_iterator = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/documents_categories.csv", iterator=True, chunksize=20000)
categories = pd.concat([chunk[chunk['document_id'].isin(all_docs)] for chunk in reading_chunks_iterator])

print("finished categories")

reading_chunks_iterator = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/documents_entities.csv", iterator=True, chunksize=20000)
entities = pd.concat([chunk[chunk['document_id'].isin(all_docs)] for chunk in reading_chunks_iterator])

print("finished entities")


# Calculating similarity features between documents
from functions import find_similarity
topic_similarities = []
entities_similarities = []
categories_similarities = []

counter = 0
for row in merged_with_meta_only_good_displays.itertuples():
    if not counter % 41432:
        print("passed through " + (str(round(counter * 100 / 4143291))) + "% of rows")
    doc_out = row[4]
    doc_in = row[7]

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

merged_with_meta_only_good_displays["topic_sim"] = topic_similarities
merged_with_meta_only_good_displays["entities_sim"] = entities_similarities
merged_with_meta_only_good_displays["categories_sim"] = categories_similarities

merged_with_meta_only_good_displays.to_csv("final_dataset.csv", index=False)


###################################################







