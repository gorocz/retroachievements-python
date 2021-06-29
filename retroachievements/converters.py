from .classes import *

def try_key_or_nr(d, k): #tries to return a key, else returns NotReturned
    try:
        return d[k]
    except KeyError:
        return NotReturned

#Converters to go from raw JSON to a proper object

def achivements_converter(a) -> achievement:
    return achievement(raw=a,
                    id=try_key_or_nr(a, "ID") or try_key_or_nr(a, "AchievementID"),
                    game_id=try_key_or_nr(a, "GameID"),
                    game_title=try_key_or_nr(a, "GameTitle"),
                    num_awarded=try_key_or_nr(a, "NumAwarded"),
                    num_awarded_hardcore=try_key_or_nr(a, "NumAwardedHardcore"),
                    title=try_key_or_nr(a, "Title"),
                    game_icon=try_key_or_nr(a, "GameIcon"),
                    description=try_key_or_nr(a, "Description"),
                    points=try_key_or_nr(a, "Points"),
                    true_ratio=try_key_or_nr(a, "TrueRatio"),
                    author=try_key_or_nr(a, "Author"),
                    date_modified=try_key_or_nr(a, "DateModified"),
                    date_created=try_key_or_nr(a, "DateCreated"),
                    badge_name=try_key_or_nr(a, "BadgeName"),
                    display_order=try_key_or_nr(a, "DisplayOrder"),
                    mem_addr=try_key_or_nr(a, "MemAddr"),
                    is_awarded=try_key_or_nr(a, "IsAwarded"),
                    date_awarded=try_key_or_nr(a, "DateAwarded") or try_key_or_nr(a, "DateEarned") or try_key_or_nr(a, "Date"),
                    date_awarded_hardcore=try_key_or_nr(a, "DateEarnedHardcore"),
                    hardcore_achieved=try_key_or_nr(a, "HardcoreMode"),
                    console_name=try_key_or_nr(a, "ConsoleName"),)


def RAuser_converter(u) -> RAuser:
    return RAuser(raw=u,
                username=u["1"],
                points=u["2"],
                retro_points=u["3"],)

def game_converter(g, game_id=None) -> game:
    if game_id is None: #we sometime must pass it from the function input instead of from the resp
        game_id=try_key_or_nr(g, "ID") or try_key_or_nr(g, "GameID") #Sometimes "GameID" is used instead, in that case just pass the id manually

    try:
        achievement_list = [achivements_converter(g["Achievements"][a]) for a in g["Achievements"]] #converts everything to achivement objects
    except KeyError:
        achievement_list = NotReturned

    return game(raw=g,
                game_id=game_id,
                title=try_key_or_nr(g, "Title"),
                forum_topic_id=try_key_or_nr(g, "ForumTopicID"),
                console_id=try_key_or_nr(g, "ConsoleID"),
                console_name=try_key_or_nr(g, "ConsoleName"),
                flags=try_key_or_nr(g, "Flags"),
                image_icon=try_key_or_nr(g, "ImageIcon"),
                image_title=try_key_or_nr(g, "ImageTitle"),
                image_in_game=try_key_or_nr(g, "ImageIngame"),
                image_box_art=try_key_or_nr(g, "ImageBoxArt"),
                publisher=try_key_or_nr(g, "Publisher"),
                developer=try_key_or_nr(g, "Developer"),
                genre=try_key_or_nr(g, "Genre"),
                release_date=try_key_or_nr(g, "Released"),
                #extended infos
                achievements=achievement_list, 
                is_final=try_key_or_nr(g, "IsFinal"),
                num_achievements=try_key_or_nr(g, "NumAchievements") or try_key_or_nr(g, "NumPossibleAchievements") or try_key_or_nr(g, "MaxPossible"),
                num_distinct_players_casual=try_key_or_nr(g, "NumDistinctPlayersCasual"),
                num_distinct_players_hardcore=try_key_or_nr(g, "NumDistinctPlayersHardcore"),
                rich_presence_patch=try_key_or_nr(g, "RichPresencePatch"),
                #user infos
                possible_score=try_key_or_nr(g, "PossibleScore"),
                num_achieved=try_key_or_nr(g, "NumAchieved") or try_key_or_nr(g, "NumAwardedToUser") or try_key_or_nr(g, "NumAwarded"),
                score_achieved=try_key_or_nr(g, "ScoreAchieved"),
                num_achieved_hardcore=try_key_or_nr(g, "NumAchievedHardcore") or try_key_or_nr(g, "NumAwardedToUserHardcore") or try_key_or_nr(g, "NumAwardedHardcore"),
                score_achieved_hardcore=try_key_or_nr(g, "ScoreAchievedHardcore"),
                last_played=try_key_or_nr(g, "LastPlayed"),
                my_vote=try_key_or_nr(g, "MyVote"),
                completion_percentage=try_key_or_nr(g, "UserCompletion") or try_key_or_nr(g, "PctWon"),
                completion_percentage_hardcore=try_key_or_nr(g, "UserCompletionHardcore") or try_key_or_nr(g, "PctWonHardcore"),)