from utils.plot_utils import create_simple_histogram,create_simple_pie_chart
from paths import *
import numpy as np
import pandas as pd
from utils.table_utils import filter_table_by_unique_ids, return_unique_values_of_column_from_table

main_table = pd.read_csv(MAIN_TABLE_YAIR)
doc_geo = pd.read_csv(DOC_GEO_YAIR)

#TODO: change all docs to displays!!

#returns the countries from display_geo who which are at list 1% from all the countries appears
def filter_countries_by_size(disp_geo,size):
    countries = disp_geo.groupby(["country"], as_index=False).agg({"document_id": np.count_nonzero})\
        .rename(index=str, columns={"document_id" : 'country_count'})[1:]
    countries = countries[countries['country_count']>len(doc_geo)/size]
    return countries

def create_binary_country(main_table):
    disp_geo_itr = pd.read_csv(DOC_GEO_YAIR, iterator=True, chunksize=1000000)
    main_table = main_table.rename(index=str, columns={"document_id_y" : 'document_id'}) #TODO: won't be needed for displays
    unique_displays = return_unique_values_of_column_from_table('document_id',main_table)
    relavent_countries = filter_table_by_unique_ids(unique_displays,"document_id",disp_geo_itr)

    # Extracting the platform vector and creating 3 boolean vectors based on it
    # TODO consider just US and NOT US
    countries = relavent_countries["country"]
    country_is_US = np.array(countries == 'US', dtype=int)
    country_is_GB = np.array(countries == 'GB', dtype=int)
    country_is_CA = np.array(countries == 'CA', dtype=int)
    country_is_AU = np.array(countries == 'AU', dtype=int)

    # Creating the result Dataframe
    res_frame = pd.DataFrame()
    res_frame["display_id"] = relavent_countries["document_id"]
    res_frame["country_is_US"] = country_is_US
    res_frame["country_is_GB"] = country_is_GB
    res_frame["country_is_CA"] = country_is_CA
    res_frame["country_is_AU"] = country_is_AU

    return res_frame




