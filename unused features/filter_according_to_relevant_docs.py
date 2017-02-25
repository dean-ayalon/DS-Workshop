import pandas as pd
import numpy as np

# Load final table as merged_4
final = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/fifth_merge_w_top_sim.csv")


docs_1 = np.array(final.document_id_x)
docs_2 = np.array(final.document_id_y)
docs_3 = np.concatenate((docs_1, docs_2))
docs_3 = pd.Series(docs_3).unique()


# For example, filtering topics

# Change chunk size if any problems happen
iter_csv = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/documents_topics.csv", iterator=True, chunksize=20000)
topics = pd.concat([chunk[chunk['document_id'].isin(docs_3)] for chunk in iter_csv])

