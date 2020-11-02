import datetime
import os
import time

import tweepy

auth = tweepy.OAuthHandler(os.getenv("ConKey"), os.getenv("ConSec"))
auth.set_access_token(os.getenv("AccTok"), os.getenv("AccTokSec"))

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
yes = ["yes", "y"]


def strf_runningtime(tdelta, round_period='second'):
    """
    https://stackoverflow.com/a/64257852/13104233
    timedelta to string,  use for measure running time
    attend period from days downto smaller period, round to minimum period
    omit zero value period
    """
    period_names = ('day', 'hour', 'minute', 'second', 'millisecond')
    if round_period not in period_names:
        raise Exception(f'round_period "{round_period}" invalid, should be one of {",".join(period_names)}')
    period_seconds = (86400, 3600, 60, 1, 1 / pow(10, 3))
    period_desc = ('days', 'hours', 'mins', 'secs', 'msecs')
    round_i = period_names.index(round_period)

    s = ''
    remainder = tdelta.total_seconds()
    for i in range(len(period_names)):
        q, remainder = divmod(remainder, period_seconds[i])
        if int(q) > 0:
            if not len(s) == 0:
                s += ' '
            s += f'{q:.0f} {period_desc[i]}'
        if i == round_i:
            break
        if i == round_i + 1:
            s += f'{remainder} {period_desc[round_i]}'
            break
    return s


def filterTweets(tweetsList):
    def addToList(interactedTweet, _user):
        if not interactedTweet.author.following:
            return
        if _user.screen_name in _interacted_users.keys():
            _now = datetime.datetime.utcnow()
            if ((_now - _interacted_users[_user.screen_name][0].created_at) - (  # time between last saved to current
                    _now - interactedTweet.created_at)).total_seconds() < 0:
                return
        _interacted_users[_user.screen_name] = (
            interactedTweet, _user, datetime.datetime.utcnow() - interactedTweet.created_at)

    _interacted_users = {}
    for _tweet in tweetsList:
        if _tweet.author == username and _tweet.in_reply_to_screen_name and _tweet.entities:
            for entity in _tweet.entities:
                if _tweet.in_reply_to_screen_name == entity.screen_name:
                    addToList(_tweet, entity)
                    break
        elif _tweet.retweeted or _tweet.favorited:
            addToList(_tweet, _tweet.author)
    return _interacted_users


def askToUnfollow(_user, lastInteraction):
    while True:
        inp = input(
            f"Would you like to unfollow \"{_user.name}\"? (@{_user.screen_name}, Last interaction: {lastInteraction}) "
            f"[yN] ").lower()
        if inp and inp in yes:
            _user.unfollow()
        return


if __name__ == '__main__':
    utcfromtimestamp = datetime.datetime.utcfromtimestamp

    start_all = time.time()

    print("Getting important information about the user...", end=" ")
    start = time.time()
    username = auth.get_username()
    user = api.get_user(screen_name=username)
    end = time.time()
    print(f"Took {strf_runningtime(datetime.timedelta(seconds=(end - start)), 'millisecond') or 'too little time'}")

    print("Getting the people you follow...", end=" ")
    start = time.time()
    followings = [u for u in tweepy.Cursor(api.friends, count=200).items()]
    end = time.time()
    print(f"Took {strf_runningtime(datetime.timedelta(seconds=(end - start)), 'millisecond') or 'too little time'}")

    print("Getting all direct messages within 30 days. This might take a while...", end=" ")
    start = time.time()
    dms = [dm for dm in tweepy.Cursor(api.list_direct_messages, count=50).items()]
    end = time.time()
    print(f"Took {strf_runningtime(datetime.timedelta(seconds=(end - start)), 'millisecond') or 'too little time'}")

    print("Getting tweeted/retweeted/liked tweets. This might take a while...", end=" ")
    start = time.time()
    tweets = [t for t in tweepy.Cursor(api.user_timeline, id=username, count=200, include_rts=True).items()]
    tweets.extend([t for t in tweepy.Cursor(api.favorites, id=username, count=200, include_rts=True).items()])
    end = time.time()
    print(f"Took {strf_runningtime(datetime.timedelta(seconds=(end - start)), 'millisecond') or 'too little time'}")

    print(f"Processing {len(tweets)} tweets...", end=" ")
    start = time.time()
    interactions = filterTweets(tweets)
    end = time.time()
    print(f"Took {strf_runningtime(datetime.timedelta(seconds=(end - start)), 'millisecond') or 'too little time'}")

    print(f"Processing {len(dms)} direct messages...",
          end=" ")  # slower for more unique users that you messaged (within 30 days)
    start = time.time()
    cached_users = {}  # continuously fetching the users will increase the time and api usage
    for dm in dms:
        user_id = dm.message_create["target"]["recipient_id"] if dm.message_create["sender_id"] == user.id else \
            dm.message_create["sender_id"]
        dm_user = cached_users[user_id] if user_id in cached_users.keys() else api.get_user(id=user_id)
        cached_users[user_id] = dm_user
        if not dm_user.following:
            continue
        creation_time = utcfromtimestamp(int(dm.created_timestamp[:-3]))
        if dm_user.screen_name in interactions.keys():
            now = datetime.datetime.utcnow()
            old_creation_time = interactions[dm_user.screen_name][0].created_at if isinstance(
                interactions[dm_user.screen_name][0], tweepy.Status) else utcfromtimestamp(
                int(interactions[dm_user.screen_name][0].created_timestamp[:-3]))
            if ((now - old_creation_time) - (now - creation_time)).total_seconds() < 0:
                continue
        interactions[dm_user.screen_name] = (dm, dm_user, datetime.datetime.utcnow() - creation_time)
    del cached_users
    end = time.time()
    print(f"Took {strf_runningtime(datetime.timedelta(seconds=(end - start)), 'millisecond') or 'too little time'}")

    print("Processing other things that must be post-processed...", end=" ")
    start = time.time()
    users = [user for tweet, user, time in interactions.values()]
    noInteractFollowings = [u for u in followings if u.following and u not in users]
    end = time.time()
    print(f"Took {strf_runningtime(datetime.timedelta(seconds=(end - start)), 'millisecond') or 'too little time'}")

    end_all = time.time()

    print(f"Done! Took {strf_runningtime(datetime.timedelta(seconds=(end_all - start_all)), 'millisecond') or 'too little time'}.\n"
          f"Now you can unfollow anyone who you haven't been interacting in some time.")
    if noInteractFollowings:
        for user in noInteractFollowings:
            askToUnfollow(user, "Undetermined")
    if interactions:
        temp = {time: user for tweet, user, time in interactions.values()}
        temp = {k: temp[k] for k in reversed(sorted(temp))}
        for time, user in temp.items():
            askToUnfollow(user, strf_runningtime(time, 'minute'))
    print("You are all done!")
