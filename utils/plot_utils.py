import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from paths import *

#main_table = pd.read_csv(MAIN_TABLE_YAIR)

def create_simple_histogram(categoryArr,countArr,title,x_label,y_label,file_name):
    fig = plt.figure()
    fig.suptitle(title,fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.bar(left=categoryArr, height=countArr)
    plt.savefig(file_name)
    #plt.show()

def plot_platform_histogram(main_table):
    platforms_count = main_table[["platform_is_desktop","platform_is_mobile","platform_is_tablet"]]
    platforms_count = np.array(platforms_count.sum())
    platforms_names = np.array(["Desktop","Mobile","Tablet"])
    fig = plt.figure()
    fig.suptitle("Amount of platforms",fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel("Platform type")
    ax.set_ylabel("Amount")
    width = 0.3
    bins = list(map(lambda x: x - width / 2, range(1, len(platforms_count) + 1)))
    ax.bar(bins, platforms_count, width=width)
    ax.set_xticks(list(map(lambda x: x, range(1, len(platforms_count) + 1))))
    ax.set_xticklabels(platforms_names)

    #plt.bar(left=platforms_names, height=platforms_count)
    #plt.savefig("test.png")
    #plt.show()

def create_disp_number_piechart(main_table):
    disp_size = main_table[["display_id","ad_id"]]
    disp_size = disp_size.groupby(["display_id"],as_index=False).agg({"ad_id":np.count_nonzero})\
        .rename(index=str, columns={"ad_id" : 'disp_size'})
    disp_size_count = disp_size.groupby(["disp_size"],as_index=False).agg({"display_id":np.count_nonzero})\
        .rename(index=str, columns={"display_id" : 'disp_size_count'})
    disp_size_count_arr = np.array(disp_size_count['disp_size_count'])
    disp_size_type = np.array(disp_size_count['disp_size'])

    #now create the pie chart
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    fig1, ax1 = plt.subplots()
    ax1.pie(disp_size_count_arr, labels=disp_size_type, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    #plt.savefig('test.png')

