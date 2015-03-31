#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import multiprocessing
import pickle
import collections
from lev import lev

# load statistics
cout_list = pickle.load(open("data/statistics", "rb"))
count = collections.Counter(dict(cout_list))
N = sum(count.values())

# prepare forms
with open("data/formy_utf.txt") as file:
    forms = file.read().split()
for i in range(len(forms)):
    forms[i] = unicode(forms[i], "utf-8")
forms_set = set(forms)
M = len(forms)

# declare alphabet
alphabet = u'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź'


#
# word generation
#

def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def known_edits1(word):
    return known(edits1(word))


def edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in forms_set)


def known(words):
    return set(w for w in words if w in forms_set)


def candidates(word):
    return list(known([arg]) or known(edits1(arg)) or known_edits2(arg) or [word])

#
# probability
#

def P_w_c(args):
    (correct, word) = args
    (distance,) = lev.lev(correct, word),
    if distance == 0:
        return (1.0 + count[word]) / (sum(map(lambda x: count[x], [word])) + M) * 4
    if distance <= 1:
        return (1.0 + count[word]) / (sum(map(lambda x: count[x], [word] + list(known_edits1(correct)))) + M) * 1.0 / distance
    return (1.0 + count[word]) / (sum(map(lambda x: count[x], [word] + list(known_edits1(correct)) + list(known_edits2(correct)))) + M) * 1.0 / distance


def P_c(args):
    (correct, word) = args
    return (count[correct] + 1.0) / (N + M)


def P_c_w(args):
    return P_w_c(args) * P_c(args)


# Initialize thread pool
pool = multiprocessing.Pool()

# Parse args
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-w', '--word', action='store', dest='word')
[args, pass_args] = parser.parse_known_args()
arg = unicode(args.word, "utf-8")

# Create candidates and check probability
cand = candidates(arg)
probabilities = map(P_c_w, zip(cand, [arg] * len(cand)))
guesses = zip(probabilities, cand)
guesses.sort(key=lambda tup: tup[0])

# Print results
for (val, word) in reversed(guesses[-10:]):
    print(val)
    print(word)
    print('\n')
