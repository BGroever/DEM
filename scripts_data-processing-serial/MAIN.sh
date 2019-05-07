#-------------------------------
# This as the main script to parse datasets into the
# compatible format with the dem scripts (for mapping).
# Please be cognizant of folder and file structures, as they
# are critical for the script the run properly.
# This script assumes Python and Spark installation on the OS.
#------------------
# Example commands:
# $ sh MAIN.sh disease
#-------------------------------


mode=$1
this=MAIN.sh

data_src=raw_data
pyspark_src=pyspark_scripts

echo $mode

#-------------------------------
# ALL DATASETS
#-------------------------------
if [ $mode == 'all' ]
then
    sh $this disease
    sh $this uv
    sh $this ozone
    sh $this pm
fi
#-------------------------------


#-------------------------------
# DATSET: CARDIOVASCULAR DISEASE
#-------------------------------
if [ $mode == 'disease' ]
then
    pyName=cardiovascular_disease.py
    runFile=$pyspark_src/$pyName
    fldr=cardiovascular_disease
    dataFldr=../data_for_maps/$fldr

    mkdir -p ../data_for_maps/$fldr

    spark-submit $runFile

    dataYears=(1980 1985 1990 1995 2000 2005 2010 2014)

    for year in ${dataYears[@]}
        do
            cat data_$year.txt/* > $dataFldr/year$year.txt

            rm -rf data_$year.txt/
    done

    head $dataFldr/year*
fi
#-------------------------------


#-------------------------------
# DATSET: UV IRRADIANCE
#-------------------------------
if [ $mode == 'uv' ]
then
    pyName=uv_irradiance.py
    runFile=$pyspark_src/$pyName
    fldr=uv_irradiance
    dataFldr=../data_for_maps/$fldr

    mkdir -p ../data_for_maps/$fldr

    spark-submit $runFile

    dataYears=(2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015)

    for year in ${dataYears[@]}
        do
            cat data_$year.txt/* > $dataFldr/year$year.txt

            rm -rf data_$year.txt/
    done

    head $dataFldr/year*
fi
#-------------------------------


#-------------------------------
# DATSET: Ozone Concentrations
#-------------------------------
if [ $mode == 'ozone' ]
then
    pyName=ozone_concentrations.py
    runFile=$pyspark_src/$pyName
    fldr=ozone_concentratios
    dataFldr=../data_for_maps/$fldr

    mkdir -p ../data_for_maps/$fldr

    spark-submit $runFile

    dataYears=(2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014)

    for year in ${dataYears[@]}
        do
            cat data_$year.txt/* > $dataFldr/year$year.txt

            rm -rf data_$year.txt/
    done

    head $dataFldr/year*
fi
#-------------------------------


#-------------------------------
# DATSET: PARTICULATE MATTER
#-------------------------------
if [ $mode == 'pm' ]
then
    pyName=particulate_matter.py
    runFile=$pyspark_src/$pyName
    fldr=particulate_matter
    dataFldr=../data_for_maps/$fldr

    mkdir -p ../data_for_maps/$fldr

    spark-submit $runFile

    dataYears=(2011JAN 2011FEB 2011MAR 2011APR 2011MAY 2011JUN 2011JUL 2011AUG 2011SEP 2011OCT 2011NOV 2011DEC 2012JAN 2012FEB 2012MAR 2012APR 2012MAY 2012JUN 2012JUL 2012AUG 2012SEP 2012OCT 2012NOV 2012DEC 2013JAN 2013FEB 2013MAR 2013APR 2013MAY 2013JUN 2013JUL 2013AUG 2013SEP 2013OCT 2013NOV 2013DEC 2014JAN 2014FEB 2014MAR 2014APR 2014MAY 2014JUN 2014JUL 2014AUG 2014SEP 2014OCT 2014NOV 2014DEC)

    for year in ${dataYears[@]}
        do
            cat data_$year.txt/* > $dataFldr/year$year.txt

            rm -rf data_$year.txt/
    done

    head $dataFldr/year*
fi
#-------------------------------
