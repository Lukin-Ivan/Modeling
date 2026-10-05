#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <cstring>
#include <iomanip>

struct Vec2
{
    double x{0.0}, v{0.0};
    Vec2 operator+(const Vec2& other) const{
        return {x + other.x, v + other.v};
    }
    Vec2 operator-(const Vec2& other) const{
        return {x - other.x, v - other.v};
    }
    Vec2 operator*(double scalar) const{
        return {x * scalar, v * scalar};
    }
    Vec2 operator/(double scalar) const{
        return {x / scalar, v / scalar};
    }
    Vec2& operator+=(const Vec2& other){
        x += other.x;
        v += other.v;
        return *this;
    }
    Vec2& operator-=(const Vec2& other){
        x -= other.x;
        v -= other.v;
        return *this;
    }

};

Vec2 f(const Vec2& vec, const double& omega){
    return Vec2 {vec.v, - omega * omega * vec.x};
}

Vec2 eylers_scheme(const Vec2& vec, const double& omega, const double& dt){
    return Vec2 {vec.x + vec.v * dt, vec.v - omega * omega * vec.x * dt};
}

Vec2 heuns_scheme(const Vec2& vec, const double& omega, const double& dt){
    Vec2 predict{vec.x + vec.v * dt, vec.v - omega * omega * vec.x * dt};
    return Vec2 {vec.x + dt / 2 * (vec.v + predict.v), vec.v - dt / 2 * omega * omega * (vec.x + predict.x)};
}

Vec2 RK_scheme(const Vec2& vec, const double& omega, const double& dt){
    Vec2 k_1, k_2, k_3, k_4;
    k_1 = f(vec, omega);
    k_2 = f(vec + k_1 * dt / 2, omega);
    k_3 = f(vec + k_2 * dt / 2, omega);
    k_4 = f(vec + k_3 * dt, omega);
    return vec + (k_1 + k_2 * 2 + k_3 * 2 + k_4) * dt / 6;
}

int main(){

    double dt = 0.1; // шаг расчетов, не меньше 0.01
    double dt_output = 10; // шаг записи
    double x_0 = 1.0;
    double v_0 = 1.0;
    double omega = 1.0;
    int t = 10000000; // общее время
    int frames = t / dt; // общее количество итераций рассчета
    int output = dt_output / dt; // общее количество записанных данных
    std::vector<std::vector<double>> buffer(1000, std::vector<double>(3));
    std::string file_name;
    Vec2 current;
    int i;
    int j;

    /* Метод Эйлера
    file_name = "eyler_" + std::to_string(t) + "_" + std::to_string(dt) + ".csv"; 
    std::ofstream file_eyler(file_name);
    file_name = "eyler_energy_" + std::to_string(t) + "_" + std::to_string(dt) + ".csv"; 
    std::ofstream file_eyler_energy(file_name);
    current.x = x_0;
    current.v = v_0;
    file_eyler << "t,x,v\n";
    file_eyler_energy << "t,E\n";
    i = 0;
    j = 0;
    while (i < frames){
        if (i % output == 0){
            buffer[j] = {i * dt, current.x, current.v};
            ++j;
        }
        current = eylers_scheme(current, omega, dt);
        if (j == 1000){
            for (int k = 0; k != 1000; ++k){
                file_eyler << buffer[k][0] << "," << buffer[k][1] << "," << buffer[k][2] << "\n";
                file_eyler_energy << buffer[k][0] << "," << buffer[k][2] * buffer[k][2] / 2 + omega * omega * buffer[k][1] * buffer[k][1] / 2 << "\n";
            }
            j = 0;
        }
        ++i;
    }
    file_eyler.close();
    file_eyler_energy.close();
    */


    /*Метод Хойна
    file_name = "heun_" + std::to_string(t) + "_" + std::to_string(dt) + ".csv"; 
    std::ofstream file_heun(file_name);
    file_name = "heun_energy_" + std::to_string(t) + "_" + std::to_string(dt) + ".csv"; 
    std::ofstream file_heun_energy(file_name);
    file_heun_energy << std::fixed << std::setprecision(20);
    current.x = x_0;
    current.v = v_0;
    file_heun << "t,x,v\n";
    file_heun_energy << "t,E\n";
    i = 0;
    j = 0;
    while (i < frames){
        if (i % output == 0){
            buffer[j] = {i * dt, current.x, current.v};
            ++j;
        }
        current = heuns_scheme(current, omega, dt);
        if (j == 1000){
            for (int k = 0; k != 1000; ++k){
                file_heun << buffer[k][0] << "," << buffer[k][1] << "," << buffer[k][2] << "\n";
                file_heun_energy << buffer[k][0] << "," << buffer[k][2] * buffer[k][2] / 2 + omega * omega * buffer[k][1] * buffer[k][1] / 2 << "\n";
            }
            j = 0;
        }
        ++i;
    }
    file_heun.close();
    file_heun_energy.close();
    */

    file_name = "RK_" + std::to_string(t) + "_" + std::to_string(dt) + ".csv"; 
    std::ofstream file_RK(file_name);
    file_name = "RK_energy_" + std::to_string(t) + "_" + std::to_string(dt) + ".csv"; 
    std::ofstream file_RK_energy(file_name);
    file_RK_energy << std::fixed << std::setprecision(20);
    current.x = x_0;
    current.v = v_0;
    file_RK << "t,x,v\n";
    file_RK_energy << "t,E\n";
    i = 0;
    j = 0;
    while (i < frames){
        if (i % output == 0){
            buffer[j] = {i * dt, current.x, current.v};
            ++j;
        }
        current = RK_scheme(current, omega, dt);
        if (j == 1000){
            for (int k = 0; k != 1000; ++k){
                file_RK << buffer[k][0] << "," << buffer[k][1] << "," << buffer[k][2] << "\n";
                file_RK_energy << buffer[k][0] << "," << buffer[k][2] * buffer[k][2] / 2 + omega * omega * buffer[k][1] * buffer[k][1] / 2 << "\n";
            }
            j = 0;
        }
        ++i;
    }
    file_RK.close();
    file_RK_energy.close();
}
