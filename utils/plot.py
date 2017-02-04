import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_simple_histogram(categoryArr,countArr, title,x_label,y_label,file_name):
    fig = plt.figure()
    fig.suptitle(title,fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.bar(left=categoryArr, height=countArr)
    plt.savefig(file_name)
    #plt.show()

