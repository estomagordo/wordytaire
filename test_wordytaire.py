from collections import Counter

from wordytaire import validate_and_score


def test_wrong_line_format():
    s0 = '5 1 blacksmith'
    s1 = '4 2 5 blacksmith'
    s2 = 'blacksmith 5 5 3 4 3'
    s3 = 'blacksmith'
    s4 = '9 5 2 8 1 blacksmith'
    
    _, score0, _ = validate_and_score({}, {}, Counter(), s0.split())
    _, score1, _ = validate_and_score({}, {}, Counter(), s1.split())
    _, score2, _ = validate_and_score({}, {}, Counter(), s2.split())
    _, score3, _ = validate_and_score({}, {}, Counter(), s3.split())
    _, score4, _ = validate_and_score({}, {}, Counter(), s4.split())

    assert(-1 == score0)
    assert(-1 == score1)
    assert(-1 == score2)
    assert(-1 == score3)
    assert(-1 == score4)


def test_first_not_numbers():
    s0 = 'blacksmith one two thisisridiculous four'
    s1 = '1 2 3.5 5 blacksmith'
    
    _, score0, _ = validate_and_score({}, {}, Counter(), s0.split())
    _, score1, _ = validate_and_score({}, {}, Counter(), s1.split())

    assert(-2 == score0)
    assert(-2 == score1)