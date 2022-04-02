import tweepy as tw


my_api_key = "XXXXXXXXXXXXXXXXX"
my_api_secret = "XXXXXXXXXXXXXXXXXXXXXXX"


auth = tw.OAuthHandler(my_api_key, my_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)