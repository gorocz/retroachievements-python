from datetime import datetime
from typing import Union

from .exceptions import *

base_url = "https://retroachievements.org"

def int_or_none(nbr) -> Union[int, None]: #converts to int except if none
    if nbr in (None, NotReturned):
        return nbr
    return int(nbr)

def full_image_url_or_none(url) -> Union[str, None]: #gets the full image url if the url isn't None
    if url in (None, NotReturned):
        return url
    return base_url + url

def strptime_or_none(s) -> Union[datetime, None]: #gets the datetime from a string if it's not None
    if s in (None, NotReturned):
        return s
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

def bool_or_none(b) -> Union[bool, None]:
    if b in (None, NotReturned):
        return b
    if type(b) == str: #isawarded is a str for some reason
        b = int(b)
    return bool(b)

def percentage_str_to_float(s) -> Union[float, None]:
    if s in (None, NotReturned):
        return s
    if type(s) == int: #for some reason it can be an int if it's 0 in GetUserCompletedGames
        return float(s)
    if "%" in s: #ex: "98.05%", like in GetGameInfoAndUserProgress
        return float(s.strip('%'))
    else: #ex: "0.5676", like in GetUserCompletedGames
        return round(float(s)*100, 2) #we need to round bc weird float behaviour
    #else: #this should never be called
        #raise ValueError(f"{type(s)}: '{s}' was not supposed to get converted, please report this")
        


class _NotReturned:
    """For when a value isn't returned by the API"""
    def __repr__(self):
        return "RAclient.NotReturned"

    def __bool__(self): #so we can use or when there's 2 possible keys
        return False


NotReturned = _NotReturned() #that way it's always the same object

class RAuser:
    def __init__(self, 
                raw,
                username=NotReturned,
                points=NotReturned,
                retro_points=NotReturned,
                ):

        self.username = username
        self.points = int_or_none(points)
        self.retro_points = int_or_none(retro_points)

        self.raw = raw #the raw json

    def __repr__(self):
        return f"<RAuser {self.username}, {self.points}pts>"

class achievement:
    def __init__(self,
                raw,
                id=NotReturned,
                game_id=NotReturned,
                game_title=NotReturned,
                game_icon=NotReturned,
                num_awarded=NotReturned,
                num_awarded_hardcore=NotReturned,
                title=NotReturned,
                description=NotReturned,
                points=NotReturned,
                true_ratio=NotReturned,
                author=NotReturned,
                date_modified=NotReturned,
                date_created=NotReturned,
                badge_name=NotReturned,
                display_order=NotReturned,
                mem_addr=NotReturned,
                is_awarded=NotReturned,
                date_awarded=NotReturned,
                date_awarded_hardcore=NotReturned,
                hardcore_achieved=NotReturned,
                console_name=NotReturned,
                a_type=NotReturned,):

        self.id = int_or_none(id)
        self.game_id = int_or_none(game_id)
        self.game_title = game_title
        self.game_icon = full_image_url_or_none(game_icon)
        self.num_awarded = int_or_none(num_awarded)
        self.num_awarded_hardcore = int_or_none(num_awarded_hardcore)
        self.title = title
        self.description = description
        self.points = int_or_none(points)
        self.true_ratio = int_or_none(true_ratio)
        self.author = author
        self.date_modified = strptime_or_none(date_modified)
        self.date_created = strptime_or_none(date_created)
        self.badge_name = badge_name
        self.display_order = int_or_none(display_order)
        self.mem_addr = mem_addr
        self.is_awarded = bool_or_none(is_awarded)
        self.date_awarded = strptime_or_none(date_awarded)
        self.date_awarded_hardcore = strptime_or_none(date_awarded_hardcore) #should be named DateEarnedHardcore but renamed for constitency
        self.hardcore_achieved = bool_or_none(hardcore_achieved) #for some reason it's often wrong in user summmary so it returns NotReturned there
        self.console_name = console_name
        self.a_type=a_type
        #CumulScore not implemented bc it works wackily and you should use sum() instead

        self.raw = raw

    def __str__(self):
        return f'Achievement {self.id}: "{self.title}"'

class game:
    def __init__(self, 
                raw,
                game_id=NotReturned,
                title=NotReturned,
                image_icon=NotReturned,
                console_id=NotReturned,
                console_name=NotReturned,
                forum_topic_id=NotReturned,
                flags=NotReturned,
                image_title=NotReturned,
                image_in_game=NotReturned,
                image_box_art=NotReturned,
                publisher=NotReturned,
                developer=NotReturned,
                genre=NotReturned,
                release_date=NotReturned,
                #stuff under is only from extended infos
                achievements=NotReturned,
                is_final=NotReturned,
                num_achievements=NotReturned,
                num_distinct_players_casual=NotReturned,
                num_distinct_players_hardcore=NotReturned,
                rich_presence_patch=NotReturned,
                #user infos
                #num_possible_achievements=NotReturned,
                possible_score=NotReturned,
                num_achieved=NotReturned,
                score_achieved=NotReturned,
                num_achieved_hardcore=NotReturned,
                score_achieved_hardcore=NotReturned,
                last_played=NotReturned,
                my_vote=NotReturned,
                completion_percentage=NotReturned, #user_completion
                completion_percentage_hardcore=NotReturned,): #user_completion_hardcore

        self.game_id = int_or_none(game_id)
        self.title = title
        self.forum_topic_id = int_or_none(forum_topic_id)
        self.console_id = int_or_none(console_id)
        self.console_name = console_name
        self.flags = flags

        self.image_icon = full_image_url_or_none(image_icon)
        self.image_title = full_image_url_or_none(image_title)
        self.image_in_game = full_image_url_or_none(image_in_game)
        self.image_box_art = full_image_url_or_none(image_box_art)

        self.publisher = publisher
        self.developer = developer
        self.genre = genre
        self.release_date = release_date

        self.achievements = achievements
        self.is_final = is_final
        self.num_achievements = num_achievements
        self.num_distinct_players_casual = num_distinct_players_casual
        self.num_distinct_players_hardcore= num_distinct_players_hardcore
        self.rich_presence_patch = rich_presence_patch

        #self.num_possible_achievements = num_possible_achievements #actually a dupe of num_achievements i think
        self.possible_score = possible_score
        self.num_achieved = num_achieved
        self.score_achieved = score_achieved
        self.num_achieved_hardcore = num_achieved_hardcore
        self.score_achieved_hardcore = score_achieved_hardcore
        self.last_played = strptime_or_none(last_played)
        self.my_vote = my_vote
        self.completion_percentage = percentage_str_to_float(completion_percentage)
        self.completion_percentage_hardcore = percentage_str_to_float(completion_percentage_hardcore)

        self.raw = raw


class user_summary:
    def __init__(self,
        username,
        id,
        awarded,
        last_activity,
        recently_played, #list of dicts
        rich_presence_msg,
        member_since,
        #last_game_id,
        last_game,
        contrib_count,
        contrib_yield,
        total_points,
        total_true_points,
        permissions,
        untracked,
        motto,
        rank,
        total_ranked,
        recent_achievements,
        user_pic,
        status,
        raw):

        self.username = username
        self.id = id
        self.awarded = awarded
        self.last_activity = last_activity
        self.recently_played = recently_played
        self.rich_presence_msg = rich_presence_msg
        self.member_since = strptime_or_none(member_since)
        #self.last_game_id = int_or_none(last_game_id) #useless so removed
        self.last_game = last_game
        self.contrib_count = int_or_none(contrib_count)
        self.contrib_yield = int_or_none(contrib_yield)
        self.total_points = int_or_none(total_points)
        self.total_true_points = int_or_none(total_true_points)
        self.permissions = int_or_none(permissions)
        self.untracked = untracked
        self.motto = motto
        self.rank = int_or_none(rank)
        self.total_ranked = int_or_none(total_ranked)
        self.recent_achievements = recent_achievements
        self.user_pic = full_image_url_or_none(user_pic)
        self.status = status
        self.raw = raw

class activity:
    def __init__(self,
        id,
        username,
        activity_type,
        data,
        data2,
        last_update,
        timestamp,
        raw,):

        self.id = id
        self.username = username #called username instead of user to not be mistaken for a RAuser object
        self.activity_type = activity_type
        self.data = data
        self.data2 = data2
        self.last_update = strptime_or_none(last_update)
        self.timestamp = strptime_or_none(timestamp)
        self.raw = raw
