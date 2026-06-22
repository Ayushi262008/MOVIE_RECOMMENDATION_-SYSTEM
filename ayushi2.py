import streamlit as st
import pickle
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")


# 2. Load the ML Model and Data
@st.cache_resource  # Keeps the app fast by caching the data
def load_data():
    # Load your movie list dataframe
    movies = pickle.load(open('movies_dict.pkl', 'rb'))
    movies_df = pd.DataFrame(movies)

    # Load your similarity matrix (the core ML model)
    similarity = pickle.load(open('movie_recommender.pkl', 'rb'))
    return movies_df, similarity


try:
    movies_df, similarity = load_data()
except FileNotFoundError:
    st.error("Please place your 'movies_dict.pkl' and 'movie_recommender.pkl' files in the project directory.")
    st.stop()


# 3. Recommendation Logic Function
def recommend(movie_name):
    # Find the index of the movie
    movie_index = movies_df[movies_df['title'] == movie_name].index[0]
    # Fetch distances/similarities
    distances = similarity[movie_index]
    # Sort them to get top 5 similar movies
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies_df.iloc[i[0]].title)
    return recommended_movies


# 4. User Interface (UI) Design
st.title("🎬 Movie Recommendation System")
st.write("Find your next favorite movie based on our Machine Learning model.")

# Dropdown menu for picking a movie
selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown:',
    movies_df['title'].values
)

# Recommend Button
if st.button('Recommend'):
    with st.spinner('Analyzing your taste...'):
        recommendations = recommend(selected_movie_name)

    st.success("Here are the top 5 movies you might like:")

    # Display recommendations in neat columns
    cols = st.columns(5)
    for index, col in enumerate(cols):
        with col:
            st.markdown(f"**{recommendations[index]}**")
            # Optional: Add a placeholder image or fetch real posters here
            st.image("https://via.placeholder.com/150x220?text=Movie", use_container_width=True)