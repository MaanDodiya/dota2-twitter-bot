# Dota2 Twitter Bot

A simple python bot which tweets your recent matches played. Data collected using [OpenDota Web API](https://docs.opendota.com/#), [requests](https://pypi.org/project/requests/) library and tweeted using [Tweepy API](http://docs.tweepy.org/en/latest/).

[twitter.com/LoganBot5](https://twitter.com/LoganBot5)

### Installation

[Python]() should be installed on your machine.
You need to install following libraries:

- [Requests](https://pypi.org/project/requests/)
- [Tweepy](http://docs.tweepy.org/en/latest/)

Now you can download the repository or clone it using the following command

`>>> git clone https://github.com/MaanDodiya/dota2-twitter-bot.git`

In "twitter.py" file:

```
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("key", "secret")
```

- Replace the "consumer_key" with API key and "consumer_secret" with API Secret key
- Replace the "key" with Access Token key and "secret" with Access Token Secret key

[Refer this Tweepy Documentation if not working](http://docs.tweepy.org/en/latest/auth_tutorial.html#oauth-1a-authentication)

Run the python file in your terminal.

Enter your MMR in the terminal (Optional, It is not tweeted but kept in log.dat file for future reference)

```
>>> C:/Python39/python.exe twitter.py
Enter the MMR: 2490
```

---

### Sample Tweets:

[<img src="images/Tweet.png"/>](images/Tweet.png)

---

### About the author

- **Name**: Maan "2di.[L]ogan" Dodiya
- **MMR**: 2.5k
- **Roles**: Offlane, Support
- **Region**: SEA
- **Heroes**: Centaur Warrunner, Earth Spirit, Earthshaker, Dragon Knight, Jakiro
