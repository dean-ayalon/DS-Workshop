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




# Importing main table
final = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/fifth_merge.csv", usecols=["display_id", "ad_id", "ad_age_in_days", "topic_sim",
                                                          "entities_sim", "categories_sim", "clicked"])

# Scaling all features
features = ["topic_sim", "entities_sim", "categories_sim", "ad_age_in_days"]
for feature in features:
    final[feature] = sklearn.preprocessing.scale(final[feature])


# Rearranging so "clicked" column is last
cols = final.columns.tolist()
cols = cols[:2] + cols[3:] + [cols[2]]
final = final[cols]

# Splitting to train (80%) and test (20%) sets
displays = final.display_id.unique()

train_displays = []
test_displays = []

for i in range(len(displays)):
    display = displays[i]
    decider = np.random.uniform()
    if decider <= 0.8:
        train_displays.append(display)
    else:
        test_displays.append(display)


# Generating new separate train and test dataframes

train_df = final[final.display_id.isin(train_displays)]
test_df = final[final.display_id.isin(test_displays)]

train_df.to_csv("train_data.csv", index=False)
test_df.to_csv("test_data.csv", index=False)


# Loading the dataframes we've just created

train_data = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/train_data.csv")

test_data = pd.read_csv("C:/Users/Dean/Documents/Semester G/Data Science Workshop/Outbrain "
                         "Data/test_data.csv")

# Extracting X and y vectors for train and test
train_x = np.dstack((train_data.ad_age_in_days, train_data.topic_sim,
                    train_data.entities_sim, train_data.categories_sim))[0]
train_y = np.array(train_data.clicked)


test_x = np.dstack((test_data.ad_age_in_days, test_data.topic_sim,
                    test_data.entities_sim, test_data.categories_sim))[0]
test_y = np.array(test_data.clicked)



# Training Logistic Regression model on training set

model = sklearn.linear_model.LogisticRegression(C=1000, penalty="l1")
model_fit = model.fit(train_x, train_y)
model_fit.score(test_x, test_y)


# Testing the model on the test set

# Extracting predicted probabilities and adding them to the test_data dataframe
display_probs = model_fit.predict_proba(test_x)[:, 1]
test_data["probability_of_click"] = display_probs

# Testing the accuracy (currently using 0/1 loss)
acc_test_frame = test_data[test_data.clicked == 1][["display_id", "ad_id"]]

prediction_frame = test_data.sort_values(by="probability_of_click", ascending=False)\
    .groupby("display_id").first()
predicted_ads = np.array(prediction_frame["ad_id"])

acc_test_frame["prediction"] = predicted_ads

accuracy = sum(acc_test_frame.ad_id == acc_test_frame.prediction) / len(acc_test_frame)

accuracy

#Computing MAP@12 Accuracy
test_displays = test_data.display_id.unique()
acc_counter = 0
counter = 0
for display in test_displays:
    if not counter % 1872:
        print("processed " + str(round((100*counter/187234))) + "% of rows")
    display_df = test_data[test_data.display_id == display]
    #print(display_df.head())
    true_ad = np.array(display_df[display_df.clicked == 1][["ad_id"]])[0][0]
    #print(true_ad)
    display_probs = np.array(display_df.probability_of_click)
    #print(probs)
    ads = np.array(display_df.ad_id)
    #print(ads)
    idx_sorted = display_probs.argsort()[::-1]
    #rint(idx_sorted)

    ads_sorted = ads[idx_sorted]
    #print(ads_sorted)

    idx_true = np.argwhere(ads_sorted == true_ad)[0][0] + 1
    #print(1/idx_true)
    acc_counter += 1 / idx_true
    counter += 1

accuracy_map = acc_counter / len(test_displays)
accuracy_map
