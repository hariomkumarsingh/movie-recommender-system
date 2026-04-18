import streamlit as st
import pickle
import pandas as pd
import requests
import os
def download_file(url, filename):
    if not os.path.exists(filename):
        st.write(f"Downloading {filename}...")
        r = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)
movie_dict_url = "https://drive.google.com/uc?id=1gz5rAK-9nHEbPasjGGNWx0mG-jWBrEMZ"
similarity_url = "https://drive.google.com/uc?id=1MFFstzS1POeAnyz6tnfSJV23YeFsJn7H"

download_file(movie_dict_url, "movie_dict.pkl")
download_file(similarity_url, "similarity.pkl")

movie_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movie=pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
def fetch(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=dc864ac8630e1c25b05a82b9b2b46684&language=en-us'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(movie_name):
    movie_index = movie[movie['title'] == movie_name].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster=[]


    for i in movie_list:
        movie_id=movie.iloc[i[0]].movie_id
        recommended_movies.append(movie.iloc[i[0]].title)
        recommended_movies_poster.append(fetch(movie_id))

    return recommended_movies, recommended_movies_poster


st.title('movie recommender system')
selected_movie_name = st.selectbox('Select a movie:', movie['title'].values)
if st.button('Recommend'):
    name, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])
