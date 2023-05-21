# pylint: disable-all

import pandas as pd
import pytest
from chart_parser import parse_point, parse_shots, score_side, shot_dictionary, shots_list

def test_parse_points():
    mock_point1 = '8k2j4j3k2j4j2n#'
    mock_point2 = '6n!'
    

    assert parse_point(mock_point1, shots_list) == ['8', 'k2', 'j4', 'j3', 'k2', 'j4', 'j2n#']
    assert parse_point(mock_point2, shots_list) == ['6n!']
    

    with pytest.raises(TypeError) as excinfo:
        parse_point(2, shots_list)
    assert str(excinfo.value) == 'point must be a string'

    with pytest.raises(TypeError) as excinfo:
        parse_point([], shots_list)
    assert str(excinfo.value) == 'point must be a string'

    with pytest.raises(TypeError) as excinfo:
        parse_point(mock_point1, 2)
    assert str(excinfo.value) == 'shots_list must be a list'

    with pytest.raises(TypeError) as excinfo:
        parse_point(mock_point1, 'list')
    assert str(excinfo.value) == 'shots_list must be a list'

    with pytest.raises(TypeError) as excinfo:
        parse_point(mock_point1, ['', 2])
    assert str(excinfo.value) == 'Each shot in shots_list must be a string'

    with pytest.raises(ValueError) as excinfo:
        parse_point('', shots_list)
    assert str(excinfo.value) == "point can't be empty"

    with pytest.raises(ValueError) as excinfo:
        parse_point('a', shots_list)
    assert str(excinfo.value) == 'First character in point must be a serve direction'

def test_parse_shots():
    mock_shots1 = ['8', 'k2', 'j4#']
    mock_shots2 = ['7n!']
    players = ['Sam', 'Roger']
    server = 'Sam'
    score = '15-15'

    expected_headers = ['Shot Type', 'Shot Direction', 'Rally Ending', 'Location', 'Return', 'Player', 'Score']
    expected_df = pd.DataFrame(columns=expected_headers)
    expected_df.at[0, 'Shot Type'] = 'first serve'
    expected_df.at[0, 'Shot Direction'] = 'wide'
    expected_df.at[0, 'Rally Ending'] = 'in'
    expected_df.at[0, 'Location'] = 'in'
    expected_df.at[0, 'Return'] = False
    expected_df.at[0, 'Player'] = 'Sam'
    expected_df.at[0, 'Score'] = '15-15'
    expected_df.at[0, 'Side'] = 'Deuce'
    expected_df.at[1, 'Shot Type'] = 'backhand'
    expected_df.at[1, 'Shot Direction'] = 'middle'
    expected_df.at[1, 'Rally Ending'] = 'in'
    expected_df.at[1, 'Location'] = 'in'
    expected_df.at[1, 'Return'] = True
    expected_df.at[1, 'Player'] = 'Roger'
    expected_df.at[1, 'Score'] = ''
    expected_df.at[1, 'Side'] = ''
    expected_df.at[2, 'Shot Type'] = 'forehand'
    expected_df.at[2, 'Shot Direction'] = 'inside-out'
    expected_df.at[2, 'Rally Ending'] = 'Forced Error'
    expected_df.at[2, 'Location'] = 'in'
    expected_df.at[2, 'Return'] = False
    expected_df.at[2, 'Player'] = 'Sam'
    expected_df.at[2, 'Score'] = ''
    expected_df.at[2, 'Side'] = ''



    df = parse_shots(mock_shots1, shot_dictionary, 'first', players, server, score)
    
    assert isinstance(df, pd.DataFrame)
    assert df.equals(expected_df)

    expected_df1 = pd.DataFrame(columns=expected_headers)
    expected_df1.at[0, 'Shot Type'] = 'second serve'
    expected_df1.at[0, 'Shot Direction'] = 'body'
    expected_df1.at[0, 'Rally Ending'] = 'Fault'
    expected_df1.at[0, 'Location'] = 'net'
    expected_df1.at[0, 'Return'] = False
    expected_df1.at[0, 'Player'] = 'Sam'
    expected_df1.at[0, 'Score'] = '15-15'
    expected_df1.at[0, 'Side'] = 'Deuce'

    df1 = parse_shots(mock_shots2, shot_dictionary, 'second', players, server, score)
    

    assert isinstance(df1, pd.DataFrame)
    assert df1.equals(expected_df1)


    with pytest.raises(TypeError) as excinfo:
        assert parse_shots(2, shot_dictionary, 'first', players, server, score)
    assert str(excinfo.value) == 'shots must be a list'

    with pytest.raises(ValueError) as excinfo:
        assert parse_shots([], shot_dictionary, 'first', players, server, score)
    assert str(excinfo.value) == "shots can't be empty"

    with pytest.raises(TypeError) as excinfo:
        assert parse_shots(mock_shots1, '', 'first', players, server, score)
    assert str(excinfo.value) == 'shot_options must be a dict'

    with pytest.raises(TypeError) as excinfo:
        assert parse_shots(mock_shots1, '', 'first', players, server, score)
    assert str(excinfo.value) == 'shot_options must be a dict'

    with pytest.raises(TypeError) as excinfo:
        assert parse_shots(mock_shots1, shot_dictionary, 2, players, server, score)
    assert str(excinfo.value) == 'first_or_second must be a string'

    with pytest.raises(TypeError) as excinfo:
        assert parse_shots(mock_shots1, shot_dictionary, 'first', 2, server, score)
    assert str(excinfo.value) == 'players must be a list'

    with pytest.raises(ValueError) as excinfo:
        assert parse_shots(mock_shots1, shot_dictionary, 'first', ['Sam'], server, score)
    assert str(excinfo.value) == 'players must contain exactly 2 elements'

    with pytest.raises(TypeError) as excinfo:
        assert parse_shots(mock_shots1, shot_dictionary, 'first', players, 2, score)
    assert str(excinfo.value) == 'server must be a string'
    
    with pytest.raises(ValueError) as excinfo:
        assert parse_shots(mock_shots1, shot_dictionary, 'first', players, 'Bob', score)
    assert str(excinfo.value) == 'server must be one of the players'

    with pytest.raises(TypeError) as excinfo:
        assert parse_shots(mock_shots1, shot_dictionary, 'first', players, server, 2)
    assert str(excinfo.value) == 'score must be a string'

    with pytest.raises(KeyError) as excinfo:
        assert parse_shots(mock_shots1, {'z': 0}, 'first', players, server, score)
    assert str(excinfo.value) == "'char not in shot_dict'"

test_parse_shots()

def test_score_side():

    assert score_side('0-0') == 'Deuce'
    assert score_side('15-15') == 'Deuce'
    assert score_side('30-30') == 'Deuce'
    assert score_side('30-0') == 'Deuce'
    assert score_side('0-30') == 'Deuce'

    assert score_side('15-0') == 'Ad'
    assert score_side('40-0') == 'Ad'
    assert score_side('0-15') == 'Ad'
    assert score_side('0-40') == 'Ad'

    assert score_side('Deuce (Deuce Side)') == 'Deuce'
    assert score_side('Deuce (Ad Side)') == 'Ad'

    # diagnose Sam_Feldman test_depression();
    # prescribe Sam_Feldman fluoxetine();

