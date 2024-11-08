import streamlit as st
import pickle
import pandas as pd
import requests
import time
import key  # Import the key module where the API key is stored

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={key.api}&language=en-US'  # Use the API key from key.py
    retries = 3  # Number of retries
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)  # Set a timeout of 5 seconds
            response.raise_for_status()  # Raises an error for HTTP issues
            data = response.json()
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Wait for 2 seconds before retrying
            else:
                return "https://via.placeholder.com/500"  # Placeholder image if all retries fail

def recommend(movie):
    # Get the index of the movie that matches the title
    movie_index = movies[movies['title'] == movie].index[0]

    # Get the distances (similarity scores) for the specified movie
    distances = similarity_matrix[movie_index]

    # Sort the movies based on their similarity scores in descending order
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # Exclude the first movie itself

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']  # Ensure 'id' is the correct column name for movie IDs
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load the movie dictionary
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))

# Convert to DataFrame
movies = pd.DataFrame(movies_dict)

# Load the similarity matrix
similarity_matrix = pickle.load(open('similarity_matrix.pkl', 'rb'))

# Title for the app
st.title("Movie Recommender System")

# Create a select box for movie titles
selected_movie_name = st.selectbox(
    'Choose a movie to get recommendations',
    movies['title'].values
)

# Display recommendations when the button is clicked
if st.button('Get Recommendations'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
