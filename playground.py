from collections import Counter

letcount = Counter()

with open('words_alpha.txt') as f:
    for line in f.readlines():
        for c in line.rstrip():
            letcount[c] += 1

for x in range(ord('a'), ord('z')+1):
    c = chr(x)
    print(c, letcount[c])

"""
letter counts, ordered alphabetically

a 295792
b 63940
c 152981
d 113190
e 376454
f 39238
g 82627
h 92368
i 313008
j 5456
k 26814
l 194914
m 105208
n 251436
o 251596
p 113663
q 5883
r 246142
s 250284
t 230895
u 131496
v 33075
w 22407
x 10493
y 70580
z 14757
"""

print()
for pair in sorted(letcount.most_common(26), key=lambda pair: pair[1]):
    print(pair[0], pair[1], round(100.0 * pair[1] / sum(p[1] for p in letcount.most_common(26)), 2), 10000 * pair[1] / sum(p[1] for p in letcount.most_common(26)))

"""
letter counts, ordered by frequency, with percentages. With manually added letter scores and proposed frequencies.

j 5456 0.16     9   16
q 5883 0.17     9   17
x 10493 0.3     8   30
z 14757 0.42    8   42
w 22407 0.64    7   64
k 26814 0.77    7   77
v 33075 0.95    6   95
f 39238 1.12    6   112
b 63940 1.83    5   183
y 70580 2.02    5   202
g 82627 2.36    5   236
h 92368 2.64    5   264
m 105208 3.01   4   301
d 113190 3.24   4   324
p 113663 3.25   4   325
u 131496 3.76   4   376
c 152981 4.38   4   438
l 194914 5.58   3   558
t 230895 6.61   2   661
r 246142 7.04   2   704
s 250284 7.16   2   716
n 251436 7.19   2   719
o 251596 7.2    2   720
a 295792 8.46   1   846
i 313008 8.96   1   896
e 376454 10.77  1   1078
"""


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

for y in range(-15, 16):
    print(' '.join(symb(rules(x, y)) for x in range(-15, 16)))


def validate(used, letters, parts):
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

    placement = {(x1+i, y1) : word[i] for i in range(n)] if x1 != x2 else [(x1, y1+i, word[i]) for i in range(n)]}

    if any((p[0], p[1]) in used for p in placement):
        return (f'Error', -7, {})

    if not used and not (0 in (x1, y1, x2, y2) or x1 < 0 < x2 or y1 < 0 < y2):
        return (f'Error', -8, {})

    


def score_submission(submission):
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

        message, valscore, newused = validate(used, letters, parts)

        if valscore < 0:
            return message, valscore

        

