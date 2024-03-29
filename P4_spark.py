#!/usr/bin/python

import sys
from pyspark import SparkContext
from random import randint

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def count(word):
    wordsList = list(word[1])
    wordsList = sorted(wordsList)
    last = None
    count = 0
    ret = []

    for w in wordsList:
        if w != last:
            if last is not None:
                ret.append((last, count))
            last = w
            count = 0

        count = count + 1

    ret.append((last, count))
    return (word[0], ret)

def max(word):
    wordList = list(word[0][1])
    maxObject = None

    for w in wordList:
        if maxObject is None:
            maxObject = w
        elif w[1] > maxObject[1]:
            maxObject = w

    return word[0][0] + " " + maxObject[0]

sc = SparkContext()
shakespeareRDD = sc.textFile("../Data/P4_data.txt")
shakespeareRDD = shakespeareRDD.flatMap(lambda word: word.split(" "))
shakespeareRDD = shakespeareRDD.filter(lambda word: not word.isupper())
shakespeareRDD = shakespeareRDD.filter(lambda word: not is_number(word))
shakespeareRDD = shakespeareRDD.zipWithIndex()
shakespeareRDD1 = shakespeareRDD
shakespeareRDD = shakespeareRDD.map(lambda word: (word[1], word[0]))
shakespeareRDD1 = shakespeareRDD1.map(lambda word: (word[1] - 1, word[0]))
shakespeareRDD2 = shakespeareRDD.join(shakespeareRDD1)
shakespeareRDD2 = shakespeareRDD2.sortByKey()
shakespeareRDD3 = shakespeareRDD2
shakespeareRDD3 = shakespeareRDD3.map(lambda word: (word[0] - 1, word[1]))
shakespeareRDD4 = shakespeareRDD3.join(shakespeareRDD2)
shakespeareRDD4 = shakespeareRDD4.sortByKey()
shakespeareRDD4 = shakespeareRDD4.map(lambda word: (word[1][1][0] + " " + word[1][1][1], word[1][0][1]))
shakespeareRDD4 = shakespeareRDD4.groupByKey()
shakespeareRDD4 = shakespeareRDD4.map(count)

for i in range(0, 10):
    ret = ""

    for j in range(0, 20):
        ret += max(shakespeareRDD4.takeSample(True, 1))

    print ret
