#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>

std::pair<double, double> eyler_scheme(const std::pair<double, double>& vec, const double& omega, const double& dt){
    return std::pair<double, double> {vec.first + vec.second * dt, vec.second - omega * omega * vec.first * dt};
}

int main(){
    double dt = 0.0000001; // шаг расчетов, не меньше 0.01
    double dt_output = 0.01; // шаг записи
    double x_0 = 1.0;
    double v_0 = 1.0;
    double omega = 1.0;
    int t = 100; // общее время
    int frames = t / dt; // общее количество итераций рассчета
    int output = dt_output / dt; // общее количество записанных данных
    std::vector<std::vector<double>> buffer(1000, std::vector<double>(3));
    std::string file_name = "eyler_" + std::to_string(t) + "_" + std::to_string(dt) + ".csv"; 
    std::ofstream file(file_name);
    std::pair<double, double> current;
    current.first = x_0;
    current.second = v_0;
    file << "t,x,v\n";
    int i = 0;
    int j = 0;
    while (i < frames){
        if (i % output == 0){
            buffer[j] = {i * dt, current.first, current.second};
            ++j;
        }
        current = eyler_scheme(current, omega, dt);
        if (j == 1000){
            for (int k = 0; k != 1000; ++k){
                file << buffer[k][0] << "," << buffer[k][1] << "," << buffer[k][2] << "\n";
            }
            j = 0;
        }
        ++i;
    }
    file.close();
}
