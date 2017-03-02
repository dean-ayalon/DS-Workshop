from utils.analysis_utils import *
import numpy as np
import pandas as pd
import sklearn.preprocessing
import sklearn.linear_model
import sklearn.ensemble
import sklearn.grid_search
from paths import *

def perform_GBoost_analysis(perform_cv=False):
    # Importing main table
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


    # Splitting to train (80%) and test (20%) sets
    train_data, test_data = split_to_test_and_train(final)

    train_features_list = [train_data[feature] for feature in features]
    test_features_list = [test_data[feature] for feature in features]

    # Extracting X and y vectors for train and test
    train_points, train_labels = prepare_dataset_for_model(train_features_list, train_data.clicked)
    test_points, test_labels = prepare_dataset_for_model(test_features_list, test_data.clicked)

    # Training Gradient Boosting model on training set
    model = sklearn.ensemble.GradientBoostingClassifier(max_depth=4, verbose=True)
    if not perform_cv:
        model.fit(train_points, train_labels)
    else:
        # Performing CV to tune the model's parameters
        print("Now performing Cross Validation to tune the max_depth parameter...")
        parameters = {"max_depth": [2, 3, 4, 5, 6]}
        cv = sklearn.grid_search.GridSearchCV(model, parameters, verbose=True)
        model = cv.fit(train_points, train_labels)
        print("Performed CV, best parameters for model are " + str(model.best_params_))

    # Testing the model on the test set

    # Extracting predicted probabilities and adding them to the test_data dataframe
    display_probs = model.predict_proba(test_points)[:, 1]
    test_data["probability_of_click"] = display_probs  # Error generated at this line can be ignored

    # Evaluating the model using 0/1 loss
    zero_one_accuracy = accuracy_zero_one_loss(test_data)
    print("0/1 Accuracy for Gradient Boosting Algorithm: " + str(zero_one_accuracy))

    # Evaluating the model using MAP@12 metric
    map12_accuracy = MAP12_Accuracy(test_data)
    print("MAP@12 Accuracy for Gradient Boosting Algorithm: " + str(map12_accuracy))

    # Returning the model so we could extract its properties
    return model
