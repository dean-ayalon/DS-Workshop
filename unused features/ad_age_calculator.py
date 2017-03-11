import time

# This feature calculates the time passed between when the ad was published
# and when it got clicked.
# We discarded it because there is a large amount of Nulls in the publish time
# (meaning this information was missing for many ads)

def ad_age_calculator(publish_times, click_times):
    real_times = []
    for i in range(len(publish_times)):
        time_struct = time.strptime(publish_times[i], "%Y-%m-%d %H:%M:%S")
        real_times.append(int(time.mktime(time_struct)))

    ad_ages = click_times - real_times
    ad_ages_in_days = ad_ages / 86400

    return ad_ages_in_days