import urllib2
import csv
import json
import datetime
from abc import ABCMeta
from urllib import urlencode
from abc import abstractmethod
from urlparse import urlunparse
from bs4 import BeautifulSoup
from time import sleep
from time import django

OUT_FILE = "where your .csv is""

class TwitterSearch:

    __metaclass__ = ABCMeta

    def __init__(self, rate_delay, error_delay=5):
    
        self.rate_delay = rate_delay
        self.error_delay = error_delay

    def search(self, query):
       
        url = self.construct_url(query)
        continue_search = True
        min_tweet = None
        response = self.execute_search(url)
        while response is not None and continue_search and response['items_html'] is not None:
            tweets = self.parse_tweets(response['items_html'])

            if len(tweets) == 0:
                break
            
            if min_tweet is None:
                min_tweet = tweets[0]

            continue_search = self.save_tweets(tweets)

            # Our max tweet is the last tweet in the list
            max_tweet = tweets[-1]
            if min_tweet['tweet_id'] is not max_tweet['tweet_id']:
                max_position = "TWEET-%s-%s" % (
                    max_tweet['tweet_id'], min_tweet['tweet_id'])
                url = self.construct_url(query, max_position=max_position)
                # Sleep for our rate_delay
                sleep(self.rate_delay)
                response = self.execute_search(url)

    def execute_search(self, url):
        
        try:
          
            headers = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
            }
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            data = json.loads(response.read())
            return data
      
        except ValueError as e:
            print e.message
            print "Sleeping for %i" % self.error_delay
            sleep(self.error_delay)
            return self.execute_search(url)

    @staticmethod
    def parse_tweets(items_html):
    
        soup = BeautifulSoup(items_html, "html.parser")
        tweets = []
        for li in soup.find_all("li", class_='js-stream-item'):

            if 'data-item-id' not in li.attrs:
                continue

            tweet = {
                'tweet_id': li['data-item-id'],
                'text': None,
                'user_id': None,
                'user_screen_name': None,
                'user_name': None,
                'created_at': None,
                'retweets': 0,
                'favorites': 0
            }

            text_p = li.find("p", class_="tweet-text")
            if text_p is not None:
                tweet['text'] = text_p.get_text().encode('utf-8')

            user_details_div = li.find("div", class_="tweet")
            if user_details_div is not None:
                tweet['user_id'] = user_details_div['data-user-id']
                tweet['user_screen_name'] = user_details_div['data-user-id']
                tweet['user_name'] = user_details_div['data-name']

            date_span = li.find("span", class_="_timestamp")
            if date_span is not None:
                tweet['created_at'] = float(date_span['data-time-ms'])

            retweet_span = li.select(
                "span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
            if retweet_span is not None and len(retweet_span) > 0:
                tweet['retweets'] = int(
                    retweet_span[0]['data-tweet-stat-count'])

            favorite_span = li.select(
                "span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
            if favorite_span is not None and len(retweet_span) > 0:
                tweet['favorites'] = int(
                    favorite_span[0]['data-tweet-stat-count'])

            tweets.append(tweet)
        return tweets

    @staticmethod
    def construct_url(query, max_position=None):

        params = {
            # Type Param
            'f': 'tweets',
            # Query Param
            'q': query
        }

        if max_position is not None:
            params['max_position'] = max_position

        url_tuple = ('https', 'twitter.com', '/i/search/timeline',
                     '', urlencode(params), '')
        return urlunparse(url_tuple)

    @abstractmethod
    def save_tweets(self, tweets):

class TwitterSearchImpl(TwitterSearch):

    def __init__(self, rate_delay, error_delay, csv_writer):

        super(TwitterSearchImpl, self).__init__(rate_delay, error_delay)
        self.writer = csv_writer

    def save_tweets(self, tweets):
    
        for tweet in tweets:
            if tweet['created_at'] is not None:
                time = datetime.datetime.fromtimestamp(
                    (tweet['created_at'] / 1000))
                fmt = "%Y-%m-%d %H:%M:%S"
                row = [tweet['text'], time.strftime(fmt), tweet['favorites'],
                       tweet['retweets'], tweet['tweet_id']]
                self.writer.writerow(row)

                return True

if __name__ == '__main__':
    with open(OUT_FILE, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Text", "Date", "Favorites", "Retweets", "Tweet ID"])
        twit = TwitterSearchImpl(0, 5, writer)
        twit.search("from:realdonaldtrump") 
        
        # You can change "realdonaldtrump" to any twitter account.
        
