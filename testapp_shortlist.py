
import os
import pandas as pd
import numpy as np
import math
#import tensorflow as tf
from math import pow, sqrt
import scipy.stats
import scipy.spatial
import scipy.stats as st
import random
from sklearn.metrics import mean_squared_error


def get_rating_(userid, movieid):
    return (ratings.loc[(ratings.userId==userid) & (ratings.movieId == movieid),'rating'].iloc[0])

# Getting the list of all movie ids the specified user has rated.
def get_movieids_(userid):
    return (ratings.loc[(ratings.userId==userid),'movieId'].tolist())

# Getting the movie titles against the movie id.
def get_movie_title_(movieid):
    return (movies.loc[(movies.movieId == movieid),'title'].iloc[0])

def distance_similarity_score(user1,user2):
    '''
    user1 & user2 : user ids of two users between which similarity score is to be calculated.
    '''
    # Count of movies watched by both the users.
    both_watch_count = 0
    for element in ratings.loc[ratings.userId==user1,'movieId'].tolist():
        if element in ratings.loc[ratings.userId==user2,'movieId'].tolist():
            both_watch_count += 1
    if both_watch_count == 0 :
        return 0
    
    # Calculating distance based similarity between both the users.
    distance = []
    for element in ratings.loc[ratings.userId==user1,'movieId'].tolist():
        if element in ratings.loc[ratings.userId==user2,'movieId'].tolist():
            rating1 = get_rating_(user1,element)
            rating2 = get_rating_(user2,element)
            distance.append(pow(rating1 - rating2, 2))
    total_distance = sum(distance)
    
    # Adding one to the denominator to avoid divide by zero error.
    return 1/(1+sqrt(total_distance))

def pearson_correlation_score(user1,user2):
    '''
    user1 & user2 : user ids of two users between which similarity score is to be calculated.
    '''
    # A list of movies watched by both the users.
    both_watch_count = []
    
    # Finding movies watched by both the users.
    for element in ratings.loc[ratings.userId==user1,'movieId'].tolist():
        if element in ratings.loc[ratings.userId==user2,'movieId'].tolist():
            both_watch_count.append(element)
    
    # Returning '0' correlation for bo common movies.
    if len(both_watch_count) == 0 :
        return 0
    
    # Calculating Co-Variances.
    rating_sum_1 = sum([get_rating_(user1,element) for element in both_watch_count])
    rating_sum_2 = sum([get_rating_(user2,element) for element in both_watch_count])
    rating_squared_sum_1 = sum([pow(get_rating_(user1,element),2) for element in both_watch_count])
    rating_squared_sum_2 = sum([pow(get_rating_(user2,element),2) for element in both_watch_count])
    product_sum_rating = sum([get_rating_(user1,element) * get_rating_(user2,element) for element in both_watch_count])
    # Returning pearson correlation between both the users.
    numerator = product_sum_rating - ((rating_sum_1 * rating_sum_2) / len(both_watch_count))
    denominator = sqrt((rating_squared_sum_1 - pow(rating_sum_1,2) / len(both_watch_count)) * (rating_squared_sum_2 - pow(rating_sum_2,2) / len(both_watch_count)))
    
    # Handling 'Divide by Zero' error.
    if denominator == 0:
        return 0
    return numerator/denominator
    
def most_similar_users_(user1, number_of_users, index, metric='pearson'):
#index = starting index from where to search users, given as user_id!
        # Getting distinct user ids.

    user_ids = ratings.userId.unique().tolist()
    
    random_user_id = index
    sid=random_user_id
    eid=sid+10
    
    # Getting similarity score between targeted and every other suer in the list(or subset of the list).
    if(metric == 'pearson'):
        similarity_score = [(pearson_correlation_score(user1,nth_user),nth_user) for nth_user in user_ids[sid:eid] if nth_user != user1]
    else:
        similarity_score = [(distance_similarity_score(user1,nth_user),nth_user) for nth_user in user_ids[sid:eid] if nth_user != user1]
    
    # Sorting in descending order.
    similarity_score.sort()
    similarity_score.reverse()
    
    # Returning the top most 'number_of_users' similar users. 
    return similarity_score[:number_of_users]

def get_most_similar_users_(userid, index, user_ids):
#    user_ids = ratings.userId.unique().tolist()
    ratings_suser_ids = []
    llength = len(user_ids)
    print(llength)

    ratings_suser_ids = []

    sin = random.randint(0, llength-10)
    
    for i in range(sin,sin+index,10): 
        print(f"at step# {i} / out of {sin+index}")
        sim_users_ids = most_similar_users_(userid, 5, i)
        print("most similar users list", sim_users_ids)
        sindex = sim_users_ids[0][1]
        ratings_suser_ids.append(sindex)
#        ratings_suser_ids.append(user_ids[sindex]-1)
        print(f"sim_score {sim_users_ids[0][0]} and it's user_id {sindex}")
    
    return ratings_suser_ids

def get_recommendation_(userid, steps):
    
    user_ids = ratings.userId.unique().tolist()
    
    user_list = get_most_similar_users_(userid, steps*10, user_ids)
#    print("length of list: ", len(user_list), user_list)
        
    total = {}
    similariy_sum = {}
    
    for user in user_list:
#       print("user_id ", user)
        # not comparing the user to itself (obviously!)
        if user == userid:
            continue
        
        # Getting similarity score between the users.
        score = pearson_correlation_score(userid,user)
        print("main function score ", score)
        
        # not considering users having zero or less similarity score.
        if score <= 0:
            continue
         # Getting weighted similarity score and sum of similarities between both the users.
        for movieid in get_movieids_(user):
            # Only considering not watched/rated movies
            if movieid not in get_movieids_(userid) or get_rating_(userid,movieid) == 0:
       #         print("entered 'if' under main_ ")
                total[movieid] = 0
                total[movieid] += get_rating_(user,movieid) * score
                similariy_sum[movieid] = 0
                similariy_sum[movieid] += score
    
    # Normalizing ratings
    ranking = [(tot/similariy_sum[movieid],movieid) for movieid,tot in total.items()]
    ranking.sort()
    ranking.reverse()
    
    # Getting movie titles against the movie ids.
    recommendations = [get_movie_title_(movieid) for score,movieid in ranking]
    return recommendations[:6]

steps=1

# Reading movies dataset into a pandas dataframe object.
movies = pd.read_csv("./data/ml-latest/movies.csv", low_memory=False, encoding = 'latin-1')

# Reading ratings dataset into a pandas dataframe object.
ratings = pd.read_csv("./output/ratings_short.csv", low_memory=False, encoding = 'latin-1')
# Getting the rating given by a user to a movie.
aint = []
user_ids = ratings.userId.unique().tolist()
for a in user_ids:
    aint.append(int(a))
        
#min_uid = min(aint)
us_start = min(aint)
us_end = max(aint)
userin = int(input(f"Enter your yser id between: {us_start} and {us_end}: "))

recc_list = []
while (len(recc_list)==0):

    recc_list = get_recommendation_(userin, steps)

    print(f"Found reccomendations for user {userin}: {recc_list}")

# users_reccs=pd.DataFrame([{"userId":userin, "reccs": recc_list}])

# users_reccs.to_csv("./output/usrecc_for_short.csv")


