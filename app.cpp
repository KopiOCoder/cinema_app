#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <fstream>
#include <sstream>

class Movie {
public:
    int id; 
    std::string title;
    std::vector<double> features;
    
    Movie(int id, std::string title, std::string genres) : id(id), title(title) {
        features.resize(18, 0.0);
        if (genres.find("Comedy") != std::string::npos) features[0] = 1.0;
        if (genres.find("Action") != std::string::npos) features[1] = 1.0;
        if (genres.find("Drama") != std::string::npos) features[2] = 1.0;
        if (genres.find("Animation") != std::string::npos) features[3] = 1.0;
        if (genres.find("Musical") != std::string::npos) features[4] = 1.0;
        if (genres.find("Children") != std::string::npos) features[5] = 1.0;
        if (genres.find("Mystery") != std::string::npos) features[6] = 1.0;
        if (genres.find("Horror") != std::string::npos) features[7] = 1.0;
        if (genres.find("Fantasy") != std::string::npos) features[8] = 1.0;
        if (genres.find("Western") != std::string::npos) features[9] = 1.0;
        if (genres.find("Sci-Fi") != std::string::npos) features[10] = 1.0;
        if (genres.find("Crime") != std::string::npos) features[11] = 1.0;
        if (genres.find("Documentary") != std::string::npos) features[12] = 1.0;
        if (genres.find("IMAX") != std::string::npos) features[13] = 1.0;
        if (genres.find("Adventure") != std::string::npos) features[14] = 1.0;
        if (genres.find("Thriller") != std::string::npos) features[15] = 1.0;
        if (genres.find("Film-Noir") != std::string::npos) features[16] = 1.0;
        if (genres.find("War") != std::string::npos) features[17] = 1.0;
    }
};


class MovieRecommender {
public:
    std::vector<Movie> movies;

    void loadMovies(const std::string& filename) {
        std::ifstream file(filename);
        std::string line;
        std::getline(file, line);

        while (std::getline(file, line)) {
            std::stringstream ss(line);
            std::string movieId, title, genres;

            std::getline(ss, movieId, ',');
            std::getline(ss, title, ',');
            std::getline(ss, genres);

            movies.push_back(Movie(std::stoi(movieId), title, genres));
        }
    }

    double Similarity(const Movie& movie1, const Movie& movie2) {
        double dotProduct = 0.0;
        double norm1 = 0.0;
        double norm2 = 0.0;

        for (size_t i=0; i < movie1.features.size(); i++) {
            dotProduct += movie1.features[i] * movie2.features[i];
            norm1 += movie1.features[i] * movie1.features[i];
            norm2 += movie2.features[i] * movie2.features[i];
        }
        if (norm1 == 0 || norm2 == 0) return 0;
        return dotProduct / (sqrt(norm1) * sqrt(norm2));
    }

    void getSimilar(int movieId) {
        Movie* target = nullptr;
        for (auto& movie : movies) {
            if (movie.id == movieId) {
                target = &movie;
                break;
            }
        }

        if (!target) {
            std::cout << "movie not found" << std::endl;
            return;
        }

        for (auto& movie : movies) {
            if (movie.id != movieId) {
                double sim = Similarity(*target, movie);
                if (sim > 0.0) {
                    std::cout << movie.title << " - " << sim << std::endl;
                }
            }
        }
    }
};

    