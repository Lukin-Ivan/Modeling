#include <iostream>
#include <fstream>

int main(){
    int n;
    std::cout << "Самое время ввести n: ";
    std::cin >> n;
    std::ofstream file("First_n.txt");
    for (int i = 1; i < n + 1; ++i){
        file << i << "\n";
    }
    file.close();
}