from bs4 import BeautifulSoup
from colorama import init, Fore, Style
from urllib import request, response
init()

def Error(errorMsg): 
    print(Fore.RED + errorMsg + Style.RESET_ALL)

class HTMLSteamStoreParser:
    """Parses the Steam Store and returns the data in a json"""

    BaseLink = "http://store.steampowered.com/app/"

    def __init__(self, appID: int):
        if(type(appID) != int): raise Exception("Incorrect appID Type!")

        self.AppID = appID
        self.CorrectID = True
        self.Exception = False
        self.Data = {} #Name, Price, AppID, isGame
        self.__Soup = None

        if(self.Open()):
            self.GetInfo()


    def Open(self)->bool:

        self.Data["Success"] = False

        try:
            self.__Soup = request.urlopen(HTMLSteamStoreParser.BaseLink + str(self.AppID))
            if not(str(self.AppID) in self.__Soup.geturl()): #if the appid is not in the url, assume that there's no game with that ID (we got redirected)
                self.CorrectID = False
                return False

            self.__Soup = BeautifulSoup(self.__Soup, "html.parser")
        except Exception as e:
            self.__Soup = None
            self.Exception = True

            Error("[HTMLSSP] An error occured trying to fetch the game site, ID %d"%self.AppID)
            return False
        else:
            self.Data["Success"] = self.__Check()
            return True


    def GetInfo(self) -> bool:

        print(str(self.AppID))
        if ((self.__Soup is None) or (not(self.Data["Success"]))): return False


        self.Data["Name"] = self.__Soup.div.find(attrs={"class": "apphub_AppName"}).text

        self.Data["Price"] = self.__Soup.find(attrs={"itemprop": "price"})["content"] if (self.__Soup.find(attrs={"itemprop": "price"}) is not None) else "NA"

        self.Data["AppID"] = self.AppID
        self.Data["isGame"] = ("game" in self.__Soup.find(attrs={"class": "blockbg"}).a.text.lower())
        return True

    def __Check(self)-> bool:
        """Checks if the currently loaded soup is valid, returns false if not"""

        #Title Check..
        title = ["error"]
        for x in title:
            if (x in self.__Soup.title.text.lower()):
                return False

        return True