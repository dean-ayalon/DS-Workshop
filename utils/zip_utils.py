import pandas as pd
import zipfile as zp
from paths import *
from utils.table_utils import return_unique_values_of_column_from_table, filter_table_by_unique_ids

#import main_table:
main_table = pd.read_csv(MAIN_TABLE_YAIR)
#with this object we zip
zf = zp.ZipFile("tables.zip", "w", zp.ZIP_DEFLATED,allowZip64=True)
relevant_displays = return_unique_values_of_column_from_table('display_id',main_table)
relevant_docs = return_unique_values_of_column_from_table('document_id_y',main_table)
relevant_ads = return_unique_values_of_column_from_table('ad_id',main_table)

samples_names = ['sample_clicks.csv','sample_document_categories.csv','sample_document_entities.csv',
                 'sample_document_meta.csv','sample_topics.csv','sample_events.csv',
                 'sample_page_views.csv','sample_promoted.csv','final_main_table.csv']
#sampling and writing to csv relevant samples from the tables
#len: 2724795
sample_clicks = filter_table_by_unique_ids(relevant_displays,'display_id',CLICKS_YAIR)
sample_clicks.to_csv('sample_clicks.csv',index=False)
#len: 171148
sample_doc_cat = filter_table_by_unique_ids(relevant_displays,'document_id',DOC_CATEGORIES_YAIR)
sample_doc_cat.to_csv('sample_document_categories.csv',index=False)
#len: 173616
sample_doc_ent = filter_table_by_unique_ids(relevant_displays,'document_id',DOC_ENTITIES_YAIR)
sample_doc_ent.to_csv('sample_document_entities.csv',index=False)
#len: 93523
sample_doc_meta = filter_table_by_unique_ids(relevant_displays,'document_id',DOC_META_YAIR)
sample_doc_meta.to_csv('sample_document_meta.csv',index=False)
#len: 353366
sample_doc_top = filter_table_by_unique_ids(relevant_displays,'document_id',DOC_TOPICS_YAIR)
sample_doc_top.to_csv('sample_topics.csv',index=False)
#len:
sample_events = filter_table_by_unique_ids(relevant_displays,'display_id',EVENTS_YAIR)
sample_events.to_csv('sample_events.csv',index=False)
#len: 527331
sample_page_views = filter_table_by_unique_ids(relevant_displays,'document_id',PAGE_VIEWS_YAIR)
sample_page_views.to_csv('sample_page_views.csv',index=False)
#len: 284217
sample_promoted = filter_table_by_unique_ids(relevant_displays,'ad_id',PROMOTED_CONTENT_YAIR)
sample_promoted.to_csv('sample_promoted.csv',index=False)



#zip all of them using their path.
print('writing to zip')
for name in samples_names:
    zf.write(name)
zf.close()
print('finished zipping')

#oz = zp.ZipFile('tables.zip')
#sample_clicks = pd.read_csv(oz.open('sample_clicks.csv'))