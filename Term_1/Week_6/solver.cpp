#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <cstring>
#include <iomanip>
#include "json.hpp"

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

Vec2 euler_scheme(const Vec2& vec, const double& omega, const double& dt){
    return Vec2 {vec.x + vec.v * dt, vec.v - omega * omega * vec.x * dt};
}

Vec2 heun_scheme(const Vec2& vec, const double& omega, const double& dt){
    Vec2 predict{vec.x + vec.v * dt, vec.v - omega * omega * vec.x * dt};
    return Vec2 {vec.x + dt / 2 * (vec.v + predict.v), vec.v - dt / 2 * omega * omega * (vec.x + predict.x)};
}

Vec2 rk4_scheme(const Vec2& vec, const double& omega, const double& dt){
    Vec2 k_1, k_2, k_3, k_4;
    k_1 = f(vec, omega);
    k_2 = f(vec + k_1 * dt / 2, omega);
    k_3 = f(vec + k_2 * dt / 2, omega);
    k_4 = f(vec + k_3 * dt, omega);
    return vec + (k_1 + k_2 * 2 + k_3 * 2 + k_4) * dt / 6;
}

using json = nlohmann::json;

int main(int argc, char* argv[]){
    std::ifstream config_file(argv[1]);
    json config;
    config_file >> config;
    config_file.close();
    
    int t = config["t"]; // общее время
    double dt = config["dt"]; // шаг расчетов, не меньше 0.01
    double dt_output = config["dt_output"]; // шаг записи
    double x_0 = config["x_0"];
    double v_0 = config["v_0"];
    double omega = config["omega"];
    std::string file_name_coords = config["output_filename_coords"];
    std::string file_name_energy = config["output_filename_energy"];
    std::string solver_type = config["solver_type"];
    int frames = t / dt; // общее количество итераций рассчета
    int output = dt_output / dt; // общее количество записанных данных
    std::vector<std::vector<double>> buffer(1000, std::vector<double>(3));
    Vec2 current;
    current.x = x_0;
    current.v = v_0;
    int i = 0;
    int j = 0;

    std::ofstream file_coords(file_name_coords);
    std::ofstream file_energy(file_name_energy);
    file_energy << std::fixed << std::setprecision(20);
    file_coords << "t,x,v\n";
    file_energy << "t,E\n";
    while (i < frames){
        if (i % output == 0){
            buffer[j] = {i * dt, current.x, current.v};
            ++j;
        }
        if (solver_type == "euler"){
            current = euler_scheme(current, omega, dt);
        }
        if (solver_type == "heun"){
            current = heun_scheme(current, omega, dt);
        }
        if (solver_type == "rk4"){
            current = rk4_scheme(current, omega, dt);
        }
        if (j == 1000){
            for (int k = 0; k != 1000; ++k){
                file_coords << buffer[k][0] << "," << buffer[k][1] << "," << buffer[k][2] << "\n";
                file_energy << buffer[k][0] << "," << buffer[k][2] * buffer[k][2] / 2 + omega * omega * buffer[k][1] * buffer[k][1] / 2 << "\n";
            }
            j = 0;
        }
        ++i;
    }
    file_coords.close();
    file_energy.close();
}
