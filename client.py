from typing import Union
import requests
import json

from .exceptions import *
from .classes import RAuser, achievement, game, game_user_info, user_summary

def achivements_converter(a) -> achievement:
    return achievement(id=a["ID"],
                num_awarded=a["NumAwarded"],
                num_awarded_hardcore=a["NumAwardedHardcore"],
                title=a["Title"],
                description=a["Description"],
                points=a["Points"],
                true_ratio=a["TrueRatio"],
                author=a["Author"],
                date_modified=a["DateModified"],
                date_created=a["DateCreated"],
                badge_name=a["BadgeName"],
                display_order=a["DisplayOrder"],
                mem_addr=a["MemAddr"])

class RAclient:
    api_url = "https://retroachievements.org/API/"

    def __init__(self, username, api_key, timeout=30):
        self.username = username
        self.api_key = api_key
        self.timeout = timeout

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

        :return: :class:`list` of 10 :class:`RAuser` objects with only the name, points and retro_points fields filled, all other fields are None
        """

        r = self._request("API_GetTopTenUsers.php").json()
        return [RAuser(username=u["1"], raw=u, points=u["2"], retro_points=u["3"])
                for u in r] #list of RAuser objects

    def GetGameInfo(self, game_id: Union[int, str]) -> game:
        """Gets basic game informations

        :param game_id: The ID of the game to fetch
        :return: :class:`game` object with basic infos or :class:`None` if the game isn't found.
        Missing infos are:
        -achievements
        -is_final
        -num_achievements
        -num_distinct_players_casual
        -num_distinct_players_hardcore
        -rich_presence_patch
        """
        #GameTitle, Console and GameIcon seem to be dupes of Title, ConsoleName and ImageIcon only present in the basic game infos so they aren't implemented

        r = self._request("API_GetGame.php", {"i": game_id}).json()
        if r["Title"] is None: #aka game doesn't exist
            return None
        return game(game_id,
                title=r["Title"],
                forum_topic_id=r["ForumTopicID"],
                console_id=r["ConsoleID"],
                console_name=r["ConsoleName"],
                flags=r["ConsoleName"],
                image_icon=r["ImageIcon"],
                image_title=r["ImageTitle"],
                image_in_game=r["ImageIngame"],
                image_box_art=r["ImageBoxArt"],
                publisher=r["Publisher"],
                developer=r["Developer"],
                genre=r["Genre"],
                release_date=r["Released"],
                raw=r
                )

    def GetGameInfoExtended(self, game_id: Union[int, str]) -> game:
        """Gets all informations on a game

        :param game_id: The ID of the game to fetch
        :return: :class:`game` object or :class:`None` if the game isn't found.
        """

        r = self._request("API_GetGameExtended.php", {"i": game_id}).json()
        if r["Title"] is None: #aka game doesn't exist
            return None
        return game(game_id,
                title=r["Title"],
                forum_topic_id=r["ForumTopicID"],
                console_id=r["ConsoleID"],
                console_name=r["ConsoleName"],
                flags=r["ConsoleName"],
                image_icon=r["ImageIcon"],
                image_title=r["ImageTitle"],
                image_in_game=r["ImageIngame"],
                image_box_art=r["ImageBoxArt"],
                publisher=r["Publisher"],
                developer=r["Developer"],
                genre=r["Genre"],
                release_date=r["Released"],
                raw=r,
                achievements=[achivements_converter(r["Achievements"][a]) for a in r["Achievements"]], #converts everything to achivement objects
                is_final=r["IsFinal"],
                num_achievements=r["NumAchievements"],
                num_distinct_players_casual=r["NumDistinctPlayersCasual"],
                num_distinct_players_hardcore=r["NumDistinctPlayersHardcore"],
                rich_presence_patch=r["RichPresencePatch"]
                )

    def GetConsoleIDs(self) -> list:
        """Gets a list of the consoles ID and the name associated with them.

        :return: :class:`list` of :class:`dict` objects with a "ID" and a "Name" key
        """

        r = self._request("API_GetConsoleIDs.php").json()
        return r

    def GetGameList(self, console_id: Union[int, str]) -> list:
        """Gets a list of games on a console.

        :param console_id: The ID of the console
        :return: :class:`list` of very trimmed down :class:`game` objects, or None if the console isn't found.
        These objects have the title, game_id, image_icon, console_id and console_name, everything else is None.
        """

        r = self._request("API_GetGameList.php", params={"i": console_id}).json()
        if r == []: #aka console not found
            return None

        return [game(title=g["Title"], game_id=g["ID"], console_id=g["ConsoleID"], image_icon=g["ImageIcon"], console_name=g["ConsoleName"], raw=g)
                for g in r] #list of RAuser objects
    
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

    def GetUserProgress(self, username: str, game_ids: list) -> dict:
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
            games.append(game_user_info(num_possible_achievements=r[g]["NumPossibleAchievements"],
                                        possible_score=r[g]["PossibleScore"],
                                        num_achieved=r[g]["NumAchieved"],
                                        score_achieved=r[g]["ScoreAchieved"],
                                        num_achieved_hardcore=r[g]["NumAchievedHardcore"],
                                        score_achieved_hardcore=r[g]["ScoreAchievedHardcore"],
                                        raw=g))
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
        games = []
        for g in r: #for each games
            user_info = game_user_info(num_possible_achievements=g["NumPossibleAchievements"],
                                        possible_score=g["PossibleScore"],
                                        num_achieved=g["NumAchieved"],
                                        score_achieved=g["ScoreAchieved"],
                                        last_played=g["LastPlayed"],
                                        my_vote=g["MyVote"])
            games.append(game(game_id=g["GameID"],
                            console_id=g["ConsoleID"],
                            console_name=g["ConsoleName"],
                            title=g["Title"],
                            image_icon=g["ImageIcon"],
                            user_info=user_info,
                            raw=g))
        return games

    def GetUserSummary(self, username: str, recent_games_count: int=5, achievements_count: int=10) -> user_summary:
        """Gets the summary of a user

        :param username: a string with the username
        :param recent_games_count (optional): how many recent games to return (the API doesn't seem to have a limit)
        :param achievements_count (optional): how many achivements to return (the API won't return more than 50 at once)
        :return: a :class:`user_summary` instance. The recently_played atttribute is a list of :class:`dict`. last_game is a complete game object. 
        """
            
        r = self._request("API_GetUserSummary.php", {"u": username, "g": recent_games_count, "a": achievements_count}).json()

        lg = r["LastGame"]
        return user_summary(recently_played=r["RecentlyPlayed"], #list of dicts
            rich_presence_msg=r["RichPresenceMsg"],
            member_since=r["MemberSince"],
            last_game_id=r["LastGameID"],
            last_game=game(game_id=lg["ID"], 
                            title=lg["Title"],
                            console_id=lg["ConsoleID"],
                            forum_topic_id=lg["ForumTopicID"],
                            flags=lg["Flags"],
                            image_icon=lg["ImageIcon"],
                            image_title=lg["ImageTitle"],
                            image_in_game=lg["ImageIngame"],
                            image_box_art=lg["ImageBoxArt"],
                            publisher=lg["Publisher"],
                            developer=lg["Developer"],
                            genre=lg["Genre"],
                            release_date=lg["Released"],
                            is_final=lg["IsFinal"],
                            console_name=lg["ConsoleName"],
                            raw=lg
                            ),
            contrib_count=r["ContribCount"],
            contrib_yield=r["ContribYield"],
            total_points=r["TotalPoints"],
            total_true_points=r["TotalTruePoints"],
            permissions=r["Permissions"],
            untracked=r["Untracked"],
            motto=r["Motto"],
            rank=r["Rank"],
            total_ranked=r["TotalRanked"],
            recent_achievements=r["RecentAchievements"],
            user_pic=r["UserPic"],
            status=r["Status"],
            raw=r)

    def GetUserGamesCompleted(self, username: str) -> dict:
        """Gets the completed games of a user

        :param username: a string with the username
        :return: a :class:`dict` instance with the completed games and other infos. 
        """
            
        r = self._request("API_GetUserSummary.php", {"u": username}).json()
        return r