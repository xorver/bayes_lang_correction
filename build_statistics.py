#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, collections
import multiprocessing
import pickle
from lev import lev


def get_stat(filename):
    with open(filename) as file:
        # all_words = re.findall('\w+', file.read().lower(), flags=re.UNICODE)
        all_words = file.read().lower().split()
        all_words = map(lambda x: unicode(x, "utf-8"), all_words)
        return collections.Counter(all_words)


def distance(args):
    [a, b] = args
    return lev.lev(a, b[:-1])


# prepare thread pool
pool = multiprocessing.Pool()

# prepare sample files
samples = []
for dirname, dirnames, filenames in os.walk('data/samples'):
    if filenames:
        samples = [os.path.join(dirname, filename) for filename in filenames]

# prepare error stats
with open("data/bledy.txt") as file:
    errors = map(lambda line: unicode(line, "utf-8").lower().split(";"), file.readlines())
error_freq = collections.Counter(map(distance, errors))


# compute stats for sample files
stat_list = pool.map(get_stat, samples)
stats = collections.Counter()
stats = reduce(lambda x, y: x+y, stat_list, stats)

# dump stats
pickle.dump(stats.items(), open("data/statistics", "wb"))
pickle.dump(error_freq.items(), open("data/error_freq", "wb"))