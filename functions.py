import numpy as np


def find_similarity(table, doc_out, doc_in, field):
    # all the topics of the doc_out
    out_frame = table[table.document_id == doc_out]
    out_items = np.array(out_frame[field])
    #print("out_topics: " + str(out_topics))
    out_conf = np.array(out_frame.confidence_level)
    #print("out_conf: " + str(out_conf))

    # all the topics of the doc_in
    in_frame = table[table.document_id == doc_in]
    in_items = np.array(in_frame[field])
    #print("in_topics: " + str(in_topics))
    in_conf = np.array(in_frame.confidence_level)
    #print("in_conf: " + str(in_conf))

    # getting similarity
    similarity = 0
    # for every out_topic
    for out_index in range(len(out_items)):
        item = out_items[out_index]
        # if the other doc has indeed the topic
        if item in in_items:
            # using the formula stated in adding attr1
            in_index = np.argwhere(in_items == item)[0][0]
            s1 = out_conf[out_index]
            s2 = in_conf[in_index]
            similarity += s1*s2
    return similarity


