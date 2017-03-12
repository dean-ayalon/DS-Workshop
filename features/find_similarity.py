import numpy as np

# Multi-purpose function used to extract similarity metrics for document topics, entities and categories


def find_similarity(table, doc_out, doc_in, field):
    # Extracting all data relevant to doc_out
    out_frame = table[table.document_id == doc_out]
    out_items = np.array(out_frame[field])
    out_conf = np.array(out_frame.confidence_level)

    # Extracting all data relevant to doc_in
    in_frame = table[table.document_id == doc_in]
    in_items = np.array(in_frame[field])
    in_conf = np.array(in_frame.confidence_level)

    # Computing requested similarity by multiplying conf levels of shared topics/entities/categories
    similarity = 0
    for out_index in range(len(out_items)):
        item = out_items[out_index]
        #TODO: add lines:
        #in_items = np.array(in_frame[field])
        #in_conf = np.array(in_frame.confidence_level)
        if item in in_items:
            in_index = np.argwhere(in_items == item)[0][0]
            s1 = out_conf[out_index]
            s2 = in_conf[in_index]
            similarity += s1*s2
    return similarity


