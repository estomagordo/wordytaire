from collections import Counter

from wordytaire import validate_and_score


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
