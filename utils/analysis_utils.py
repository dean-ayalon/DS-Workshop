import numpy as np
import sklearn.preprocessing
import sklearn.linear_model


# TODO: this function should receive a list of features and dynamically create a table from it.
def create_final_table_from_features(feature_list):
    pass


def scale_features(final, features_names_list):
    for feature in features_names_list:
        final[feature] = sklearn.preprocessing.scale(final[feature])

# Receives a dataframe with all the features and splits it to train and test


def split_to_test_and_train(final, write_to_files=False):
    displays = final.display_id.unique()
    # Create an array were 80% of the indexes labeled as True
    rand_bool_array = np.random.RandomState(0).rand(len(displays)) < 0.8
    # In the train displays only indexes who are labeled as True will be included.
    train_displays = displays[rand_bool_array]
    test_displays = displays[~rand_bool_array]

    # Generating new separate train and test dataframes
    train_df = final[final.display_id.isin(train_displays)]
    test_df = final[final.display_id.isin(test_displays)]

    if write_to_files:
        train_df.to_csv("train_data.csv", index=False)
        test_df.to_csv("test_data.csv", index=False)

    return train_df, test_df

# Receives a dataframe and returns a feature vectors and a label vector


def prepare_dataset_for_model(features_list, clicked):
    points = np.dstack(features_list)[0]
    labels = np.array(clicked)
    return points, labels

# Testing the accuracy (using 0/1 loss)
# Notice that the train data need to have a column named "probability_of_click"


def accuracy_zero_one_loss(test_data):
    acc_test_frame = test_data[test_data.clicked == 1][["display_id", "ad_id"]]

    prediction_frame = test_data.sort_values(by="probability_of_click", ascending=False) \
        .groupby("display_id").first()
    predicted_ads = np.array(prediction_frame["ad_id"])

    acc_test_frame["prediction"] = predicted_ads

    accuracy = sum(acc_test_frame.ad_id == acc_test_frame.prediction) / len(acc_test_frame)

    return accuracy

#Computing MAP@12 Accuracy according to TODO: add the link to the relevent place in kaggle
#TODO: i am not sure it is a good idea to add the "probability_of_click" column directly to the table. should check if it can be done when it is separate.
def MAP12_Accuracy(test_data):
    test_displays = test_data.display_id.unique()
    acc_counter = 0
    counter = 0
    for display in test_displays:
        if not counter % (len(test_displays)//100):
            print("processed " + str(round(100 * float(counter) / len(test_displays))) + "% of displays")
        display_df = test_data[test_data.display_id == display]
        true_ad = np.array(display_df[display_df.clicked == 1][["ad_id"]])[0][0]

        display_probs = np.array(display_df.probability_of_click)
        ads = np.array(display_df.ad_id)
        idx_sorted = display_probs.argsort()[::-1]
        ads_sorted = ads[idx_sorted]

        idx_true = np.argwhere(ads_sorted == true_ad)[0][0] + 1
        acc_counter += 1 / idx_true
        counter += 1

    accuracy_map = acc_counter / len(test_displays)
    return accuracy_map
