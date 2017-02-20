from utils.analysis_utils import *
import numpy as np
import pandas as pd
import sklearn.preprocessing
import sklearn.linear_model
from paths import *


# Importing main table
final = pd.read_csv(MAIN_TABLE_DEAN)

# Scaling all features
features = ["topic_sim", "entities_sim", "categories_sim",
            "is_morning", "is_noon", "is_afternoon", "is_evening", "is_night",
            "is_weekend", "platform_is_mobile", "platform_is_desktop", "platform_is_tablet",
            "clicks_appearances_ratio", "ad_count_per_display", "ads_per_advertiser",
            "ads_per_campaign"]

features_to_scale = ["topic_sim", "entities_sim", "categories_sim",
                     "clicks_appearances_ratio", "ad_count_per_display",
                     "ads_per_advertiser", "ads_per_campaign"]

for feature in features_to_scale:
    final[feature] = sklearn.preprocessing.scale(final[feature])


# Splitting to train (80%) and test (20%) sets
train_data, test_data = split_to_test_and_train(final)

train_features_list = [train_data[feature] for feature in features]
test_features_list = [test_data[feature] for feature in features]

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
zero_one_accuracy = accuracy_zero_one_loss(test_data)
print(zero_one_accuracy)

#Computing MAP@12 Accuracy
accuracy_map = MAP12_Accuracy(test_data)

print(accuracy_map)
