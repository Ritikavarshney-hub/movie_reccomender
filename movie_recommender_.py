
# -*- coding: utf-8 -*-
"""movie recommender .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gRxrVoH2wbdJ7lFJcc_rcu_o1msCIiwD
"""

import pandas as pd
import numpy as np
import ast
movies=pd.read_csv('tmdb_5000_movies.csv')
credits=pd.read_csv('tmdb_5000_credits.csv')
print(type(movies))
print(movies.head())
movies=movies.merge(credits,on='title')
print(type(movies))
movies.head()
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.info()
movies.head()
movies.isnull().sum()
movies.dropna(inplace=True)
movies.iloc[0].genres
movies.duplicated().sum()
def convert(obj):
    l=[]
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l
movies['genres'] = movies['genres'].apply(convert)
import ast
def convert3(obj):
    l=[]
    c=0
    for i in ast.literal_eval(obj):
        if c!=3:
            l.append(i['name'])
            c+=1
        else:
            break
    return l

movies['cast'] = movies['cast'].apply(convert3)
def convert2(obj):
    l=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            l.append(i['name'])
            break
    return l
movies['crew'] = movies['crew'].apply(convert2)
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['keywords'] = movies['keywords'].apply(convert)
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
display(movies.head())

new_df=movies[['movie_id','title','tags']]
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
new_df.head()

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
vector=cv.fit_transform(new_df['tags']).toarray()
vector.shape
cv.get_feature_names_out()
from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vector)
similarity.shape

!pip install nltk

import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return "".join(y)
new_df['tags']=new_df['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
vector=cv.fit_transform(new_df['tags']).toarray()
vector.shape
cv.get_feature_names_out()
from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vector)
similarity.shape
def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)
recommend('Avatar')

cv.get_feature_names_out()

import pickle

pickle.dump(new_df.to_dict(),open('moviesdict.pkl','wb'))

pickle.dump(similarity,open('similarity.pkl','wb'))