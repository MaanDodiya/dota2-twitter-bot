from bs4 import BeautifulSoup
import requests
import pickle
import time
import os
import json

__DOTA2_ID = 336910173
__STEAM_ID = 0
__LAST_MATCH_ID = 5740045349
__MMR = 2490


def init_log(matchid, mmr):
    log = {'LastMatchId': matchid, 'MMR': mmr}
    pickling_on = open("log.dat", "wb")
    pickle.dump(log, pickling_on)
    pickling_on.close()


def load_log():
    pickle_off = open("log.dat", 'rb')
    log = pickle.load(pickle_off)
    return log["LastMatchId"], log["MMR"]


def get_matchIDs():
    matchIDs = []
    link = "https://api.opendota.com/api/players/" + \
        str(__DOTA2_ID) + "/recentMatches"
    source = requests.get(link, headers={'User-agent': 'your bot 0.1'}).text
    soup = BeautifulSoup(source, 'lxml')
    DataString = soup.find('body').text
    DataJSON = json.loads(DataString)
    __lastMatchId, __MMR = load_log()
    for match in DataJSON:
        if(match["match_id"] == __lastMatchId):
            print("Match found!!!")
            break
        else:
            matchIDs.append(match["match_id"])
    if(len(matchIDs) == 0):
        print("No New Matches Played :(")
        return False
    else:
        return matchIDs


def get_matchDetails():
    matchIDs = get_matchIDs()
    if(matchIDs == False):
        return False
    else:
        for match in matchIDs:
            link = "https://api.opendota.com/api/matches/" + str(match)
            source = requests.get(
                link, headers={'User-agent': 'your bot 0.1'}).text
            soup = BeautifulSoup(source, 'lxml')
            DataString = soup.find('body').text
            DataJSON = json.loads(DataString)
