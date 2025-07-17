import streamlit as st
import pickle
import pandas as pd

# Load the data
movies_dict = pickle.load(open('moviesdict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Recommend function
def recommend(movie):
    if movie not in movies['title'].values:
        return ["Movie not found. Try another."]
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Streamlit UI
st.set_page_config("Movie Recommender", layout="centered")
st.title("🎬 Simple Movie Recommender System")

selected_movie = st.selectbox("Search for a movie:", sorted(movies['title'].values))

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    st.subheader("Top 5 Recommendations:")
    for movie in recommendations:
        st.write("🎥", movie)
