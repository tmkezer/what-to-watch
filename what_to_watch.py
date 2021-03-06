import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("IMDB_movies_clean.csv")

df['avg_vote'] = df['avg_vote'].astype(str)
df['year'] = df['year'].astype(str)
df['description'] = df['description'].astype(str)

for i in ["director","writer", "actors", "production_company"]:
    df[i] = df[i].str.replace(' ', '')

for i in ["director","writer", "actors", "production_company"]:
    df[i] = df[i].str.replace(',', ' ')

features = ['title', 'director', 'year', 'genre', 'keywords', 'production_company', 'writer', 'actors']

def combine_features(row):
    return row['title']+" "+((row['director'] +" ") * 2)+" "+row['year']+" "+((row['genre'] +" ") * 2)+" "+row['keywords']+" "+row['production_company']+" "+row['writer']+" "+row['actors']

for feature in features:
    df[feature] = df[feature].fillna('') #filling all NaNs with blank string

df["combined_features"] = df.apply(combine_features,axis=1) #applying combined_features() method over each rows of dataframe and storing the combined string in "combined_features" column

cv = CountVectorizer() #creating new CountVectorizer() object
count_matrix = cv.fit_transform(df["combined_features"]) #feeding combined strings(movie contents) to CountVectorizer() object

cosine_sim = cosine_similarity(count_matrix)

df = df.reset_index()

def get_title_from_index(index):
    return df[df.index == index]["title_year"].values[0]
def get_index_from_title(title_year):
    return df[df.title_year == title_year]["index"].values[0]

movie_user_likes = input("Enter Movie Title: ") 

movie_index = get_index_from_title(movie_user_likes)
similar_movies = list(enumerate(cosine_sim[movie_index])) #accessing the row corresponding to given movie to find all the similarity scores for that movie and then enumerating over it

sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

i=0
print("Top 6 similar movies to "+movie_user_likes+" are:\n")
for element in sorted_similar_movies:
    print(get_title_from_index(element[0]))
    i=i+1
    if i>5:
        break