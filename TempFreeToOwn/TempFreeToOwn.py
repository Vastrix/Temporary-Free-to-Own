# -*- coding: utf-8 -*-
import urllib.request
import sys
sys.path.append("C:\Python36\Lib\site-packages\pysteamkit\protobuf")
import json
from HTMLSteamStoreParser import HTMLSteamStoreParser
from time import sleep
from colorama import init, Fore, Style
from pysteamkit.steam3 import client
init()


class SimpleHandler():
    def handle_message(self, emsg_real, body):
        pass
    def try_initialize_connection(self, *args, **kwargs):
        return True

   
client = client.SteamClient(SimpleHandler())

client.initialize()
client.login_anonymous()
print("Response:", client.steamapps.get_product_info(apps=(620,)))
# SteamApps caches the json values for apps and packages
print("Json data:", client.steamapps.app_cache[620])

class TempFreeToOwn:
    """Crawls alls steam games in search for temporary free to own games"""

    def __init__(self, blackList):
        self.blackList = blackList
        self.currentFreeToOwn = {}
        self.appList = []

        for i in range(10):
            if self.Load():
                break
            elif i == 9:
                raise Exception("Couldn't fetch the steam apps list!")

            sleep(5)


    def Load(self):
        """caches the appID list and applies the blacklist"""

        try:
            print("Fetching the steam apps list..")
            con = urllib.request.urlopen("http://api.steampowered.com/ISteamApps/GetAppList/v0002/")
            self.appList = json.load(con)["applist"]["apps"]
        except:
            return False
        else:
            print("%d apps loaded. Done!\n\nApplying blacklist.." % len(self.appList))

            jsn = json.load(open(self.blackList))

            self.appList = [x for x in self.appList if not x["appid"] in [jsn[n][a] for n in jsn if (type(jsn[n]) is type([])) for a in range(len(jsn[n]))]] #If it's in a list in the blacklist, Don't keep it

            print("%d remaining" % (len(self.appList)))

            return True


    def Process(self):

        print(Fore.YELLOW + "Crawling Initiated!" + Style.RESET_ALL)
        for v in self.appList:
            sleep(.5)
            #print(Fore.GREEN + str(v["appid"]) + Style.RESET_ALL, end='\r')
            temp = HTMLSteamStoreParser(v["appid"])

            while(temp.Exception == True):
                temp.Exception = False
                temp.Open()
                sleep(.5)

            print(Fore.MAGENTA + "%d; %s"%(v["appid"], temp.Data["Success"]) + Style.RESET_ALL )
            if(not(temp.Data["Success"])): continue

            if(not(temp.CorrectID) or (not(temp.Data["isGame"]))): #if the ID is incorrect or it's not a game -> Blacklist
                jsn = json.load(open(self.blackList))
                jsn["notAGame"].append(v["appid"])
                json.dump(jsn, open(self.blackList ,'w'))
                continue



test = TempFreeToOwn("blackList.json")

test.Process()
