#!/usr/bin/env python
# -*- coding: utf-8 -*-

inf = 100
similar_chars = {
    u"e:ę", u"u:ó", u"o:ó", u"a:ą", u"l:ł", u"z:ż", u"z:ź", u"ż:ź", u"c:ć", u"n:ń",
    u"sz:rz", u"ż:rz", u"h:ch", u"ą:on", u"ę:en"}


def char_distance(a, b):
    if a == b:
        return 0
    if len(a) == 2 and len(b) == 2 and a[0] == b[1] and b[0] == a[1]:
        return 0.5
    if (a + u":" + b in similar_chars) or (b + u":" + a in similar_chars):
        return 0.5
    if len(a) == 1 and len(b) == 1:
        return 1
    return 2


def lev(word1, word2):
    if min(len(word1), len(word2)) == 0:
        return max(len(word1), len(word2))
    row = ([range(len(word1)+1), [0] * (len(word1)+1), [0] * (len(word1)+1)])
    for i in range(1, len(word2)+1):
        i0 = i % 3
        i1 = (i-1) % 3
        i2 = (i-2) % 3
        row[i0][0] = i
        for j in range(1, len(word1)+1):
            j0 = j
            j1 = j-1
            j2 = j-2
            row[i0][j0] = min(
                row[i0][j1] + 1,
                row[i1][j0] + 1,
                row[i1][j1] + char_distance(word1[j-1], word2[i-1]),
                (row[i1][j2] + char_distance(word1[j-2:j],  word2[i-1])) if j in range(2, len(word1)+1) else inf,
                (row[i2][j1] + char_distance(word1[j-1],  word2[i-2:i])) if i in range(2, len(word2)+1) else inf,
                (row[i2][j2] + char_distance(word1[j-2:j],  word2[i-2:i])) if (i in range(2, len(word2)+1)) and (j in range(2, len(word1)+1)) else inf
                )
    return row[len(word2) % 3][-1]