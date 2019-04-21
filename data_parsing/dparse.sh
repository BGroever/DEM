pysparkFile=card_dis.py

dataYears=(1980 1985 1990 1995 2000 2005 2010 2014)

spark-submit $pysparkFile

for year in ${dataYears[@]}
    do
        cat data_$year.txt/* > year$year.txt

        rm -rf data_$year.txt/
done

head year*
