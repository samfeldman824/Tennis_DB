# pylint: disable-all
import pandas as pd


# Dictionary with mappings for each shot
shot_dictionary = {
    "j": ["Shot Type", "forehand"],
    "k": ["Shot Type", "backhand"],
    "u": ["Shot Type", "fh slice"],
    "i": ["Shot Type", "bh slice"],
    "o": ["Shot Type", "fh volley"],
    "p": ["Shot Type", "bh volley"],
    "l": ["Shot Type", "overhead"],
    "n": ["Shot Type", "fh dropshot"],
    "m": ["Shot Type", "bh dropshot"],
    "g": ["Shot Type", "fh lob"],
    "h": ["Shot Type", "bh lob"],
    "*": ["Rally Ending", "Winner"],
    "@": ["Rally Ending", "Unforced Error"],
    "#": ["Rally Ending", "Forced Error"],
    "!": ["Rally Ending", "Fault"],
    "1": ["Shot Direction", "line"],
    "2": ["Shot Direction", "middle"],
    "3": ["Shot Direction", "cross"],
    "4": ["Shot Direction", "inside-out"],
    "5": ["Shot Direction", "inside-in"],
    "6": ["Shot Direction", "t"],
    "7": ["Shot Direction", "body"],
    "8": ["Shot Direction", "wide"],
    "w": ["Location", "wide"],
    "d": ["Location", "deep"],
    "n": ["Location", "net"]
}

# Fills shots_list with with all characters that are shots so point string can be separated into shots
shots_list = []
for key, value in shot_dictionary.items():
    if value[0] == 'Shot Type':
        shots_list.append(key)

def score_side(score: str):
    score_dict = {
        '0': 0,
        '15': 1,
        '30': 2,
        '40': 3
    }
    if "Deuce" in score:
        if "Ad" in score:
            return "Ad"
        else:
            return "Deuce"
    else:
        server, returner = score.split("-")
        mapped_server = score_dict[server]
        mapped_returner = score_dict[returner]
        score_diff = abs(mapped_server - mapped_returner)
        if score_diff % 2 == 0:
            return "Deuce"
        else:
            return "Ad"

def parse_point(point: str, shots_list: list) -> list:
    """
    Parse a point string and extract substrings based on a list of shots.

    Args:
        point (str): The point string to be parsed.
        shots_list (list): A list of shots to be used for parsing.

    Returns:
        list: A list of substrings extracted from the point string.
    """
    
    # Input validation checks

    # checking point
    if not isinstance(point, str):
        raise TypeError("point must be a string")
    
    if len(point) == 0:
        raise ValueError("point can't be empty")

    if point[0] not in ['6', '7', '8']:
        raise ValueError("First character in point must be a serve direction")

    # checking shots_list
    if not isinstance(shots_list, list):
        raise TypeError("shots_list must be a list")
    
    for char in shots_list:
        if not isinstance(char, str):
            raise TypeError("Each shot in shots_list must be a string")

    substrings = []
    current_substring = ""

    # Check if point doesn not contain any shots other than serve
    only_serve = True
    char_index = 0
    for char in point:
        if char in shots_list:
            only_serve = False
            break
        char_index += 1
    
    # If point has shots after serve, parse and split them into shots
    if not only_serve:
        substrings.append(point[0:char_index])
        i = char_index
        while i < len(point):
            char = point[i]
            if char in shots_list:
                # Add the current character and the characters after it until the next shot character
                j = i + 1
                while j < len(point) and point[j] not in shots_list:
                    j += 1
                current_substring = point[i:j]
                # Add the current substring to the list
                if current_substring != "":
                    substrings.append(current_substring)
                i = j
        return substrings
    # If point only contained a serve
    else:
        return [point]

def parse_shots(shots: list, shot_options: dict, first_or_second: str, players: list, server: str, score: str) -> pd.DataFrame:
    """
    Parses each shot and adds the corresponding details to a Pandas Dataframe

    Args:
        shots (list): List of all separated shots to be parsed
        shot_options (dict): Dictionary used to map each character to certain stat
        first_or_second (str): Whether it is first or second serve
        players (list): List with the names of both players
        server (str): Name of server of the point
        score (str): Score at beginning of point

    Returns:
        pd.Dataframe: A dataframe containing each shot and corresponding details

    """

    if not isinstance(shots, list):
        raise TypeError("shots must be a list")
    
    if len(shots) == 0:
        raise ValueError("shots can't be empty")

    if not isinstance(shot_options, dict):
        raise TypeError("shot_options must be a dict")
    
    if not isinstance(first_or_second, str):
        raise TypeError("first_or_second must be a string")
    
    if not isinstance(players, list):
        raise TypeError("players must be a list")
    
    if len(players) != 2:
        raise ValueError("players must contain exactly 2 elements")

    if not isinstance(server, str):
        raise TypeError("server must be a string")
    
    if server not in players:
        raise ValueError("server must be one of the players")
    
    if not isinstance(score, str):
        raise TypeError("score must be a string")

    # Header names for df
    headers = ['Shot Type', 'Shot Direction', 'Rally Ending', 'Location', 'Return', 'Player', 'Score', 'Side']
    df = pd.DataFrame(columns=headers)

    table_i = 0

    # Have the server's name first in the list of players
    if players[0] != server:
        players[1] = players[0]
        players[0] = server
        
    # Alternate the player name for each shot
    for index, shot in enumerate(shots):
        if index % 2 == 0:
            df.at[table_i, 'Player'] = players[0]
        else:
            df.at[table_i, 'Player'] = players[1]

        # If first shot of point, it is a serve
        if index == 0:
            serve = shot[0]
            try:
                mapped_serve = shot_options[serve]
            except:
                raise KeyError("char not in shot_dict")
            df.at[table_i, 'Shot Direction'] = mapped_serve[1]
            df.at[table_i, 'Shot Type'] = first_or_second + ' serve'
            df.at[table_i, 'Score'] = score
            df.at[table_i, 'Side'] = score_side(score)
            
        else:
            df.at[table_i, 'Score'] = ''
        
        # If second shot of point, it is a return
        if index == 1:
            df.at[table_i, 'Return'] = True
        else:
            df.at[table_i, 'Return'] = False

        # Map each character to a stat of the shot
        i = 0
        while i < len(shot):
            try:
                char = shot[i]
            except:
                raise KeyError("char not in shot_dict")
            mapped_char = shot_options[char]
            column = mapped_char[0]
            stat = mapped_char[1]
            df.at[table_i, column] = stat
            i += 1
        
        
        table_i += 1

    # Fill missing values in 'Location' and 'Rally Ending' columns with 'in'
    df['Location'].fillna('in', inplace=True)
    df['Rally Ending'].fillna('in', inplace=True)
    df['Side'].fillna('', inplace=True)

    return df

def parse_match(filepath: str):
    """
    Parses a match data file and creates a Pandas DataFrame with the parsed data.

    Args:
        filepath (str): Filepath of the match data file.

    Returns:
        pd.DataFrame: A DataFrame containing the parsed match data.

    """



    match_df = pd.DataFrame()  # Initialize an empty DataFrame to store the parsed match data
    df = pd.read_csv(filepath)  # Read the match data from the CSV file into a DataFrame
    players_column = df['Players'].to_list()  # Extract the 'Players' column from the DataFrame and convert it to a list
    players = [players_column[0], players_column[1]]  # Extract the names of the players from the 'Players' column


    # Iterate through each row in the DataFrame and parse the match data
    for index, row in df[["Server", "Score", "1st", "2nd"]].iterrows():
        point_df = pd.DataFrame()  # Initialize an empty DataFrame to store the parsed point data
        point_df2 = pd.DataFrame()  # Initialize an empty DataFrame to store the parsed point data for the second serve

        server = str(row.values.tolist()[0])  # Extract the server's name from the row
        game_score = str(row.values.tolist()[1])  # Extract the game score from the row
        first_serve = str(row.values.tolist()[2])  # Extract the first serve data from the row
        second_serve = str(row.values.tolist()[3])  # Extract the second serve data from the row

        shots = parse_point(first_serve, shots_list)  # Parse the first serve data to obtain a list of shots
        point_df = parse_shots(shots, shot_dictionary, 'first', players, server, game_score)  # Parse the shots and create a DataFrame for the first serve

        # If there is second serve data, parse it and create a DataFrame for the second serve
        if second_serve != 'nan':
            shots = parse_point(second_serve, shots_list)  # Parse the second serve data to obtain a list of shots
            point_df2 = parse_shots(shots, shot_dictionary, 'second', players, server, game_score)  # Parse the shots and create a DataFrame for the second serve

        point_df = pd.concat([point_df, point_df2], axis=0)  # Concatenate the point data for first and second serves
        point_df = point_df.reset_index(drop=True)  # Reset the index of the point data DataFrame
        match_df = pd.concat([match_df, point_df], axis=0)  # Concatenate the point data to the match data

    return match_df # Return the final parsed match data DataFrame

match_df = parse_match('./csvs/corey.csv')
# print(match_df)