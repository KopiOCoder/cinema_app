import csv
import math

def create_features(genres):
    features = [0.0] * 18
    
    if "Comedy" in genres: features[0] = 1.0
    if "Action" in genres: features[1] = 1.0
    if "Drama" in genres: features[2] = 1.0
    if "Animation" in genres: features[3] = 1.0
    if "Musical" in genres: features[4] = 1.0
    if "Children" in genres: features[5] = 1.0
    if "Mystery" in genres: features[6] = 1.0
    if "Horror" in genres: features[7] = 1.0
    if "Fantasy" in genres: features[8] = 1.0
    if "Western" in genres: features[9] = 1.0
    if "Sci-Fi" in genres: features[10] = 1.0
    if "Crime" in genres: features[11] = 1.0
    if "Documentary" in genres: features[12] = 1.0
    if "IMAX" in genres: features[13] = 1.0
    if "Adventure" in genres: features[14] = 1.0
    if "Thriller" in genres: features[15] = 1.0
    if "Film-Noir" in genres: features[16] = 1.0
    if "War" in genres: features[17] = 1.0

    return features

def load_csv(filename):
    movies = []
    
    with open(filename, 'r', encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader)  
        
        for row in reader:
            movie = {
                'id': int(row[0]),
                'title': row[1],
                'genres': row[2],
                'features': create_features(row[2])
            }
            movies.append(movie)
    
    return movies
