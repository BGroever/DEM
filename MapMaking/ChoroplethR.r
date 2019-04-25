library(choroplethr)
library(acs)
library(ggplot2)
library(RColorBrewer)
#setwd("C:/Github/DataBlog")
col.pal<-brewer.pal(7,"Greens")

###### API key
# Need to go to http://api.census.gov/data/key_signup.html to set API key
api.key.install("95147043cfb3460867a1fc678808514e4a3d04fc")

###### Basic ACS Table IDs 
# B19301 = Per Capita Income
# B01003 = Population

###### Plotting
## Basic by State
state_choropleth_acs(tableId="B19301")
state_choropleth_acs(tableId="B19301") +
  labs(title="US 2011 Per Capita Income by State")

## Per Capita Income by County
county_choropleth_acs(tableId="B19301")
county_choropleth_acs(tableId="B19301",state_zoom="california")

## Population by County by Ethnicity
county_choropleth_acs(tableId="B01003")+labs(title="Total US Population by County (2011)")
county_choropleth_acs(tableId="B02008")+labs(title="US Population by County (2011) - White")
county_choropleth_acs(tableId="B02009")+labs(title="US Population by County (2011) - Black ")
county_choropleth_acs(tableId="B02011")+labs(title="US Population by County (2011) - Asian")
county_choropleth_acs(tableId="B03001")+labs(title="US Population by County (2011) - Hispanic")

# Changing colors, easy but doesn't work for Alaska)
county_choropleth_acs(tableId="B19301") +
  scale_fill_brewer(palette=2) 

df_2015<-get_acs_data(tableId="B19301",map="county",endyear=2015)
df_2014<-get_acs_data(tableId="B19301",map="county",endyear=2014)
df_2013<-get_acs_data(tableId="B19301",map="county",endyear=2013)
df_2012<-get_acs_data(tableId="B19301",map="county",endyear=2012)
df_2011<-get_acs_data(tableId="B19301",map="county",endyear=2011)
df_2010<-get_acs_data(tableId="B19301",map="county",endyear=2010)

# Changing colors, harder and works for all states
choro1<-CountyChoropleth$new(df_2015$df)
choro1$title = "2015 Per Capita Income"
choro1$ggplot_scale <- scale_fill_manual(name="Per Capita Income",values=c("blue", "red","orange","green","black","purple","yellow"), drop=FALSE)
choro1$render()

choro1$ggplot_scale <- scale_fill_manual(name="Per Capita Income",values=col.pal, drop=FALSE)
choro1$render()

###### Animated Choropleth
choro_list<-list()
choro_list[[1]]<-county_choropleth(df_2010$df)
choro_list[[2]]<-county_choropleth(df_2011$df)
choro_list[[3]]<-county_choropleth(df_2012$df)
choro_list[[4]]<-county_choropleth(df_2013$df)
choro_list[[5]]<-county_choropleth(df_2014$df)
choro_list[[6]]<-county_choropleth(df_2015$df)

choroplethr_animate(choro_list)

# Number of bins
county_choropleth_acs(tableId="B19301")
county_choropleth_acs(tableId="B19301",num_colors=4) 
county_choropleth_acs(tableId="B19301",num_colors=1)  # continuous

###### Set fixed break points
df_2010$df$breaks<-""
for (i in 1:nrow(df_2010$df))
{
  if (is.na(df_2010$df[i,"value"])) 
    {
    df_2010$df[i,"breaks"] <- "$20-$30K"
  } else if (df_2010$df[i,"value"] < 10000) {
    df_2010$df[i,"breaks"] <- "$0-$10K"
  } else if (df_2010$df[i,"value"]>=10000 & df_2010$df[i,"value"]<20000) {
    df_2010$df[i,"breaks"] <- "$10-$20K"
  } else if (df_2010$df[i,"value"]>=20000 & df_2010$df[i,"value"]<30000) {
    df_2010$df[i,"breaks"] <- "$20-$30K"
  } else if (df_2010$df[i,"value"]>=30000 & df_2010$df[i,"value"]<40000) {
    df_2010$df[i,"breaks"] <- "$30-$40K"
  } else if (df_2010$df[i,"value"]>=40000) {
    df_2010$df[i,"breaks"] <- "$40K+"
  } 
}
df_2010$df$value<-df_2010$df$breaks
county_choropleth(df_2010$df)
