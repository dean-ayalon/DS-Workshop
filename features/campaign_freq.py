import numpy as np

# Similar to advertiser_freq, returns a DataFrame of ads and their campaign's "frequency"
# That is, num. of ads belonging to same campaign
def campaign_freq(promoted):
    # Loading the relevant tables
    ad_campaigns = promoted[["ad_id", "campaign_id"]]
    # Counting the number of times an advertiser appeared:
    ad_per_campaign = ad_campaigns.groupby(["campaign_id"], as_index=False).agg({"ad_id": np.count_nonzero})\
        .rename(index=str, columns={"ad_id": "ads_per_campaign"})
    campaign_freq_per_ad = ad_campaigns.merge(ad_per_campaign, on="campaign_id", copy=False)
    campaign_freq_per_ad.drop(['campaign_id'], axis=1, inplace=True)
    return campaign_freq_per_ad
