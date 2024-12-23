import streamlit as st
import pickle
import pandas as pd
import requests


# Load data and models
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('feature_similarities.pkl', 'rb'))
# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=28784089caa8c08abb24103179062cf2'
    )
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

# Function to recommend movies based on the selected criteria
def recommend(movie, criteria):
    feature_column = {
        "story": "overview",
        "genres": "genres",
        "keywords": "keywords",
        "actors": "cast",
        "director": "crew",
        "tags": "tags",  # Default
    }.get(criteria.lower(), "tags")

    similarity_matrix = similarity.get(feature_column)
    
    if similarity_matrix is None:
        raise ValueError(f"No similarity matrix found for the selected feature: {criteria}")
    
    # Find the movie index
    try:
        movie_index = movies[movies["title"] == movie].index[0]
    except IndexError:
        raise ValueError(f"The movie '{movie}' was not found in the dataset.")

    distances = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster



# Streamlit interface
st.title("Enhanced Movie Recommender System")

# User input
selected_movie_name = st.selectbox("Select a movie:", movies['title'].values)

criteria = st.radio(
    "On what basis would you like recommendations?",
    ("Story", "Director", "Actors", "Technicians", "Keywords")
)

if st.button("Recommend"):
    # Generate recommendations
    names, posters = recommend(selected_movie_name, criteria)
    
    if names:
        # Dynamically create columns based on the number of recommendations
        cols = st.columns(len(names))
        for idx, col in enumerate(cols):
            with col:
                st.text(names[idx])
                st.image(posters[idx])
    else:
        st.error("No recommendations found for the selected criteria!")