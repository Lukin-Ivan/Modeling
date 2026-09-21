#include <iostream>
#include <cmath>
#include <iomanip>
#include <bitset>
#include <cstring>
#include <numbers>

std::bitset<64> printDoubleBits(double value) {
    uint64_t bits;
    std::memcpy(&bits, &value, sizeof(value));
    std::bitset<64> bs(bits);
    return bs;
}

int main(int argc, char* argv[]){
    double cnt = 0;
    double x;
    std::cin >> x;
    long long n = 0;
    while (x > 2 * std::numbers::pi){
        x -= 2 * std::numbers::pi;
    }
    std::cout << std::fixed << std::setprecision(20);
    while (true){
        double cnt_prev = cnt;
        cnt += 1.0 * std::pow(x, 2 * n + 1) * std::pow(-1, n) / std::tgamma(2 * n + 2);
        if (cnt == cnt_prev){
            break;
        }
        std::cout << n << " " << cnt << " " << printDoubleBits(cnt) << "\n";
        n += 1;
    }
}