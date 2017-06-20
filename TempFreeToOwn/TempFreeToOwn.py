# -*- coding: utf-8 -*-
import urllib2
import sys
import json
from time import sleep
from colorama import init
from pysteamkit.steam3.client import SteamClient
init()
#client.steamapps.get_product_info(apps=(440,))
#print "Response:", client.steamapps.app_cache[440]

class TempFreeToOwn:
    """Crawls alls steam games in search for temporary free to own games"""

    def __init__(self, blackList):
        self.blackList = json.load(open(blackList))
        self.currentFreeToOwn = {}
        self.appList = []
        self.Initialize()

        for i in range(10):
            if self.Load():
                break
            elif i == 9:
                raise Exception("Couldn't fetch the steam apps list!")

            sleep(5)


 

    def Initialize(self):
        class SimpleCallBack:
            def handle_message(self, emsg_real, body):
                pass
            def try_initialize_connection(self, *args, **kwargs):
                return True

        client = SteamClient(SimpleCallBack())
        client.initialize()
        client.login_anonymous()


    def Load(self):
        """caches the appID list and applies the blacklist"""

        try:
            print("Fetching the steam apps list..")
            con = urllib2.urlopen("http://api.steampowered.com/ISteamApps/GetAppList/v0002/")
            self.appList = json.load(con)["applist"]["apps"]
        except:
            return False
        else:
            print("%d apps loaded. Done!\n\nApplying blacklist.." % len(self.appList))

            count = 0
            for i in self.appList:
                for val in self.blackList:
                    if i["appid"] in self.blackList[val]:
                        self.appList.remove(i)
                        count +=1
            print "Removed %d apps, %d remaining" % (count, len(self.appList))

            return True


    def Process(self):
        pass

test = TempFreeToOwn("blackList.json")
