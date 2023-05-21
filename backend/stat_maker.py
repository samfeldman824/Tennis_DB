# pylint: disable-all

import pandas as pd
import chart_parser

players = ['Sam Feldman', 'Corey Craig']
match_df = chart_parser.parse_match('./csvs/corey.csv')
player1_df = match_df[match_df['Player'] == players[0]]
player2_df = match_df[match_df['Player'] == players[1]]
# print(match_df)
# print(player1_df)
# print(player2_df)

def to_percent(number1: int, number2: int):
    """
    This function takes two numbers as input and returns the percentage of number1 out of number2,
    rounded to two decimal places as a string with a '%' sign appended at the end.
    If number2 is zero, it returns '0%'.
    """
    if not isinstance(number1, int):
        raise TypeError("number1 must be a float")
    
    if not isinstance(number2, int):
        raise TypeError("number2 must be a float")

    try:
        decimal = number1 / number2
        r_decimal = round(decimal * 100, 2)
        if r_decimal == 0.0:
            return '0%'
        return str(r_decimal) + '%'
    except:
        return '0%'

serve_directions_headers = ['Hit', 'In', 'T (Deuce)', 'Body (Deuce)', 'Wide (Deuce)', 'T (Ad)', 'Body (Ad)', 'Wide (Ad)']
serve_directions_index = ['1st Serve', '2nd Serve']
serve_directions = pd.DataFrame(columns=serve_directions_headers, index=serve_directions_index)

serve_df = player1_df[(player1_df['Shot Type'].str.contains('serve'))]

# first serve

first_serves_hit = serve_df[serve_df['Shot Type'] == 'first serve']
first_serves_hit_deuce = first_serves_hit[first_serves_hit['Side'] == 'Deuce']
first_serves_hit_ad = first_serves_hit[first_serves_hit['Side'] == 'Ad']

first_serves_deuce_t = first_serves_hit_deuce[first_serves_hit_deuce['Shot Direction'] == 't']
first_serves_deuce_body = first_serves_hit_deuce[first_serves_hit_deuce['Shot Direction'] == 'body']
first_serves_deuce_wide = first_serves_hit_deuce[first_serves_hit_deuce['Shot Direction'] == 'wide']

first_serves_ad_t = first_serves_hit_ad[first_serves_hit_ad['Shot Direction'] == 't']
first_serves_ad_body = first_serves_hit_ad[first_serves_hit_ad['Shot Direction'] == 'body']
first_serves_ad_wide = first_serves_hit_ad[first_serves_hit_ad['Shot Direction'] == 'wide']

first_serves_in = first_serves_hit[first_serves_hit['Location'] == 'in']
first_serves_t = first_serves_hit[first_serves_hit['Shot Direction'] == 't']
first_serves_body = first_serves_hit[first_serves_hit['Shot Direction'] == 'body']
first_serves_wide = first_serves_hit[first_serves_hit['Shot Direction'] == 'wide']

serve_directions.at['1st Serve', 'Hit'] = len(first_serves_hit)
serve_directions.at['1st Serve', 'In'] = to_percent(len(first_serves_in), len(first_serves_hit))
serve_directions.at['1st Serve', 'T (Deuce)'] = to_percent(len(first_serves_deuce_t), len(first_serves_hit_deuce))
serve_directions.at['1st Serve', 'Body (Deuce)'] = to_percent(len(first_serves_deuce_body), len(first_serves_hit_deuce))
serve_directions.at['1st Serve', 'Wide (Deuce)'] = to_percent(len(first_serves_deuce_wide), len(first_serves_hit_deuce))
serve_directions.at['1st Serve', 'T (Ad)'] = to_percent(len(first_serves_ad_t), len(first_serves_hit_ad))
serve_directions.at['1st Serve', 'Body (Ad)'] = to_percent(len(first_serves_ad_body), len(first_serves_hit_ad))
serve_directions.at['1st Serve', 'Wide (Ad)'] = to_percent(len(first_serves_ad_wide), len(first_serves_hit_ad))

# print('first serve percentage is:',first_serve_percentage)

# second serve

second_serves_hit = serve_df[serve_df['Shot Type'] == 'second serve']
second_serves_in = second_serves_hit[second_serves_hit['Location'] == 'in']

second_serves_hit_deuce = second_serves_hit[second_serves_hit['Side'] == 'Deuce']
second_serves_hit_ad = second_serves_hit[second_serves_hit['Side'] == 'Ad']

second_serves_deuce_t = second_serves_hit_deuce[second_serves_hit_deuce['Shot Direction'] == 't']
second_serves_deuce_body = second_serves_hit_deuce[second_serves_hit_deuce['Shot Direction'] == 'body']
second_serves_deuce_wide = second_serves_hit_deuce[second_serves_hit_deuce['Shot Direction'] == 'wide']

second_serves_ad_t = second_serves_hit_ad[second_serves_hit_ad['Shot Direction'] == 't']
second_serves_ad_body = second_serves_hit_ad[second_serves_hit_ad['Shot Direction'] == 'body']
second_serves_ad_wide = second_serves_hit_ad[second_serves_hit_ad['Shot Direction'] == 'wide']


serve_directions.at['2nd Serve', 'Hit'] = len(second_serves_hit)
serve_directions.at['2nd Serve', 'In'] = to_percent(len(second_serves_in), len(second_serves_hit))
serve_directions.at['2nd Serve', 'T (Deuce)'] = to_percent(len(second_serves_deuce_t), len(second_serves_hit_deuce))
serve_directions.at['2nd Serve', 'Body (Deuce)'] = to_percent(len(second_serves_deuce_body), len(second_serves_hit_deuce))
serve_directions.at['2nd Serve', 'Wide (Deuce)'] = to_percent(len(second_serves_deuce_wide), len(second_serves_hit_deuce))
serve_directions.at['2nd Serve', 'T (Ad)'] = to_percent(len(second_serves_ad_t), len(second_serves_hit_ad))
serve_directions.at['2nd Serve', 'Body (Ad)'] = to_percent(len(second_serves_ad_body), len(second_serves_hit_ad))
serve_directions.at['2nd Serve', 'Wide (Ad)'] = to_percent(len(second_serves_ad_wide), len(second_serves_hit_ad))

server_scores = set(serve_df['Score'].to_list())
# print(server_scores)
for score in server_scores:
    server_score_df = serve_df[serve_df['Score'] == score]
    if score == '30-30':
        print(score)
        print(server_score_df)

# print('second serve percentage is:',second_serve_percentage)


# print(serve_directions)

shot_directions_headers = ['Hit', 'Cross', 'Middle', 'Line', 'Inside-out', 'Inside-in']
shot_directions_index = ['Forehands', 'Backhands', 'FH Slices', 'BH Slices', 'FH Volleys', 'BH Volleys']
shot_directions = pd.DataFrame(columns=shot_directions_headers, index=shot_directions_index)




# forehands

forehands_hit = player1_df[player1_df['Shot Type'] == 'forehand']
forehands_in = forehands_hit[forehands_hit['Location'] == 'in']
forehands_cross = forehands_hit[forehands_hit['Shot Direction'] == 'cross']
forehands_middle = forehands_hit[forehands_hit['Shot Direction'] == 'middle']
forehands_line = forehands_hit[forehands_hit['Shot Direction'] == 'line']
forehands_inside_out = forehands_hit[forehands_hit['Shot Direction'] == 'inside-out']
forehands_inside_in = forehands_hit[forehands_hit['Shot Direction'] == 'inside-in']
forehands_unforced_errors = forehands_hit[forehands_hit['Rally Ending'] == 'Unforced Error']
forehands_forced_errors = forehands_hit[forehands_hit['Rally Ending'] == 'Forced Error']
forehands_winners = forehands_hit[forehands_hit['Rally Ending'] == 'Winner']
forehands_wide = forehands_hit[forehands_hit['Location'] == 'wide']
forehands_deep = forehands_hit[forehands_hit['Location'] == 'deep']
forehands_net = forehands_hit[forehands_hit['Location'] == 'net']
# print('forehands hit:',len(forehands_hit))

shot_directions.at['Forehands', 'Hit'] = len(forehands_hit)
shot_directions.at['Forehands', 'Cross'] = to_percent(len(forehands_cross), len(forehands_hit))
shot_directions.at['Forehands', 'Middle'] = to_percent(len(forehands_middle), len(forehands_hit))
shot_directions.at['Forehands', 'Line'] = to_percent(len(forehands_line), len(forehands_hit))
shot_directions.at['Forehands', 'Inside-out'] = to_percent(len(forehands_inside_out), len(forehands_hit))
shot_directions.at['Forehands', 'Inside-in'] = to_percent(len(forehands_inside_in), len(forehands_hit))


# backhands

backhands_hit = player1_df[player1_df['Shot Type'] == 'backhand']
backhands_in = backhands_hit[backhands_hit['Location'] == 'in']
backhands_cross = backhands_hit[backhands_hit['Shot Direction'] == 'cross']
backhands_middle = backhands_hit[backhands_hit['Shot Direction'] == 'middle']
backhands_line = backhands_hit[backhands_hit['Shot Direction'] == 'line']
backhands_inside_out = backhands_hit[backhands_hit['Shot Direction'] == 'inside-out']
backhands_inside_in = backhands_hit[backhands_hit['Shot Direction'] == 'inside-in']
backhands_unforced_errors = backhands_hit[backhands_hit['Rally Ending'] == 'Unforced Error']
backhands_forced_errors = backhands_hit[backhands_hit['Rally Ending'] == 'Forced Error']
backhands_winners = backhands_hit[backhands_hit['Rally Ending'] == 'Winner']
backhands_wide = backhands_hit[backhands_hit['Location'] == 'wide']
backhands_deep = backhands_hit[backhands_hit['Location'] == 'deep']
backhands_net = backhands_hit[backhands_hit['Location'] == 'net']

shot_directions.at['Backhands', 'Hit'] = len(backhands_hit)
shot_directions.at['Backhands', 'Cross'] = to_percent(len(backhands_cross), len(backhands_hit))
shot_directions.at['Backhands', 'Middle'] = to_percent(len(backhands_middle), len(backhands_hit))
shot_directions.at['Backhands', 'Line'] = to_percent(len(backhands_line), len(backhands_hit))
shot_directions.at['Backhands', 'Inside-out'] = to_percent(len(backhands_inside_out), len(backhands_hit))
shot_directions.at['Backhands', 'Inside-in'] = to_percent(len(backhands_inside_in), len(backhands_hit))

# print('backhands hit:', len(backhands_hit))

# fh slices

fh_slices_hit = player1_df[player1_df['Shot Type'] == 'fh slice']
fh_slices_in = fh_slices_hit[fh_slices_hit['Location'] == 'in']
fh_slices_cross = fh_slices_hit[fh_slices_hit['Shot Direction'] == 'cross']
fh_slices_middle = fh_slices_hit[fh_slices_hit['Shot Direction'] == 'middle']
fh_slices_line = fh_slices_hit[fh_slices_hit['Shot Direction'] == 'line']
fh_slices_inside_out = fh_slices_hit[fh_slices_hit['Shot Direction'] == 'inside-out']
fh_slices_inside_in = fh_slices_hit[fh_slices_hit['Shot Direction'] == 'inside-in']
fh_slices_unforced_errors = fh_slices_hit[fh_slices_hit['Rally Ending'] == 'Unforced Error']
fh_slices_forced_errors = fh_slices_hit[fh_slices_hit['Rally Ending'] == 'Forced Error']
fh_slices_winners = fh_slices_hit[fh_slices_hit['Rally Ending'] == 'Winner']
fh_slices_wide = fh_slices_hit[fh_slices_hit['Location'] == 'wide']
fh_slices_deep = fh_slices_hit[fh_slices_hit['Location'] == 'deep']
fh_slices_net = fh_slices_hit[fh_slices_hit['Location'] == 'net']

shot_directions.at['FH Slices', 'Hit'] = len(fh_slices_hit)
shot_directions.at['FH Slices', 'Cross'] = to_percent(len(fh_slices_cross), len(fh_slices_hit))
shot_directions.at['FH Slices', 'Middle'] = to_percent(len(fh_slices_middle), len(fh_slices_hit))
shot_directions.at['FH Slices', 'Line'] = to_percent(len(fh_slices_line), len(fh_slices_hit))
shot_directions.at['FH Slices', 'Inside-out'] = to_percent(len(fh_slices_inside_out), len(fh_slices_hit))
shot_directions.at['FH Slices', 'Inside-in'] = to_percent(len(fh_slices_inside_in), len(fh_slices_hit))



# print('fh slices hit:', len(fh_slices_hit))

# bh slices

bh_slices_hit = player1_df[player1_df['Shot Type'] == 'bh slice']
bh_slices_in = bh_slices_hit[bh_slices_hit['Location'] == 'in']
bh_slices_cross = bh_slices_hit[bh_slices_hit['Shot Direction'] == 'cross']
bh_slices_middle = bh_slices_hit[bh_slices_hit['Shot Direction'] == 'middle']
bh_slices_line = bh_slices_hit[bh_slices_hit['Shot Direction'] == 'line']
bh_slices_inside_out = bh_slices_hit[bh_slices_hit['Shot Direction'] == 'inside-out']
bh_slices_inside_in = bh_slices_hit[bh_slices_hit['Shot Direction'] == 'inside-in']
bh_slices_unforced_errors = bh_slices_hit[bh_slices_hit['Rally Ending'] == 'Unforced Error']
bh_slices_forced_errors = bh_slices_hit[bh_slices_hit['Rally Ending'] == 'Forced Error']
bh_slices_winners = bh_slices_hit[bh_slices_hit['Rally Ending'] == 'Winner']
bh_slices_wide = bh_slices_hit[bh_slices_hit['Location'] == 'wide']
bh_slices_deep = bh_slices_hit[bh_slices_hit['Location'] == 'deep']
bh_slices_net = bh_slices_hit[bh_slices_hit['Location'] == 'net']

shot_directions.at['BH Slices', 'Hit'] = len(bh_slices_hit)
shot_directions.at['BH Slices', 'Cross'] = to_percent(len(bh_slices_cross), len(bh_slices_hit))
shot_directions.at['BH Slices', 'Middle'] = to_percent(len(bh_slices_middle), len(bh_slices_hit))
shot_directions.at['BH Slices', 'Line'] = to_percent(len(bh_slices_line), len(bh_slices_hit))
shot_directions.at['BH Slices', 'Inside-out'] = to_percent(len(bh_slices_inside_out), len(bh_slices_hit))
shot_directions.at['BH Slices', 'Inside-in'] = to_percent(len(bh_slices_inside_in), len(bh_slices_hit))


# print('bh slices hit:', len(bh_slices_hit))

# fh volleys

fh_volleys_hit = player1_df[player1_df['Shot Type'] == 'fh volley']
fh_volleys_in = fh_volleys_hit[fh_volleys_hit['Location'] == 'in']
fh_volleys_cross = fh_volleys_hit[fh_volleys_hit['Shot Direction'] == 'cross']
fh_volleys_middle = fh_volleys_hit[fh_volleys_hit['Shot Direction'] == 'middle']
fh_volleys_line = fh_volleys_hit[fh_volleys_hit['Shot Direction'] == 'line']
fh_volleys_inside_out = fh_volleys_hit[fh_volleys_hit['Shot Direction'] == 'inside-out']
fh_volleys_inside_in = fh_volleys_hit[fh_volleys_hit['Shot Direction'] == 'inside-in']
fh_volleys_unforced_errors = fh_volleys_hit[fh_volleys_hit['Rally Ending'] == 'Unforced Error']
fh_volleys_forced_errors = fh_volleys_hit[fh_volleys_hit['Rally Ending'] == 'Forced Error']
fh_volleys_winners = fh_volleys_hit[fh_volleys_hit['Rally Ending'] == 'Winner']
fh_volleys_wide = fh_volleys_hit[fh_volleys_hit['Location'] == 'wide']
fh_volleys_deep = fh_volleys_hit[fh_volleys_hit['Location'] == 'deep']
fh_volleys_net = fh_volleys_hit[fh_volleys_hit['Location'] == 'net']

shot_directions.at['FH Volleys', 'Hit'] = len(fh_volleys_hit)
shot_directions.at['FH Volleys', 'Cross'] = to_percent(len(fh_volleys_cross), len(fh_volleys_hit))
shot_directions.at['FH Volleys', 'Middle'] = to_percent(len(fh_volleys_middle), len(fh_volleys_hit))
shot_directions.at['FH Volleys', 'Line'] = to_percent(len(fh_volleys_line), len(fh_volleys_hit))
shot_directions.at['FH Volleys', 'Inside-out'] = to_percent(len(fh_volleys_inside_out), len(fh_volleys_hit))
shot_directions.at['FH Volleys', 'Inside-in'] = to_percent(len(fh_volleys_inside_in), len(fh_volleys_hit))


# bh volleys

bh_volleys_hit = player1_df[player1_df['Shot Type'] == 'bh volley']
bh_volleys_in = bh_volleys_hit[bh_volleys_hit['Location'] == 'in']
bh_volleys_cross = bh_volleys_hit[bh_volleys_hit['Shot Direction'] == 'cross']
bh_volleys_middle = bh_volleys_hit[bh_volleys_hit['Shot Direction'] == 'middle']
bh_volleys_line = bh_volleys_hit[bh_volleys_hit['Shot Direction'] == 'line']
bh_volleys_inside_out = bh_volleys_hit[bh_volleys_hit['Shot Direction'] == 'inside-out']
bh_volleys_inside_in = bh_volleys_hit[bh_volleys_hit['Shot Direction'] == 'inside-in']
bh_volleys_unforced_errors = bh_volleys_hit[bh_volleys_hit['Rally Ending'] == 'Unforced Error']
bh_volleys_forced_errors = bh_volleys_hit[bh_volleys_hit['Rally Ending'] == 'Forced Error']
bh_volleys_winners = bh_volleys_hit[bh_volleys_hit['Rally Ending'] == 'Winner']
bh_volleys_wide = bh_volleys_hit[bh_volleys_hit['Location'] == 'wide']
bh_volleys_deep = bh_volleys_hit[bh_volleys_hit['Location'] == 'deep']
bh_volleys_net = bh_volleys_hit[bh_volleys_hit['Location'] == 'net']

shot_directions.at['BH Volleys', 'Hit'] = len(bh_volleys_hit)
shot_directions.at['BH Volleys', 'Cross'] = to_percent(len(bh_volleys_cross), len(bh_volleys_hit))
shot_directions.at['BH Volleys', 'Middle'] = to_percent(len(bh_volleys_middle), len(bh_volleys_hit))
shot_directions.at['BH Volleys', 'Line'] = to_percent(len(bh_volleys_line), len(bh_volleys_hit))
shot_directions.at['BH Volleys', 'Inside-out'] = to_percent(len(bh_volleys_inside_out), len(bh_volleys_hit))
shot_directions.at['BH Volleys', 'Inside-in'] = to_percent(len(bh_volleys_inside_in), len(bh_volleys_hit))


# overheads

overheads_hit = player1_df[player1_df['Shot Type'] == 'overhead']
overheads_in = overheads_hit[overheads_hit['Location'] == 'in']
overheads_cross = overheads_hit[overheads_hit['Shot Direction'] == 'cross']
overheads_middle = overheads_hit[overheads_hit['Shot Direction'] == 'middle']
overheads_line = overheads_hit[overheads_hit['Shot Direction'] == 'line']
overheads_inside_out = overheads_hit[overheads_hit['Shot Direction'] == 'inside-out']
overheads_inside_in = overheads_hit[overheads_hit['Shot Direction'] == 'inside-in']
overheads_unforced_errors = overheads_hit[overheads_hit['Rally Ending'] == 'Unforced Error']
overheads_forced_errors = overheads_hit[overheads_hit['Rally Ending'] == 'Forced Error']
overheads_winners = overheads_hit[overheads_hit['Rally Ending'] == 'Winner']
overheads_wide = overheads_hit[overheads_hit['Location'] == 'wide']
overheads_deep = overheads_hit[overheads_hit['Location'] == 'deep']
overheads_net = overheads_hit[overheads_hit['Location'] == 'net']

shot_directions.at['Overheads', 'Hit'] = len(overheads_hit)
shot_directions.at['Overheads', 'Cross'] = to_percent(len(overheads_cross), len(overheads_hit))
shot_directions.at['Overheads', 'Middle'] = to_percent(len(overheads_middle), len(overheads_hit))
shot_directions.at['Overheads', 'Line'] = to_percent(len(overheads_line), len(overheads_hit))
shot_directions.at['Overheads', 'Inside-out'] = to_percent(len(overheads_inside_out), len(overheads_hit))
shot_directions.at['Overheads', 'Inside-in'] = to_percent(len(overheads_inside_in), len(overheads_hit))


# print(shot_directions)