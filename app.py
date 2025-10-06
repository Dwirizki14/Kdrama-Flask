from flask import Flask, render_template, request
import pickle
import requests
import os

# Inisialisasi Flask
app = Flask(__name__)

# 🔑 Masukkan API Key TMDb kamu
TMDB_API_KEY = "162e06d62e183a0044a381f753e040ec"
# Load model dan data
with open('kdrama_recommender.pkl', 'rb') as file:
    data = pickle.load(file)
    tfidf = data['tfidf']
    cosine_sim_df = data['cosine_sim_df']
    df = data['df']

# Fungsi rekomendasi
def recommend(title, top_n=5):
    if title not in df['Name'].values:
        return []
    idx = df[df['Name'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim_df.iloc[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[1:top_n+1]]
    return df['Name'].iloc[top_indices].tolist()

# Fungsi ambil poster TMDb
def get_poster(title):
    try:
        url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={title}"
        response = requests.get(url).json()
        if response["results"]:
            poster_path = response["results"][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass
    return "https://via.placeholder.com/300x450?text=Poster+Not+Found"

# Halaman utama
@app.route('/')
def home():
    return render_template('index.html')

# Halaman rekomendasi
@app.route('/recommend', methods=['POST'])
def recommend_page():
    title = request.form['movie']
    recommendations = recommend(title)
    
    if not recommendations:
        return render_template('index.html', title=title, posters=None, message="Judul tidak ditemukan.")
    
    posters = []
    for rec in recommendations:
        posters.append({
            "title": rec,
            "poster": get_poster(rec)
        })
    
    return render_template('index.html', title=title, posters=posters, message=None)

if __name__ == '__main__':
    app.run()