from pyspark import SparkConf, SparkContext
import string
import time

conf = SparkConf().setAppName('CardiovascularDisease')

sc = SparkContext(conf = conf)

cardRDD = sc.textFile("IHME_USA_COUNTY_CVD_MORTALITY_RATES_1980_2014_NATIONAL_Y2017M05D16.txt")


remRecs1 = (time.time())
# 'Location,FIPS,"Mortality Rate, 1980*","Mortality Rate, 1985*","Mortality Rate, 1990*","Mortality Rate, 1995*","Mortality Rate, 2000*","Mortality Rate, 2005*","Mortality Rate, 2010*","Mortality Rate, 2014*","% Change in Mortality Rate, 1980-2014"'
cardRDDHead = cardRDD.first()

cleanRDD = cardRDD.filter(lambda x: x!= cardRDDHead).map(lambda x: x.split('\t')).filter(lambda x: x[0][0] != '')


# count = 3142
counties = cleanRDD.filter(lambda x: (len(x[1]) > 2))
remRecs2 = (time.time())

totRemRecs = remRecs2-remRecs1
print('Time for removing records: ' + str(totRemRecs))




map1 = time.time()
# FIPS \s NUMERICAL_DATA
year1980 = counties.map(lambda x: str(x[2].split(' ')[0].replace('"', '') +' '+x[1]))
year1985 = counties.map(lambda x: str(x[3].split(' ')[0].replace('"', '') +' '+x[1]))
year1990 = counties.map(lambda x: str(x[4].split(' ')[0].replace('"', '') +' '+x[1]))
year1995 = counties.map(lambda x: str(x[5].split(' ')[0].replace('"', '') +' '+x[1]))
year2000 = counties.map(lambda x: str(x[6].split(' ')[0].replace('"', '') +' '+x[1]))
year2005 = counties.map(lambda x: str(x[7].split(' ')[0].replace('"', '') +' '+x[1]))
year2010 = counties.map(lambda x: str(x[8].split(' ')[0].replace('"', '') +' '+x[1]))
year2014 = counties.map(lambda x: str(x[9].split(' ')[0].replace('"', '') +' '+x[1]))
map2 = time.time()
totMap = map2-map1
print('Time for mapping: ' + str(totMap))



textF1 = time.time()
year1980.saveAsTextFile('data_1980.txt')
year1985.saveAsTextFile('data_1985.txt')
year1990.saveAsTextFile('data_1990.txt')
year1995.saveAsTextFile('data_1995.txt')
year2000.saveAsTextFile('data_2000.txt')
year2005.saveAsTextFile('data_2005.txt')
year2010.saveAsTextFile('data_2010.txt')
year2014.saveAsTextFile('data_2014.txt')


textF2 = time.time()
totTextF = textF2-textF1
print('Time for writing files: ' + str(totTextF))
