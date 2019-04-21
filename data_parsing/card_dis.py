from pyspark import SparkConf, SparkContext
import string

conf = SparkConf().setMaster('local').setAppName('CardiDisease')

sc = SparkContext(conf = conf)

cardRDD = sc.textFile("cardiovascular_disease.txt")

# 'Location,FIPS,"Mortality Rate, 1980*","Mortality Rate, 1985*","Mortality Rate, 1990*","Mortality Rate, 1995*","Mortality Rate, 2000*","Mortality Rate, 2005*","Mortality Rate, 2010*","Mortality Rate, 2014*","% Change in Mortality Rate, 1980-2014"'
cardRDDHead = cardRDD.first()

cleanRDD = cardRDD.filter(lambda x: x!= cardRDDHead).map(lambda x: x.split('\t')).filter(lambda x: x[0][0] != '')


# count = 3142
counties = cleanRDD.filter(lambda x: (len(x[1]) > 2))

# FIPS \s NUMERICAL_DATA
year1980 = counties.map(lambda x: str(x[2].split(' ')[0].replace('"', '') +' '+x[1]))
year1985 = counties.map(lambda x: str(x[3].split(' ')[0].replace('"', '') +' '+x[1]))
year1990 = counties.map(lambda x: str(x[4].split(' ')[0].replace('"', '') +' '+x[1]))
year1995 = counties.map(lambda x: str(x[5].split(' ')[0].replace('"', '') +' '+x[1]))
year2000 = counties.map(lambda x: str(x[6].split(' ')[0].replace('"', '') +' '+x[1]))
year2005 = counties.map(lambda x: str(x[7].split(' ')[0].replace('"', '') +' '+x[1]))
year2010 = counties.map(lambda x: str(x[8].split(' ')[0].replace('"', '') +' '+x[1]))
year2014 = counties.map(lambda x: str(x[9].split(' ')[0].replace('"', '') +' '+x[1]))



year1980.saveAsTextFile('year1980.txt')
year1985.saveAsTextFile('year1985.txt')
year1990.saveAsTextFile('year1990.txt')
year1995.saveAsTextFile('year1995.txt')
year2000.saveAsTextFile('year2000.txt')
year2005.saveAsTextFile('year2005.txt')
year2010.saveAsTextFile('year2010.txt')
year2014.saveAsTextFile('year2014.txt')
