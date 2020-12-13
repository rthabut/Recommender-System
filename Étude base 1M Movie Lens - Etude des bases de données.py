#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
import numpy as np 
#import functions as fct
from sklearn import decomposition
from sklearn import preprocessing
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import seaborn as sns
from matplotlib.collections import LineCollection


# # Creation de la base de donnée.

# In[4]:


ratings=pd.read_table('C:/Users/rapha/OneDrive/Documents/ENSAE Travail/2A/Info/ml-1m/ratings.dat',sep="::",engine='python',names=['UserID','MovieID','Rating','Timestamp'])
users=pd.read_table('C:/Users/rapha/OneDrive/Documents/ENSAE Travail/2A/Info/ml-1m/users.dat',sep="::",engine='python',names=['UserID','Gender','Age','Occupation','Zip-code'])
movies=pd.read_table('C:/Users/rapha/OneDrive/Documents/ENSAE Travail/2A/Info/ml-1m/movies.dat',sep="::",engine='python',names=['MovieID','Title','Genres'])
links=pd.read_csv('C:/Users/rapha/OneDrive/Documents/ENSAE Travail/2A/Info/ml-25m/links.csv')


# On va étudier chaque datframe.

# In[5]:


links.head()


# links donne les identifiants des films dans la base de donnée d'IMDb.  

# In[6]:


links.info()


# In[7]:


movies.tail()


# In[8]:


movies.info()


# On va réaliser une jointure afin d'avoir les identifiants de Movielens et d'IMDb pour chaque films.

# In[9]:


print('avant la jointure il y a')
print(movies.shape[0]) 
print('films')
links['MovieID']=links['movieId']
del links['movieId']
#On renomme la colonne pour realiser la jointure. 
movies=movies.merge(links,on='MovieID',how='inner')
print('après la jointure il y a')
print(movies.shape[0]) 
print('films')


# On va rajouter une colonne rating au dataframe movie, qui donne la note moyenne du film.    
# Pour cela on va utiliser les notes fournies par la base de données d'imdb. On a en effet plus de votes disponibles avec cette base de données qu'avec MovieLens.   
# Pour accéder aux notes, on va ouvrir la base de donnée d'IMDb et utiliser la variable imdbId. 

# In[13]:


title_rating = pd.read_csv('C:/Users/rapha/OneDrive/Documents/ENSAE Travail/2A/Info/title.ratings.tsv', sep="\t") #Base de donnée d'IMDb


# In[9]:


title_rating.head()


# In[15]:


title_rating.info()


# On doit retirer les 'tt' dans la variable tconst. Les notes des utilsateurs movies sont sur 5, on va donc diviser par 2 la note IMDb. On change ensuite le nom de la variable tconst pour ensuite realiser une jointure sur la tablle movies.

# In[16]:


title_rating['imdbId']=title_rating['tconst'].str[2:]
title_rating['imdbId']=title_rating.imdbId.astype(int)
movies=movies.merge(title_rating,on='imdbId',how='inner')
#On enlève ensuite les colonnes qui ne sont pas utiles
del movies['tmdbId']
del movies['tconst']
movies['rating']=movies['averageRating']/2 #On met la note IMDb sur 5
del movies['averageRating']
del movies['numVotes']
print('après la jointure il y a')
print(movies.shape[0]) 
print('films')


# Une soixantaine de films ont été supprimé de la base de donnée. On va les retirer de la base de données. On les retire de la base rating.   

# In[17]:


ratings.head()


# In[20]:


ratings.info()


# On va enlever les films qui n'ont pas de notes dans la base de donnée ratings, ou qui ont été retiré lors de la jointure précédente.

# In[21]:


print('avant la jointure il y a')
print(ratings.shape[0]) 
print('ratings')
index=movies['MovieID'].to_frame()
ratings=ratings.merge(index,on='MovieID',how='inner')
print('après la jointure il y a')
print(ratings.shape[0]) 
print('ratings')


# On a perdu quelques notes, il y avait sans doute des doublons de movies qui ne correspondait à aucun films.

# On va modifier la variable timestamp, pour avoir l'année du rating.

# In[22]:


import time
ratings['Timestamp'] = ratings['Timestamp'].apply(lambda x: time.strftime('%Y', time.localtime(x)))
ratings.head()


# In[23]:


ratings.info() 


# In[24]:


users.head()


# In[25]:


users.info() #On regarde le type de chacune des variables

