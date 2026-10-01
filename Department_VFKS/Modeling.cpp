#include <vector>
#include <cmath>
#include <random>
#include <fstream>
#include <iostream>
#include <array>

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
};

double compute_forces(std::vector<Particle>& particles, double box_len, double r_cut = 3){
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

void pbc(std::vector<Particle>& particles, double box_len){
    for (auto& p : particles){
        p.r.x -= box_len * std::floor(p.r.x / box_len); // проверяем, чтобы частицы не вышли за границу куба
        p.r.y -= box_len * std::floor(p.r.y / box_len);
        p.r.z -= box_len * std::floor(p.r.z / box_len);
    }
}

std::array<double, 6> compute_parametrs(std::vector<Particle>& particles, int& step,double& pot_energy, double& m, double& delta_t){
    double kin_energy = 0.0;
    double p_x = 0.0;
    double p_y = 0.0;
    double p_z = 0.0;
    double p_rms = 0.0;
    for (auto& p : particles){
        kin_energy += m * p.v.norm() / 2.0; // расчет кинетической энергии
        p_x += m * p.v.x;
        p_y += m * p.v.y;
        p_z += m * p.v.z;
        p_rms += m * p.v.norm();
    }
    return {step * delta_t, pot_energy, kin_energy, p_x / p_rms, p_y / p_rms, p_z / p_rms};
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

std::vector<Particle> random_speed(std::vector<Particle>& particles,int n_per_side, int seed=67, double sigma = 1.0, double mu = 0.0){
    int N = n_per_side * n_per_side * n_per_side; // частиц всего
    
    std::mt19937 gen(67); // типо инициализация рандома по сиду сикс севен
    std::normal_distribution<double> dist(0.0, 1.0); // гауссово распределение скоростей с sigma = 1.0

    int part_number = 0;
    for (int ix = 0; ix < n_per_side; ++ix){
        for (int iy = 0; iy < n_per_side; ++iy){
            for (int iz = 0; iz < n_per_side; ++iz){
                particles[part_number].v.x = dist(gen); // рандомная скорость, соответствующая распределению Гаусса
                particles[part_number].v.y = dist(gen);
                particles[part_number].v.z = dist(gen);
                part_number++;
            }
        }
    }
    Vec3 v_cm{0.0, 0.0, 0.0};
    for (const auto& p : particles){
        v_cm += p.v; // считаем суммарную скорость всех частиц
    }
    v_cm = v_cm / N; // находим получившуюся скорость центра масс
    for (auto& p : particles){
        p.v -= v_cm; // вычитаем скорость центра масс, чтобы не было дрейфа
    }
    return particles;
}

int main(){
    int n_per_side = 15; // частиц на оси
    double density = 1.0; // плотность

    int N = n_per_side * n_per_side * n_per_side; // частиц всего
    double box_len = std::cbrt(N / density); // длина куба
    double spacing = box_len / n_per_side; // шаг решетки
    std::vector<Particle> particles(N); // создание вектора из N частиц

    std::ofstream file("time_pot_energy_kin_energy_pulse.bin", std::ios::binary); // открытие файла для записи энергии и импульса
    std::ofstream file_v("N_velocity.bin", std::ios::binary);

    particles = generate_position(particles, n_per_side, density); // расставление частиц в центр кубиков
    particles = random_speed(particles, n_per_side); // генерация рандомных скоростей согласно распределению Гаусса

    double delta_t = 0.01; // шаг по времени
    double total_time = 10; // общее время в секундах
    int total_steps = total_time / delta_t; // общее количество шагов
    double m = 1.0; // масса одной частицы

    double pot_energy = compute_forces(particles, box_len); // расчет сил в момент времени t 
    for (int step = 0; step < total_steps; ++step){
        for (auto& p : particles){
            Vec3 a = p.f / m;
            p.r = p.r + p.v * delta_t + a * delta_t * delta_t / 2.0; // первый шаг схемы Верле, r(t+dt)
            p.v = p.v + a * delta_t / 2.0; // v(t+dt/2)
        }
        pbc(particles, box_len); // расчет сил в момент времени t+dt
        pot_energy = compute_forces(particles, box_len);
        for (auto& p : particles){
            Vec3 a = p.f / m;
            p.v = p.v + a * delta_t / 2.0; // второй шаг схемы Верле, v(t+dt)
        }
        if (step % (total_steps / 1000) == 0 && step * delta_t > 1.5){
            std::array<double, 6> record = compute_parametrs(particles, step, pot_energy, m, delta_t);
            file.write(reinterpret_cast<const char*>(record.data()), sizeof(double) * record.size());
        }
        if (step == total_steps / 2){
            for (int i = 0; i < N; ++i){
                std::array<double, 3> velocity = {particles[i].v.x, particles[i].v.y, particles[i].v.z};
                file_v.write(reinterpret_cast<const char*>(velocity.data()), sizeof(double) * velocity.size());
            }
        }
    }
    file.close();
    file_v.close();
}
