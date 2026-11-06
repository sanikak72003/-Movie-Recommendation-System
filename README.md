Movie Recommendation System

A content-based movie recommendation system built using Python and Streamlit.
This application recommends movies based on the similarity of their content, including genres, keywords, cast, and other movie-related information.
Users can select a movie and receive a list of similar movies along with their posters fetched using the TMDB API.

Features
Content-based movie recommendations
Interactive movie selection using Streamlit
Similarity-based recommendations using cosine similarity
Movie poster fetching through the TMDB API
Automatic downloading of the similarity matrix when the application starts
Precomputed similarity scores for faster recommendations

Technologies Used
Python
Pandas
Scikit-learn
NumPy
Streamlit
Requests
TMDB API
Google Drive / gdown
Git and GitHub
Jupyter Notebook

How It Works
The recommendation system follows these steps:
Dataset Collection: Uses the TMDB 5000 Movies and TMDB 5000 Credits datasets containing movie metadata, genres, keywords, cast, crew, and overviews.
Data Preprocessing: Merges the two datasets using movie IDs and extracts relevant information, including genres, keywords, cast, director, and overview.
Feature Engineering: Combines the extracted information into a single text column called tags for each movie.
Text Vectorization: Uses CountVectorizer from Scikit-learn to convert movie tags into numerical feature vectors. The vectorizer uses a maximum of 5,000 features and removes English stop words.
Similarity Calculation: Uses cosine similarity to calculate how similar each movie is to every other movie based on its numerical representation.
Recommendation Generation: When a user selects a movie, the system retrieves its similarity scores, ranks other movies in descending order, excludes the selected movie itself, and returns the five most similar movies.

Poster Fetching
The application uses the TMDB API to retrieve movie posters.
Movie Identification: Each movie's unique TMDB ID is passed to the API instead of its title. This avoids ambiguity caused by duplicate movie names.
API Request: The requests library sends an HTTP GET request to the TMDB movie endpoint. Authentication is handled using a Bearer token stored in Streamlit secrets.
Response Processing: TMDB returns movie information in JSON format. The response.json() method converts this response into Python objects.
Poster Extraction: The application extracts the poster_path using the dictionary's .get() method. This safely handles cases where poster information is unavailable.
Image URL Construction: The relative poster path is combined with TMDB's image base URL to generate the complete image URL.
Error Handling: The function handles network errors and missing poster information so that an unsuccessful poster request does not crash the application.

Project Structure
Movie-Recommendation-System/
│
├── app.py
├── requirements.txt
├── movies.pkl
├── README.md
├── .gitignore
│
├── dataset/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
├── notebooks/
│   └── movie_recommendation.ipynb
│
└── .streamlit/
    └── secrets.toml (local only, not uploaded)

Important Files and Folders
app.py: Contains the Streamlit application, recommendation function, and TMDB API integration.
requirements.txt: Lists the Python libraries required to run the application.
movies.pkl: Stores the processed movie dataset used by the application.
dataset/: Contains the original movie and credits CSV datasets.
notebooks/: Contains the Jupyter Notebook used for data preprocessing, feature engineering, vectorization, and similarity calculations.
.streamlit/secrets.toml: Stores the TMDB API token securely on the local machine. It is excluded from GitHub.
.gitignore: Specifies files and folders that Git should not upload to the repository.

Similarity Matrix Storage
The sim.pkl file contains the precomputed cosine similarity matrix.
Since the file is approximately 185 MB, it is hosted on Google Drive instead of being committed to GitHub.
The application automatically downloads it when it is missing from the project directory using the gdown library.

Installation and Setup
1. Clone the Repository
git clone https://github.com/sanikak72003/-Movie-Recommendation-System.git
2. Navigate to the Project Directory
cd -Movie-Recommendation-System
3. Install Dependencies
pip install -r requirements.txt
4. Configure TMDB API Token
Create a folder named .streamlit in the project root if it does not already exist.
Inside it, create a file named secrets.toml and add:
TMDB_API_TOKEN = "your_tmdb_bearer_token"
Replace the placeholder with your own TMDB API Bearer token.
5. Run the Application
streamlit run app.py
The application will open in your browser.

Note: On the first run, the application automatically downloads the similarity matrix (sim.pkl) from Google Drive. An internet connection is required.

Dataset and External Resources
Dataset: TMDB 5000 Movie Dataset
Credits Dataset: TMDB 5000 Credits Dataset
Movie Posters and Metadata: The Movie Database (TMDB) API
Similarity Matrix: Hosted on Google Drive and downloaded automatically when required.

Future Improvements
Improve recommendation quality using TF-IDF and other text representation techniques.
Explore collaborative filtering and hybrid recommendation approaches.
Add more movie details such as ratings, release dates, and descriptions.
Improve the user interface and recommendation experience.
Deploy the application online so that it can be accessed publicly.

Acknowledgements
The Movie Database (TMDB) for movie data, metadata, and poster images.
Scikit-learn for machine learning and text vectorization tools.
Streamlit for building the interactive web application.