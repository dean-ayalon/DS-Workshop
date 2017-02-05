import numpy as np
import pandas as pd


#given a table name and a column name - returns only unique appearences of value from that column
def return_unique_values_of_column_from_table(column_name,table_name):
    unique_column = pd.read_csv(table_name, usecols = [column_name])
    unique_column = pd.Series(np.array(unique_column[column_name])).unique()
    return unique_column

def filter_table_by_unique_ids(filter_column,filter_name,table_to_filter):
    filtered_table = pd.concat([chunk[chunk[filter_name].isin(filter_column)] for chunk in table_to_filter])
    return filtered_table
