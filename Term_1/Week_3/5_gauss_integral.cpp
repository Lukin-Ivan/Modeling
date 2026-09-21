#include <iostream>
#include <cmath>
#include <iomanip>
#include <bitset>
#include <cstring>
#include <numbers>
#include <vector>

std::bitset<64> printDoubleBits(double value) {
    uint64_t bits;
    std::memcpy(&bits, &value, sizeof(value));
    std::bitset<64> bs(bits);
    return bs;
}

int main(int argc, char* argv[]){
    double real = std::pow(std::numbers::pi, 0.5) / 2;
    std::cout << std::fixed << std::setprecision(20);
    std::cout << "Трапеции:" << "\n";
    for (int i = 0; i != 20; ++i){
        double cnt = 0;
        long long n = 0;
        double delta_x = 1.0 / std::pow(2, i);
        while (true){
            double cnt_prev = cnt;
            cnt += (std::exp(-std::pow(n * delta_x, 2)) + std::exp(-std::pow((n + 1) * delta_x, 2))) * delta_x / 2;
            if (cnt == cnt_prev){
                break;
            }
            //std::cout << n << " " << cnt << " " << printDoubleBits(cnt) << "\n";
            n += 1;
        }
        std::cout << n << "\t" << std::abs(cnt - real) / real << "\t" << delta_x << "\n";
        cnt = 0;
        long long n_0 = n;
        while (n != 0){
        double cnt_prev = cnt;
        cnt += (std::exp(-std::pow(n * delta_x, 2)) + std::exp(-std::pow((n + 1) * delta_x, 2))) * delta_x / 2;
        n -= 1;
        }
        std::cout << "***" << n_0 << "\t" << std::abs(cnt - real) / real << "\t" << delta_x << "\n";
    }
}