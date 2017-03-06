from utils.analysis_utils import *
import numpy as np
import pandas as pd
import sklearn.preprocessing
import sklearn.linear_model
import sklearn.ensemble
import sklearn.grid_search
from paths import *


def main_accuracy_test():
    final = pd.read_csv(MAIN_TABLE_DEAN)

    # Full feature list, before eliminating unimportant features
    features = ["topic_sim", "entities_sim", "categories_sim",
                "is_morning", "is_noon", "is_afternoon", "is_evening", "is_night",
                "is_weekend", "platform_is_mobile", "platform_is_desktop", "platform_is_tablet",
                "clicks_appearances_ratio", "ad_count_per_display", "ads_per_advertiser",
                "ads_per_campaign"]

    # Short feature list - only important features according to model
    #features = ["topic_sim", "entities_sim", "categories_sim",
    #            "is_evening", "platform_is_mobile", "platform_is_desktop",
    #            "clicks_appearances_ratio", "ad_count_per_display",
    #            "ads_per_advertiser", "ads_per_campaign"]

    features_to_scale = ["topic_sim", "entities_sim", "categories_sim",
                         "clicks_appearances_ratio", "ad_count_per_display",
                         "ads_per_advertiser", "ads_per_campaign"]

    # Scaling all non-boolean features to zero mean and unit variance
    for feature in features_to_scale:
        final[feature] = sklearn.preprocessing.scale(final[feature])

    displays = final.display_id.unique()
    np.random.RandomState(0).shuffle(displays)

    # Performing 7-fold CV
    zero_one_accuracies = np.zeros(shape=7)
    map_12_accuracies = np.zeros(shape=7)

    for i in range(7):
        print("Now working on fold number " + str(i))
        test_displays = displays[i*75333:(i+1)*75333]
        if i == 0:
            train_displays = displays[75333:]
        elif i == 6:
            train_displays = displays[:6*75333]
        else:
            train_displays = np.concatenate((displays[:i*75333], displays[(i+1)*75333:]))

        train_df = final[final.display_id.isin(train_displays)]
        test_df = final[final.display_id.isin(test_displays)]

        train_features_list = [train_df[feature] for feature in features]
        test_features_list = [test_df[feature] for feature in features]

        # Extracting X and y vectors for train and test
        train_points, train_labels = prepare_dataset_for_model(train_features_list, train_df.clicked)
        test_points, test_labels = prepare_dataset_for_model(test_features_list, test_df.clicked)

        model = sklearn.ensemble.GradientBoostingClassifier(max_depth=4, verbose=True)
        model.fit(train_points, train_labels)

        display_probs = model.predict_proba(test_points)[:, 1]
        test_df["probability_of_click"] = display_probs  # Error generated at this line can be ignored

        # Evaluating the model using 0/1 loss
        zero_one_accuracy = accuracy_zero_one_loss(test_df)
        zero_one_accuracies[i] = zero_one_accuracy
        print("0/1 Accuracy for Gradient Boosting Algorithm: " + str(zero_one_accuracy))

        # Evaluating the model using MAP@12 metric
        map12_accuracy = MAP12_Accuracy(test_df)
        map_12_accuracies[i] = map12_accuracy
        print("MAP@12 Accuracy for Gradient Boosting Algorithm: " + str(map12_accuracy))

    print("Mean 0-1 Accuracy: " + str(zero_one_accuracies.mean()))
    print("Mean Map@12 Accuracy: " + str(map_12_accuracies.mean()))









