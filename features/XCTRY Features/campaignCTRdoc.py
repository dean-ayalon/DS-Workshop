from features.XCTRY_feature import *
from paths import *

main_table = pd.read_csv(MAIN_TABLE_DEAN)
main_table = main_table.rename(index=str, columns={"document_id_y": 'document_id'})
#promoted = pd.read_csv(PROMOTED_CONTENT_YAIR)
meta = pd.read_csv(DOC_META_DEAN)
doc_category = pd.read_csv(DOC_CATEGORIES_DEAN)
doc_topic = pd.read_csv(DOC_TOPICS_DEAN)
doc_category = pd.read_csv(DOC_CATEGORIES_YAIR,)
#doc_topic = pd.read_csv(DOC_TOPICS_YAIR)
#events = pd.read_csv(EVENTS_YAIR)

#TODO: this works
def create_publishCTRcampaign(main_table,promoted,meta):
    f = XCTRY(main_table,promoted,meta,'campaign_id','publisher_id','document_id')
    return f
'''
def create_advertiserCTRcampign(main_table,promoted):
    f = XCTRY(main_table,promoted,promoted,'campaign_id','advertiser_id','document_id',with_test=True)
    return f
'''

#TODO: memory error....
def create_categoryCTRsource(main_table, doc_category, doc_meta):
    f = XCTRY(main_table,doc_category,doc_meta,'category_id','source_id','document_id',with_test=True)
    return f

#TODO: this works
def create_publishCTRadvertiser(main_table, promoted, meta):
    f = XCTRY(main_table,promoted,meta,'advertiser_id','publisher_id','document_id',with_test=True)
    return f

#TODO: got memory error
def create_topicCTRpublisher(main_table, doc_topics, doc_meta):
    f = XCTRY(main_table,doc_topics,doc_meta,'topic_id','publisher_id','document_id')
    return f

#tests:
#1
#f = create_publishCTRcampaign(main_table,promoted,meta)

#2
#f = create_advertiserCTRcampign(main_table,promoted) TODO: DO NOT ACIVATE THIS!

#3
ad_doc_category = doc_category.merge(main_table, on=['document_id'], copy=False)
f = create_categoryCTRsource(main_table, ad_doc_category, meta) #TODO: got memory error for this feature...

#4
#f = create_publishCTRadvertiser(main_table,promoted,meta)

#5
ad_doc_topic = doc_topic.merge(main_table, on=['document_id'])[['ad_id','topic_id','document_id']]
f = create_topicCTRpublisher(main_table,ad_doc_topic,meta)
print(f.head(100))