from pyspark import SparkConf, SparkContext
import string
import time

conf = SparkConf().setMaster('local').setAppName('ParticulateMatter')

sc = SparkContext(conf = conf)


def avg(x):
    return sum(x)/len(x)

def isFloat(x):
    try:
        float(x)
        return float(x)
    except ValueError:
        return False


def getMean(iMean, x):
    if (x != ''):
        return x
    else:
        return iMean

remRecs2 = (time.time())
allCounties = sc.textFile("references/CtyFIPS.txt",1)
allCounties = allCounties.map(lambda x: x.split(' \t')).map(lambda x: (str(int(x[1])), ''))


dAcounties = allCounties.map(lambda x: x[0])



remRecs1 = (time.time())
#'year,date,statefips,countyfips,ctfips,latitude,longitude,ds_pm_pred,ds_pm_stdd'
# filter on year => month, key on countyfips, value on ds_pm_pred


pmRDD = sc.textFile("raw_data/Daily_Census_Tract-Level_PM2.5_Concentrations__2011-2014.csv",1)
pmRDDhead = pmRDD.first()
cleanRDD = pmRDD.filter(lambda x: x!= pmRDDhead).map(lambda x: x.split(','))



counties = cleanRDD.map(lambda x: x[3])
# count = 3109
dCounties = counties.distinct()
rmCty = dCounties.subtract(dAcounties).collect()

totRemRecs = remRecs2-remRecs1
print('Time for loading data and gathering unique counties: ' + str(totRemRecs))




map1 = time.time()

#--------------------------------------
# YEAR 2011
# count: 26383295
#--------------------------------------

year2011 = cleanRDD.filter(lambda x: x[0] == '2011').map(lambda x: (str(x[1])[2:5], x[3], isFloat(x[7])))

#-------------------
# JAN 2011
#-------------------
y2011mJAN = year2011.filter(lambda x: x[0]=='JAN').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mJAN = y2011mJAN.map(lambda x: x[1]).mean()

# to get ALL counties
join2011JAN = y2011mJAN.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mJAN, list(x[1])[0]))))
#-------------------

#-------------------
# FEB 2011
#-------------------
y2011mFEB = year2011.filter(lambda x: x[0]=='FEB').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mFEB = y2011mFEB.map(lambda x: x[1]).mean()

# to get ALL counties
join2011FEB = y2011mFEB.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mFEB, list(x[1])[0]))))
#-------------------

#-------------------
# MAR 2011
#-------------------
y2011mMAR = year2011.filter(lambda x: x[0]=='MAR').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mMAR = y2011mMAR.map(lambda x: x[1]).mean()

# to get ALL counties
join2011MAR = y2011mMAR.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mMAR, list(x[1])[0]))))
#-------------------

#-------------------
# APR 2011
#-------------------
y2011mAPR = year2011.filter(lambda x: x[0]=='APR').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mAPR = y2011mAPR.map(lambda x: x[1]).mean()

# to get ALL counties
join2011APR = y2011mAPR.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mAPR, list(x[1])[0]))))
#-------------------

#-------------------
# MAY 2011
#-------------------
y2011mMAY = year2011.filter(lambda x: x[0]=='MAY').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mMAY = y2011mMAY.map(lambda x: x[1]).mean()

# to get ALL counties
join2011MAY = y2011mMAY.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mMAY, list(x[1])[0]))))
#-------------------

#-------------------
# JUN 2011
#-------------------
y2011mJUN = year2011.filter(lambda x: x[0]=='JUN').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mJUN = y2011mJUN.map(lambda x: x[1]).mean()

# to get ALL counties
join2011JUN = y2011mJUN.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mJUN, list(x[1])[0]))))
#-------------------

#-------------------
# JUL 2011
#-------------------
y2011mJUL = year2011.filter(lambda x: x[0]=='JUL').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mJUL = y2011mJUL.map(lambda x: x[1]).mean()

# to get ALL counties
join2011JUL = y2011mJUL.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mJUL, list(x[1])[0]))))
#-------------------

#-------------------
# AUG 2011
#-------------------
y2011mAUG = year2011.filter(lambda x: x[0]=='AUG').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mAUG = y2011mAUG.map(lambda x: x[1]).mean()

# to get ALL counties
join2011AUG = y2011mAUG.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mAUG, list(x[1])[0]))))
#-------------------

#-------------------
# SEP 2011
#-------------------
y2011mSEP = year2011.filter(lambda x: x[0]=='SEP').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mSEP = y2011mSEP.map(lambda x: x[1]).mean()

# to get ALL counties
join2011SEP = y2011mSEP.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mSEP, list(x[1])[0]))))
#-------------------

#-------------------
# OCT 2011
#-------------------
y2011mOCT = year2011.filter(lambda x: x[0]=='OCT').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mOCT = y2011mOCT.map(lambda x: x[1]).mean()

# to get ALL counties
join2011OCT = y2011mOCT.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mOCT, list(x[1])[0]))))
#-------------------

#-------------------
# NOV 2011
#-------------------
y2011mNOV = year2011.filter(lambda x: x[0]=='NOV').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mNOV = y2011mNOV.map(lambda x: x[1]).mean()

# to get ALL counties
join2011NOV = y2011mNOV.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mNOV, list(x[1])[0]))))
#-------------------

#-------------------
# DEC 2011
#-------------------
y2011mDEC = year2011.filter(lambda x: x[0]=='DEC').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2011mDEC = y2011mDEC.map(lambda x: x[1]).mean()

# to get ALL counties
join2011DEC = y2011mDEC.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2011mDEC, list(x[1])[0]))))
#-------------------


#--------------------------------------
# YEAR 2012
#--------------------------------------

year2012 = cleanRDD.filter(lambda x: x[0] == '2012').map(lambda x: (str(x[1])[2:5], x[3], isFloat(x[7])))

#-------------------
# JAN 2012
#-------------------
y2012mJAN = year2012.filter(lambda x: x[0]=='JAN').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mJAN = y2012mJAN.map(lambda x: x[1]).mean()

# to get ALL counties
join2012JAN = y2012mJAN.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mJAN, list(x[1])[0]))))
#-------------------

#-------------------
# FEB 2012
#-------------------
y2012mFEB = year2012.filter(lambda x: x[0]=='FEB').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mFEB = y2012mFEB.map(lambda x: x[1]).mean()

# to get ALL counties
join2012FEB = y2012mFEB.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mFEB, list(x[1])[0]))))
#-------------------

#-------------------
# MAR 2012
#-------------------
y2012mMAR = year2012.filter(lambda x: x[0]=='MAR').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mMAR = y2012mMAR.map(lambda x: x[1]).mean()

# to get ALL counties
join2012MAR = y2012mMAR.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mMAR, list(x[1])[0]))))
#-------------------

#-------------------
# APR 2012
#-------------------
y2012mAPR = year2012.filter(lambda x: x[0]=='APR').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mAPR = y2012mAPR.map(lambda x: x[1]).mean()

# to get ALL counties
join2012APR = y2012mAPR.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mAPR, list(x[1])[0]))))
#-------------------

#-------------------
# MAY 2012
#-------------------
y2012mMAY = year2012.filter(lambda x: x[0]=='MAY').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mMAY = y2012mMAY.map(lambda x: x[1]).mean()

# to get ALL counties
join2012MAY = y2012mMAY.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mMAY, list(x[1])[0]))))
#-------------------

#-------------------
# JUN 2012
#-------------------
y2012mJUN = year2012.filter(lambda x: x[0]=='JUN').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mJUN = y2012mJUN.map(lambda x: x[1]).mean()

# to get ALL counties
join2012JUN = y2012mJUN.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mJUN, list(x[1])[0]))))
#-------------------

#-------------------
# JUL 2012
#-------------------
y2012mJUL = year2012.filter(lambda x: x[0]=='JUL').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mJUL = y2012mJUL.map(lambda x: x[1]).mean()

# to get ALL counties
join2012JUL = y2012mJUL.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mJUL, list(x[1])[0]))))
#-------------------

#-------------------
# AUG 2012
#-------------------
y2012mAUG = year2012.filter(lambda x: x[0]=='AUG').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mAUG = y2012mAUG.map(lambda x: x[1]).mean()

# to get ALL counties
join2012AUG = y2012mAUG.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mAUG, list(x[1])[0]))))
#-------------------

#-------------------
# SEP 2012
#-------------------
y2012mSEP = year2012.filter(lambda x: x[0]=='SEP').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mSEP = y2012mSEP.map(lambda x: x[1]).mean()

# to get ALL counties
join2012SEP = y2012mSEP.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mSEP, list(x[1])[0]))))
#-------------------

#-------------------
# OCT 2012
#-------------------
y2012mOCT = year2012.filter(lambda x: x[0]=='OCT').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mOCT = y2012mOCT.map(lambda x: x[1]).mean()

# to get ALL counties
join2012OCT = y2012mOCT.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mOCT, list(x[1])[0]))))
#-------------------

#-------------------
# NOV 2012
#-------------------
y2012mNOV = year2012.filter(lambda x: x[0]=='NOV').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mNOV = y2012mNOV.map(lambda x: x[1]).mean()

# to get ALL counties
join2012NOV = y2012mNOV.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mNOV, list(x[1])[0]))))
#-------------------

#-------------------
# DEC 2012
#-------------------
y2012mDEC = year2012.filter(lambda x: x[0]=='DEC').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2012mDEC = y2012mDEC.map(lambda x: x[1]).mean()

# to get ALL counties
join2012DEC = y2012mDEC.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2012mDEC, list(x[1])[0]))))
#-------------------


#--------------------------------------
# YEAR 2013
#--------------------------------------

year2013 = cleanRDD.filter(lambda x: x[0] == '2013').map(lambda x: (str(x[1])[2:5], x[3], isFloat(x[7])))

#-------------------
# JAN 2013
#-------------------
y2013mJAN = year2013.filter(lambda x: x[0]=='JAN').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mJAN = y2013mJAN.map(lambda x: x[1]).mean()

# to get ALL counties
join2013JAN = y2013mJAN.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mJAN, list(x[1])[0]))))
#-------------------

#-------------------
# FEB 2013
#-------------------
y2013mFEB = year2013.filter(lambda x: x[0]=='FEB').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mFEB = y2013mFEB.map(lambda x: x[1]).mean()

# to get ALL counties
join2013FEB = y2013mFEB.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mFEB, list(x[1])[0]))))
#-------------------

#-------------------
# MAR 2013
#-------------------
y2013mMAR = year2013.filter(lambda x: x[0]=='MAR').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mMAR = y2013mMAR.map(lambda x: x[1]).mean()

# to get ALL counties
join2013MAR = y2013mMAR.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mMAR, list(x[1])[0]))))
#-------------------

#-------------------
# APR 2013
#-------------------
y2013mAPR = year2013.filter(lambda x: x[0]=='APR').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mAPR = y2013mAPR.map(lambda x: x[1]).mean()

# to get ALL counties
join2013APR = y2013mAPR.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mAPR, list(x[1])[0]))))
#-------------------

#-------------------
# MAY 2013
#-------------------
y2013mMAY = year2013.filter(lambda x: x[0]=='MAY').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mMAY = y2013mMAY.map(lambda x: x[1]).mean()

# to get ALL counties
join2013MAY = y2013mMAY.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mMAY, list(x[1])[0]))))
#-------------------

#-------------------
# JUN 2013
#-------------------
y2013mJUN = year2013.filter(lambda x: x[0]=='JUN').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mJUN = y2013mJUN.map(lambda x: x[1]).mean()

# to get ALL counties
join2013JUN = y2013mJUN.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mJUN, list(x[1])[0]))))
#-------------------

#-------------------
# JUL 2013
#-------------------
y2013mJUL = year2013.filter(lambda x: x[0]=='JUL').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mJUL = y2013mJUL.map(lambda x: x[1]).mean()

# to get ALL counties
join2013JUL = y2013mJUL.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mJUL, list(x[1])[0]))))
#-------------------

#-------------------
# AUG 2013
#-------------------
y2013mAUG = year2013.filter(lambda x: x[0]=='AUG').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mAUG = y2013mAUG.map(lambda x: x[1]).mean()

# to get ALL counties
join2013AUG = y2013mAUG.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mAUG, list(x[1])[0]))))
#-------------------

#-------------------
# SEP 2013
#-------------------
y2013mSEP = year2013.filter(lambda x: x[0]=='SEP').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mSEP = y2013mSEP.map(lambda x: x[1]).mean()

# to get ALL counties
join2013SEP = y2013mSEP.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mSEP, list(x[1])[0]))))
#-------------------

#-------------------
# OCT 2013
#-------------------
y2013mOCT = year2013.filter(lambda x: x[0]=='OCT').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mOCT = y2013mOCT.map(lambda x: x[1]).mean()

# to get ALL counties
join2013OCT = y2013mOCT.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mOCT, list(x[1])[0]))))
#-------------------

#-------------------
# NOV 2013
#-------------------
y2013mNOV = year2013.filter(lambda x: x[0]=='NOV').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mNOV = y2013mNOV.map(lambda x: x[1]).mean()

# to get ALL counties
join2013NOV = y2013mNOV.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mNOV, list(x[1])[0]))))
#-------------------

#-------------------
# DEC 2013
#-------------------
y2013mDEC = year2013.filter(lambda x: x[0]=='DEC').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2013mDEC = y2013mDEC.map(lambda x: x[1]).mean()

# to get ALL counties
join2013DEC = y2013mDEC.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2013mDEC, list(x[1])[0]))))
#-------------------


#--------------------------------------
# YEAR 2014
#--------------------------------------

year2014 = cleanRDD.filter(lambda x: x[0] == '2014').map(lambda x: (str(x[1])[2:5], x[3], isFloat(x[7])))

#-------------------
# JAN 2014
#-------------------
y2014mJAN = year2014.filter(lambda x: x[0]=='JAN').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mJAN = y2014mJAN.map(lambda x: x[1]).mean()

# to get ALL counties
join2014JAN = y2014mJAN.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mJAN, list(x[1])[0]))))
#-------------------

#-------------------
# FEB 2014
#-------------------
y2014mFEB = year2014.filter(lambda x: x[0]=='FEB').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mFEB = y2014mFEB.map(lambda x: x[1]).mean()

# to get ALL counties
join2014FEB = y2014mFEB.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mFEB, list(x[1])[0]))))
#-------------------

#-------------------
# MAR 2014
#-------------------
y2014mMAR = year2014.filter(lambda x: x[0]=='MAR').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mMAR = y2014mMAR.map(lambda x: x[1]).mean()

# to get ALL counties
join2014MAR = y2014mMAR.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mMAR, list(x[1])[0]))))
#-------------------

#-------------------
# APR 2014
#-------------------
y2014mAPR = year2014.filter(lambda x: x[0]=='APR').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mAPR = y2014mAPR.map(lambda x: x[1]).mean()

# to get ALL counties
join2014APR = y2014mAPR.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mAPR, list(x[1])[0]))))
#-------------------

#-------------------
# MAY 2014
#-------------------
y2014mMAY = year2014.filter(lambda x: x[0]=='MAY').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mMAY = y2014mMAY.map(lambda x: x[1]).mean()

# to get ALL counties
join2014MAY = y2014mMAY.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mMAY, list(x[1])[0]))))
#-------------------

#-------------------
# JUN 2014
#-------------------
y2014mJUN = year2014.filter(lambda x: x[0]=='JUN').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mJUN = y2014mJUN.map(lambda x: x[1]).mean()

# to get ALL counties
join2014JUN = y2014mJUN.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mJUN, list(x[1])[0]))))
#-------------------

#-------------------
# JUL 2014
#-------------------
y2014mJUL = year2014.filter(lambda x: x[0]=='JUL').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mJUL = y2014mJUL.map(lambda x: x[1]).mean()

# to get ALL counties
join2014JUL = y2014mJUL.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mJUL, list(x[1])[0]))))
#-------------------

#-------------------
# AUG 2014
#-------------------
y2014mAUG = year2014.filter(lambda x: x[0]=='AUG').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mAUG = y2014mAUG.map(lambda x: x[1]).mean()

# to get ALL counties
join2014AUG = y2014mAUG.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mAUG, list(x[1])[0]))))
#-------------------

#-------------------
# SEP 2014
#-------------------
y2014mSEP = year2014.filter(lambda x: x[0]=='SEP').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mSEP = y2014mSEP.map(lambda x: x[1]).mean()

# to get ALL counties
join2014SEP = y2014mSEP.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mSEP, list(x[1])[0]))))
#-------------------

#-------------------
# OCT 2014
#-------------------
y2014mOCT = year2014.filter(lambda x: x[0]=='OCT').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mOCT = y2014mOCT.map(lambda x: x[1]).mean()

# to get ALL counties
join2014OCT = y2014mOCT.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mOCT, list(x[1])[0]))))
#-------------------

#-------------------
# NOV 2014
#-------------------
y2014mNOV = year2014.filter(lambda x: x[0]=='NOV').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mNOV = y2014mNOV.map(lambda x: x[1]).mean()

# to get ALL counties
join2014NOV = y2014mNOV.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mNOV, list(x[1])[0]))))
#-------------------

#-------------------
# DEC 2014
#-------------------
y2014mDEC = year2014.filter(lambda x: x[0]=='DEC').filter(lambda x: isFloat(x[2])).map(lambda x: (x[1], x[2])).groupByKey().mapValues(avg).sortByKey()

mean2014mDEC = y2014mDEC.map(lambda x: x[1]).mean()

# to get ALL counties
join2014DEC = y2014mDEC.union(allCounties).groupByKey().filter(lambda x: (x[0] != rmCty[0]) and (x[0] != rmCty[1])).map(lambda x: str(x[0] +' '+ str(getMean(mean2014mDEC, list(x[1])[0]))))
#-------------------


map2 = time.time()
totMap = map2-map1
print('Time for mapping: ' + str(totMap))



textF1 = time.time()
join2011JAN.saveAsTextFile('data_2011JAN.txt')
join2011FEB.saveAsTextFile('data_2011FEB.txt')
join2011MAR.saveAsTextFile('data_2011MAR.txt')
join2011APR.saveAsTextFile('data_2011APR.txt')
join2011MAY.saveAsTextFile('data_2011MAY.txt')
join2011JUN.saveAsTextFile('data_2011JUN.txt')
join2011JUL.saveAsTextFile('data_2011JUL.txt')
join2011AUG.saveAsTextFile('data_2011AUG.txt')
join2011SEP.saveAsTextFile('data_2011SEP.txt')
join2011OCT.saveAsTextFile('data_2011OCT.txt')
join2011NOV.saveAsTextFile('data_2011NOV.txt')
join2011DEC.saveAsTextFile('data_2011DEC.txt')

join2012JAN.saveAsTextFile('data_2012JAN.txt')
join2012FEB.saveAsTextFile('data_2012FEB.txt')
join2012MAR.saveAsTextFile('data_2012MAR.txt')
join2012APR.saveAsTextFile('data_2012APR.txt')
join2012MAY.saveAsTextFile('data_2012MAY.txt')
join2012JUN.saveAsTextFile('data_2012JUN.txt')
join2012JUL.saveAsTextFile('data_2012JUL.txt')
join2012AUG.saveAsTextFile('data_2012AUG.txt')
join2012SEP.saveAsTextFile('data_2012SEP.txt')
join2012OCT.saveAsTextFile('data_2012OCT.txt')
join2012NOV.saveAsTextFile('data_2012NOV.txt')
join2012DEC.saveAsTextFile('data_2012DEC.txt')

join2013JAN.saveAsTextFile('data_2013JAN.txt')
join2013FEB.saveAsTextFile('data_2013FEB.txt')
join2013MAR.saveAsTextFile('data_2013MAR.txt')
join2013APR.saveAsTextFile('data_2013APR.txt')
join2013MAY.saveAsTextFile('data_2013MAY.txt')
join2013JUN.saveAsTextFile('data_2013JUN.txt')
join2013JUL.saveAsTextFile('data_2013JUL.txt')
join2013AUG.saveAsTextFile('data_2013AUG.txt')
join2013SEP.saveAsTextFile('data_2013SEP.txt')
join2013OCT.saveAsTextFile('data_2013OCT.txt')
join2013NOV.saveAsTextFile('data_2013NOV.txt')
join2013DEC.saveAsTextFile('data_2013DEC.txt')

join2014JAN.saveAsTextFile('data_2014JAN.txt')
join2014FEB.saveAsTextFile('data_2014FEB.txt')
join2014MAR.saveAsTextFile('data_2014MAR.txt')
join2014APR.saveAsTextFile('data_2014APR.txt')
join2014MAY.saveAsTextFile('data_2014MAY.txt')
join2014JUN.saveAsTextFile('data_2014JUN.txt')
join2014JUL.saveAsTextFile('data_2014JUL.txt')
join2014AUG.saveAsTextFile('data_2014AUG.txt')
join2014SEP.saveAsTextFile('data_2014SEP.txt')
join2014OCT.saveAsTextFile('data_2014OCT.txt')
join2014NOV.saveAsTextFile('data_2014NOV.txt')
join2014DEC.saveAsTextFile('data_2014DEC.txt')

textF2 = time.time()
totTextF = textF2-textF1
print('Time for writing files: ' + str(totTextF))
