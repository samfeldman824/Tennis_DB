# pylint: disable-all

import re
import os
from flask import Response, request
import json
from bson.objectid import ObjectId
import pymongo
import csv

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.Tennis_DB
    mongo.server_info()
except:
    print("Error -- can't connect")

def original():
    return Response(
            response= json.dumps({"message": "sup cuh"}),
            status=200,
            mimetype="application/json"
        )



# function to list all players
def get_all_players():
    try:
        data = list(db.player_stats.find()) # list of all players in db
        
        
        for player in data:
            player['Match List'] = []
            player['Advanced Stats']['Included Match List'] = []
            player["_id"] = str(player["_id"])
            player["Match List"] = str(player["Match List"])
        
        return Response(
            response= json.dumps({"message": "Players found", "players": data}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "cannot read players"}),
            status=500,
            mimetype="application/json"
        )

# function to list all matches by given player
def get_all_player_matches(name):
    try:
        match_filter = {"$or": [{"Winner": {"$regex": f"^{name}$", "$options": "i"}}, {"Loser": {"$regex": f"^{name}$", "$options": "i"}}]}
        data = list(db.matches.find(match_filter)) # list of all matches in db
        if len(data) == 0:
            return Response(
            response= json.dumps({"message": f"{name} has no matches"}),
            status=200,
            mimetype="application/json"
        )
        for m in data:
                m["_id"] = str(m["_id"])    
        
        print(data)
        print('data length:',len(data))
        
    
        # returning all matches
        return Response(
            response= json.dumps({"message": f"{name} has played {len(data)} matches", "matches": data}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "cannot read matches"}),
            status=500,
            mimetype="application/json"
        )

# function to get all players wins
def get_player_win_totals():
    try:
        
        data = list(db.player_stats.find({}, {'_id': 0, 'Name': 1, 'Wins': 1}).sort("Wins", -1)) # list players win in a sorted list
        
        return Response(
            response= json.dumps({"message": "Players found", "data": data}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "cannot read player win totals"}),
            status=500,
            mimetype="application/json"
        )

# function to add player to db
def create_player(name):
    # creating dictionary to represent new player
    
    



    try:

        player_filter = {"Name": {"$regex": f"^{name}$", "$options": "i"}}
        data = list(db.player_stats.find(player_filter))
        if len(data) > 0:
            return Response(
                response= json.dumps(
                {"message": f"{name} already exists"}
                ),
                status=200,
                mimetype="application/json"
            )

        new_player = {
            "Name": name,
            "Wins": 0,
            "Losses": 0,
            "Sets Won": 0,
            "Sets Lost": 0,
            "3 Set Matches": 0,
            "Games Won": 0,
            "Games Lost": 0,
            "Match List": [],
            "Advanced Stats": {
            "1st Serves In": 0,
            "1st Serves Hit": 0,
            "1st Serve Points Won": 0,
            "1st Serve Points Lost": 0,
            "2nd Serves In": 0,
            "2nd Serves Hit": 0,
            "2nd Serve Points Won": 0,
            "2nd Serve Points Lost": 0,
            "Game Points Won": 0,
            "Game Points Lost": 0,
            "Double Faults": 0,
            "1st Serve Points Won on Return": 0,
            "1st Serve Points Played on Return": 0,
            "2nd Serve Points Won on Return": 0,
            "2nd Serve Points Played on Return": 0,
            "Break Points Won": 0,
            "Break Points Lost": 0,
            "Opponent Double Faults": 0,
            "First Shot Error After Serve": 0,
            "First Shot Error After Return": 0,
            "Matches with Advanced Stats": 0,
            "Included Match List": []},
            }
        dbResponse = db.player_stats.insert_one(new_player)
        print(dbResponse.inserted_id)
        return Response(
            response= json.dumps(
            {"message": f"{name} created",
            "name": f"{name}"}
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps(
            {"message": "Player not created",
            "name": f"{dbResponse.player}"}
            ),
            status=500,
            mimetype="application/json"
        )
    
# function to add match to matches db
def add_match(winner, loser, sets, score, advanced_stats_dict={}):
    try:
        # create dictionary representing new match
        new_match = {
            "Winner": winner,
            "Loser": loser,
            "Number of Sets": int(sets),
            "Set Scores": json.loads(score),
            "Advanced Stats": {},
            }
        
        print(advanced_stats_dict)

        # if advanced_stats were given, create variables for each stat
        if bool(advanced_stats_dict):
            print('yes')
            player = advanced_stats_dict['Player']
            first_serves_in = int(advanced_stats_dict['1st Serves In'])
            first_serves_hit = int(advanced_stats_dict['1st Serves Hit'])
            first_serve_points_won = int(advanced_stats_dict['1st Serve Points Won'])
            first_serve_points_lost = int(advanced_stats_dict['1st Serve Points Lost'])
            second_serves_in = int(advanced_stats_dict['2nd Serves In'])
            second_serves_hit = int(advanced_stats_dict['2nd Serves Hit'])
            second_serve_points_won = int(advanced_stats_dict['2nd Serve Points Won'])
            second_serve_points_lost = int(advanced_stats_dict['2nd Serve Points Lost'])
            game_points_won = int(advanced_stats_dict['Game Points Won'])
            game_points_lost = int(advanced_stats_dict['Game Points Lost'])
            double_faults = int(advanced_stats_dict['Double Faults'])
            first_serve_points_won_on_return = int(advanced_stats_dict['1st Serve Points Won on Return'])
            first_serve_points_lost_on_return = int(advanced_stats_dict['1st Serve Points Lost on Return'])
            second_serve_points_won_on_return = int(advanced_stats_dict['2nd Serve Points Won on Return'])
            second_serve_points_lost_on_return = int(advanced_stats_dict['2nd Serve Points Lost on Return'])
            break_points_won = int(advanced_stats_dict['Break Points Won'])
            break_points_lost = int(advanced_stats_dict['Break Points Lost'])
            opponent_double_faults = int(advanced_stats_dict['Opponent Double Faults'])
            first_shot_error_after_serve = int(advanced_stats_dict['First Shot Error after Serve'])
            first_shot_error_after_return = int(advanced_stats_dict['First Shot Error after Return'])

            # Adding advanced stats for whichever player has them
            new_match['Advanced Stats']['Player'] = player
            new_match['Advanced Stats']['First Serves In'] = first_serves_in
            new_match['Advanced Stats']['First Serves Hit'] = first_serves_hit
            new_match['Advanced Stats']['First Serve Points Won'] = first_serve_points_won
            new_match['Advanced Stats']['First Serve Points Lost'] = first_serve_points_lost
            new_match['Advanced Stats']['Second Serves In'] = second_serves_in
            new_match['Advanced Stats']['Second Serves Hit'] = second_serves_hit
            new_match['Advanced Stats']['Second Serve Points Won'] = second_serve_points_won
            new_match['Advanced Stats']['Second Serve Points Played'] = second_serve_points_lost
            new_match['Advanced Stats']['Game Points Won'] = game_points_won
            new_match['Advanced Stats']['Game Points Lost'] = game_points_lost
            new_match['Advanced Stats']['Double Faults'] = double_faults
            new_match['Advanced Stats']['First Serve Points Won On Return'] = first_serve_points_won_on_return
            new_match['Advanced Stats']['First Serve Points Lost On Return'] = first_serve_points_lost_on_return
            new_match['Advanced Stats']['Second Serve Points Won On Return'] = second_serve_points_won_on_return
            new_match['Advanced Stats']['Second Serve Points Lost On Return'] = second_serve_points_lost_on_return
            new_match['Advanced Stats']['Break Points Won'] = break_points_won
            new_match['Advanced Stats']['Break Points Lost'] = break_points_lost
            new_match['Advanced Stats']['Opponent Double Faults'] = opponent_double_faults
            new_match['Advanced Stats']['First Shot Error After Serve'] = first_shot_error_after_serve
            new_match['Advanced Stats']['First Shot Error After Return'] = first_shot_error_after_return


            # updating player's advanced stats
            db.player_stats.update_one(
            {"Name": {"$regex": f"^{player}$", "$options": "i"}},
            {"$inc":
            {
            "Advanced Stats.1st Serves In": first_serves_in,
            "Advanced Stats.1st Serves Hit": first_serves_hit,
            "Advanced Stats.1st Serve Points Won": first_serve_points_won,
            "Advanced Stats.1st Serve Points Lost": first_serve_points_lost,
            "Advanced Stats.2nd Serves In": second_serves_in,
            "Advanced Stats.2nd Serves Hit": second_serves_hit,
            "Advanced Stats.2nd Serve Points Won": second_serve_points_won,
            "Advanced Stats.2nd Serve Points Lost": second_serve_points_lost,
            "Advanced Stats.Game Points Won": game_points_won,
            "Advanced Stats.Game Points Lost": game_points_lost,
            "Advanced Stats.Double Faults": double_faults,
            "Advanced Stats.1st Serve Points Won on Return": first_serve_points_won_on_return,
            "Advanced Stats.1st Serve Points Lost on Return": first_serve_points_lost_on_return,
            "Advanced Stats.2nd Serve Points Won on Return": second_serve_points_won_on_return,
            "Advanced Stats.2nd Serve Points Lost on Return": second_serve_points_lost_on_return,
            "Advanced Stats.Break Points Won": break_points_won,
            "Advanced Stats.Break Points Lost": break_points_lost,
            "Advanced Stats.Opponent Double Faults": opponent_double_faults,
            "Advanced Stats.First Shot Error after Serve": first_shot_error_after_serve,
            "Advanced Stats.First Shot Error after Return": first_shot_error_after_return,
            "Advanced Stats.Matches with Advanced Stats": 1
            }
            }
            )
        print('still working')
        # check if winner of match is a player in db, if not, player is added
        player_w = db.player_stats.find_one({"Name": {"$regex": f"^{winner}$", "$options": "i"}})

        # match score in array of arrays
        match_score = json.loads(score)

        # number of sets in match
        sets_played = len(match_score)

        # whether there was a third set
        if sets_played == 3:
            was_third_set = 1
        else:
            was_third_set = 0

        if player_w is None:
            create_player(winner)

        # calculating games won for winner and loser
        winner_games = sum(sublist[0] for sublist in match_score)
        loser_games = sum(sublist[1] for sublist in match_score)

        # updating winner's stats
        db.player_stats.update_one(
            {"Name": {"$regex": f"^{winner}$", "$options": "i"}},
            {"$inc":
            {"Wins": 1,
            "Sets Won": 2,
            "Sets Lost": was_third_set,
            "3 Set Matches": was_third_set,
            "Games Won": winner_games,
            "Games Lost": loser_games,
            }
            }
            )
        

        # check if loser of match is a player in db, if not, player is added
        player_l = db.player_stats.find_one({"Name": {"$regex": f"^{loser}$", "$options": "i"}})
        if player_l is None:
            create_player(loser)

        # updating loser's stats
        db.player_stats.update_one(
            {"Name": {"$regex": f"^{loser}$", "$options": "i"}},
            {"$inc":
            {"Losses": 1,
            "Sets Won": was_third_set,
            "Sets Lost": 2,
            "3 Set Matches": was_third_set,
            "Games Won": loser_games,
            "Games Lost": winner_games
            }
            }
            )

        # adds match to matches db
        inserted_match = db.matches.insert_one(new_match)

        # get object id of inserted match
        match_id = inserted_match.inserted_id

        # adding match id to matches list for each player
        db.player_stats.update_one(
            {"Name": {"$regex": f"^{winner}$", "$options": "i"}},
            {"$push": {"Match List": match_id}})
        
        db.player_stats.update_one(
            {"Name": {"$regex": f"^{loser}$", "$options": "i"}},
            {"$push": {"Match List": match_id}})

        db.player_stats.update_one(
            {"Name": {"$regex": f"^{player}$", "$options": "i"}},
            {"$push": {"Advanced Stats.Included Match List": match_id}}
        )
        
        return Response(
            response= json.dumps(
            {"message": "match created",
            }
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        print('fuck')
        return Response(
            response= json.dumps(
            {"message": "match not added"}),
            status=500,
            mimetype="application/json"
        )

# function to parse csv file with match data
def add_match_from_csv(filepath):
    file_found = False
    try:
        try:
            with open(filepath, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                print("file read in1")
                        
                new_match = {}
                    
                for row in reader:
                    new_match = {**new_match, **row}
                file_found = True
        except Exception as ex:
            print(ex)

        if not file_found:
            try:
                with open("/" + filepath, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    print("file read in2")
                            
                    new_match = {}
                        
                    for row in reader:
                        new_match = {**new_match, **row}
                    file_found = True
            except Exception as ex:
                print(ex)

        
        if not file_found:
                try:
                    with open("." + filepath, newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        print("file read in3")
                                
                        new_match = {}
                            
                        for row in reader:
                            new_match = {**new_match, **row}
                        file_found = True
                except Exception as ex:
                    print(ex)    

        
        if not file_found:
                try:
                    with open("./" + filepath, newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        print("file read in4")
                                
                        new_match = {}
                            
                        for row in reader:
                            new_match = {**new_match, **row}
                        file_found = True
                except Exception as ex:
                    print(ex)    
                
        winner = new_match['Winner']
        loser = new_match['Loser']
        n_sets = new_match['Number of Sets']
        score = new_match['Score']

        print(new_match)

        add_match(winner, loser, n_sets, score, new_match)
        return Response(
        response= json.dumps(
        {"message": "match read"}),
        status=200,
        mimetype="application/json")
    except Exception as ex:
        return Response(
            response= json.dumps(
            {"message": "match not read"}),
            status=500,
            mimetype="application/json"
        )

def add_match_from_uploaded_csv():
    file = request.files['file']
    contents = file.read()
    reader = csv.DictReader(contents.decode().splitlines())
    data = []
    for row in reader:
        data.append(row)
    new_match = data[0]

    winner = new_match['Winner']
    # print(winner)
    loser = new_match['Loser']
    # print(loser)
    n_sets = new_match['Number of Sets']
    # print(n_sets)
    score = new_match['Score']
    # print(score)
    

    add_match(winner, loser, n_sets, score, new_match)
    # print(file)
    # print('works')
    
    
    return Response(
            response= json.dumps({"message": "received"}),
            status=200,
            mimetype="application/json"
        )

# function to update a current player name
def update_name(id):
    print("hello")
    try:
        name = request.form["Name"]
        dbResponse = db.player_stats.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"Name": name}}
        )
        query_winner = {"Winner": {"$regex": f"^{name}$", "$options": "i"}}
        query_loser = {"Loser": {"$regex": f"^{name}$", "$options": "i"}}
        
        update_winner = {"$set": {"Winner": name}}
        update_loser = {"$set": {"Loser": name}}

        db.matches.update_many(query_winner, update_winner)
        db.matches.update_many(query_loser, update_loser)
    
        if dbResponse.modified_count == 1:
            return Response(
                response= json.dumps({"message": "player name updated", "name": f"{name}"}),
                status=200,
                mimetype="application/json"
        )
        else:
            return Response(
                response= json.dumps({"message": "nothing to update"}),
                status=500,
                mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "didn't work"}),
            status=500,
            mimetype="application/json"
        )

# function to update score and corresponding player stats
def update_score(id):

    try:
        new_score = json.loads(request.form['Set Score'])

        old_match_dict = db.matches.find_one({"_id": ObjectId(id)}, {"Set Scores": 1, "Winner": 1, "Loser": 1, "_id": 0})

        old_score = old_match_dict['Set Scores']
        winner = old_match_dict['Winner']
        loser = old_match_dict['Loser']

        old_sets_played = len(old_score)

        winner_old_games = sum(sublist[0] for sublist in old_score)
        loser_old_games = sum(sublist[1] for sublist in old_score)

        new_sets_played = len(new_score)

        winner_new_games = sum(sublist[0] for sublist in new_score)
        loser_new_games = sum(sublist[1] for sublist in new_score)
        
        set_diff = new_sets_played - old_sets_played

        winner_game_diff = winner_new_games - winner_old_games
        loser_game_diff = loser_new_games - loser_old_games



        third_set_update = 0
        if set_diff != 0:
            if old_sets_played > new_sets_played:
                third_set_update = -1
            else:
                third_set_update = 1

        db.matches.update_one({"_id": ObjectId(id)}, {"$set": {"Set Scores": new_score}})
        
        db.player_stats.update_one({"Name": {"$regex": f"^{winner}$", "$options": "i"}}, {"$inc": {"Games Won": winner_game_diff, "Games Lost": loser_game_diff, "3 Set Matches": third_set_update, "Sets Lost": third_set_update}})
        db.player_stats.update_one({"Name": {"$regex": f"^{loser}$", "$options": "i"}}, {"$inc": {"Games Won": loser_game_diff, "Games Lost": winner_game_diff, "3 Set Matches": third_set_update, "Sets Won": third_set_update}})
        

        return Response(
                response= json.dumps({"message": "match updated"}),
                status=200,
                mimetype="application/json"
        )

    except Exception as ex:
        return Response(
            response= json.dumps({"message": "score not updated"}),
            status=500,
            mimetype="application/json"
        )

# function to delete match given id
def delete_match(id):
    try:

        match_to_delete = db.matches.find_one({"_id":ObjectId(id)})

        player = match_to_delete['Advanced Stats']['Player']
        first_serves_in = match_to_delete['Advanced Stats']['First Serves In']
        first_serves_hit = match_to_delete['Advanced Stats']['First Serves Hit']
        first_serve_points_won = match_to_delete['Advanced Stats']['First Serve Points Won']
        first_serve_points_lost = match_to_delete['Advanced Stats']['First Serve Points Lost']
        second_serves_in = match_to_delete['Advanced Stats']['Second Serves In']
        second_serves_hit = match_to_delete['Advanced Stats']['Second Serves Hit']
        second_serve_points_won = match_to_delete['Advanced Stats']['Second Serve Points Won']
        second_serve_points_lost = match_to_delete['Advanced Stats']['Second Serve Points Played']
        game_points_won = match_to_delete['Advanced Stats']['Game Points Won']
        game_points_lost = match_to_delete['Advanced Stats']['Game Points Lost']
        double_faults = match_to_delete['Advanced Stats']['Double Faults']
        first_serve_points_won_on_return = match_to_delete['Advanced Stats']['First Serve Points Won On Return']
        first_serve_points_lost_on_return = match_to_delete['Advanced Stats']['First Serve Points Lost On Return']
        second_serve_points_won_on_return = match_to_delete['Advanced Stats']['Second Serve Points Won On Return']
        second_serve_points_lost_on_return = match_to_delete['Advanced Stats']['Second Serve Points Lost On Return']
        break_points_won = match_to_delete['Advanced Stats']['Break Points Won']
        break_points_lost = match_to_delete['Advanced Stats']['Break Points Lost']
        opponent_double_faults = match_to_delete['Advanced Stats']['Opponent Double Faults']
        first_shot_error_after_serve = match_to_delete['Advanced Stats']['First Shot Error After Serve']
        first_shot_error_after_return = match_to_delete['Advanced Stats']['First Shot Error After Return']

        # removing match stats from player stats
        db.player_stats.update_one(
            {"Name": {"$regex": f"^{player}$", "$options": "i"}},
            {"$inc":
            {
            "Advanced Stats.1st Serves In": -first_serves_in,
            "Advanced Stats.1st Serves Hit": -first_serves_hit,
            "Advanced Stats.1st Serve Points Won": -first_serve_points_won,
            "Advanced Stats.1st Serve Points Lost": -first_serve_points_lost,
            "Advanced Stats.2nd Serves In": -second_serves_in,
            "Advanced Stats.2nd Serves Hit": -second_serves_hit,
            "Advanced Stats.2nd Serve Points Won": -second_serve_points_won,
            "Advanced Stats.2nd Serve Points Lost": -second_serve_points_lost,
            "Advanced Stats.Game Points Won": -game_points_won,
            "Advanced Stats.Game Points Lost": -game_points_lost,
            "Advanced Stats.Double Faults": -double_faults,
            "Advanced Stats.1st Serve Points Won on Return": -first_serve_points_won_on_return,
            "Advanced Stats.1st Serve Points Lost on Return": -first_serve_points_lost_on_return,
            "Advanced Stats.2nd Serve Points Won on Return": -second_serve_points_won_on_return,
            "Advanced Stats.2nd Serve Points Lost on Return": -second_serve_points_lost_on_return,
            "Advanced Stats.Break Points Won": -break_points_won,
            "Advanced Stats.Break Points Lost": -break_points_lost,
            "Advanced Stats.Opponent Double Faults": -opponent_double_faults,
            "Advanced Stats.First Shot Error after Serve": -first_shot_error_after_serve,
            "Advanced Stats.First Shot Error after Return": -first_shot_error_after_return,
            "Advanced Stats.Matches with Advanced Stats": -1
            }
            }
                                   )
        dbResponse = db.matches.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
                response= json.dumps({"message": "match deleted"}),
                status=200,
                mimetype="application/json"
            )



    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "match not deleted"}),
            status=500,
            mimetype="application/json"
        )

# function to delete player given id
def delete_player_id(id):
    try:
        dbResponse = db.player_stats.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
                response= json.dumps({"message": "player deleted"}),
                status=200,
                mimetype="application/json"
            )


    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "player not deleted"}),
            status=500,
            mimetype="application/json"
        )

# function to delete player given name
def delete_player_name(name):
    try:
        dbResponse = db.player_stats.delete_one({"Name": {"$regex": f"^{name}$", "$options": "i"}})
        if dbResponse.deleted_count == 1:
            return Response(
                response= json.dumps({"message": f"{name} deleted"}),
                status=200,
                mimetype="application/json"
            )


    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": f"{name} not deleted"}),
            status=500,
            mimetype="application/json"
        )

def delete_matches():
    try:
        db.matches.delete_many({})
        return Response(
                response= json.dumps({"message": "matches deleted"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "matches not deleted"}),
            status=500,
            mimetype="application/json"
        )
