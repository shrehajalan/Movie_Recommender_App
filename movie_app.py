from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests



app = Flask(__name__)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b5e5bcb080ada56f3cd1c2120e30214e&language=en-US'.format(movie_id))
    data = response.json()
    return ('https://image.tmdb.org/t/p/w500/'+ data['poster_path'])

def recommend(movie):
    movies = pickle.load(open('movies.pkl','rb'))
    similarity = pickle.load(open('similarity.pkl','rb'))

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]
    rec_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movie_poster = []

    for i in rec_list:
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_movie_poster.append(fetch_poster(movies.iloc[i[0]]['movie_id']))

    return recommended_movies,recommended_movie_poster

@app.route('/')
def index():
    movies = pickle.load(open('movies.pkl','rb'))
    movies_list = movies['title'].values
    return render_template('homepage.html', movies_list=movies_list)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    selected_movie_name = request.form['selected_movie_name']
    names, posters = recommend(selected_movie_name)

    return render_template('recommend.html', names=names, posters=posters)


if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=8080)

