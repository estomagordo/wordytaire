from collections import Counter

from wordytaire import score_move, score_submission, tile_value, validate_and_score


def test_one_part():
    s = 'blacksmith'
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-1 == score)


def test_two_parts():
    s = '5 blacksmith'
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-1 == score)

def test_three_parts():
    s = '5 1 blacksmith'
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-1 == score)


def test_four_parts():
    s = '4 2 5 blacksmith'
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-1 == score)


def test_six_parts():
    s = 'blacksmith 5 5 3 4 3'
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-1 == score)


def test_no_numbers():
    s = 'blacksmith one two thisisridiculous four'    
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())

    assert(-2 == score)


def test_float():
    s = '1 2 3.5 5 blacksmith'    
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-2 == score)



def test_lone_minus():
    s = '1 2 - 5 blacksmith'    
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-2 == score)


def test_upper():
    s = '0 0 0 0 abcDEF'  
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-3 == score)


def test_hyphen():
    s = '1 2 5 5 hack-eyed'   
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-3 == score)


def test_scandi():
    s = '82 5 28 1 smörgåsbord'  
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-3 == score)


def test_point():
    s = '1 1 1 1 sausage'  
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-4 == score)


def test_wrong_way():
    s = '1 1 1 -1 sausage'  
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-4 == score)


def test_diagonal():
    s = '1 1 3 3 sausage'  
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-4 == score)


def test_short_word():
    s = '1 1 1 3 up'  
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-5 == score)


def test_long_word():
    s = '1 1 1 3 upend'  
    _, score, _ = validate_and_score(set(), {}, Counter(), s.split())
    assert(-5 == score)


def test_missing_letters():
    s = '1 1 1 3 rub'
    letters = Counter('aaaaaaaaru') 
    _, score, _ = validate_and_score(set(), {}, letters, s.split())
    assert(-6 == score)


def test_overwriting():
    s = '1 1 1 3 rub'
    used = {(1, 1): 'z', (1, 2): 'y'}
    letters = Counter('burn')
    _, score, _ = validate_and_score(set(), used, letters, s.split())
    assert(-7 == score)


def test_unknown_word():
    s = '1 1 1 9 degaullic'
    dictionary = {'summer', 'pluto', 'aphrodisiac'}
    letters = Counter('degaullicandsuchwordsyouknow') 
    _, score, _ = validate_and_score(dictionary, {}, letters, s.split())
    assert(-8 == score)


def test_false_start():
    s = '1 1 1 3 rub'
    dictionary = {'rubber', 'rub'}
    letters = Counter('burn')
    _, score, _ = validate_and_score(dictionary, {}, letters, s.split())
    assert(-9 == score)


def test_make_illegal_words():
    s0 = '0 1 0 3 rub'
    s1 = '0 -3 0 -1 rub'
    s2 = '-5 0 -3 0 rub'
    s3 = '1 0 3 0 rub'
    
    dictionary = {'rubber', 'rub'}
    used = {(-2, 0): 'r', (-1, 0): 'u', (0, 0): 'b'}
    letters = Counter('burn')
    _, score0, _ = validate_and_score(dictionary, used, letters, s0.split())
    _, score1, _ = validate_and_score(dictionary, used, letters, s1.split())
    _, score2, _ = validate_and_score(dictionary, used, letters, s2.split())
    _, score3, _ = validate_and_score(dictionary, used, letters, s3.split())
    
    assert(-10 == score0)
    assert(-10 == score1)
    assert(-10 == score2)
    assert(-10 == score3)


def test_tile_value():
    center = (0, 0)
    five_col0 = (25, 0)
    five_col1 = (-120, 0)
    four_row0 = (7, 9)
    four_row1 = (7, -124)
    l2_0 = (7, 0)
    l2_1 = (-2, -5)
    l2_2 = (-4, -2)
    l3_0 = (34, 1)
    l3_1 = (-804, 1)
    w2_0 = (1, -1)
    w2_1 = (-1, -1)
    w2_2 = (1, -111)
    w3_0 = (3, 3)
    w3_1 = (-28, 33)

    center_val = tile_value(center)
    five_col0_val = tile_value(five_col0)
    five_col1_val = tile_value(five_col1)
    four_row0_val = tile_value(four_row0)
    four_row1_val = tile_value(four_row1)
    l2_0_val = tile_value(l2_0)
    l2_1_val = tile_value(l2_1)
    l2_2_val = tile_value(l2_2)
    l3_0_val = tile_value(l3_0)
    l3_1_val = tile_value(l3_1)
    w2_0_val = tile_value(w2_0)
    w2_1_val = tile_value(w2_1)
    w2_2_val = tile_value(w2_2)
    w3_0_val = tile_value(w3_0)
    w3_1_val = tile_value(w3_1)

    assert((1, 1) == center_val)
    assert((1, 1) == five_col0_val)
    assert((1, 1) == five_col1_val)
    assert((1, 1) == four_row0_val)
    assert((1, 1) == four_row1_val)
    assert((2, 1) == l2_0_val)
    assert((2, 1) == l2_1_val)
    assert((2, 1) == l2_2_val)
    assert((3, 1) == l3_0_val)
    assert((3, 1) == l3_1_val)
    assert((1, 2) == w2_0_val)
    assert((1, 2) == w2_1_val)
    assert((1, 2) == w2_2_val)
    assert((1, 3) == w3_0_val)
    assert((1, 3) == w3_1_val)


def test_score_openers():
    downward = '0 0 0 2 cat'
    rightward = '-1 0 1 0 cat'
    rightward_with_bonus = '0 0 2 0 cat'

    dictionary = {'cat'}
    letters = Counter('cat')

    _, downward_score, _ = validate_and_score(dictionary, {}, letters, downward.split())
    _, rightward_score, _ = validate_and_score(dictionary, {}, letters, rightward.split())
    _, rightward_with_bonus_score, _ = validate_and_score(dictionary, {}, letters, rightward_with_bonus.split())

    assert(7 == downward_score)
    assert(7 == rightward_score)
    assert(9 == rightward_with_bonus_score)


def test_score_submission():
    illegal_fifth_word = [
        '0 0 2 0 dog',
        '3 -3 3 1 house',
        '3 2 6 2 spun',
        '0 1 0 3 oge',
        '1 3 6 3 rudite',
        '4 -3 5 -3 ex'
    ]

    fifth_removed = [
        '0 0 2 0 dog',
        '3 -3 3 1 house',
        '3 2 6 2 spun',
        '0 1 0 3 oge',
        '4 -3 5 -3 ex'
    ]

    dictionary = {'dog', 'dogs', 'house', 'houses', 'spun', 'doge', 'erudite', 'hex'}

    # _, illegal_score = score_submission(dictionary, illegal_fifth_word)
    _, legal_score = score_submission(dictionary, fifth_removed)

    # assert(-10 == illegal_score)
    assert(129 == legal_score)