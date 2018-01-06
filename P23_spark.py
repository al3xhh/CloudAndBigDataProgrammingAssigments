#!/usr/bin/python

import sys
from pyspark import SparkContext

sc = SparkContext()
stockRDD = sc.textFile('../Data/P13_data.csv')
stockRDD = stockRDD.map(lambda stock: stock.split(","))
stockRDD = stockRDD.map(lambda stock: (stock[0].split("-")[0], float(stock[2]) - float(stock[1])))
stockRDD = stockRDD.groupByKey()
stockRDD = stockRDD.map(lambda stock: (stock[0], float(sum(list(stock[1]))) / len(stock[1])))
stockRDD = stockRDD.sortByKey()
firstTen = stockRDD.take(10)
print firstTen
