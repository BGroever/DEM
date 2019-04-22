from pyspark import SparkConf, SparkContext
import string
import re

conf = SparkConf().setMaster('local').setAppName('CtyMaking')

sc = SparkContext(conf = conf)

stateRDD = sc.textFile("FIPS_COUNTY.txt")

stateRDD = stateRDD.filter(lambda x: len(x.split())==2 or len(x.split())==3)

print(stateRDD.take(4))


countyRDD = sc.textFile("FIPS_COUNTY_NOSTATE.txt")

ctyRDD = countyRDD.map(lambda x: re.findall(r"^[\w\s]+(?=County)", x)[0].replace(" ","_")+"__"+re.findall(r"\w[\w\s]+(?=\s\d+)", x)[0].replace(" ","_"))

print(ctyRDD.take(6))

