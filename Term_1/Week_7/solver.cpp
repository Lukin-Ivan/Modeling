#include <iostream>
#include <vector>
#include <array>
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

Vec2 f(const Vec2& vec, double omega){
    return Vec2 {vec.v, - omega * omega * std::sin(vec.x)};
}

Vec2 euler_scheme(const Vec2& vec, double omega, double dt){
    return vec + f(vec, omega) * dt;
}

Vec2 heun_scheme(const Vec2& vec, double omega, double dt){
    Vec2 predict = vec + f(vec, omega) * dt;
    return vec + (f(vec, omega) + f(predict, omega)) * dt / 2;
}

Vec2 rk4_scheme(const Vec2& vec, double omega, double dt){
    Vec2 k_1, k_2, k_3, k_4;
    k_1 = f(vec, omega);
    k_2 = f(vec + k_1 * dt / 2, omega);
    k_3 = f(vec + k_2 * dt / 2, omega);
    k_4 = f(vec + k_3 * dt, omega);
    return vec + (k_1 + k_2 * 2 + k_3 * 2 + k_4) * dt / 6;
}

double calculate_energy(double x, double v, double omega){
    return (v * v) / 2 + omega * omega * (1 - std::cos(x));
}

void write_buffer(std::ofstream& file, const std::string& file_type, double omega, 
                  const std::vector<std::array<double, 3>>& buffer, int count) {
    for (int k = 0; k < count; ++k) {
        double t = buffer[k][0];
        double x = buffer[k][1];
        double v = buffer[k][2];
        double E = calculate_energy(x, v, omega);

        if (file_type == ".csv") {
            file << t << "," << x << "," << v << "," << E << "\n";
        } else if (file_type == ".bin") {
            std::array<double, 4> record = {t, x, v, E};
            file.write(reinterpret_cast<const char*>(record.data()), sizeof(record));
        }
    }
}

using json = nlohmann::json;

int main(int argc, char* argv[]){
    std::ifstream config_file(argv[1]);
    json config;
    config_file >> config;
    config_file.close();
    
    double t = config["t"]; // общее время
    double dt = config["dt"]; // шаг расчетов, не меньше 0.01
    double dt_output = config["dt_output"]; // шаг записи
    double x_0 = config["x_0"];
    double v_0 = config["v_0"];
    double omega = config["omega"];
    std::string file_name = config["output_filename"];
    std::string solver_type = config["solver_type"];

    std::string file_type = file_name.substr(file_name.rfind('.'));
    std::ofstream file;
    if (file_type == ".bin"){
        file.open(file_name, std::ios::binary);
    }else if (file_type == ".csv"){
        file.open(file_name);
        file << std::fixed << std::setprecision(20);
        file << "t,x,v,E\n";
    }

    int frames = t / dt; // общее количество итераций рассчета
    int output = dt_output / dt; // общее количество записанных данных
    const int BUFFER_SIZE = 1000;
    std::vector<std::array<double, 3>> buffer(BUFFER_SIZE);
    Vec2 current {x_0, v_0};
    int j = 0;

    for (int i = 0; i != frames; ++i){
        if (i % output == 0){
            buffer[j] = {i * dt, current.x, current.v};
            ++j;
            if (j == BUFFER_SIZE){
                write_buffer(file, file_type, omega, buffer, BUFFER_SIZE);
                j = 0;
            }
        }
        if (solver_type == "euler"){
            current = euler_scheme(current, omega, dt);
        }else if (solver_type == "heun"){
            current = heun_scheme(current, omega, dt);
        }else if (solver_type == "rk4"){
            current = rk4_scheme(current, omega, dt);
        }
    }
    write_buffer(file, file_type, omega, buffer, j);

    file.close();
}
