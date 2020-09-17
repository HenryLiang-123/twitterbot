import tweepy
import time
auth = tweepy.OAuthHandler('*', '*')
# API key and API secret key
auth.set_access_token('*', '*')
# access token and access token secret
api = tweepy.API(auth)
user = api.me()

# twitter limit handler
def limit_handle(cursor):
	#twitter api has limit of times you can hit it
	#this function makes sure there is time in between cursor hits if there is RateLimitError
	while True:
		try:
			yield cursor.next()
		except tweepy.RateLimitError:
			time.sleep(5000)
		except StopIteration:
			break

# Like tweets based on keywords

search_list = ['"coronavirus new york times"',
			   '"public health"',
			   '"emergency prepardness"',
			   '"COVID-19"',
			   '"wildfires"',
			   '"active shooter"',
			   '"fake news COVID-19"']	

location_str = '"California"'
#goal: optimize search lists such that theres no bullshit(search for relavent info)
#location should be CA
#use search query q

#retweet 3 verified tweets for each key word in search list
numbersOfTweets = 3
for search_string in search_list:
	search_string = search_string + location_str
	for tweet in limit_handle(tweepy.Cursor(api.search, q = search_string + ' -filter:retweets AND filter:verified AND filter:media').items(numbersOfTweets)):
		if tweet.lang == 'en':
			try:
				tweet.favorite()
				print('i like that tweet')
			except tweepy.TweepError as e:
				print(e.reason)
				break

#retweeting
for search_string in search_list:
	search_string = search_string + location_str
	for tweet in limit_handle(tweepy.Cursor(api.search, q = search_string+ ' -filter:retweets AND filter:verified AND filter:media').items(numbersOfTweets)): #searches keyword, filters retweets
		if tweet.lang == 'en':
			try:
				tweet.retweet()
				print('i retweeted')
			except tweepy.TweepError as e:
				print(e.reason)
				break



# followback bot
for follower in limit_handle(tweepy.Cursor(api.followers).items()):
	follower.follow()
