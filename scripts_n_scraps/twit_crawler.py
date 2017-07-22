## TWITTER PULL REQUESTS: FOR NLP LEARNING DATA ##
import sys, json, tweepy

#Twitter API credentials
consumer_key = "HQRcJux2iypXbPOfTlUYFxF4J"
consumer_secret = "XTXCQc29QLJlgUR20Rnvd9StDyjNiDnkT16JLWK7dW9DGl7P01"
access_key = "28452416-pHr7tQJuNoyLcMGvDxYC3siul6gk5yjZgJrAfb1HI"
access_secret = "x5IZCG6B0LE5vBHnAT8UEhdwnBZt2nOj5uui0okSMfybv"

#json_file = "tweets00.json"
visited_users = set()

def get_tweets(screen_name):
# ORIGIN: https://gist.github.com/yanofsky/5436496:--
    # Twitter only allows access to a users most recent 3240 tweets with this method
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)                                   # authorise twitter
    auth.set_access_token(access_key, access_secret)                                            # authorise twitter
    api = tweepy.API(auth)                                                                      # init tweepy

    #if '.' or '!' or ':' or '?' or ',' in screen_name: screen_name = " "  
    if screen_name[0] == '@': screen_name = screen_name[1:]                                     # format screen name to remove '@'


    try:
        alltweets = []                                                               
        new_tweets = api.user_timeline(screen_name = screen_name,count=200)                     # make initial request for most recent tweets (200 is the maximum allowed count)
        alltweets.extend(new_tweets)                                                            # save most recent tweets
        oldest = alltweets[-1].id - 1                                                           # save the id of the oldest tweet less one

        while len(new_tweets) > 0:                                                              # keep grabbing tweets until there are no tweets left to grab
            new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)   # all subsiquent requests use the max_id param to prevent duplicates
            alltweets.extend(new_tweets)                                                        # save most recent tweets
            oldest = alltweets[-1].id - 1                                                       # update the id of the oldest tweet less one

    except: pass
#--
## OWN ##
    d = {}                                                                                      # blank dictionary to hold json data
    text = []                                                                                   # blank list to hold text of tweets
    for tweet in alltweets:                                                                     # loop over tweets
        try: text.append(tweet.text.encode('utf-8').decode('ascii'))                            # get text # decode it to ascii # append to text list
        except: pass
    d[screen_name] = text                                                                       # populate dictionary # k=username v=tweets

    # with open(json_file, 'r', encoding='utf-8') as infile:                                           # open json file so far
    #     try: d.update(json.load(infile))
    #     except: pass                                                        # add old json data to dictionary

    with open("./twit_json/{}.json".format(screen_name), 'w', encoding='utf-8') as outfile:                                                       # prepare to write to json file
        json.dump(d, outfile, skipkeys=False, ensure_ascii=True, sort_keys=True)               # write newly extended dictionary to json file

    return screen_name

def crawl(screen_name):
    with open("./twit_json/{}.json".format(screen_name), 'r', encoding='utf-8') as infile:
        data = json.load(infile)
        tweets = []
        for k in data:
            visited_users.add("@" + k)
            tweets.append(data[k])
        user_set = set()
        for tweet in tweets:
            temp = [str(tweet).split(' ')]
            for at in temp:
                for i in at:
                    try: 
                        if str(i)[0] == '@': user_set.add(i)
                    except: pass
        print(visited_users)
        #if len(visited_users) > 20: sys.exit(0)
        for user in user_set:
            if user not in visited_users:
                visited_users.add(user) 
                crawl(get_tweets(user))
                           
if __name__ == '__main__':
#pass in the username of the account you want to download        
    crawl(get_tweets(sys.argv[1]))