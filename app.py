import requests # send req to external APIs
import streamlit as stream
import pickle
import gdown
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent # Path finds the path of the parent of current file we are working in i.e app.py
# # current working file accesed with __file__
# # BASE_DIR stores path to parent folder of app.py i.e our movie-recommendation-system folder

# movies = pickle.load(open(BASE_DIR / 'movies.pkl', 'rb'))  # open specifies the path of file to open and store in movies object
# # BASE_DIR IS C:\Users\sanik\placement campusx\project\Movie-Recommendation-System and in front of that  'movies.pkl'
# # means entire path is specified to open the file movies.pkl and the path is
# # C:\Users\sanik\placement campusx\project\Movie-Recommendation-System\movies.pkl
# # load in binary and store in movies

# similarity = pickle.load(open(BASE_DIR / 'sim.pkl', 'rb'))
# # same as above load sim matrix here

# loading files
movies_path = BASE_DIR / 'movies.pkl'
similarity_path = BASE_DIR / 'sim.pkl'

# Download similarity matrix if it doesn't exist
if not similarity_path.exists():

    url = 'https://drive.google.com/uc?id=18qI340U7D8TMTqZlJnkY4MnbmQNVoxvV'

    with stream.spinner('Downloading movie similarity data...'):
        gdown.download(url, str(similarity_path), quiet=False)

# Load pickle files
movies = pickle.load(open(movies_path, 'rb'))

similarity = pickle.load(open(similarity_path, 'rb'))

# API connection
TMDB_API_TOKEN = stream.secrets["TMDB_API_TOKEN"]  # access the tmdb api token stored in .streamlit folder and secrets.toml file

# to send req these are headers
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_TOKEN}"
}

stream.title('Movie Recommendation System')

# select drop down menu for movies
movie_list = movies['original_title'].values
selected_movie = stream.selectbox(  # selected_movie stores user selected movie name
    'Select a movie:',  # shows on the box
    movie_list  # options listed in it are movie names
)

# function to fetch poster
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:

            data = response.json()

            poster_path = data.get('poster_path')

            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

    except requests.exceptions.RequestException:
        pass

    return None

# recommend function
def recommend(movie_name):
    
    # extract the row idx of the movie from movies dataset
    movie_row_idx=movies[movies['original_title']==movie_name].index[0]
    
    # extract similarity score of that movie with every other movie from similarity matrix
    sim_scores=similarity[movie_row_idx]
    
    # now these scores give indexes and arrange in decsending order from highest sim score to lowest sim score
    sim_scores_sorted=sorted(
        list(enumerate(sim_scores)),  # looks like [(0,1),(1,0.5),(2,0.4),(3,0.9)....(10,0.85)] # idx of movie and sim score of curr movie with that movie
        key=lambda x:x[1],  # x is a tuple in the list above sort on basis of 2nd element of tuple i.e sim score
        reverse=True  # in desc order
    )
    
    top_5=[] # will store id and name of top 5 movies
    
    for i in range(1,6): # start with idx1 cause at idx0 of sim_scores_sorted is same movie with sim score 1
        similar_movie_idx=sim_scores_sorted[i][0]  # let say i=1 then sim_scores_sorted[1] is (1,0.9) let say its 0th element i.e 1 i.e idx you access
        # here you are acceesing the idx no of the movies sim to curr movie 
        
        # extract name of that movie from movies dataset and using idx extracted above and store in top_5
        top_5.append((movies['id'].iloc[similar_movie_idx],movies['original_title'].iloc[similar_movie_idx]))
        
    return top_5




#recommendation button do properly return id and title
# if stream.button('Recommend'):
    
#     recommendations=recommend(selected_movie)
    
#     stream.subheader('Top recommended movies')
    
#     # index,movie move along the tuple elements 
#     for index,movie in enumerate(recommendations,start=1):  # enumerate converts recommendations into a list of tuples as follows
#         # eg [(0,Aliens),(1,Stark),(2,Game)]
#         # by doing start=1 we start numbering idx from 1 i.e [(1,Aliens),(2,Stark),(3,Game)]
#         print(f'{index}.{movie}')  # print idx and movie
     
# need to display posters also

if stream.button('Recommend'):  # if Recommend button is pressed

    recommendations = recommend(selected_movie)  # call recommend function pass movie name selected from drop down 
    # the recommend function returns a list of tuples where each tuple has movie id and movie title stoe=re that in recommendations
     
    stream.subheader('Recommended Movies') # add heading before displaying 

    cols = stream.columns(5)  # create 5 cols side by side col0 | col1 | col2 | col3 | col4

    for index, (movie_id, movie_title) in enumerate(recommendations):

        poster = fetch_poster(movie_id) # call fetch poster function and pass the movie_ids one by one 
        # poster url is stored in poster

        with cols[index]:   # index by idx access cols
            stream.text(movie_title)  # in the selected col (let say index is 0 so in col0) write the movie name

            # if poster url exists display image in same col below title
            if poster:
                stream.image(poster)
            else:  # if not give error
                stream.write('Poster unavailable')



                