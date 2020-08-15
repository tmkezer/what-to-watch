import flask
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__, template_folder='templates')

df2 = pd.read_csv('./model/final_movies.csv')

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['combined_features'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

#df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title_year'])
all_titles = [df2['title_year'][i] for i in range(len(df2['title_year']))]

def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['title'].iloc[movie_indices]
    dat = df2['year'].iloc[movie_indices]
    img = df2['img_url'].iloc[movie_indices]
    des = df2['description'].iloc[movie_indices]
    dir = df2['director_spaces'].iloc[movie_indices]
    act = df2['actors_spaces'].iloc[movie_indices]
    vote = df2['avg_vote'].iloc[movie_indices]
    return_df = pd.DataFrame(columns=['Title','Year', 'img_url', 'description', 'director', 'actors', 'avg_vote'])
    return_df['Title'] = tit
    return_df['Year'] = dat
    return_df['img_url'] = img
    return_df['description'] = des
    return_df['director'] = dir
    return_df['actors'] = act
    return_df['avg_vote'] = vote
    return return_df

# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('tk_test.html'))
            
    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        m_name = m_name.title()
#        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
        if m_name not in all_titles:
            return(flask.render_template('negative.html',name=m_name))
        else:
            result_final = get_recommendations(m_name)
            #print(result_final)
            names = []
            dates = []
            posters = []
            descriptions = []
            directors = []
            actors = []
            votes = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                dates.append(result_final.iloc[i][1])
                posters.append(result_final.iloc[i][2])
                descriptions.append(result_final.iloc[i][3])
                directors.append(result_final.iloc[i][4])
                actors.append(result_final.iloc[i][5])
                votes.append(result_final.iloc[i][6])
            #print(names, dates, posters)
            return flask.render_template('tk_rec.html',movie_names=names,movie_date=dates,movie_posters=posters, \
                movie_descriptions=descriptions, movie_directors=directors, movie_actors=actors, movie_votes=votes, \
                search_name=m_name)

if __name__ == '__main__':
    app.run(debug=True, port=5001)