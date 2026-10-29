#include <vector>
#include <cmath>
#include <random>
#include <fstream>
#include <iostream>
#include <array>
#include "json.hpp"

struct Vec3
{
    double x{0.0}, y{0.0}, z{0.0};
    Vec3 operator+(const Vec3& other) const{
        return {x + other.x, y + other.y, z + other.z};
    }
    Vec3 operator-(const Vec3& other) const{
        return {x - other.x, y - other.y, z - other.z};
    }
    Vec3 operator*(double scalar) const{
        return {x * scalar, y * scalar, z * scalar};
    }
    Vec3 operator/(double scalar) const{
        return {x / scalar, y / scalar, z / scalar};
    }
    Vec3& operator+=(const Vec3& other){
        x += other.x;
        y += other.y;
        z += other.z;
        return *this;
    }
    Vec3& operator-=(const Vec3& other){
        x -= other.x;
        y -= other.y;
        z -= other.z;
        return *this;
    }
    double norm() const{
        return x*x + y*y + z*z;
    }

};

struct Particle
{
    Vec3 r;
    Vec3 v;
    Vec3 f;
    Vec3 r0;
    Vec3 wrapped(double box_len) const{
        Vec3 rw = r;
        rw.x -= box_len * std::floor(rw.x / box_len);
        rw.y -= box_len * std::floor(rw.y / box_len);
        rw.z -= box_len * std::floor(rw.z / box_len);
        return rw;
    }
};

double compute_forces(std::vector<Particle>& particles, double box_len, double r_cut = 3.0){
    double pot_energy = 0.0;
    for (auto& p : particles){
        p.f = {0.0, 0.0, 0.0}; // обнуляем предыдущие силы
    }
    for (int i = 0; i < particles.size(); ++i){
        for (int j = i + 1; j < particles.size(); ++j){
            Vec3 delta_r = particles[i].r - particles[j].r; // инициализируем вектор расстояния между частицами
            delta_r.x -= box_len * std::round(delta_r.x / box_len); // считаем расстояние до минимального образа частицы (ПГУ)
            delta_r.y -= box_len * std::round(delta_r.y / box_len);
            delta_r.z -= box_len * std::round(delta_r.z / box_len);
            double r2 = delta_r.norm();
            if (r2 < r_cut * r_cut){ // проверяем, находимся ли мы в радиусе, где взаимодействие не пренебрежимо мало
                Vec3 force = delta_r * (24.0 / r2 * (2.0 / (r2 * r2 * r2 * r2 * r2 * r2) - 1.0 / (r2 * r2 * r2))); // считаем вектор силы взаимодействия между парой частиц
                particles[i].f += force;
                particles[j].f -= force;
                pot_energy += 4.0 * (1.0 / (r2 * r2 * r2 * r2 * r2 * r2) - 1.0 / (r2 * r2 * r2));
            }
        }
    }
    return pot_energy;
}

std::array<double, 7> compute_parametrs(std::vector<Particle>& particles, int& step,double& pot_energy, double& m, double& delta_t){
    double kin_energy = 0.0;
    double p_x = 0.0;
    double p_y = 0.0;
    double p_z = 0.0;
    double p_rms = 0.0;
    double r_rms = 0.0;
    double t = step * delta_t;
    for (auto& p : particles){
        kin_energy += m * p.v.norm() / 2.0; // расчет кинетической энергии
        p_x += m * p.v.x;
        p_y += m * p.v.y;
        p_z += m * p.v.z;
        Vec3 dr = p.r - p.r0;
        r_rms += dr.norm();
    }
    r_rms /= particles.size();
    p_rms = std::sqrt(2 * kin_energy * m / particles.size());
    return std::array<double, 7> {t, pot_energy, kin_energy, p_x / p_rms, p_y / p_rms, p_z / p_rms, r_rms};
}

std::vector<Particle> generate_position(std::vector<Particle>& particles,int n_per_side, double density){
    int N = n_per_side * n_per_side * n_per_side; // частиц всего
    double box_len = std::cbrt(N / density); // длина куба
    double spacing = box_len / n_per_side; // шаг решетки
    
    int part_number = 0;
    for (int ix = 0; ix < n_per_side; ++ix){
        for (int iy = 0; iy < n_per_side; ++iy){
            for (int iz = 0; iz < n_per_side; ++iz){
                particles[part_number].r.x = (ix + 0.5) * spacing; // помещаем частиц в центр ячеек
                particles[part_number].r.y = (iy + 0.5) * spacing;
                particles[part_number].r.z = (iz + 0.5) * spacing;
                part_number++;
            }
        }
    }
    return particles;
}

using json = nlohmann::json;

int main(int argc, char* argv[]){
    std::ifstream config_file(argv[1]);
    json config;
    config_file >> config;
    config_file.close();

    int n_per_side = config["n_per_side"]; // частиц на оси
    double total_time = config["total_time"]; // общее время в секундах
    double start_record_time = config["start_record_time"]; // время начала записи
    double delta_t = config["delta_t"]; // шаг разбиения по времени
    double delta_t_output = config["delta_t_output"]; // шаг записи по времени
    double density = config["density"]; // плотность
    double m = config["m"]; // масса одной частицы
    std::string output_file_name_parametrs = config["output_file_name_parametrs"];
    std::string output_file_name_velocities = config["output_file_name_velocities"];
    std::string output_file_name_coordinates = config["output_file_name_coordinates"];

    int N = n_per_side * n_per_side * n_per_side; // частиц всего
    double box_len = std::cbrt(N / density); // длина куба
    double spacing = box_len / n_per_side; // шаг решетки
    int total_steps = static_cast<int>(std::round(total_time / delta_t));
    int output_steps = static_cast<int>(std::round(delta_t_output / delta_t));
    int start_record_step = static_cast<int>(std::round(start_record_time / delta_t));

    std::vector<Particle> particles(N); // создание вектора из N частиц
    particles = generate_position(particles, n_per_side, density); // расставление частиц в центр кубиков
    std::vector<std::vector<Vec3>> velocity_history;
    std::vector<std::array<double,7>> records_history;

    std::ofstream file_parametrs(output_file_name_parametrs); // открытие файла для записи энергии и импульса
    std::ofstream file_velocities(output_file_name_velocities);
    std::ofstream file_coordinates(output_file_name_coordinates);

    file_parametrs << "t,U,K,p_x,p_y,p_z,r_rms,vacf\n";
    file_velocities << "v_pr\n";
    bool flag = true;

    double pot_energy = compute_forces(particles, box_len); // расчет сил в момент времени t 
    for (int step = 0; step < total_steps; ++step){
        for (auto& p : particles){
            Vec3 a = p.f / m;
            p.r = p.r + p.v * delta_t + a * delta_t * delta_t / 2.0; // первый шаг схемы Верле, r(t+dt)
            p.v = p.v + a * delta_t / 2.0; // v(t+dt/2)
        }
        
        pot_energy = compute_forces(particles, box_len);
        for (auto& p : particles){
            Vec3 a = p.f / m;
            p.v = p.v + a * delta_t / 2.0; // второй шаг схемы Верле, v(t+dt)
        }
        if (step == start_record_step && flag){
            for (auto& p : particles) {
                p.r0 = p.r;
            }
            flag = false;
        }
        if (step % output_steps == 0 && step >= start_record_step){
            records_history.push_back(compute_parametrs(particles, step, pot_energy, m, delta_t));
            file_coordinates << N << "\n";
            file_coordinates << "time = " << step * delta_t << "\n";
            std::vector<Vec3> current_velocities(N);
            for (int i = 0; i < N; ++i){
                Vec3 rw = particles[i].wrapped(box_len);
                file_coordinates << rw.x << " " << rw.y << " " << rw.z << "\n";
                file_velocities << particles[i].v.x << "\n" << particles[i].v.y << "\n" << particles[i].v.z << "\n";
                current_velocities[i] = particles[i].v;
            }
            velocity_history.push_back(current_velocities);
        }
    }
    int T = velocity_history.size();
    int max_lag = T / 2;
    std::vector<double> vacf(max_lag, 0.0);
    for (int delta = 0; delta < max_lag; ++delta){
        double sum_i = 0.0;
        for (int T0 = 0; T0 < T - delta; ++T0){
            double dot_sum = 0.0;
            for (int part_index = 0; part_index < N; ++part_index){
                Vec3 v1 = velocity_history[T0][part_index];
                Vec3 v2 = velocity_history[T0 + delta][part_index];
                dot_sum += (v1.x * v2.x + v1.y * v2.y + v1.z * v2.z);
            }
            sum_i += dot_sum / N;
        }
        vacf[delta] = sum_i / (T - delta);
    }
    double D = 0.0;
    for (int i = 0; i < max_lag - 1; ++i){
        D += (vacf[i] + vacf[i + 1]) * delta_t_output / 6;
    }
    double vacf_0 = vacf[0];
    std::cout << "D(VACF) = " << D;
    for (int i = 0; i < max_lag; ++i){
        vacf[i] /= vacf_0;
    }
    for (int i = 0; i < T; ++i){
        auto rec = records_history[i];
        file_parametrs << rec[0] << "," << rec[1] << "," << rec[2] << "," << rec[3] << "," << rec[4] << "," << rec[5] << "," << rec[6] << ",";
        if (i < max_lag) {
            file_parametrs << vacf[i] << "\n";
        } else {
            file_parametrs << "nan\n";
        }
    }

    file_parametrs.close();
    file_velocities.close();
    file_coordinates.close();

}
