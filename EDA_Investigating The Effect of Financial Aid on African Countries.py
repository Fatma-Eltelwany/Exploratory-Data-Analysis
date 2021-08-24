#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigating The Effect of Financial Aid on African Countries
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# <li><a href="#limitations">Limitations</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# I have chosen datasets from [Gapminder](https://www.gapminder.org/data/). I chose the aid received per person dataset from the economy section and the income per person dataset. I want to have a glimse of whether financial aid is really helping the receiving countries especially in Africa. I will explore the trends of how much aid per person an african country is receiving through the years and how the income per person is changing. For sure, income per person is a complex factor to pin down on a single paramter so I won't expect to have sharp conclusions only inferences or inclinations. This might give us a direction on what else can be analyzed to get a clearer picture.

# In[1]:


# imporying packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling

# In[2]:


# loading data
df_aid = pd.read_csv('aid_received_per_person_current_us.csv')
df_aid.head()


# In[3]:


df_aid.info()


# In[4]:


df_income = pd.read_csv('income_per_person_gdppercapita_ppp_inflation_adjusted.csv')
df_income.head()


# In[5]:


df_income.info()


# By inspecting the five datasets I am using, I observed the following:
# * They don't have the same number of countries which won't matter since I will be focusing on African ones only. I will need to make sure they have the same african countries later and drop all other ones. I might find it useful to make the countries column the index.
# * They don't share the same timeframe as well. I noticed that in the income dataframe there are predictions for the future till the year 2040. I checked the data documentations [here](https://www.gapminder.org/data/documentation/gd001/) to make sure. To fix that I will use the years included in them all so that the results make sense. The years range I will use is from 1995 to 2017. All other years columns will be dropped.
# * I noticed that the earlier the year the more null values there are which is understandable. The lack of techologies or means to collect these data back then is a reasonable explanation. However, this might not be an issue after dropping the years that are not included in all the data sets. I will deal with null values after dropping the unwanted years and selected countries in Africa only.
# * The income dataset has int instead of float for all the years. I think this wouldn't pose a problem. So I will not change it and see what happens.
# 

# 
# 
# ### Data Cleaning 

# In[6]:


#selecting the years range
years_list = ['country','1995', '1996', '1997', '1998', '1999', '2000', '2001',
       '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
       '2011', '2012', '2013', '2014', '2015', '2016', '2017']
df_aid = df_aid[years_list]
df_aid.head()


# Preparing a list of the african countries contained in the aid dataset. I have chosen the aid dataset specifically beacause it has the least number of countries (157 country) compared to the other dataset.

# In[7]:


df_income = df_income[years_list]


# In[8]:


allafrican_countries = ['Algeria','Egypt', 'Libya','Morocco','Tunisia','Burundi','Comoros','Djibouti','Eritrea','Ethiopia',
'Kenya','Madagascar','Malawi','Mauritius','Mayotte','Mozambique','Rwanda','Somalia','Sudan','Uganda','Tanzania','Zambia','Zimbabwe','Angola','Cameroon','Chad','Congo','Equatorial Guinea','Gabon','Botswana','Lesotho',
                     'Namibia','South Africa','Swaziland','Benin','Burkina Faso','Cape Verde','Gambia','Ghana','Guinea',
                     'Guinea-Bissau','Liberia','Mali','Mauritania','Niger','Nigeria','Senegal','Sierra Leone','Togo']
print(allafrican_countries)


# In[9]:


allcountries_list = df_aid['country'].tolist()
print(allcountries_list)


# In[10]:


af_set = set(allafrican_countries)
all_set = set(allcountries_list)


# In[11]:


af_set.issubset(all_set)


# In[12]:


af = all_set.intersection(af_set)
print(af)


# In[13]:


african_countries = list(af)
print(african_countries)


# Getting the countries in Africa only in the aid dataframe.

# Note:
# I have tried many ways to filter off any countries other than the african ones. I tried loops on the african list and the set version of it and used the query method inside it. I got different kinds of errors related to indices and what not. I also tried converting the african list to a series and adding it to the dataframe as a new column. However, that missed up the arrangement of the countries with its actual value. Please direct me to the best way to do this. 

# In[14]:


#step 1
df_aidtrans = df_aid.set_index('country').transpose()
df_aid.head()


# In[15]:


df_aidtrans.head()


# In[16]:


#step 2
df_aidtrans = df_aidtrans[african_countries]


# In[17]:


#step 3
df_africanaid = df_aidtrans.transpose().reset_index()


# In[18]:


df_africanaid


# In[19]:


df_africanaid.info()


# Since there are 11 countries which have null values at some years, it's not reasonable to drop them as this would narrow down the countries we analyze greatly. Instead, I will fill out these with the mean value for each country.

# In[20]:


means = df_africanaid.mean(axis = 1)
print(means)


# In[21]:


df_africanaid.T.fillna(df_africanaid.mean(axis=1)).T


# Getting the countries in Africa only in the income dataframe.

# In[22]:


df_incometrans = df_income.set_index('country').transpose()
df_incometrans.head()


# In[23]:


df_incometrans = df_incometrans[african_countries]


# In[24]:


df_africanincome = df_incometrans.transpose().reset_index()


# In[25]:


df_africanincome.info()


# In[26]:


df_africanincome


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# ### What are the top 2 countries in terms of aid received and what are the bottom 2?

# In[32]:


plt.figure(figsize=(35,15))
plt.xlabel('African Countries')
plt.ylabel('Average Aid Received per Person (Dollars)')
plt.title('Average Aid Received by African Countries')
plt.bar(df_africanaid['country'], means);
plt.xticks(rotation = 90);


# From the previous figure we that the top 2 countries in receiving aid per person are (more aid to less aid): \
# __Cape Verde__ \
# __Djibouti__ \
# While the bottom 2 are (more aid to less aid): \
# __Nigeria__ \
# __Algeria__ 

# <a id='eda'></a>
# ## Exploring trends in aid and income of the top and bottom countries.

# In[33]:


df_africanaid.set_index('country', inplace = True)


# In[34]:


#Exploring how the aid per person of the top and bottom countries changed over the years
years = ['1995', '1996', '1997', '1998', '1999', '2000', '2001',
       '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
       '2011', '2012', '2013', '2014', '2015', '2016', '2017']
def aidplots(cname, color):
    cplot = plt.plot(years, df_africanaid.loc[cname, :], color,label = cname)
    return cplot
plt.figure(figsize=(16,10))
plt.xlabel('Years')
plt.ylabel('Aid Received per person (Dollar)')
plt.title('Aid Received over the Years')
aidplots('Cape Verde', 'g')
aidplots('Djibouti', 'y')
aidplots('Nigeria', 'r')
aidplots('Algeria', 'b')
plt.legend(loc='best')


# We can notice a trend here which is that regardless of whether a country is a top or botton receiving aid, the amount of aid per person is decreasing through the years. For cape Verde, it's the most turbulent country when it comes to the amount of aid it receives. Nigeria seems to not engage in receiving aids that much, it has a period (from 2004 to 2007) before or after that the aid is minute.

# In[35]:


df_africanincome.set_index('country', inplace = True)


# In[37]:


#Exploring how the income per person of the top and bottom countries changed over the years
years = ['1995', '1996', '1997', '1998', '1999', '2000', '2001',
       '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
       '2011', '2012', '2013', '2014', '2015', '2016', '2017']
def incomeplots(cname, color):
    iplot = plt.plot(years, df_africanincome.loc[cname, :], color, label = cname)
    return iplot
plt.figure(figsize=(16,10))
plt.xlabel('Years')
plt.ylabel('Income per Person (Dollars)')
plt.title('Income over the Years')
incomeplots('Cape Verde', 'g')
incomeplots('Djibouti', 'y')
incomeplots('Nigeria', 'r')
incomeplots('Algeria', 'b')
plt.legend(loc = 'best')


# We can see here that the results are not conclusive. It is most apparant for Cape Verde (the country that received the most aid per person) that significant increase in income is noticed which may mean that fininaical aid is really helping. We can compare this with Djibouti(which didn't receive as much aid and almost had the same starting point in the year 1995) to see the difference. For Algeria, it seems that the low aid it received had not affected the income per person. Nigeria on the other hand, seems to make progress and witnesing an increase in incomes even though it didn't receive as much aid as Cape verde for example. Of course there are many other factors not considered here. These are inferences constrained by the analysis done so far. 

# <a id='conclusions'></a>
# ## Conclusions

# * Cape Verde is the african country that received the __highest__ average aid per person from 1995 to 2017
# * Algeria is the african country that received the __lowest__ average aid per person from 1995 to 2017
# * The four countries considered (Cape Verde, Djibouti, Nigeria, Algeria) mostly took their aid in peaks not with a flat rate
# * Algeria has the __highest__ income per person in the start of the years range and also at the end of it, that is in 1995 and in 2017
# * Djibouti, however, started with second lowest income and ended with the __lowest__ income even though it is the second country after Cape Verde in receiving aid.
# * It is observed that income per person across the four countries kept increasing over the years

# <a id='limitations'></a>
# ## Limitations

# * I observed the trends in aid receiving and income, however it is not possible to pin down how these two are tied together
# * The income per person is affected by several factors other than the aid a country is receiving
# * Receiving aid might be helping with other aspects than just the income. For instance, it can help with health, eduaction, food and many other areas that were not explored here.
# * Still the observation that some countries kept their income increasing without receiving as much as aid as others is worth noting. This is the case of Algeria and Cape Verde. They both kept their income raising but Algeria received much less aid than Cape verde. This may have varying meanings like maybe countries who are most struggling revert to aid so they can barely keep up and maybe the opposite. Maybe receiving aid and having to pay it back x folds prevents counrtries from making enough progress. Also many factors are at play here like management, corruption or natural resources. This needs further analysis and investigation to be able to draw a conlusion and generalise on other countries.
