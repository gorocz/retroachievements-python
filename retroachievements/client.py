from datetime import time
import json
from typing import Union

import requests

from .classes import *
from .exceptions import *
from .converters import *


class RAclient:
    api_url = "https://retroachievements.org/API/"
    NotReturned = NotReturned #we need an easy way to get it and it's the best i could find ngl

    def __init__(self, username, api_key, timeout=30):
        self.username = username
        self.api_key = api_key
        self.timeout = timeout
        self.NotReturned = NotReturned #also put it here just in case

    def _request(self, endpoint, params={}):
        #params |= {"z": self.username, "y": self.api_key} #we simply add the auth info. breaks support for python < 3.9 so we use another method
        params.update({"z": self.username, "y": self.api_key}) #we add the auth information
        r = requests.get(f"{self.api_url}/{endpoint}" , params=params, timeout=self.timeout)
        if r.text == "Invalid API Key":
            #it says "Invalid API Key" if the username is invalid as well
            raise InvalidAuth("Your API key or username is invalid")
        return r #we return the request

    def GetTopTenUsers(self) -> list:
        """Gets the top ten users by points.

        This is the same values as http://retroachievements.org/globalRanking.php?s=5&t=2&f=0

        :return: :class:`list` of 10 :class:`RAuser` objects.
        """

        r = self._request("API_GetTopTenUsers.php").json()
        return [RAuser_converter(u) for u in r] #list of RAuser objects

    def GetGameInfo(self, game_id: Union[int, str]) -> game:
        """Gets basic game informations

        :param game_id: The ID of the game to fetch
        :return: :class:`game` object with basic infos or :class:`None` if the game isn't found.
        """
        #GameTitle, Console and GameIcon seem to be dupes of Title, ConsoleName and ImageIcon only present in the basic game infos so they aren't implemented

        r = self._request("API_GetGame.php", {"i": game_id}).json()
        if r["Title"] is None: #aka game doesn't exist
            return None
        return game_converter(r, game_id=game_id,)

    def GetGameInfoExtended(self, game_id: Union[int, str]) -> game:
        """Gets informations on a game

        :param game_id: The ID of the game to fetch
        :return: :class:`game` object or :class:`None` if the game isn't found.
        """

        r = self._request("API_GetGameExtended.php", {"i": game_id}).json()
        if r["Title"] is None: #aka game doesn't exist
            return None
        return game_converter(r, game_id=game_id,)

    def GetConsoleIDs(self) -> list:
        """Gets a list of the consoles ID and the name associated with them.

        :return: :class:`list` of :class:`dict` objects with a "ID" and a "Name" key
        """

        r = self._request("API_GetConsoleIDs.php").json()
        return r

    def GetGameList(self, console_id: Union[int, str]) -> list:
        """Gets a list of games on a console.

        :param console_id: The ID of the console
        :return: :class:`list` of very trimmed down :class:`game` objects, the list is empty if the console isn't found.
        """

        r = self._request("API_GetGameList.php", params={"i": console_id}).json()
        # if r == []: #aka console not found
        #     return None

        return [game_converter(g) for g in r] #list of game objects
    
    #def GetFeedFor(self, user, count, offset):
    #not implemented bc no matter what i tried, API_GetFeed.php always just returned {"success":false}

    def GetUserRankAndScore(self, username: str) -> dict:
        """Gets the score and rank of a user, as well as the total number of ranked users.

        :param username: a string with the username
        :return: :class:`dict` with a "Score", "Rank" and "TotalRanked" key
        If the user doesn't exist, Score will be None and rank will be 1
        """

        r = self._request("API_GetUserRankAndScore.php", {"u": username}).json()
        r["TotalRanked"] = int(r["TotalRanked"]) #for some reason it's a string
        return r

    def GetUserProgress(self, username: str, game_ids: list) -> list:
        """Gets infos on a game's achivements and score, as well as the progress of a user
        You can fetch infos for multiple games at once

        :param username: a string with the username
        :param game_ids: a list of str or int, each with a game's id
        :return: :class:`list` of :class:`game_user_info` (last_played and my_vote are None)
        If the game doesn't exist, each attribute under user_info will be 0
        """
        game_ids = [str(g) for g in game_ids]
        game_string = ",".join(game_ids)
        r = self._request("API_GetUserProgress.php", {"u": username, "i": game_string}).json()
        games = []
        for g in r: #for each games
            games.append(game_converter(r[g], game_id=g))
        return games


    def GetUserRecentlyPlayedGames(self, username: str, limit: int=None, offset: int=0) -> list:
        """Gets the latest games played by a user

        :param username: a string with the username
        :param limit (optional): how many games to return (the API won't return more than 50 at once)
        :param offset (optional): the offset, this can allow you to see further than the latest 50 games
        :return: :class:`list` of very trimmed down :class:`game` objects with an extra .user_info attribute that contains a :class:`game_user_info` instance.
        The :class:`game` instance has the id, console_id, console_name, title, image_icon and user_info attributes, and the :class:`game_user_info` contains all attributes but num_achieved_hardcore and score_achieved_hardcore (or the raw attribute as it's in the game object)
        
        (the list will be empty if the user isn't found)
        """

        r = self._request("API_GetUserRecentlyPlayedGames.php", {"u": username, "c": limit, "o": offset}).json()
        return [game_converter(g) for g in r]

    def GetUserSummary(self, username: str, recent_games_count: int=5, achievements_count: int=10) -> user_summary:
        """Gets the summary of a user

        :param username: a string with the username
        :param recent_games_count (optional): how many recent games to return (the API doesn't seem to have a limit)
        :param achievements_count (optional): how many achivements to return (the API won't return more than 50 at once)
        :return: a :class:`user_summary` instance. The recently_played atttribute is a list of :class:`game`. last_game is a complete game object. awarded is a list of :class:`game` with only achievements informations.
        """
            
        r = self._request("API_GetUserSummary.php", {"u": username, "g": recent_games_count, "a": achievements_count}).json()

        la = r["LastActivity"]
        last_activity = activity(id=la["ID"],
                                username=la["User"], #called username instead of user to not be mistaken for a RAuser object
                                activity_type=la["activitytype"],
                                data=la["data"],
                                data2=la["data2"],
                                last_update=la["lastupdate"],
                                timestamp=la["timestamp"],
                                raw=la,)
            
        recent_achievements = []    
        for g in r["RecentAchievements"]: #for each game
            for a in r["RecentAchievements"][g]: #for each achivement in that game
                recent_achievements.append(achivements_converter(r["RecentAchievements"][g][a]))


        return user_summary(username=username,
            id=r["ID"],
            awarded=[game_converter(r['Awarded'][g], game_id=g) for g in r['Awarded']],
            last_activity=last_activity,
            recently_played=[game_converter(g) for g in r["RecentlyPlayed"]], #list of dicts
            rich_presence_msg=r["RichPresenceMsg"],
            member_since=r["MemberSince"],
            #last_game_id=r["LastGameID"],
            last_game=game_converter(r["LastGame"]),
            contrib_count=r["ContribCount"],
            contrib_yield=r["ContribYield"],
            total_points=r["TotalPoints"],
            total_true_points=r["TotalTruePoints"],
            permissions=r["Permissions"],
            untracked=r["Untracked"],
            motto=r["Motto"],
            rank=r["Rank"],
            total_ranked=r["TotalRanked"],
            recent_achievements=recent_achievements,
            user_pic=r["UserPic"],
            status=r["Status"],
            raw=r,)

    def GetUserGamesCompleted(self, username: str) -> list:
        """Gets the completed games of a user

        :param username: a string with the username
        :return: a :class:`list` of :class:`game` with the % of completion, sorted by reverse % of completion
        """
            
        r = self._request("API_GetUserCompletedGames.php", {"u": username}).json()
        #hardcore and non-hardcore counts as separate, so we need to "fuse" them in a single game
        #god forgive me for this unoptimized code
        games_list=[]
        while True:
            try:
                d = r.pop(0) #get the first dict and remove it 
                for i in r: #we check every other dict to see if one has the same game_id
                    if d["GameID"] == i["GameID"]: #we did find another game with this id
                        if int(i["HardcoreMode"]) == 1: #i is the hardcore mode
                            d["PctWonHardcore"] = i["PctWon"]
                            d["NumAwardedHardcore"] = i["NumAwarded"]
                            games_list.append(d)
                            r.remove(i) #no need to iterate any more
                            break
                        else: #d is the hardcore mode
                            i["PctWonHardcore"] = d["PctWon"]
                            i["NumAwardedHardcore"] = d["NumAwarded"]
                            games_list.append(i)
                            r.remove(i) #we popped d already, but i is still in the list so we remove him
                            break
                else: #didn't fibd a hardcore mode (aka no break)
                    d["PctWonHardcore"] = 0
                    d["NumAwardedHardcore"] = 0
                    games_list.append(d)

            except IndexError: #we went over the whole list
                break
        
        return [game_converter(g) for g in games_list] #we convert into actual games

    def GetGameInfoAndUserProgress(self, username: str, game_id: Union[int, str]) -> game:
        """Gets a game's info as well as the progress of a user on that game

        :param username: a string with the username
        :param game_id: the game's id
        :return: a :class:`game` instance.
        """
            
        r = self._request("API_GetGameInfoAndUserProgress.php", {"u": username, "g": game_id}).json()
        return game_converter(r)

    def GetAchievementsEarnedOnDay(self, username: str, date: datetime) -> list:
        """Gets achievements earned by a user on a specific day

        :param username: a string with the username
        :param date: a datetime object of the day to fetch (time doesn't matter).
        :return: a :class:`list` of :class:`achievement` instance.
        """
            
        r = self._request("API_GetAchievementsEarnedOnDay.php", {"u": username, "d": date.strftime('%Y-%m-%d')}).json()
        return [achivements_converter(a) for a in r]

    #the endpoint doesn't work so not implemented
    # def GetAchievementsEarnedBetween(self, username: str, from: datetime, to: datetime) -> list:
    #     """Gets achievements earned by a user between two dates

    #     :param username: a string with the username
    #     :return: a :class:`list` of :class:`achievement` instance.
    #     """
            
    #     r = self._request("API_GetAchievementsEarnedOnDay.php", {"u": username, "f": from.strftime('%Y-%m-%d'), "t": to.strftime('%Y-%m-%d')}).json()
    #     return [achivements_converter(a) for a in r]