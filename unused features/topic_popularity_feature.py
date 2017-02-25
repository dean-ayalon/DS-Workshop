from utils.plot_utils import create_simple_histogram
from utils.table_utils import *
from paths import *
import numpy as np
import pandas as pd
import gc


def create_topics_popularity(main_table, topics, with_confidence=True):
    # ------------------------------Clicks per topic----------------------
    relevant_ads_and_docs = main_table[["document_id_y", "ad_id", "clicked"]]\
        .rename(index=str, columns={"document_id_y": "document_id"})

    relevant_ads_docs_and_topics = relevant_ads_and_docs.merge(topics, on='document_id', how='left')
    print("relevant_ads_and_docs_and_topics is")
    print(relevant_ads_docs_and_topics.head())

    clicks_per_topic = relevant_ads_docs_and_topics.groupby(["topic_id"], as_index=False).agg({"clicked": np.sum})\
        .rename(index=str, columns={'clicked': 'clicks_No'})

    print("clicks per topic is")
    print(clicks_per_topic.head())
    '''
    #creates histogram
    topicArr = np.array(clicks_per_topic[["topic_id"]])
    clicksArr = np.array(clicks_per_topic[["clicked"]])
    create_simple_histogram(topicArr,clicksArr,"Clicks Per topic","Topics","Clicks","clicks_per_topics.png")
    '''
    # -----------------------Topic per Document Histogram------------------------

    docs_per_topic = topics.groupby(["topic_id"], as_index=False).agg({"document_id": np.count_nonzero})\
        .rename(index=str, columns={"document_id": "doc_No"})

    print("docs_per_topic is")
    print(docs_per_topic.head())

    topic_popularity = topics.merge(clicks_per_topic, on="topic_id", how="left")\
                             .merge(docs_per_topic, on="topic_id", how="left")

    print("topic_popularity is")


    documents = topic_popularity["document_id"].unique()
    topic_popularity_vector = np.zeros(shape=len(documents))
    print(documents[:10])

    for document in documents:
        doc_frame = topic_popularity[topic_popularity["document_id"] == document]
        doc_topics = doc_frame["topic_id"]
        doc_topic_confs = doc_frame["confidence_level"]
        doc_topic_popularities = doc_frame["clicks_No"]

        break

    if with_confidence:
        topic_popularity['topic_popularity_conf'] = \
            (topic_popularity['clicks_No']*topic_popularity['confidence_level'])/topic_popularity['doc_No']
    else:
        topic_popularity['topic_popularity'] = topic_popularity['clicks_No'] / topic_popularity['doc_No']

    topic_popularity.drop(['clicked', 'document_id', 'topic_id', 'confidence_level', 'clicks_No', 'doc_No'],
                          axis=1, inplace=True)
    topic_popularity.groupby(["ad_id"], as_index=False)

    return topic_popularity

main_table = pd.read_csv(MAIN_TABLE_DEAN)
topics = pd.read_csv(DOC_TOPICS_DEAN)
T = create_topics_popularity(main_table, topics)

print(T.head())
