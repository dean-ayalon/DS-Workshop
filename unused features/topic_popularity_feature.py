from utils.plot_utils import create_simple_histogram
#from utils.table_utils import *
from paths import *
import numpy as np
import pandas as pd
import gc


def create_topics_popularity(main_table, topics, with_confidence=True, with_test=False):
    # ------------------------------Clicks per topic----------------------
    relevant_ads_and_docs = main_table[["document_id_y", "ad_id", "clicked"]]\
        .rename(index=str, columns={"document_id_y": "document_id"})

    #len: 7206463
    relevant_ads_docs_and_topics = relevant_ads_and_docs.merge(topics, on='document_id')
    if(with_test):
        print("relevant_ads_and_docs_and_topics is")
        print(relevant_ads_docs_and_topics.head())

    #len: 300
    clicks_per_topic = relevant_ads_docs_and_topics.groupby(["topic_id"], as_index=False).agg({"clicked": np.sum})\
        .rename(index=str, columns={'clicked': 'clicks_No'})
    if(with_test):
        print("clicks per topic is")
        print(clicks_per_topic.head())
    '''
    #creates histogram
    topicArr = np.array(clicks_per_topic[["topic_id"]])
    clicksArr = np.array(clicks_per_topic[["clicked"]])
    create_simple_histogram(topicArr,clicksArr,"Clicks Per topic","Topics","Clicks","clicks_per_topics.png")
    '''
    # -----------------------Topic per Document Histogram------------------------

    #len: 300
    docs_per_topic = topics.groupby(["topic_id"], as_index=False).agg({"document_id": np.count_nonzero})\
        .rename(index=str, columns={"document_id": "doc_No"})

    if(with_test):
        print("docs_per_topic is")
        print(docs_per_topic.head())

    '''
    #creates docs per topics histogram
    topic_ids = np.array(docs_per_topic[["topic_id"]])
    number_of_documents = np.array(docs_per_topic[["document_id"]])
    create_simple_histogram(topic_ids,number_of_documents,"Docs_per_topics","Topics","Docs","docs_per_topics.png")
    '''

    topic_popularity = relevant_ads_docs_and_topics.merge(clicks_per_topic, on="topic_id")\
                             .merge(docs_per_topic, on="topic_id")

    if with_confidence:
        topic_popularity['topic_popularity_conf'] = \
            (topic_popularity['clicks_No']*topic_popularity['confidence_level'])/topic_popularity['doc_No']
    else:
        topic_popularity['topic_popularity'] = topic_popularity['clicks_No'] / topic_popularity['doc_No']

    topic_popularity = topic_popularity.drop_duplicates()
    topic_popularity.drop(['clicked', 'document_id', 'topic_id', 'confidence_level', 'clicks_No', 'doc_No'],
                          axis=1, inplace=True)
    topic_popularity = topic_popularity.groupby(["ad_id"], as_index=False).agg({"topic_popularity_conf": np.sum})
    #len(topic_popularity) is 138378
    return topic_popularity

#this code cn merge the feature to the main table. it keeps it size.
#main_table = pd.read_csv(MAIN_TABLE_YAIR)
#topics = pd.read_csv(DOC_TOPICS_YAIR)
#T = create_topics_popularity(main_table, topics)
#m = main_table.merge(T, on="ad_id",how="left")
#print(T.head())

#TODO: later trasfer this code to hist_utils
ads_no = 30000
indexes = np.random.RandomState(0).permutation(len(T))[:ads_no]
create_simple_histogram(np.array(T["ad_id"])[indexes],np.array(T["topic_popularity_conf"])[indexes],"Topic popularity per ad",
                         "Ad id","Topic popularity rate","Topic_popularity_rate_hist.png",do_print=True)



