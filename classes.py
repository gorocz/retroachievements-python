from datetime import datetime

base_url = "https://retroachievements.org"

def int_or_none(nbr): #converts to int except if none
    if nbr is None:
        return None
    return int(nbr)

def full_image_url_or_none(url): #gets the full image url if the url isn't None
    if url is None:
        return None
    return base_url + url

def strptime_or_none(s): #gets the datetime from a string if it's not None
    if s is None:
        return None
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


class RAuser:
    def __init__(self, 
                username,
                raw,
                points=None,
                retro_points=None,
                ):

        self.username = username
        self.points = int_or_none(points)
        self.retro_points = int_or_none(retro_points)

        self.raw = raw #the raw json

class achievement:
    def __init__(self,
                id,
                num_awarded,
                num_awarded_hardcore,
                title,
                description,
                points,
                true_ratio,
                author,
                date_modified,
                date_created,
                badge_name,
                display_order,
                mem_addr):

        self.id = int_or_none(id)
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

        def __str__(self):
            return f'Achievement {self.id}: "{self.title}"'

class game:
    def __init__(self, 
                game_id,
                title,
                image_icon,
                console_id,
                console_name,
                raw,
                forum_topic_id=None,
                flags=None,
                image_title=None,
                image_in_game=None,
                image_box_art=None,
                publisher=None,
                developer=None,
                genre=None,
                release_date=None,
                #stuff under is only from extended infos
                achievements=None,
                is_final=None,
                num_achievements=None,
                num_distinct_players_casual=None,
                num_distinct_players_hardcore=None,
                rich_presence_patch=None,
                user_info=None
                ):

        self.game_id = int_or_none(game_id)
        self.title = title
        self.forum_topic_id = int_or_none(forum_topic_id)
        self.console_id = int_or_none(console_id)
        self.console_name = console_name
        self.flags = flags

        self.image_icon = full_image_url_or_none(image_icon)
        self.image_title = full_image_url_or_none(image_title)
        self.image_in_game = full_image_url_or_none(image_in_game)
        image_box_art = full_image_url_or_none(image_box_art)

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

        self.user_info = user_info
        self.raw = raw

class game_user_info:
    """not meant to be directly used or accessed
    only used for game infos obtained by specifying a user
    """
    def __init__(self, 
            num_possible_achievements,
            possible_score,
            num_achieved,
            score_achieved,
            num_achieved_hardcore=None,
            score_achieved_hardcore=None,
            last_played=None,
            my_vote=None,
            raw=None
            ):
        
        self.num_possible_achievements = num_possible_achievements
        self.possible_score = possible_score
        self.num_achieved = num_achieved
        self.score_achieved = score_achieved
        self.num_achieved_hardcore = num_achieved_hardcore
        self.score_achieved_hardcore = score_achieved_hardcore
        self.last_played = strptime_or_none(last_played)
        self.my_vote = my_vote

        self.raw = raw

class user_summary:
    def __init__(self, 
        recently_played, #list of dicts
        rich_presence_msg,
        member_since,
        last_game_id,
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

        self.recently_played = recently_played
        self.rich_presence_msg = rich_presence_msg
        self.member_since = strptime_or_none(member_since)
        self.last_game_id = int_or_none(last_game_id)
        self.last_game = last_game
        self.contrib_count = int_or_none(contrib_count)
        self.contrib_yield = int_or_none(contrib_yield)
        self.total_points = int_or_none(total_points)
        self.total_true_points = int_or_none(total_true_points)
        self.permissions = permissions
        self.untracked = untracked
        self.motto = motto
        self.rank = rank
        self.total_ranked = int_or_none(total_ranked)
        self.recent_achievements = recent_achievements
        self.user_pic = full_image_url_or_none(user_pic)
        self.status = status
        self.raw = raw
