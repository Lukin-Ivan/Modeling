#include <iostream>
#include <fstream>

int main(){
    std::ofstream file("output.txt");
    for (int i = 1; i < 31; ++i){
        file << i << "\n";
    }
    file.close();
}