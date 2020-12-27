from collections import Counter


def rules(y, x):
    dy, dx = abs(y)%5, abs(x)%5

    if abs(dy) == abs(dx) and dy%2:
        if dy in (1, 4):
            return (1, 2)
        return (1, 3)

    if abs(dy-dx) in (2,3) and dy > dx and not dy%2:
        return (abs(dy-dx), 1)

    return (1, 1)


def symb(val):
    if val == (1, 3):
        return 'W3'
    if val == (1, 2):
        return 'W2'
    if val == (3, 1):
        return 'L3'
    if val == (2, 1):
        return 'L2'
    return '  '
    

def get_connected_words(used, placement):
    pass


def score_move(placement, connected_words):
    pass


def validate(dictionary, used, letters, parts):
    if len(parts) != 5:
        return (f'Error', -1, {})

    if not all(parts[x].isdigit() for x in range(4)):
        return (f'Error', -2, {})

    if not all(c in 'abcdefghijklmnopqrstuvwxyz' for c in parts[4]):
        return (f'Error', -3, {})

    x1, y1, x2, y2 = map(int, parts[:4])
    word = parts[4]
    n = len(word)
    
    if not (x2 > x1 and y2 == y1) or (x2 == x1 and y2 > y1):
        return (f'Error', -4, {})

    if not (x2-x1 == n-1 or y2-y1 == n-1):
        return (f'Error', -5, {})

    wordletters = Counter(word)

    if wordletters - letters:
        return (f'Error', -6, {})
    
    placement = {(x1+i, y1) : word[i] for i in range(n)} if x1 != x2 else {(x1, y1+i, word[i]) for i in range(n)}

    if any((p[0], p[1]) in used for p in placement):
        return (f'Error', -7, {})

    if word not in dictionary:
        return (f'Error', -8, {})

    if not used and not (0 in (x1, y1, x2, y2) or x1 < 0 < x2 or y1 < 0 < y2):
        return (f'Error', -9, {})

    connected_words = get_connected_words(used, placement)

    for word in connected_words:
        if ''.join(c for c in word[0]) not in dictionary:
            return (f'Error', -10, {})

    move_score = score_move(placement, connected_words)

    for k,v in placement.items():
        used[k] = v

    return ('', move_score, used)


def score_submission(dictionary, submission):
    used = {}
    letters = Counter()

    letters['a'] = 846
    letters['b'] = 183
    letters['c'] = 438
    letters['d'] = 324
    letters['e'] = 1078
    letters['f'] = 112
    letters['g'] = 236
    letters['h'] = 264
    letters['i'] = 896
    letters['j'] = 16
    letters['k'] = 77
    letters['l'] = 558
    letters['m'] = 301
    letters['n'] = 719
    letters['o'] = 720
    letters['p'] = 325
    letters['q'] = 17
    letters['r'] = 704
    letters['s'] = 716
    letters['t'] = 661
    letters['u'] = 376
    letters['v'] = 95
    letters['w'] = 64
    letters['x'] = 30
    letters['y'] = 202
    letters['z'] = 42

    score = 0

    for i, line in enumerate(submission):
        parts = line.split()

        if not parts:
            continue

        message, valscore, used = validate(dictionary, used, letters, parts)

        if valscore < 0:
            return (message, valscore)

        score += valscore

    return ('', score)