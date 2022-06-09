#!/usr/bin/env python
# coding: utf-8

# # Project: Investigate a Dataset - [Dataset-name]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# This data set contains information about 10,000 movies collected from The Movie Database (TMDb).
# 
# > **The dataset columns are**:
# * imdb_id
# * popularity
# * budget
# * revenue
# * original_title
# * cast
# * homepage
# * director
# * tagline
# * keywords
# * overview
# * runtime
# * genres
# * production_companies
# * release_date
# * vote_count
# * vote_average
# * release_year
# * budget_adj
# * revenue_adj
# 
# 
# ### Question(s) for Analysis
# 
# 1. What are the most profitable movies?
# 2. What are the highly voted movies and their profits?
# 3. What is the trend in annual movie release?
# 4. What is the annual profits made from movies?
# 5. What is the comparison between popularity and profits made from movies?

# In[3]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas numpy seaborn matplotlib')


# <a id='wrangling'></a>
# ## Data Wrangling

# In[4]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv('Database_TMDb_movie_data/tmdb-movies.csv')
df.head(20)


# In[3]:


# Viewing the last 20 lines of data
df.tail(20)


# In[5]:


# Knowing how large the dataset is in terms of rows and columns
df.shape


# In[6]:


# Getting general info on dataset
df.info()


# In[7]:


# Getting the data type of each column
df.dtypes


# In[8]:


# Getting the descriptive statistics summary of dataframe
df.describe()


# In[9]:


# checking for null/missing values
df.isnull().sum()


# In[10]:


# checking for duplicated values
df.duplicated().sum()


# In[11]:


# checking for cases of repeated Original Titles
df['original_title'].duplicated().sum()


# In[12]:


# checking for unique values
df.nunique()


# 
# ### Data Cleaning

# *From __Data Wrangling__ done above, I have noted that the following cleaning need to done*
# 1. Remove duplicated data.
# 2. Remove null values.
# 3. Convert budget and revenue columns to float dtype
# 4. Fill zeroes/inaccurate data in budget,budget_adj values and revenue,revenue_adj values.
# 5. Drop redundant columns and correcting datatypes.
# 6. Split values in every colunm, that are separated with pipe "|"

# In[5]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.

# 1. Remove duplicated data.
df.drop_duplicates(inplace=True)

# Checking if duplicated data have been removed
df.duplicated().sum()


# In[6]:


# 2. Remove null values.
interest_columns = ['cast', 'director', 'genres', 'production_companies']
for col in interest_columns :
    df = df[~df[col].isnull()]
df.info()


# In[7]:


# 3. Convert budget, revenue columns to float dtype
df.budget = df.budget.astype('float')
df.revenue = df.revenue.astype('float')
df.head(20)


# In[8]:


# 4. Fill zeroes/inaccurate data in budget,budget_adj values and revenue,revenue_adj values.
# View in information if zeroes are removed
col_zeroes = ['budget', 'revenue', 'budget_adj', 'revenue_adj']
for col in col_zeroes :
    df[col] = df[col].replace(0, np.nan)
    df[col] = df[col].fillna(df.groupby('release_year')[col].transform('mean'))
    
df.info()


# In[9]:


# 5. Drop redundant columns and correcting datatypes.
df.drop(['imdb_id', 'homepage', 'tagline', 'keywords', 'overview', 'release_date'], axis=1, inplace=True)

# Making new order.
df = df[['original_title', 'release_year', 'runtime', 'production_companies','director', 'cast', 'genres', 'popularity', 'vote_average', 'vote_count', 'budget', 'budget_adj', 'revenue', 'revenue_adj']]


# Viewing information
df.info()


# In[11]:


# Checking if columns have been removed
df.head(20)


# In[12]:


# 6. Split values in every colunm, that are separated with pipe "|"
for col in interest_columns :
    df[col] = df[col].str.split("|")
df.head()


# In[7]:


# Add new column - profit
profit_movie= df['revenue_adj'] - df['budget_adj']

df['profit']=profit_movie
df.head(20)


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 

# In[22]:


# Plotting histogram of data
df.hist(bins=20,figsize=(50,50),color='red');


# ### Research Question 1 (What are the most profitable movies?)

# In[26]:


# Use this, and more code cells, to explore your data. Don't forget to add
#   Markdown cells to document your observations and findings.
most_profitable = df.sort_values('profit', ascending=False)
top_movies=most_profitable.loc[:,['original_title', 'profit', 'release_year']]
top_movies.head(20)


# In[5]:


# User defined function to avoid repetition of code when plotting
def plot_bar(col1,col2,plot_type):
    plt.figure(figsize=(16,8))
    df.groupby(col1)[col2].mean().sort_values(ascending=False)[:20].plot(kind=plot_type)
#     plt.title("")
#     plt.xlabel("")
#     plt.ylabel("")


# In[8]:


# Plotting bar graph of movies and profits made

# plt.figure(figsize=(50 * .5, 30 * .5))
# df.groupby('original_title')['profit'].mean().sort_values(ascending=False)[:20].plot(kind="bar")

plot_bar('original_title','profit','bar') # Calling pre-defined function and passing arguments
plt.title('Movies and profits made')
plt.xlabel('Movie name')
plt.ylabel('Profit');


# > According to the analysis made above, it is evident that __Star Wars__ is the most profitable movie

# ### Research Question 2  (What are the highly voted movies and their profits?)

# In[25]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.
vote = df.sort_values('vote_count', ascending=False)
top_movies=vote.loc[:,['original_title', 'vote_count', 'release_year']]
top_movies.head(20)


# In[9]:


# Plotting bar graph of most voted movies and their profits

# plt.figure(figsize=(50 * .5, 30 * .5))
# df.groupby('original_title')['vote_count'].mean().sort_values(ascending=False)[:20].plot(kind="bar")

plot_bar('original_title', 'vote_count', 'bar') # Calling pre-defined function and passing arguments
plt.title('Most Voted Movies and their profits')
plt.xlabel('Movie name')
plt.ylabel('Profit');


# > According to the analysis made above, vote count and profit have a positive correlation. It is evident that __Inception__ is the most voted movie and it have the highest profit.

# ### Research Question 3  (What is the trend in annual movie release?)

# In[19]:


# Plotting graph of number of movies released annually

df['release_year'].value_counts().plot(kind='bar', figsize=(16,16));
plt.title('Number of movies released annually')
plt.xlabel('Release Year');
plt.ylabel('Profits');


# > According to the analysis made above, I have observed that the number of movies released increases annually.

# ### Research Question 4  (What is the annual profits made from movies?)

# In[11]:


# Plotting a bar chart between the years and profits made from movies

df.groupby('release_year')['profit'].mean().sort_values(ascending=False).plot(kind="bar", figsize=(16,16))


# plot_bar('release_year', 'profit', 'bar') # Function is giving the first 20 data so I have not used it here as I want all output
plt.title('the revenue made in each year')
plt.xlabel('Year')
plt.ylabel('Profit');


# > According to the analysis made above, I have observed that highest profit was made in the year 1977 and the least profit was made in the year 1966.

# ### Research Question 5  (What is the comparison between popularity and profits made from movies?)

# In[17]:


# Plotting the relationship between popularity and profits made from movies
plt.figure(figsize=(16,16))
plt.scatter('popularity', 'profit', data=df)
plt.title('Relationship between movie popularity and profit')
plt.xlabel('Popluratiy')
plt.ylabel('Profit')
plt.show()


# > From the above plot, it may be observed that there is a slight positive correlation between movie __popularity__ and __profit__ made, that is profit increases with increase in movie popularity.

# <a id='conclusions'></a>
# ## Conclusions
# > From graph of _**Most Voted Movies and their profits**_, I have observed that vote count have influence on profit made. Therefore, profit increases with increase in vote count.
# 
# > The number of movies released, increase annually, hence movie production may be a great venture.
# 
# > Whenever movie becomes popular, profit seems to increase.
# 
# ### Limitations
# > Dropping alot of data due to the zero values leads to losing of a lot of data, hence we may not get the right insights from the data.
# 

# In[12]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




