import streamlit as st
import pickle
import pandas as pd
import requests

st.title("Movie Recommendation System") 

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    # Inside the request.get, we write the url for the json file from which we can obtain the poster path of the movie
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=fa6ff91687ac7098baa28b95ff00407d&language=en-US'.format(movie_id))
    data = response.json()
    # Here the response from the url is converted into a json format so that we can obtain the poster path of that movie
    # and also for the complete path, we need to combine the poster path and the tmdb image path
    return 'http://image.tmdb.org/t/p/w500/' + data['poster_path'] 


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movie_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_poster = []
    for i in movie_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        # fetch movie poster from the api
        recommended_movie_poster.append(fetch_poster(movie_id))
    return recommended_movie_names,recommended_movie_poster
 

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values,
    index=None,
    placeholder="Movies...",
)


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])