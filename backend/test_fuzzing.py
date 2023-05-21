# pylint: disable-all
from hypothesis import given, settings, strategies as st
from chart_parser import parse_point, parse_shots
import pandas as pd

# Define a strategy for generating valid points

random_number_strategy = st.integers(min_value=6, max_value=8).map(str)
random_string_strategy = st.text(
    alphabet=st.characters(blacklist_categories=('Cs', 'Co', 'Cc'),),
    min_size=4,
    max_size=12
)
shots_list_strategy = st.lists(st.text(min_size=1, max_size=1), min_size=2, max_size=12)


# Define the Hypothesis test
@settings(max_examples=100)
@given(first_char=random_number_strategy, r_point=random_string_strategy, shots_list=shots_list_strategy)
def test_parse_point(first_char, r_point, shots_list):
    # Call the function being tested

    point = first_char + r_point

    print(f"Generated point: {point}")
    print(f"Generated shots_list: {shots_list}")
    result = parse_point(point, shots_list)
    
    # Assertions
    assert isinstance(result, list)
    # Check if the substrings are correctly extracted
    assert ''.join(result) == point
    # Check if the result contains only substrings extracted from point
    for substring in result:
        assert substring in point



shots_strategy = st.lists(st.text(min_size=2, max_size=4), min_size=2, max_size=12)

shot_options_strategy = st.dictionaries(keys=st.text(min_size=1, max_size=1), values=st.lists(st.text(min_size=1, max_size=8),min_size=2, max_size=2))

@settings(max_examples=100)
@given(shots=shots_strategy)
def test_parse_shots(shots):
    
    players = ['Sam', 'Roger']
    server = 'Sam'
    score = '15-15'

    dict = {}

    for shot in shots:
        for char in shot:
            if char not in dict:
                dict[char] = ['abc', 'def']

    print(shots)

    result = parse_shots(shots, dict, 'first', players, server, score)

    assert isinstance(result, pd.DataFrame)

test_parse_shots()