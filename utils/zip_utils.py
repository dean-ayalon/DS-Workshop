import pandas as pd
import zipfile as zp
from paths import *
from utils.table_utils import return_unique_values_of_column_from_table, filter_table_by_unique_ids

#import main_table:
main_table = pd.read_csv(MAIN_TABLE_YAIR)
#dataset = pd.read_csv(DATASET)
#with this object we zip
zf = zp.ZipFile("./tables.zip", "w", zp.ZIP_DEFLATED,allowZip64=True)
relevant_displays = return_unique_values_of_column_from_table('display_id',main_table)
relevant_docs_in = return_unique_values_of_column_from_table('document_id_y',main_table)
relevant_docs_out = return_unique_values_of_column_from_table('document_id_x',main_table)
relevant_ads = return_unique_values_of_column_from_table('ad_id',main_table)

samples_names = ['./sample_clicks.csv','./sample_document_categories.csv','./sample_document_entities.csv',
                 './sample_document_meta.csv','./sample_topics.csv','./sample_events.csv',
                 './sample_promoted.csv','./sample_display_geo.csv']

print('sampling tables and writing them to csv files...')
#sampling and writing to csv relevant samples from the tables
#len: 2724795
sample_clicks = filter_table_by_unique_ids(relevant_displays,'display_id',CLICKS_YAIR)
sample_clicks.to_csv('./sample_clicks.csv',index=False)
#len: 120546
sample_doc_cat = filter_table_by_unique_ids(relevant_docs_in,'document_id',DOC_CATEGORIES_YAIR)
sample_doc_cat.to_csv('./sample_document_categories.csv',index=False)
#len: 137335
sample_doc_ent = filter_table_by_unique_ids(relevant_docs_in,'document_id',DOC_ENTITIES_YAIR)
sample_doc_ent.to_csv('./sample_document_entities.csv',index=False)
#len: 60484
sample_doc_meta = filter_table_by_unique_ids(relevant_docs_in,'document_id',DOC_META_YAIR)
sample_doc_meta.to_csv('./sample_document_meta.csv',index=False)
#len: 227895
sample_doc_top = filter_table_by_unique_ids(relevant_docs_in,'document_id',DOC_TOPICS_YAIR)
sample_doc_top.to_csv('./sample_topics.csv',index=False)
#len:527331
sample_events = filter_table_by_unique_ids(relevant_displays,'display_id',EVENTS_YAIR)
sample_events.to_csv('./sample_events.csv',index=False)
#len: 201077
sample_page_views = filter_table_by_unique_ids(relevant_docs_out,'document_id',PAGE_VIEWS_YAIR)
sample_page_views.to_csv('./sample_page_views.csv',index=False)
#len: 143610
sample_promoted = filter_table_by_unique_ids(relevant_ads,'ad_id',PROMOTED_CONTENT_YAIR)
sample_promoted.to_csv('./sample_promoted.csv',index=False)
#len: 527331
sample_display_geo = filter_table_by_unique_ids(relevant_displays,'display_id',DISPLAY_GEO_YAIR)
sample_display_geo.to_csv('./sample_display_geo.csv',index=False)
print('finished sampling')

#zip all of them using their path.
print('writing to zip')
for name in samples_names:
    zf.write(name)
zf.close()
print('finished zipping')

#this code splits the data set into two different parts
def split_in_half_and_zip_table(path,zip_name,file_name):
    print('spliting and zipping dataset')
    dataset = pd.read_csv(path)
    #isStateCount = True
    #if(isStateCount):
    #    dataset.drop('state_count',axis=1,inplace=True) #this feature is not good
    print("zipping first part")
    middle = len(dataset)//2
    #writing the first part
    zf = zp.ZipFile("./"+zip_name+"_p1.zip", "w", zp.ZIP_DEFLATED,allowZip64=True)
    dataset_p1 = dataset[:middle]
    dataset_p1.to_csv('./'+file_name+'_p1.csv',index=False)
    zf.write('./'+file_name+'_p1.csv')
    zf.close()
    print("finished zipping first part")

    #writing the second part
    print("zipping second part")
    zf = zp.ZipFile("./"+zip_name+"_p2.zip", "w", zp.ZIP_DEFLATED,allowZip64=True)
    dataset_p2 = dataset[middle:]
    dataset_p2.to_csv('./'+file_name+'_p2.csv',index=False)
    zf.write('./'+file_name+'_p2.csv')
    zf.close()
    print("finished zipping second part")
    print('finished spliting and zipping main dataset')

#main dataset zips
split_in_half_and_zip_table(DATASET,'dataset','final_dataset')
#page_views is huge and therefore needs 2 zips
split_in_half_and_zip_table(PAGE_VIEWS,'page_views','sample_page_views')


#Example how to read table from zip
#oz = zp.ZipFile('tables.zip')
#sample_clicks = pd.read_csv(oz.open('sample_clicks.csv'))

#EXAMPLE:
dataset = pd.read_csv(DATASET)
#this code imports and unite the two parts of the dataset:
z_dataset_p1 = zp.ZipFile('./dataset_p1.zip')
z_dataset_p2 = zp.ZipFile('./dataset_p2.zip')

dataset_p1 = pd.read_csv(z_dataset_p1.open('final_dataset_p1.csv'))
dataset_p2 = pd.read_csv(z_dataset_p2.open('final_dataset_p2.csv'))

dataset_t = pd.concat([dataset_p1,dataset_p2],ignore_index=True)

print('original dataset and united two halves of dataset are equal: '+str(dataset.equals(dataset_t)))
#sanity check:
#dataset.equals(dataset_t)
