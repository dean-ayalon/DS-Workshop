import time

def ad_age_calculator(publish_times, click_times):
    real_times = []
    for i in range(len(publish_times)):
        time_struct = time.strptime(publish_times[i], "%Y-%m-%d %H:%M:%S")
        real_times.append(int(time.mktime(time_struct)))

    ad_ages = click_times - real_times
    ad_ages_in_days = ad_ages / 86400

    return ad_ages_in_days