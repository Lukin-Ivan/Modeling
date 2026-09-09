#include <iostream>
#include <fstream>
#include <cstdlib>

int main(int argc, char* argv[]){
    int n = std::atoi(argv[1]);
    std::ofstream file("First_n.txt");
    for (int i = 1; i < n + 1; ++i){
        file << i << "\n";
    }
    file.close();
}