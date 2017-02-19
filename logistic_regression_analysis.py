from utils.analysis_utils import *
import numpy as np
import pandas as pd
import sklearn.preprocessing
import sklearn.linear_model
from scipy.stats import describe
from scipy.stats.mstats import mode
import statsmodels.api as sm
import gc
import seaborn as sns
import sys
import time
sns.set(color_codes=True)
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from paths import *


# Importing main table
final = pd.read_csv(MAIN_TABLE_YAIR, usecols=["display_id", "ad_id", "ad_age_in_days", "topic_sim",
                                                          "entities_sim", "categories_sim", "clicked"])

# Scaling all features
features = ["topic_sim", "entities_sim", "categories_sim", "ad_age_in_days"]
for feature in features:
    final[feature] = sklearn.preprocessing.scale(final[feature])

# Rearranging so "clicked" column is last TODO: this should be done before when creating the table
cols = final.columns.tolist()
cols = cols[:2] + cols[3:] + [cols[2]]
final = final[cols]

# Splitting to train (80%) and test (20%) sets
train_data,test_data = split_to_test_and_train(final)


#TODO: the lists are temporary and should be done with a function
train_features_list = [train_data.ad_age_in_days, train_data.topic_sim,
                    train_data.entities_sim, train_data.categories_sim]

test_features_list = [test_data.ad_age_in_days, test_data.topic_sim,
                    test_data.entities_sim, test_data.categories_sim]

# Extracting X and y vectors for train and test
train_points, train_labels = prepare_dataset_for_model(train_features_list, train_data.clicked)

test_points, test_labels = prepare_dataset_for_model(test_features_list, test_data.clicked)

# Training Logistic Regression model on training set

model = sklearn.linear_model.LogisticRegression(C=1000, penalty="l1")
model_fit = model.fit(train_points, train_labels)
model_fit.score(test_points, test_labels)

# Testing the model on the test set

# Extracting predicted probabilities and adding them to the test_data dataframe
display_probs = model_fit.predict_proba(test_points)[:, 1]
test_data["probability_of_click"] = display_probs #TODO: something is wrong here, got a warning. need to fix it

# Testing the accuracy (currently using 0/1 loss)
zero_one_accuracy = accueacy_zero_one_lost(test_data)
print(zero_one_accuracy)

#Computing MAP@12 Accuracy
accuracy_map = MAP12_Accuracy(test_data)

print(accuracy_map)
