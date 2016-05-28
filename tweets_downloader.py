# https://gist.github.com/yanofsky/5436496

# !/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv

# Twitter API credentials
consumer_key = "7ayO8FSQxuKS9crzwSqAOcjlX"
consumer_secret = "TKV9GCL4oCtrLLvqJUBiFoSnAJ73O2kH1pAKrPMxo0QDf5jfDM"
access_key = "120130490-4ta4Q95fFSruztpAeMgyg8XlHMtvyN0oLvHKzJcB"
access_secret = "82faFF3ZET65GClDztn7aYjPsiZrAZYkVPzwNAEauPZtJ"


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    for new_tweet in new_tweets:
        if new_tweet.text.startswith('RT') or new_tweet.text.startswith('@'):
            continue
        else:
            alltweets.append(new_tweet)
    #alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        for new_tweet in new_tweets:
            if new_tweet.text.startswith('RT') or new_tweet.text.startswith('@'):
                continue
            else:
                alltweets.append(new_tweet)
        # alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))
        if len(alltweets) > 1000:
            break

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]

    # write the csv
    with open('%s_tweets.csv' % screen_name, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    pass


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("Monatique")
