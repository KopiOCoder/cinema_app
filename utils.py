import csv
import math

def create_features(genres):
    features = [0.0] * 18
    
    if "Comedy" in genres: features[0] = 1.0
    if "Action" in genres: features[1] = 1.0
    if "Drama" in genres: features[2] = 1.0
    if "Animation" in genres: features[3] = 1.0

    return features
