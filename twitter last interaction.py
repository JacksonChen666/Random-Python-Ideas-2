import datetime
import os
import time

import tweepy

auth = tweepy.OAuthHandler(os.getenv("ConKey"), os.getenv("ConSec"))
auth.set_access_token(os.getenv("AccTok"), os.getenv("AccTokSec"))

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
yes = ["yes", "y"]


def filterTweets(tweetsList):
    def addToList(interactedTweet, _user):
        if not interactedTweet.author.following:
            return
        if _user.screen_name in _interacted_users.keys():
            now = datetime.datetime.utcnow()
            if ((now - _interacted_users[_user.screen_name][0].created_at) - (  # time between last saved to current
                    now - interactedTweet.created_at)).total_seconds() < 0:
                return
        _interacted_users[_user.screen_name] = (
            interactedTweet, _user, datetime.datetime.utcnow() - interactedTweet.created_at)

    _interacted_users = {}
    for _tweet in tweetsList:
        if _tweet.author == username and _tweet.in_reply_to_screen_name and _tweet.entities:
            for entity in _tweet.entities:
                if _tweet.in_reply_to_screen_name == entity.screen_name:
                    addToList(_tweet, entity)
        elif _tweet.retweeted or _tweet.favorited:
            addToList(_tweet, _tweet.author)
    return _interacted_users


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


def askToUnfollow(user, lastInteraction):
    while True:
        inp = input(
            f"Would you like to unfollow \"{user.name}\"? (@{user.screen_name}, Last interaction: {lastInteraction}) "
            f"[yN] ").lower()
        if inp and inp in yes:
            user.unfollow()
        return


if __name__ == '__main__':
    username = auth.get_username()

    print("Getting the people you follow...", end=" ")
    start = time.time()
    followings = [u for u in tweepy.Cursor(api.friends, count=200).items()]
    end = time.time()
    print(f"Took {strf_runningtime(datetime.timedelta(seconds=(end - start)), 'millisecond') or 'too little time'}")

    print("Getting tweeted/retweeted/liked tweets. This will take a while...", end=" ")
    start = time.time()
    tweets = [t for t in tweepy.Cursor(api.user_timeline, id=username, count=200, include_rts=True).items()]
    tweets.extend([t for t in tweepy.Cursor(api.favorites, id=username, count=200, include_rts=True).items()])
    end = time.time()
    print(f"Took {strf_runningtime(datetime.timedelta(seconds=(end - start)), 'millisecond') or 'too little time'}")

    print(f"Processing {len(tweets)} tweets...", end=" ")
    start = time.time()
    interactedUsersTweets = filterTweets(tweets)
    users = [user for tweet, user, time in interactedUsersTweets.values()]
    noInteractFollowings = [u for u in followings if u.following and u not in users]
    end = time.time()
    print(f"Took {strf_runningtime(datetime.timedelta(seconds=(end - start)), 'millisecond') or 'too little time'}")

    print("Done! Now you can unfollow anyone who you haven't been interacting in some time.")
    if noInteractFollowings:
        for user in noInteractFollowings:
            askToUnfollow(user, "Undetermined")
    if interactedUsersTweets:
        temp = {time: user for tweet, user, time in interactedUsersTweets.values()}
        temp = {k: temp[k] for k in reversed(sorted(temp))}
        for time, user in temp.items():
            askToUnfollow(user, strf_runningtime(time, 'minute'))
    print("You are all done!")
