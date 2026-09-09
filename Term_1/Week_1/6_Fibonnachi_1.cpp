#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>

int main(int argc, char* argv[]){
    int n = std::atoi(argv[1]);
    std::vector<int> fib(n + 1);
    fib[0] = 0;
    fib[1] = 1;
    for (int i = 2; i < n + 1; ++i){
        fib[i] = fib[i - 1] + fib[i - 2];
    }
    std::ofstream file("output.txt");
    for (int i = 1; i < n + 1; ++i){
        file << i << " " << fib[i] << "\n";
    }
    file.close();
}