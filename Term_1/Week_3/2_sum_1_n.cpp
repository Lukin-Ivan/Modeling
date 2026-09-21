#include <iostream>
#include <cmath>
#include <iomanip>
#include <bitset>
#include <cstring>

std::bitset<32> printDoubleBits(float value) {
    uint64_t bits;
    std::memcpy(&bits, &value, sizeof(value));
    std::bitset<32> bs(bits);
    return bs;
}

int main(int argc, char* argv[]){
    float cnt = 0;
    long long n = 1;
    std::cout << std::fixed << std::setprecision(20);
    while (true){
        float cnt_prev = cnt;
        cnt += 1.0f / n;
        if (cnt == cnt_prev){
            break;
        }
        // std::cout << n << " " << cnt << " " << printDoubleBits(cnt) << "\n";
        n += 1;
    }
    std::cout << n << " " << cnt << " " << printDoubleBits(cnt) << "\n";
}