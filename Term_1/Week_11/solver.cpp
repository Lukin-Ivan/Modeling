#include <iostream>
#include <vector>
#include <array>
#include <cmath>
#include <fstream>
#include <cstring>
#include <iomanip>
#include "json.hpp"

struct Vec4
{
    double x1{0.0}, v1{0.0}, x2{0.0}, v2{0.0};
    Vec4 operator+(const Vec4& other) const{
        return {x1 + other.x1, v1 + other.v1, x2 + other.x2, v2 + other.v2};
    }
    Vec4 operator-(const Vec4& other) const{
        return {x1 - other.x1, v1 - other.v1, x2 - other.x2, v2 - other.v2};
    }
    Vec4 operator*(double scalar) const{
        return {x1 * scalar, v1 * scalar, x2 * scalar, v2 * scalar};
    }
    Vec4 operator/(double scalar) const{
        return {x1 / scalar, v1 / scalar, x2 / scalar, v2 / scalar};
    }
    Vec4& operator+=(const Vec4& other){
        x1 += other.x1;
        v1 += other.v1;
        x2 += other.x2;
        v2 += other.v2;
        return *this;
    }
    Vec4& operator-=(const Vec4& other){
        x1 -= other.x1;
        v1 -= other.v1;
        x2 -= other.x2;
        v2 -= other.v2;
        return *this;
    }

};

Vec4 f(const Vec4& vec, const double m_1, const double m_2, const double L_1, const double L_2, const double g, const double t){
    double x1 = vec.x1;
    double v1 = vec.v1;
    double x2 = vec.x2;
    double v2 = vec.v2;
    double denominator = 2 * m_1 + m_2 - m_2 * std::cos(2 * (x1 - x2));
    double a1 = (-m_2 * g * std::sin(x1 - 2 * x2) - (2 * m_1 + m_2) * g * std::sin(x1) - 2 * m_2 * std::sin(x1 - x2) * (L_2 * v2 * v2 + L_1 * v1 * v1 * std::cos(x1 - x2))) / (L_1 * denominator);
    double a2 = (2 * std::sin(x1 - x2) * ((m_1 + m_2) * (L_1 * v1 * v1 + g * std::cos(x1)) + m_2 * L_2 * v2 * v2 * std::cos(x1 - x2))) / (L_2 * denominator);
    return Vec4 {v1, a1, v2, a2};
}

Vec4 euler_scheme(const Vec4& vec, const double m_1, const double m_2, const double L_1, const double L_2, const double g, const double t, const double dt){
    return vec + f(vec, m_1, m_2, L_1, L_2, g, t) * dt;
}

Vec4 heun_scheme(const Vec4& vec, const double m_1, const double m_2, const double L_1, const double L_2, const double g, const double t, const double dt){
    Vec4 predict = vec + f(vec, m_1, m_2, L_1, L_2, g, t) * dt;
    return vec + (f(vec, m_1, m_2, L_1, L_2, g, t) + f(predict, m_1, m_2, L_1, L_2, g, t + dt)) * dt / 2;
}

Vec4 rk4_scheme(const Vec4& vec, const double m_1, const double m_2, const double L_1, const double L_2, const double g, const double t, const double dt){
    Vec4 k_1, k_2, k_3, k_4;
    k_1 = f(vec, m_1, m_2, L_1, L_2, g, t);
    k_2 = f(vec + k_1 * dt / 2, m_1, m_2, L_1, L_2, g, t + dt / 2);
    k_3 = f(vec + k_2 * dt / 2, m_1, m_2, L_1, L_2, g, t + dt / 2);
    k_4 = f(vec + k_3 * dt, m_1, m_2, L_1, L_2, g, t + dt);
    return vec + (k_1 + k_2 * 2 + k_3 * 2 + k_4) * dt / 6;
}

double calculate_energy(const double x1, const double v1, const double x2, const double v2, const double m_1, const double m_2, const double L_1, const double L_2, const double g){
    double K = (m_1 + m_2) * v1 * v1 * L_1 * L_1 / 2 + m_2 * v2 * v2 * L_2 * L_2 / 2 + m_2 * L_1 * L_2 * v1 * v2 * std::cos(x1 - x2);
    double U = m_1 * g * (L_1 - L_1 * std::cos(x1)) + m_2 * g * (L_1 + L_2 - L_1 * std::cos(x1) - L_2 * std::cos(x2));
    return K + U;
}

void write_buffer(std::ofstream& file, const std::string& file_type, const std::vector<std::array<double, 5>>& buffer, int count, const double m_1, const double m_2, const double L_1, const double L_2, const double g) {
    for (int k = 0; k < count; ++k) {
        double t = buffer[k][0];
        double x1 = buffer[k][1];
        double v1 = buffer[k][2];
        double x2 = buffer[k][3];
        double v2 = buffer[k][4];
        double E = calculate_energy(x1, v1, x2, v2, m_1, m_2, L_1, L_2, g);

        if (file_type == ".csv") {
            file << t << "," << x1 << "," << v1 << "," << x2 << "," << v2 << "," << E << "\n";
        } else if (file_type == ".bin") {
            std::array<double, 6> record = {t, x1, v1, x2, v2, E};
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
    
    double t_0 = config["t_0"]; // общее время
    double dt = config["dt"]; // шаг расчетов, не меньше 0.01
    double dt_output = config["dt_output"]; // шаг записи
    double phi_1_0 = config["phi_1_0"];
    double phi_2_0 = config["phi_2_0"];
    double dot_phi_1_0 = config["dot_phi_1_0"];
    double dot_phi_2_0 = config["dot_phi_2_0"];
    double m_1 = config["m_1"];
    double m_2 = config["m_2"];
    double L_1 = config["L_1"];
    double L_2 = config["L_2"];
    double g = config["g"];
    std::string file_name = config["output_filename"];
    std::string solver_type = config["solver_type"];

    std::string file_type = file_name.substr(file_name.rfind('.'));
    std::ofstream file;
    if (file_type == ".bin"){
        file.open(file_name, std::ios::binary);
    }else if (file_type == ".csv"){
        file.open(file_name);
        file << std::fixed << std::setprecision(20);
        file << "t,phi_1,dot_phi_1,phi_2,dot_phi_2,E\n";
    }

    int frames = t_0 / dt; // общее количество итераций рассчета
    int output = dt_output / dt; // общее количество записанных данных
    int BUFFER_SIZE = 1000;
    std::vector<std::array<double, 5>> buffer(BUFFER_SIZE);
    Vec4 current {phi_1_0, dot_phi_1_0, phi_2_0, dot_phi_2_0};
    int j = 0;

    for (int i = 0; i != frames; ++i){
        double t = i * dt;
        if (i % output == 0){
            buffer[j] = {t, current.x1, current.v1, current.x2, current.v2};
            ++j;
            if (j == BUFFER_SIZE){
                write_buffer(file, file_type, buffer, BUFFER_SIZE, m_1, m_2, L_1, L_2, g);
                j = 0;
            }
        }
        if (solver_type == "euler"){
            current = euler_scheme(current, m_1, m_2, L_1, L_2, g, t, dt);
        }else if (solver_type == "heun"){
            current = heun_scheme(current, m_1, m_2, L_1, L_2, g, t, dt);
        }else if (solver_type == "rk4"){
            current = rk4_scheme(current, m_1, m_2, L_1, L_2, g, t, dt);
        }
    }
    write_buffer(file, file_type, buffer, j, m_1, m_2, L_1, L_2, g);

    file.close();
}
