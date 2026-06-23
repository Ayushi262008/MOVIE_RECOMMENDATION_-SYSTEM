import streamlit as st
import pickle
import pandas as pd
import requests
import urllib.parse


# 1. New function replacing fetch_poster(movie_id)
def fetch_poster(movie_title):
    # Put your unique 8-character OMDb API key here
    api_key = "d4c7d8df"

    # URL-encode the movie name to handle spaces safely (e.g. "Iron Man" -> "Iron+Man")
    encoded_title = urllib.parse.quote(movie_title.strip())
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={encoded_title}"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True":
            poster_url = data.get("Poster")
            # Ensure OMDb actually has an image asset for it
            if poster_url and poster_url != "N/A":
                return poster_url

        # Fallback placeholder image if the poster is missing
        return "https://via.placeholder.com/500x750.png?text=Poster+Not+Found"
    except Exception:
        return "https://via.placeholder.com/500x750.png?text=Error"


# 2. Your core recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        # Get the title instead of movie_id since we are using OMDb
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        # Fetch the poster by passing the title string
        recommended_movies_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_movies_posters


# 3. Loading your datasets
# ... (your fetch_poster and recommend functions are above here)

# 3. Loading your datasets safely
import os
# This line finds the exact folder where your ayushi.py file is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# These lines use that folder path to find your .pkl files without getting lost
# Line 63: Notice the 's' in 'movies_dict.pkl' and the added 'rb'
movies_dict = pickle.load(open(os.path.join(BASE_DIR, 'movies_dict.pkl'), 'rb'))
movies = pd.DataFrame(movies_dict)
# Line 66: Added the missing 'rb' at the end of the open function
# similarity = pickle.load(open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb'))
# ==========================================
# # 3. Loading your datasets safely
# ==========================================
# ==============================================================================
# 3. Loading your datasets safely from OneDrive
# ==============================================================================
import pickle
import base64
import urllib.request
import pandas as pd

# Define paths safely using BASE_DIR
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_DICT_PATH = os.path.join(BASE_DIR, 'movies_dict.pkl')
PICKLE_FILE = os.path.join(BASE_DIR, 'similarity.pkl')

# Your exact OneDrive link
ONEDRIVE_SHARE_LINK = "https://1drv.ms/u/c/6E6089629DE166A2/IQAcqybHgTqfS4XbX_1U5V8WAUhz2DZyc8Wzbg-VagXng9Y?e=zyyWfI"


# Function to convert standard OneDrive share link to a direct download link
def create_onedrive_direct_download(sharing_url):
    base64_bytes = base64.b64encode(sharing_url.encode("utf-8"))
    base64_string = base64_bytes.decode("utf-8").replace('=', '').replace('/', '_').replace('+', '-')
    return f"https://api.onedrive.com/v1.0/shares/u!{base64_string}/root/content"


@st.cache_resource
def load_datasets():
    # 1. Load movies dictionary
    with open(MOVIES_DICT_PATH, 'rb') as f:
        movies_dict = pickle.load(f)
    movies_df = pd.DataFrame(movies_dict)

    # 2. PASTE THE NEW SAFETY CHECK CODE HERE:
    # If the file doesn't exist OR if it is tiny (less than 1MB, meaning it's corrupted)
    if not os.path.exists(PICKLE_FILE) or os.path.getsize(PICKLE_FILE) < 1000000:
        # Delete the broken tiny file first if it exists
        if os.path.exists(PICKLE_FILE):
            os.remove(PICKLE_FILE)

        with st.spinner("Downloading similarity matrix from OneDrive... Please wait."):
            direct_download_url = create_onedrive_direct_download(ONEDRIVE_SHARE_LINK)
            urllib.request.urlretrieve(direct_download_url, PICKLE_FILE)

    # 3. Load the downloaded similarity matrix file safely
    with open(PICKLE_FILE, 'rb') as f:
        similarity_matrix = pickle.load(f)

    return movies_df, similarity_matrix



# Initialize your datasets safely
movies, similarity = load_datasets()

# movies_dict = pickle.load(open(os.path.join(BASE_DIR, 'movie_dict.pkl'), 'rb'))

# movies = pd.DataFrame(movies_dict)
#

# similarity = pickle.load(open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb'))

# 4. Streamlit UI Layout
st.title('𝕐𝕠𝕦𝕣ℕ𝕖𝕩𝕥𝕎𝕒𝕥𝕔𝕙')
# ... (the rest of your Streamlit code follows below)
# movies = pd.DataFrame(movies_dict)
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# 4. Streamlit UI Layout
# st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    '📽️🍿 𝐒𝐞𝐚𝐫𝐜𝐡 𝐟𝐫𝐨𝐦 𝐨𝐯𝐞𝐫 𝟓,𝟎𝟎𝟎+ 𝐌𝐨𝐯𝐢𝐞𝐬 𝐭𝐨 𝐠𝐞𝐭 𝐬𝐭𝐚𝐫𝐭𝐞𝐝 :',
    movies['title'].values
)

if st.button('𝙂𝙚𝙣𝙚𝙧𝙖𝙩𝙚 𝙈𝙮 𝙒𝙖𝙩𝙘𝙝𝙡𝙞𝙨𝙩'):
    names, posters = recommend(selected_movie_name)

    # Note: Modern Streamlit uses st.columns(5) instead of st.beta_columns(5)
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


# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies =[]
#     for i in movies_list:
#         movie_id = i[0]
#         # fetch poster from API
#         recommended_movies.append(movies.iloc[i[0]].title)
#     return recommended_movies
#         # print(new_df.iloc[i[0]].title)
#
#
# movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# st.title('𝕐𝕠𝕦𝕣ℕ𝕖𝕩𝕥𝕎𝕒𝕥𝕔𝕙')
# selected_movies_name = st.selectbox(
#     label='🎥🍿 𝐂𝐡𝐨𝐨𝐬𝐞 𝐚 𝐒𝐞𝐞𝐝 𝐌𝐨𝐯𝐢𝐞 𝐭𝐨 𝐬𝐭𝐚𝐫𝐭 𝐰𝐢𝐭𝐡 𝐎𝐯𝐞𝐫 𝟓𝟎𝟎𝟎+ 𝐌𝐨𝐯𝐢𝐞 :',
#     options=movies['title'].values
# )
# if st.button('RECOMMENDATION'):
#     recommendations=recommend(selected_movies_name)
#     for i in recommendations:
#         st.write(i)
#
#
