from utils import load_csv, inference

def main():
    movies = load_csv("movies.csv")
    results = inference(movies, 1)
    if results is None:
        print("Movie not found")
        return

    print(f"Movies similar to: {results['target_title']}")
    print("-" * 40)
    
    for movie in results['similar_movies']:
        print(f"{movie['title']} - {movie['similarity']:.3f}")

if __name__ == "__main__":
    main()
