from pyspark import SparkConf, SparkContext
import string
import time

conf = SparkConf().setAppName('OzoneConcentrations')

sc = SparkContext(conf = conf)


def avg(x):
    return sum(x)/len(x)

def isFloat(x):
    try:
        float(x)
        return float(x)
    except ValueError:
        return False


def yearMean(yrMean, x):
    if (x != ''):
        return x
    else:
        return yrMean

remRecs2 = (time.time())
allCounties = sc.textFile("CtyFIPS.txt")
allCounties = allCounties.map(lambda x: x.split(' \t')).map(lambda x: (str(int(x[1])), ''))


dAcounties = allCounties.map(lambda x: x[0])



remRecs1 = (time.time())
#'year,date,statefips,countyfips,o3_max_pred,o3_med_pred,o3_mean_pred,o3_pop_pred'
# filter on year, key on countyfips, value on mean


ozoneRDD = sc.textFile("Daily_County-Level_Ozone_Concentrations__2001-2014.csv",1)
ozoneRDDhead = ozoneRDD.first()
cleanRDD = ozoneRDD.filter(lambda x: x!= ozoneRDDhead).map(lambda x: x.split(','))



counties = cleanRDD.map(lambda x: x[3])
# count = 3109
dCounties = counties.distinct()
rmCty = dCounties.subtract(dAcounties).collect()

totRemRecs = remRecs2-remRecs1
print('Time for loading data and gathering unique counties: ' + str(totRemRecs))




map1 = time.time()

#-------------------
# YEAR 2001
#-------------------
year2001 = cleanRDD.filter(lambda x: x[0] == '2001').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2001 = year2001.map(lambda x: x[1]).mean()

# to get ALL counties
join2001 = year2001.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2001, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2002
#-------------------
year2002 = cleanRDD.filter(lambda x: x[0] == '2002').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2002 = year2002.map(lambda x: x[1]).mean()

# to get ALL counties
join2002 = year2002.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2002, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2003
#-------------------
year2003 = cleanRDD.filter(lambda x: x[0] == '2003').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2003 = year2003.map(lambda x: x[1]).mean()

# to get ALL counties
join2003 = year2003.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2003, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2004
#-------------------
year2004 = cleanRDD.filter(lambda x: x[0] == '2004').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2004 = year2004.map(lambda x: x[1]).mean()

# to get ALL counties
join2004 = year2004.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2004, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2005
#-------------------
year2005 = cleanRDD.filter(lambda x: x[0] == '2005').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2005 = year2005.map(lambda x: x[1]).mean()

# to get ALL counties
join2005 = year2005.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2005, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2006
#-------------------
year2006 = cleanRDD.filter(lambda x: x[0] == '2006').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2006 = year2006.map(lambda x: x[1]).mean()

# to get ALL counties
join2006 = year2006.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2006, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2007
#-------------------
year2007 = cleanRDD.filter(lambda x: x[0] == '2007').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2007 = year2007.map(lambda x: x[1]).mean()

# to get ALL counties
join2007 = year2007.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2007, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2008
#-------------------
year2008 = cleanRDD.filter(lambda x: x[0] == '2008').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2008 = year2008.map(lambda x: x[1]).mean()

# to get ALL counties
join2008 = year2008.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2008, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2009
#-------------------
year2009 = cleanRDD.filter(lambda x: x[0] == '2009').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2009 = year2009.map(lambda x: x[1]).mean()

# to get ALL counties
join2009 = year2009.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2009, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2010
#-------------------
year2010 = cleanRDD.filter(lambda x: x[0] == '2010').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2010 = year2010.map(lambda x: x[1]).mean()

# to get ALL counties
join2010 = year2010.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2010, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2011
#-------------------
year2011 = cleanRDD.filter(lambda x: x[0] == '2011').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2011 = year2011.map(lambda x: x[1]).mean()

# to get ALL counties
join2011 = year2011.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2011, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2012
#-------------------
year2012 = cleanRDD.filter(lambda x: x[0] == '2012').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2012 = year2012.map(lambda x: x[1]).mean()

# to get ALL counties
join2012 = year2012.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2012, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2013
#-------------------
year2013 = cleanRDD.filter(lambda x: x[0] == '2013').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2013 = year2013.map(lambda x: x[1]).mean()

# to get ALL counties
join2013 = year2013.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2013, list(x[1])[0])) + ' ' + x[0]))
#-------------------


#-------------------
# YEAR 2014
#-------------------
year2014 = cleanRDD.filter(lambda x: x[0] == '2014').map(lambda x: (str(int(x[3])), isFloat(x[6]))).filter(lambda x: isFloat(x[1])).groupByKey().mapValues(avg).sortByKey()

mean2014 = year2014.map(lambda x: x[1]).mean()

# to get ALL counties
join2014 = year2014.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(str(yearMean(mean2014, list(x[1])[0])) + ' ' + x[0]))
#-------------------

map2 = time.time()
totMap = map2-map1
print('Time for mapping: ' + str(totMap))



textF1 = time.time()
join2001.saveAsTextFile('data_2001.txt')
join2002.saveAsTextFile('data_2002.txt')
join2003.saveAsTextFile('data_2003.txt')
join2004.saveAsTextFile('data_2004.txt')
join2005.saveAsTextFile('data_2005.txt')
join2006.saveAsTextFile('data_2006.txt')
join2007.saveAsTextFile('data_2007.txt')
join2008.saveAsTextFile('data_2008.txt')
join2009.saveAsTextFile('data_2009.txt')
join2010.saveAsTextFile('data_2010.txt')
join2011.saveAsTextFile('data_2011.txt')
join2012.saveAsTextFile('data_2012.txt')
join2013.saveAsTextFile('data_2013.txt')
join2014.saveAsTextFile('data_2014.txt')
join2015.saveAsTextFile('data_2015.txt')
textF2 = time.time()

totTextF = textF2-textF1

print('Time for writing files: ' + str(totTextF))
