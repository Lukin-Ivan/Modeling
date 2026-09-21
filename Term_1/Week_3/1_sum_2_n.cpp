#include <iostream>
#include <cmath>
#include <iomanip>
#include <bitset>
#include <cstring>

std::bitset<64> printDoubleBits(double value) {
    uint64_t bits;
    std::memcpy(&bits, &value, sizeof(value));
    std::bitset<64> bs(bits);
    return bs;
}

int main(int argc, char* argv[]){
    double cnt = 0;
    int n = 1;
    std::cout << std::fixed << std::setprecision(20);
    while (true){
        int cnt_prev = cnt;
        cnt += 1/(std::pow(2, n));
        if (cnt == cnt_prev){
            break;
        }
        std::cout << n << " " << cnt << " " << printDoubleBits(cnt) << "\n";
        n += 1;
    }
}