import requests
import pickle
import time
import os
from constants import *
from datetime import datetime


def initLog(matchid, mmr):
    log = {'LastMatchId': matchid, 'MMR': mmr}
    pickling_on = open("log.dat", "wb")
    pickle.dump(log, pickling_on)
    pickling_on.close()


# initLog(LAST_MATCH_ID, MMR)


def loadLog():
    pickle_off = open("log.dat", 'rb')
    log = pickle.load(pickle_off)
    return log["LastMatchId"], log["MMR"]


def getRecentMatches():
    data = []
    url = "https://api.opendota.com/api/players/" + \
        str(DOTA2_ID) + "/recentMatches"
    source = requests.get(url)
    DataJSON = source.json()
    __lastMatchId, MMR = loadLog()
    for match in DataJSON:
        if(match["match_id"] == __lastMatchId):
            break
        else:
            dat = {}
            dat["match_id"] = match["match_id"]
            dat["my_hero"] = match["hero_id"]
            dat["start_time"] = match["start_time"]
            dat["kills"] = match["kills"]
            dat["deaths"] = match["deaths"]
            dat["assists"] = match["assists"]
            dat["duration"] = match["duration"]
            dat["gameMode"] = str(match["game_mode"])
            dat["lobbyType"] = str(match["lobby_type"])
            timestamp = match["start_time"]
            dt_object = datetime.fromtimestamp(timestamp)
            dat["time"] = dt_object

            if(match["player_slot"] < 128):
                dat["my_side"] = "radiant"
            else:
                dat["my_side"] = "dire"

            if(match["radiant_win"] == False):
                dat["result"] = "dire"
            else:
                dat["result"] = "radiant"
        data.append(dat)

    if(len(data) == 0):
        print("No New Matches Played :(")
        return False
    else:
        return data


def getMatchDetails():
    tweets = []
    recentJSON = getRecentMatches()
    if(recentJSON == False):
        return False
    else:
        for match in recentJSON:
            tweetData = {}

            url = "https://api.opendota.com/api/matches/" + \
                str(match["match_id"])
            source = requests.get(url)
            DataJSON = source.json()
            tweetData["match_id"] = DataJSON["match_id"]
            tweetData["dire_score"] = DataJSON["dire_score"]
            tweetData["radiant_score"] = DataJSON["radiant_score"]
            tweetData["radiant_heroes"] = []
            tweetData["dire_heroes"] = []
            for i in range(10):
                if(DataJSON["players"][i]["player_slot"] < 128):
                    tweetData["radiant_heroes"].append(
                        DataJSON["players"][i]["hero_id"])
                else:
                    tweetData["dire_heroes"].append(
                        DataJSON["players"][i]["hero_id"])
            tweetData["my_hero"] = match["my_hero"]
            tweetData["my_side"] = match["my_side"]
            tweetData["result"] = match["result"]
            tweetData["kills"] = match["kills"]
            tweetData["deaths"] = match["deaths"]
            tweetData["assists"] = match["assists"]
            tweetData["duration"] = match["duration"]
            tweetData["time"] = match["time"]
            tweetData["gameMode"] = GAMEMODES[match["gameMode"]]
            tweetData["lobbyType"] = LOBBYTYPES[match["lobbyType"]]
            tweets.append(tweetData)
    mmr = int(input("Enter the MMR: "))
    initLog(tweets[0]["match_id"], mmr)
    return tweets


def getRank():
    tier = ["Herald", "Guardian", "Crusader", "Archon",
            "Legend", "Ancient", "Divine", "Immortal"]
    url = "https://api.opendota.com/api/players/" + str(DOTA2_ID)
    source = requests.get(url)
    DataJSON = source.json()
    rank = tier[int((DataJSON["rank_tier"]/10)-1)] + \
        "-" + str(DataJSON["rank_tier"] % 10)
    return rank


def getHeroNames():
    encoding = {}
    url = "https://raw.githubusercontent.com/odota/dotaconstants/master/build/hero_names.json"
    source = requests.get(url)
    DataJSON = source.json()
    for hero in DataJSON.keys():
        encoding[DataJSON[hero]["id"]] = DataJSON[hero]["localized_name"]
    return encoding


def compileTweet():
    rank = getRank()
    tweetData = getMatchDetails()
    if(tweetData == False):
        return False
    nGames = len(tweetData)
    tweets = []
    count = nGames

    IntroTweet = ""
    IntroTweet += "Summary of " + str(nGames) + " games\n"
    w, l = findWinLoss(tweetData)
    IntroTweet += str(w) + "-" + str(l) + " (W-L)" + "\n"
    IntroTweet += "Final Rank: " + getRank()

    for match in tweetData:
        tweet = "MATCH " + str(count) + "(" + str(nGames) + ")\n"
        tweet += "[" + str(match["time"].day) + "/" + \
            str(match["time"].month) + "/" + str(match["time"].year) + " "
        tweet += str(match["time"].hour//10) + \
            str(match["time"].hour % 10) + ":"
        tweet += str(match["time"].minute//10) + \
            str(match["time"].minute % 10) + ":"
        tweet += str(match["time"].second//10) + \
            str(match["time"].second % 10) + " IST" + "]\n\n"
        tweet += "MATCH ID: " + str(match["match_id"]) + "\n"
        tweet += "Type: " + match["gameMode"] + " " + match["lobbyType"] + "\n"

        if(match["result"] == match["my_side"]):
            status = "Won"
        else:
            status = "Lost"

        tweet += "HERO: " + encoding[match["my_hero"]] + "\nSTATUS: " + status
        tweet += "\nDURATION: " + str(match["duration"]//60) + ":" + str(
            (match["duration"] % 60)//10) + str((match["duration"] % 60) % 10) + "\n\n"
        rad = []
        dire = []
        for i in range(5):
            rad.append(encoding[match["radiant_heroes"][i]])
            dire.append(encoding[match["dire_heroes"][i]])
        if(match["my_side"] == "radiant"):
            i = rad.index(encoding[match["my_hero"]])
            rad[i] += " (Maan)"
        else:
            i = dire.index(encoding[match["my_hero"]])
            dire[i] += " (Maan)"

        tweet += "RADIANT: " + rad[0] + ", " + rad[1] + \
            ", " + rad[2] + ", " + rad[3] + ", " + rad[4] + "\n"
        tweet += "DIRE: " + dire[0] + ", " + dire[1] + \
            ", " + dire[2] + ", " + dire[3] + ", " + dire[4]

        tweets.append(tweet)
        count -= 1
    tweets.append(IntroTweet)
    tweets.reverse()
    return tweets


def findWinLoss(tweetData):
    w = 0
    l = 0
    for match in tweetData:
        if(match["result"] == match["my_side"]):
            w += 1
        else:
            l += 1
    return w, l


encoding = getHeroNames()
