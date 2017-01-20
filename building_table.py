import numpy as np
import pandas as pd
import sklearn.preprocessing
from scipy.stats import describe
from scipy.stats.mstats import mode
import statsmodels.api as sm
import gc
import seaborn as sns
import sys
import time
sns.set(color_codes=True)
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# Sampling a fourth of displays in the dataset

# importing clicks.csv
clicks = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/clicks_train.csv", usecols=["display_id"])

np.random.RandomState(0)

displays_ids = clicks.display_id
unique_displays = displays_ids.unique()
l = len(unique_displays)


chosen_displays = np.random.choice(unique_displays, size=4218648)

# Generating a separate dataframe containing only the chosen displays
iter_csv = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/events.csv", iterator=True, chunksize=20000)
df = pd.concat([chunk[chunk['display_id'].isin(chosen_displays)] for chunk in iter_csv])
print("finished creating df")

df.to_csv("sampled_events.csv")

print("saved to csv")

# Reloading the sampled tables

clicks = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/sampled_clicks.csv", usecols=["display_id", "ad_id", "clicked"])

events = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/sampled_events.csv", usecols=["display_id", "document_id", "timestamp",
                                                             "platform", "geo_location"])
print("finished loading")

# Beginning preprocessing

# Turning current timestamps to real timestamps
current_timestamp = events["timestamp"]

real_timestamp = np.array(current_timestamp + 1465876799998) // 1000

events["timestamp"] = real_timestamp

# Initial merging

merged_1 = clicks.merge(events, on="display_id")
print("finished merge")

merged_1.rename(index=str, columns={"timestamp" : "click_tstamp"}, inplace=True)

merged_1.to_csv("first_merge.csv", index=False)


# Reloading first merge
data = pd.read_csv('C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain '
                   'Data/first_merge.csv')

promoted = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/promoted_content.csv", usecols=["document_id", "ad_id"])

meta = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/documents_meta.csv", usecols=["document_id", "publish_time"])


merged_2 = data.merge(promoted, on='ad_id', how='left', sort=False)

merged_2.head()


meta.rename(index=str, columns={"document_id" : "document_id_y"}, inplace=True)

merged_3 = merged_2.merge(meta, on="document_id_y", how='left')

merged_3.head()

merged_3.to_csv("third_merge.csv")

# Finding problematic timestamps (before 1971 or after 28.6.2016)
counter = 0
problem_displays = []
for row in merged_3.itertuples():
    if not counter % 1926862:
        print("passed through " + str(counter*100/19268603) + "% of rows")
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
                # print("bad month or day in 2016")

    counter += 1

problem_displays = pd.Series(problem_displays).unique()
all_displays = merged_3.display_id.unique()
good_displays = []

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
iter_csv = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/third_merge.csv", iterator=True, chunksize=20000)
merged_4 = pd.concat([chunk[chunk['display_id'].isin(good_displays)] for chunk in iter_csv])

merged_4.head(100)


merged_4.to_csv("fourth_merge.csv", index=False)





#######################
# Loading 4th merged table

merged_4 = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/fourth_merge.csv", usecols=["display_id", "ad_id", "clicked", "document_id_x",
                                                           "click_tstamp", "platform", "geo_location",
                                                           "document_id_y", "publish_time"])
# Calculating "ad age" = click_timestamp - publish_timestamp in days
times = merged_4.publish_time
real_times = []

for i in range(len(times)):
    time_struct = time.strptime(times[i], "%Y-%m-%d %H:%M:%S")
    real_times.append(int(time.mktime(time_struct)))

real_times[:10]

click_times = merged_4.click_tstamp

ad_ages = click_times - real_times
ad_ages_in_days = ad_ages / 86400


merged_4["ad_age_in_days"] = ad_ages_in_days

merged_4.drop(["click_tstamp", "publish_time"], axis=1, inplace=True)


merged_4.to_csv("fourth_merge_w_ad_age.csv", index=False)


#############################################

merged_4 = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/fourth_merge_w_ad_age.csv")

docs_1 = np.array(merged_4.document_id_x)
docs_2 = np.array(merged_4.document_id_y)
docs_3 = np.concatenate((docs_1, docs_2))
docs_3 = pd.Series(docs_3).unique()


# Creating filtered versions of document attributes tables to include only relevant displays,
# This makes calculations down the road much quicker
iter_csv = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/documents_topics.csv", iterator=True, chunksize=20000)
topics = pd.concat([chunk[chunk['document_id'].isin(docs_3)] for chunk in iter_csv])

print("finished topics")

iter_csv = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/documents_categories.csv", iterator=True, chunksize=20000)
categories = pd.concat([chunk[chunk['document_id'].isin(docs_3)] for chunk in iter_csv])

print("finished categories")

iter_csv = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/documents_entities.csv", iterator=True, chunksize=20000)
entities = pd.concat([chunk[chunk['document_id'].isin(docs_3)] for chunk in iter_csv])

print("finished entities")


# Calculating similarities between documents
from functions import find_similarity
topic_similarities = []
entities_similarities = []
categories_similarities = []

counter = 0
for row in merged_4.itertuples():
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

# Saving the final table

merged_4["topic_sim"] = topic_similarities
merged_4["entities_sim"] = entities_similarities
merged_4["categories_sim"] = categories_similarities

merged_4.to_csv("fifth_merge.csv", index=False)


###################################################







