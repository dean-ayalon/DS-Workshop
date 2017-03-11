import numpy as np
import pandas as pd

'''
input: standard table and one of the entities, categories and topics tables
output: a credentiality factor for each ad
the formula for the credentiality is the sum of all confidences.
'''
def calculate_credentiality(main_table,elements,promoted_content):
    # Slicing only necessary columns
    ad_table = main_table[["ad_id", "clicked"]]
    ##changing ad_id to document_id using the promoted_content table
    with_doc = ad_table.merge(promoted_content, on="ad_id")
    ##summing up all elements confidence levels for all docs
    doc_cred = elements.groupby(["document_id"],as_index=False).agg({"confidence_level":np.sum})
    #return what's relevant for main_table, that is, only ad and new attribute
    attribute = pd.merge(with_doc, doc_cred, on="document_id")
    return attribute[["ad_id", "confidence_level"]]
