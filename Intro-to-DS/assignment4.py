#!/usr/bin/env python
# coding: utf-8

# # Assignment 4
# ## Description
# In this assignment you must read in a file of metropolitan regions and associated sports teams from [assets/wikipedia_data.html](assets/wikipedia_data.html) and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in [assets/nfl.csv](assets/nfl.csv)), MLB (baseball, in [assets/mlb.csv](assets/mlb.csv)), NBA (basketball, in [assets/nba.csv](assets/nba.csv) or NHL (hockey, in [assets/nhl.csv](assets/nhl.csv)). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!
# 
# For each sport I would like you to answer the question: **what is the win/loss ratio's correlation with the population of the city it is in?** Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with [`pearsonr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html), so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%\*4=80%) of the grade for this assignment. You should only use data **from year 2018** for your analysis -- this is important!
# 
# ## Notes
# 
# 1. Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
# 2. I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
# 3. It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
# 4. There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!

# ## Question 1
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NHL** using **2018** data.

# In[97]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re



def nhl_correlation(): 
    # YOUR CODE HERE
    nhl_df=pd.read_csv("assets/nhl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    
    nhl_df['team'] = nhl_df['team'].str.strip('*')
    nhl_df = nhl_df[nhl_df['year'] == 2018]
    nhl_df['team'] = nhl_df['team'].str.replace(r'[A-Z]\w+\s','')
    nhl_df['team'] = nhl_df['team'].replace({'Leafs':'Maple Leafs','Wings':'Red Wings', 'Jackets':'Blue Jackets','Knights':'Golden Knights','St. Blues':'Blues'})
    NYC = pd.Series({'team':'RangersIslandersDevils','W':44+35+34,'L':29+37+39,'year':2018})
    LA = pd.Series({'team':'KingsDucks','W':44+45,'L':29+25,'year':2018})
    nhl_df = nhl_df.append([NYC,LA],ignore_index=True)
    nhl_df = nhl_df.drop(index =[0,9,18,26,14,16,17,28,30])
    nhl_df.drop([ 'GP','OL', 'PTS', 'PTS%', 'GF', 'GA', 'SRS', 'SOS',
           'RPt%', 'ROW', 'League'],axis=1,inplace=True)

    nhl_df['W'] = pd.to_numeric(nhl_df['W'])
    nhl_df['L'] = pd.to_numeric(nhl_df['L'])
    total_game = nhl_df['W']+nhl_df['L']
    nhl_df['win_loss'] = nhl_df['W']/total_game
    #print(nhl_df)
    
    cities['team']= cities['NHL'].str.replace(r'\[[a-z]+\s[0-9]+\]','')
    col = ['NFL', 'MLB', 'NBA','NHL']
    cities = cities.drop(col, axis =1)
    #print(cities)


    merged = pd.merge(cities, nhl_df,on = 'team')
    
    merged['Population (2016 est.)[8]'] = pd.to_numeric(merged['Population (2016 est.)[8]'])
    merged['win_loss']=pd.to_numeric(merged['win_loss'])
    
    
    #raise NotImplementedError()
    
    population_by_region = [] # pass in metropolitan area population from cities
    for i in merged['Population (2016 est.)[8]']:
        population_by_region.append(i)
        
    win_loss_by_region = [] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    for n in merged['win_loss']:
        win_loss_by_region.append(n)
 
        
    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
nhl_correlation()


# In[ ]:





# ## Question 2
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NBA** using **2018** data.

# In[11]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nba_df=pd.read_csv("assets/nba.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
#nba_df = nba_df.set_index('team')
#print(nba_df['team'])

def nba_correlation():
    
    # YOUR CODE HERE
    mynba = nba_df.copy()
    mynba = mynba[mynba['year']==2018]
    
    
    mynba['team'] = mynba['team'].str.extract(r'(.+(?=\s\(\d+\)))')
    mynba['team']= mynba['team'].str.replace(r'(\*)','')
    mynba['team']=mynba['team'].str.replace(r'([A-Z][a-z]+\s)','')
    mynba['team']=mynba['team'].replace({'Blazers':'Trail Blazers'})
    NYC = pd.Series({'team':'KnicksNets','W':29+28,'L':53+54,'year':2018})
    LA = pd.Series({'team':'LakersClippers','W':42+35,'L':40+47,'year':2018})
    mynba = mynba.append([NYC,LA],ignore_index=True)
    mynba.drop(index=[10,11,24,25],inplace = True)
    mynba.drop(['W/L%', 'GB', 'PS/G', 'PA/G', 'SRS','League'], axis=1, inplace=True)
    mynba['W']=pd.to_numeric(mynba['W'])
    mynba['L']=pd.to_numeric(mynba['L'])
    mynba['ratio']=mynba['W']/(mynba['W']+mynba['L'])
    
    mycity = cities.copy()
    mycity.drop(['NFL', 'MLB','NHL'],axis=1,inplace=True)
    mycity['NBA'] = mycity['NBA'].str.replace(r'\[[a-z]+\s[0-9]+\]','')
    mycity = mycity.rename(columns = {'NBA':'team'})
    mycity['Population (2016 est.)[8]'] = pd.to_numeric(mycity['Population (2016 est.)[8]'])
    #print(mycity)
    
    merged2 = pd.merge(mycity, mynba, on = 'team')
    print(merged2)
    
    #print(mynba)
    #raise NotImplementedError()
    
    population_by_region = [x for x in merged2['Population (2016 est.)[8]']] # pass in metropolitan area population from cities
    #print(population_by_region)
    win_loss_by_region = [i for i in merged2['ratio']] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]
    #print(win_loss_by_region)
    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
nba_correlation()


# In[ ]:





# ## Question 3
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **MLB** using **2018** data.

# In[128]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]


def mlb_correlation(): 
    # YOUR CODE HERE
    mymlb = mlb_df.copy()
    mymlb = mymlb[mymlb['year']==2018]
    mymlb['team']=mymlb['team'].str.replace(r'[A-Z][a-z]+\s','')
    mymlb.loc[0,'team']= 'Red Sox'
    mymlb['team']=mymlb['team'].replace({'Sox':'White Sox','Jays':'Blue Jays','St. Cardinals':'Cardinals'})
    mymlb.drop(['W-L%','GB','year','League'],axis=1,inplace=True)
    mymlb = mymlb.append(mymlb.iloc[1]+mymlb.iloc[18],ignore_index=True)
    mymlb = mymlb.append(mymlb.iloc[25]+mymlb.iloc[13],ignore_index=True)
    mymlb = mymlb.append(mymlb.iloc[28]+mymlb.iloc[11],ignore_index=True)
    mymlb = mymlb.append(mymlb.iloc[21]+mymlb.iloc[8],ignore_index=True)
    mymlb.drop([1,18,13,25,11,28,8,21],inplace=True)
    mymlb['W']=pd.to_numeric(mymlb['W'])
    mymlb['L']=pd.to_numeric(mymlb['L'])
    mymlb['ratio']= mymlb['W']/(mymlb['W']+mymlb['L'])
    
  
    
    mycity = cities.copy()
    mycity.drop(['NFL','NBA','NHL'],axis=1,inplace=True)
    mycity['MLB'] = mycity['MLB'].str.replace(r'\[[a-z]+\s[0-9]+\]','')
    mycity= mycity.rename(columns = {'MLB':'team'})
    mycity['Population (2016 est.)[8]'] = pd.to_numeric(mycity['Population (2016 est.)[8]'])

    
    merged3 = pd.merge(mycity, mymlb, on = 'team')
    #print(merged3.shape)
    #raise NotImplementedError()
    
    population_by_region = [x for x in merged3['Population (2016 est.)[8]']] # pass in metropolitan area population from cities
    win_loss_by_region = [i for i in merged3['ratio']] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
mlb_correlation()


# In[ ]:





# ## Question 4
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NFL** using **2018** data.

# In[187]:


11/16


# In[25]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def nfl_correlation(): 
    # YOUR CODE HERE
    mynfl = nfl_df.copy()
    mynfl = mynfl[mynfl['year']==2018]
    mynfl = mynfl[['L','W','team']]
    mynfl.drop(index=[0,5,10,15,20,25,30,35],inplace=True)
    #mynfl = mynfl.reset_index()
    
    mynfl['team']=mynfl['team'].str.replace(r'[A-Z][a-z]+\s|\*|\+','')
    mynfl['W'] = pd.to_numeric(mynfl['W'])
    mynfl['L'] = pd.to_numeric(mynfl['L'])
    mynfl = mynfl.reset_index()
    
    NYC = mynfl.iloc[19]+mynfl.iloc[3]
    mynfl = mynfl.append(NYC,ignore_index=True)
    mynfl = mynfl.append(mynfl.iloc[28]+mynfl.iloc[13],ignore_index=True)
    mynfl = mynfl.append(mynfl.iloc[30]+mynfl.iloc[15],ignore_index=True)
    mynfl.drop(index=[19,3,28,30,13,15],inplace=True)
    mynfl.drop(columns='index',axis=1,inplace=True)
    

    mynfl['ratio']= mynfl['W']/(mynfl['W']+mynfl['L'])
    #print(mynfl)
    
    mycity = cities.copy()
    mycity = mycity[['Metropolitan area','Population (2016 est.)[8]','NFL']]
    mycity['NFL'] = mycity['NFL'].str.replace(r'\[[a-z]+\s[0-9]+\]','')
    mycity['Population (2016 est.)[8]'] = pd.to_numeric(mycity['Population (2016 est.)[8]'])
    mycity.rename(columns = {'NFL':'team'},inplace = True)
    #print(mycity)
    
    merged4 = pd.merge(mycity, mynfl,on='team')
    print(merged4)
    #raise NotImplementedError()
    
    population_by_region = [x for x in merged4['Population (2016 est.)[8]']] # pass in metropolitan area population from cities
    win_loss_by_region = [i for i in merged4['ratio']] # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
nfl_correlation()


# In[ ]:





# In[ ]:





# ## Question 5
# In this question I would like you to explore the hypothesis that **given that an area has two sports teams in different sports, those teams will perform the same within their respective sports**. How I would like to see this explored is with a series of paired t-tests (so use [`ttest_rel`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html)) between all pairs of sports. Are there any sports where we can reject the null hypothesis? Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this assignment.

# In[51]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

#mlb
mymlb = mlb_df.copy()
mymlb = mymlb[mymlb['year']==2018]
mymlb['team']=mymlb['team'].str.replace(r'[A-Z][a-z]+\s','')
mymlb.loc[0,'team']= 'Red Sox'
mymlb['team']=mymlb['team'].replace({'Sox':'White Sox','Jays':'Blue Jays','St. Cardinals':'Cardinals'})
mymlb.drop(['W-L%','GB','year','League'],axis=1,inplace=True)
mymlb = mymlb.append(mymlb.iloc[1]+mymlb.iloc[18],ignore_index=True)
mymlb = mymlb.append(mymlb.iloc[25]+mymlb.iloc[13],ignore_index=True)
mymlb = mymlb.append(mymlb.iloc[28]+mymlb.iloc[11],ignore_index=True)
mymlb = mymlb.append(mymlb.iloc[21]+mymlb.iloc[8],ignore_index=True)
mymlb.drop([1,18,13,25,11,28,8,21],inplace=True)
mymlb['W']=pd.to_numeric(mymlb['W'])
mymlb['L']=pd.to_numeric(mymlb['L'])
mymlb['ratio']= mymlb['W']/(mymlb['W']+mymlb['L'])
mycity = cities.copy()
mycity.drop(['NFL','NBA','NHL'],axis=1,inplace=True)
mycity['MLB'] = mycity['MLB'].str.replace(r'\[[a-z]+\s[0-9]+\]','')
mycity= mycity.rename(columns = {'MLB':'team'})
mycity['Population (2016 est.)[8]'] = pd.to_numeric(mycity['Population (2016 est.)[8]'])    
mergedmlb = pd.merge(mycity, mymlb, on = 'team')

#nba
mynba = nba_df.copy()
mynba = mynba[mynba['year']==2018]    
mynba['team'] = mynba['team'].str.extract(r'(.+(?=\s\(\d+\)))')
mynba['team']= mynba['team'].str.replace(r'(\*)','')
mynba['team']=mynba['team'].str.replace(r'([A-Z][a-z]+\s)','')
mynba['team']=mynba['team'].replace({'Blazers':'Trail Blazers'})
NYC = pd.Series({'team':'KnicksNets','W':29+28,'L':53+54,'year':2018})
LA = pd.Series({'team':'LakersClippers','W':42+35,'L':40+47,'year':2018})
mynba = mynba.append([NYC,LA],ignore_index=True)
mynba.drop(index=[10,11,24,25],inplace = True)
mynba.drop(['W/L%', 'GB', 'PS/G', 'PA/G', 'SRS','League'], axis=1, inplace=True)
mynba['W']=pd.to_numeric(mynba['W'])
mynba['L']=pd.to_numeric(mynba['L'])
mynba['ratio']=mynba['W']/(mynba['W']+mynba['L'])    
mycity = cities.copy()
mycity.drop(['NFL', 'MLB','NHL'],axis=1,inplace=True)
mycity['NBA'] = mycity['NBA'].str.replace(r'\[[a-z]+\s[0-9]+\]','')
mycity = mycity.rename(columns = {'NBA':'team'})
mycity['Population (2016 est.)[8]'] = pd.to_numeric(mycity['Population (2016 est.)[8]'])   
mergednba = pd.merge(mycity, mynba, on = 'team')
#nfl
mynfl = nfl_df.copy()
mynfl = mynfl[mynfl['year']==2018]
mynfl = mynfl[['L','W','team']]
mynfl.drop(index=[0,5,10,15,20,25,30,35],inplace=True) 
mynfl['team']=mynfl['team'].str.replace(r'[A-Z][a-z]+\s|\*|\+','')
mynfl['W'] = pd.to_numeric(mynfl['W'])
mynfl['L'] = pd.to_numeric(mynfl['L'])
mynfl = mynfl.reset_index()    
NYC = mynfl.iloc[19]+mynfl.iloc[3]
mynfl = mynfl.append(NYC,ignore_index=True)
mynfl = mynfl.append(mynfl.iloc[28]+mynfl.iloc[13],ignore_index=True)
mynfl = mynfl.append(mynfl.iloc[30]+mynfl.iloc[15],ignore_index=True)
mynfl.drop(index=[19,3,28,30,13,15],inplace=True)
mynfl.drop(columns='index',axis=1,inplace=True)
mynfl['ratio']= mynfl['W']/(mynfl['W']+mynfl['L'])
mycity = cities.copy()
mycity = mycity[['Metropolitan area','Population (2016 est.)[8]','NFL']]
mycity['NFL'] = mycity['NFL'].str.replace(r'\[[a-z]+\s[0-9]+\]','')
mycity['Population (2016 est.)[8]'] = pd.to_numeric(mycity['Population (2016 est.)[8]'])
mycity.rename(columns = {'NFL':'team'},inplace = True)
mergednfl = pd.merge(mycity, mynfl,on='team')
#nhl
nhl_df['team'] = nhl_df['team'].str.strip('*')
nhl_df = nhl_df[nhl_df['year'] == 2018]
nhl_df['team'] = nhl_df['team'].str.replace(r'[A-Z]\w+\s','')
nhl_df['team'] = nhl_df['team'].replace({'Leafs':'Maple Leafs','Wings':'Red Wings', 'Jackets':'Blue Jackets','Knights':'Golden Knights','St. Blues':'Blues'})
NYC = pd.Series({'team':'RangersIslandersDevils','W':44+35+34,'L':29+37+39,'year':2018})
LA = pd.Series({'team':'KingsDucks','W':44+45,'L':29+25,'year':2018})
nhl_df = nhl_df.append([NYC,LA],ignore_index=True)
nhl_df = nhl_df.drop(index =[0,9,18,26,14,16,17,28,30])
nhl_df.drop([ 'GP','OL', 'PTS', 'PTS%', 'GF', 'GA', 'SRS', 'SOS',
           'RPt%', 'ROW', 'League'],axis=1,inplace=True)

nhl_df['W'] = pd.to_numeric(nhl_df['W'])
nhl_df['L'] = pd.to_numeric(nhl_df['L'])
total_game = nhl_df['W']+nhl_df['L']
nhl_df['win_loss'] = nhl_df['W']/total_game
cities['team']= cities['NHL'].str.replace(r'\[[a-z]+\s[0-9]+\]','')
col = ['NFL', 'MLB', 'NBA','NHL']
cities = cities.drop(col, axis =1)
mergednhl = pd.merge(cities, nhl_df,on = 'team')
mergednhl['Population (2016 est.)[8]'] = pd.to_numeric(mergednhl['Population (2016 est.)[8]'])
mergednhl['win_loss']=pd.to_numeric(mergednhl['win_loss'])
#print(mergednhl)

def sports_team_performance():
    # YOUR CODE HERE
    
    nba_mlb_df = pd.merge(mergednba, mergedmlb, on = 'Metropolitan area')
    nba_mlb_df = nba_mlb_df[['Metropolitan area','ratio_x','ratio_y']]
    nba_mlb_df = nba_mlb_df.rename(columns = {'ratio_x':'ratio_nba','ratio_y':'ratio_mlb'})
    p_nba_mlb = stats.ttest_rel(nba_mlb_df['ratio_nba'],nba_mlb_df['ratio_mlb'] )
    
    nba_nfl_df = pd.merge(mergednba, mergednfl, on = 'Metropolitan area')
    nba_nfl_df = nba_nfl_df[['Metropolitan area','ratio_x','ratio_y']]
    nba_nfl_df = nba_nfl_df.rename(columns = {'ratio_x':'ratio_nba','ratio_y':'ratio_nfl'})
    p_nba_nfl = stats.ttest_rel(nba_nfl_df['ratio_nba'],nba_nfl_df['ratio_nfl'] )
    
    nba_nhl_df = pd.merge(mergednba, mergednhl, on = 'Metropolitan area')
    nba_nhl_df = nba_nhl_df[['Metropolitan area','ratio','win_loss']]
    nba_nhl_df = nba_nhl_df.rename(columns = {'ratio':'ratio_nba','win_loss':'ratio_nhl'})
    p_nba_nhl = stats.ttest_rel(nba_nhl_df['ratio_nba'],nba_nhl_df['ratio_nhl'] )
    
    nfl_mlb_df = pd.merge(mergednfl, mergedmlb, on = 'Metropolitan area')
    nfl_mlb_df = nfl_mlb_df[['Metropolitan area','ratio_x','ratio_y']]
    nfl_mlb_df = nfl_mlb_df.rename(columns = {'ratio_x':'ratio_nfl','ratio_y':'ratio_mlb'})
    p_nfl_mlb = stats.ttest_rel(nfl_mlb_df['ratio_nfl'],nfl_mlb_df['ratio_mlb'] )
    
    nfl_nhl_df = pd.merge(mergednfl, mergednhl, on = 'Metropolitan area')
    nfl_nhl_df = nfl_nhl_df[['Metropolitan area','ratio','win_loss']]
    nfl_nhl_df = nfl_nhl_df.rename(columns = {'ratio':'ratio_nfl','win_loss':'ratio_nhl'})
    p_nfl_nhl = stats.ttest_rel(nfl_nhl_df['ratio_nfl'],nfl_nhl_df['ratio_nhl'] )
    
    mlb_nhl_df = pd.merge(mergedmlb, mergednhl, on = 'Metropolitan area')
    mlb_nhl_df = mlb_nhl_df[['Metropolitan area','ratio','win_loss']]
    mlb_nhl_df = mlb_nhl_df.rename(columns = {'ratio':'ratio_mlb','win_loss':'ratio_nhl'})
    p_mlb_nhl = stats.ttest_rel(mlb_nhl_df['ratio_mlb'],mlb_nhl_df['ratio_nhl'] )
   
    
    #raise NotImplementedError()
    
    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)
    p_values.loc['NFL','NBA']= p_values.loc['NBA','NFL'] = p_nba_nfl[1]
    p_values.loc['NFL','NHL']= p_values.loc['NHL','NFL'] = p_nfl_nhl[1]
    p_values.loc['NFL','MLB']= p_values.loc['MLB','NFL'] = p_nfl_mlb[1]
    p_values.loc['NBA','NHL']= p_values.loc['NHL','NBA'] = p_nba_nhl[1]
    p_values.loc['NBA','MLB']= p_values.loc['MLB','NBA'] = p_nba_mlb[1]
    p_values.loc['NHL','MLB']= p_values.loc['MLB','NHL'] = p_mlb_nhl[1]
    
    
    
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values
sports_team_performance()


# In[ ]:




