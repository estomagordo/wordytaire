from collections import Counter
from functools import reduce

import re

letvals = {
    'a': 1,
    'b': 5,
    'c': 4,
    'd': 4,
    'e': 1,
    'f': 6,
    'g': 5,
    'h': 5,
    'i': 1,
    'j': 9,
    'k': 7,
    'l': 3,
    'm': 4,
    'n': 2,
    'o': 2,
    'p': 4,
    'q': 9,
    'r': 2,
    's': 2,
    't': 2,
    'u': 4,
    'v': 6,
    'w': 7,
    'x': 8,
    'y': 5,
    'z': 8
    }
class Wordytaire:
    def __init__(self, dictionary=None):
        if dictionary:
            self.dictionary = dictionary
        else:
            self.dictionary = set()
            
            with open('words_alpha.txt') as f:
                for line in f.readlines():
                    self.dictionary.add(line.rstrip())

    def tile_value(self, tile):
        x, y = tile
        dx, dy = abs(x)%5, abs(y)%5

        if abs(dy) == abs(dx) and dx%2:
            if dx in (1, 4):
                return (1, 2)
            return (1, 3)

        if abs(dy-dx) in (2,3) and dx > dy and not dx%2:
            return (abs(dy-dx), 1)

        return (1, 1)

    def get_connected_words(self, used, placement, x1, y1, x2, y2):
        connected_words = []
        
        if x2 > x1:
            if (x1-1, y1) in used or (x2+1, y1) in used:
                extended_start = x1
                extended_end = x2
                
                while (extended_start-1, y1) in used:
                    extended_start -= 1

                while (extended_end+1, y1) in used:
                    extended_end += 1

                extended = []

                for x in range(extended_start, extended_end+1):
                    if (x, y1) in placement:
                        extended.append([(x, y1), placement[(x, y1)]])
                    else:
                        extended.append([(x, y1), used[(x, y1)]])

                connected_words.append(extended)

            for x in range(x1, x2+1):
                if (x, y1-1) in used or (x, y1+1) in used:
                    vertical_start = y1
                    vertical_end = y1
                    
                    while (x, vertical_start-1) in used:
                        vertical_start -= 1

                    while (x, vertical_end+1) in used:
                        vertical_end += 1

                    vertical = []

                    for y in range(vertical_start, vertical_end+1):
                        if (x, y) in placement:
                            vertical.append([(x, y), placement[(x, y)]])
                        else:
                            vertical.append([(x, y), used[(x, y)]])

                    connected_words.append(vertical)
        else:
            if (x1, y1-1) in used or (x1, y2+1) in used:
                extended_start = y1
                extended_end = y2
                
                while (x1, extended_start-1) in used:
                    extended_start -= 1

                while (x1, extended_end+1) in used:
                    extended_end += 1

                extended = []

                for y in range(extended_start, extended_end+1):
                    if (x1, y) in placement:
                        extended.append([(x1, y), placement[(x1, y)]])
                    else:
                        extended.append([(x1, y), used[(x1, y)]])

                connected_words.append(extended)

            for y in range(y1, y2+1):
                if (x1-1, y) in used or (x1+1, y) in used:
                    horizontal_start = x1
                    horizontal_end = x1
                    
                    while (horizontal_start-1, y) in used:
                        horizontal_start -= 1

                    while (horizontal_end+1, y) in used:
                        horizontal_end += 1

                    horizontal = []

                    for x in range(horizontal_start, horizontal_end+1):
                        if (x, y) in placement:
                            horizontal.append([(x, y), placement[(x, y)]])
                        else:
                            horizontal.append([(x, y), used[(x, y)]])

                    connected_words.append(horizontal)

        return connected_words

    def score_placement(self, placement):
        tilevals = sum(letvals[v] * self.tile_value(k)[0] for k,v in placement.items())
        multi = reduce(lambda a,b: a*b, [self.tile_value(k)[1] for k in placement.keys()])

        return tilevals * multi

    def score_connected_word(self, placement, word):
        tilevals = sum([letvals[c[1]] * (self.tile_value(c[0])[0] if c[0] in placement else 1) for c in word])
        multi = reduce(lambda a,b: a*b, [self.tile_value(c[0])[1] if c[0] in placement else 1 for c in word])

        return tilevals * multi        

    def score_move(self, placement, connected_words, extension):
        return (0 if extension else self.score_placement(placement)) + sum(self.score_connected_word(placement, word) for word in connected_words)

    def validate_and_score(self, used, letters, parts):
        if len(parts) != 5:
            return (f'Error', -1, {})

        if not all(re.search('^-?\\d+$', part) for part in parts[:4]):
            return (f'Error', -2, {})

        if not all(c in 'abcdefghijklmnopqrstuvwxyz' for c in parts[4]):
            return (f'Error', -3, {})

        x1, y1, x2, y2 = map(int, parts[:4])
        word = parts[4]
        n = len(word)
        
        if not ((x2 > x1 and y2 == y1) or (x2 == x1 and y2 > y1)):
            return (f'Error', -4, {})

        if not (x2-x1 == n-1 or y2-y1 == n-1):
            return (f'Error', -5, {})

        wordletters = Counter(word)

        if wordletters - letters:
            return (f'Error', -6, {})
        
        placement = {(x1+i, y1) : word[i] for i in range(n)} if x1 != x2 else {(x1, y1+i): word[i] for i in range(n)}

        if any((p[0], p[1]) in used for p in placement):
            return (f'Error', -7, {})

        connected_words = self.get_connected_words(used, placement, x1, y1, x2, y2)
        extension = connected_words and sum(c[0] in placement for c in connected_words[0]) == len(word)

        if word not in self.dictionary and not extension:
            return (f'Error', -8, {})

        if not used and not (0 in (x1, y1, x2, y2) or x1 < 0 < x2 or y1 < 0 < y2):
            return (f'Error', -9, {})

        for word in connected_words:
            if ''.join(c[1] for c in word) not in self.dictionary:
                return (f'Error', -10, {})

        move_score = self.score_move(placement, connected_words, extension)

        for k,v in placement.items():
            used[k] = v

        return ('', move_score, used)

    def score_submission(self, submission):
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

        for line in submission:
            parts = line.split()

            if not parts:
                continue

            message, valscore, used = self.validate_and_score(used, letters, parts)

            if valscore < 0:
                return (message, valscore)

            score += valscore

        return ('', score)