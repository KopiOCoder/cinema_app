#include <iostream>
#include <vector>
#include <string>
#include <cmath>

class Movie {
    int id; 
    std :: string title;
    std :: vector<double> features;
    Movie(int id, std::string title, std::vector<double> features) : id(id), title(title), features(features) {} 
};

