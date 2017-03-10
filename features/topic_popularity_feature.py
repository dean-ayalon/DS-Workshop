from utils.plot_utils import create_simple_histogram
from utils.table_utils import return_unique_values_of_column_from_table,filter_table_by_unique_ids
from paths import *
import numpy as np
import pandas as pd


def create_topics_popularity(main_table, topics, with_confidence=True, with_test=False):
    # ------------------------------Clicks per topic----------------------
    #this block of code counts for each relevant topic the amount of clicks it got.
    #get relevant ads and blocks
    relevant_ads_and_docs = main_table[["document_id_y", "ad_id", "clicked"]]\
        .rename(index=str, columns={"document_id_y": "document_id"})

    #merge them with document_topics
    relevant_ads_docs_and_topics = relevant_ads_and_docs.merge(topics, on='document_id')
    if(with_test):
        print("relevant_ads_and_docs_and_topics is")
        print(relevant_ads_docs_and_topics.head())

    #count the amount of clicks
    clicks_per_topic = relevant_ads_docs_and_topics.groupby(["topic_id"], as_index=False).agg({"clicked": np.sum})\
        .rename(index=str, columns={'clicked': 'clicks_No'})

    if(with_test):
        print("clicks per topic is")
        print(clicks_per_topic.head())

    # -----------------------Topic per Document Histogram------------------------

    #filter from the whole docuemnt_topics table the relevant rows
    relevant_docs = return_unique_values_of_column_from_table('document_id_y',main_table)
    f_topics = filter_table_by_unique_ids(relevant_docs,'document_id',DOC_TOPICS_YAIR)

    #for each topic count the amount of docs he has
    docs_per_topic = f_topics.groupby(["topic_id"], as_index=False).agg({"document_id": np.count_nonzero})\
        .rename(index=str, columns={"document_id": "doc_No"})

    if(with_test):
        print("docs_per_topic is")
        print(docs_per_topic.head())

    #merge the two relations we have creates previously
    topic_popularity = relevant_ads_docs_and_topics.merge(clicks_per_topic, on="topic_id")\
                             .merge(docs_per_topic, on="topic_id")

    #choose if you want to calculate with conficence or not
    if with_confidence:
        topic_popularity['topic_popularity_conf'] = \
            (topic_popularity['clicks_No']*topic_popularity['confidence_level'])/topic_popularity['doc_No']
    else:
        topic_popularity['topic_popularity'] = topic_popularity['clicks_No'] / topic_popularity['doc_No']

    #drop unnecessary columns and duclicated rows and sum the whole values we got for each ad (since an ad can have different topics)
    topic_popularity = topic_popularity.drop_duplicates()
    topic_popularity.drop(['clicked', 'document_id', 'topic_id', 'confidence_level', 'clicks_No', 'doc_No'],
                          axis=1, inplace=True)
    topic_popularity = topic_popularity.groupby(["ad_id"], as_index=False).agg({"topic_popularity_conf": np.sum})

    return topic_popularity





