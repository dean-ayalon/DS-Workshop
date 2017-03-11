from utils.table_utils import get_ads_per_feat

# Returns a DataFrame of ads and the number of times their advertiser published an ad.
def advertiser_freq(promoted):
    # Loading the relevant tables
    ad_advertisers = promoted[["ad_id", "advertiser_id"]]
    # Counting the number of times an advertiser appeared:
    ad_per_advertiser = get_ads_per_feat(promoted, "advertiser_id")
    advertiser_freq_per_ad = ad_advertisers.merge(ad_per_advertiser, on="advertiser_id")
    advertiser_freq_per_ad.drop(['advertiser_id'], axis=1, inplace=True)
    return advertiser_freq_per_ad


