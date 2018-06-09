from scipy.integrate import ode
import matplotlib.pyplot as plt
import matplotlib as mlb
import numpy as np
from math import sin, cos, sqrt, copysign, atan, pi
import unittest


m = (10 + 5.5) * 10 ** 3  # Масса ракеты в начале перелёта, кг.
M_E = 5.97 * 10 ** 24  # Масса Земли, кг.
M_M = 7.35 * 10 ** 22  # Масса Луны, кг.
R_E = 6375 * 10 ** 3  # Радиус Земли, м.
R_M = 1738 * 10 ** 3  # Радиус Луны, м.
R_orb = 384405 * 10 ** 3  # Радиус орбиты Луны, м.
V_M = 1.023 * 10 ** 3  # Скорость
G = 6.67 * 10 ** (-11)  # Гравитационная постоянная.
F = [1016 * 10 ** 3, 97.75 * 10 ** 3]  # Массив со значениями сил тяги разных двигателей (F[i], Н).
U = [4130, 3050]  # Массив со скоростями истечения продуктов сгорания (U[i], м/c).
fuel = [F[0] / U[0], F[1] / U[1]]  # Массив со значениями расхода топлива (fuel[i], кг/c).
dt = 0.5  # Промежуток времени для численного интегрирования.
Moon_pos = [R_orb, 0]  # Начальное положение Луны.
x0 = 0  # Координаты начального положение ракеты.
y0 = R_E + 185 * 10 ** 3  # Координаты начального положение ракеты.
V_x0 = - sqrt(G * M_E / sqrt(x0 ** 2 + y0 ** 2))  # Проекция скорости ракеты в начале перелёта.
V_y0 = 0  # Проекция скорости ракеты в начале перелёта.
v_final = sqrt(G * M_M / (R_M + 50 * 10 ** 3))  # Желаемая скорость на окололунной орбите.
V = []  # Массив, содержащий массивы проекций скоростей ракеты на протяжении полёта.
coord = []  # Массив, содержащий массивы координат ракеты на протяжении полёта.
MOON_pos = []  # Аналогичный массив для положения Луны.
MOON_V = []
c_in_m_fr = []
Earth = []
for phi in np.linspace(0, 2 * pi, 1000):
    Earth.append(([R_E * cos(phi), R_E * sin(phi)]))


def cos_between_vect(v1, v2): # Функция, определяющая модуль косинуса угла между векторами.
    lengt_v1 = sqrt(v1[0] ** 2 + v1[1] ** 2)
    lengt_v2 = sqrt(v2[0] ** 2 + v2[1] ** 2)
    return abs(v1[0] * v2[0] + v1[1] * v2[1]) / (lengt_v1 * lengt_v2)


def angle(pos):  # Функция для определения угла между вектором и осью Ox.
    if pos[0] == 0:
        return pi / 2 if pos[1] > 0 else 3 * pi / 2
    elif pos[0] > 0:
        return atan(pos[1] / pos[0]) if pos[1] > 0 else 2 * pi + atan(pos[1] / pos[0])
    else:
        return pi + atan(pos[1] / pos[0])


def moon_coord(pos, t):  # Определение координат Луны через время t.
    w = V_M / R_orb
    return [R_orb * cos(angle(pos) - w * t), R_orb * sin(angle(pos) - w * t)]


def coord_v_in_dif_fr(r_pos, v, m_pos, frame='Moon'):  # Перевода координат и проекций скорости из одной СО в другую.
    if frame == 'Moon':  # Перевод в СО, связанную с Луной.
        new_pos = [r_pos[i] - m_pos[i] for i in range(2)]
        new_v = [v[i] - moon_vel(m_pos)[i] for i in range(2)]
    else:
        new_pos = [r_pos[i] + m_pos[i] for i in range(2)]
        new_v = [v[i] + moon_vel(m_pos)[i] for i in range(2)]
    return new_pos, new_v


def moon_vel(pos):  # Функция, возвращающая скорость Луны в указанном положении.
    return [V_M * sin(angle(pos)), - V_M * cos(angle(pos))]


def pos_and_velocity(r_pos, v, m_pos, fx, fy, m, dt, frame='Earth'):  # Численное интегрирование.
    # Вычисление положения ракеты и проекций её скоростей через время dt в различных СО.
    x, y = r_pos[0], r_pos[1]
    if frame == 'Earth':
        x_m, y_m = m_pos[0], m_pos[1]
        a_x = fx / m - G * M_E * x / (x ** 2 + y ** 2) ** (3 / 2) - G * M_M * (x - x_m) / ((x - x_m) ** 2 +
                                                                                       (y - y_m) ** 2) ** (3 / 2)
        a_y = fy / m - G * M_E * y / (x ** 2 + y ** 2) ** (3 / 2) - G * M_M * (y - y_m) / ((x - x_m) ** 2 +
                                                                                       (y - y_m) ** 2) ** (3 / 2)
    else:
        a_x = fx / m - G * M_M * x / (x ** 2 + y ** 2) ** (3 / 2)
        a_y = fy / m - G * M_M * y / (x ** 2 + y ** 2) ** (3 / 2)
    v_new = [v[0] + a_x * dt, v[1] + a_y * dt]
    pos_new = []
    for i in range(2):
        pos_new.append(r_pos[i] + (v[i] + v_new[i]) * 0.5 * dt)
    return pos_new, v_new


def optimal_angle(start_pos, start_v, mass):  # Поиск оптимального положения для начала полёта.
    global MOON_pos, coord, Moon_pos
    for ang in np.linspace(0, pi / 4, 50):
        m_pos = [0, - R_orb]
        r_pos = [0, - sqrt(start_pos[0] ** 2 + start_pos[1] ** 2)]
        local_m = mass
        dist = [R_orb]
        v = [sqrt(start_v[0] ** 2 + start_v[1] ** 2) * cos(ang), sqrt(start_v[0] ** 2 + start_v[1] ** 2) * sin(ang)]
        t = 0
        while local_m >= (5 + 5.5) * 10 ** 3 + fuel[1] * dt:
            fx = F[1] * v[0] / sqrt(v[0] ** 2 + v[1] ** 2)
            fy = F[1] * v[1] / sqrt(v[0] ** 2 + v[1] ** 2)
            r_pos, v = pos_and_velocity(r_pos, v, m_pos, fx, fy, local_m, dt, 'Moon')
            local_m -= fuel[1] * dt
            t += dt
            m_pos = moon_coord(m_pos, dt)
            r_pos_in_E = coord_v_in_dif_fr(r_pos, v, m_pos, 'Earth')[0]
            dist.append(sqrt(r_pos_in_E[0] ** 2 + r_pos_in_E[1] ** 2))
        local_m -= 4.8 * 10 ** 3
        r_pos, v = coord_v_in_dif_fr(r_pos, v, m_pos, 'Earth')
        dist.append(sqrt(r_pos[0] ** 2 + r_pos[1] ** 2))
        while t < 200000:
            dist.append(sqrt(r_pos[0] ** 2 + r_pos[1] ** 2))
            t += dt
            m_pos = moon_coord(m_pos, dt)
            r_pos, v = pos_and_velocity(r_pos, v, m_pos, 0, 0, local_m, dt)
        print(min(dist) * 10 ** (-3), ang)
        if R_E + 70 * 10 ** 3 < min(dist) < R_E + 1070 * 10 ** 3:
            break
    m_pos = [0, - R_orb]
    r_pos = [0, - sqrt(start_pos[0] ** 2 + start_pos[1] ** 2)]
    v = [sqrt(start_v[0] ** 2 + start_v[1] ** 2) * cos(ang), sqrt(start_v[0] ** 2 + start_v[1] ** 2) * sin(ang)]
    r_pos, v = coord_v_in_dif_fr(r_pos, v, m_pos, 'Earth')
    print(angle([- r_pos[i] for i in range(2)]), angle(v))
    return angle([- r_pos[i] for i in range(2)]) - angle(v)


def waiting(r_pos, v, m_pos, ang):  # Поиск времени ожидания на орбите Луны для оптимального полёта.
    global MOON_pos, coord, Moon_pos
    waiting_time = 0
    r_pos_in_E, v_in_E = coord_v_in_dif_fr(r_pos, v, m_pos, 'Earth')
    while abs(angle([- r_pos_in_E[i] for i in range(2)]) - angle(v_in_E) - ang) > 0.01:
        # print(angle([- r_pos_in_E[i] for i in range(2)]) - angle(v_in_E), ang)
        m_pos = moon_coord(m_pos, dt)
        r_pos, v = pos_and_velocity(r_pos, v, m_pos, 0, 0, m, dt, 'Moon')
        r_pos_in_E, v_in_E = coord_v_in_dif_fr(r_pos, v, m_pos, 'Earth')
        waiting_time += dt
        MOON_pos.append(m_pos)
        coord.append(r_pos_in_E)
        V.append(v_in_E)
        c_in_m_fr.append(r_pos)
        print(waiting_time)
    return waiting_time, r_pos, v


def flight(r_pos, v, m_pos):  # Основная функция, соединяющая части полёта.
    global m, MOON_pos, coord, Moon_pos, MOON_V, c_in_m_fr
    t, r_pos, v = waiting(r_pos, v, m_pos, optimal_angle(r_pos, v, m))
    while m >= (5 + 5.5) * 10 ** 3 + fuel[1] * dt:
        fx = F[1] * v[0] / sqrt(v[0] ** 2 + v[1] ** 2)
        fy = F[1] * v[1] / sqrt(v[0] ** 2 + v[1] ** 2)
        r_pos, v = pos_and_velocity(r_pos, v, m_pos, fx, fy, m, dt, 'Moon')
        m -= fuel[1] * dt
        t += dt
        m_pos = moon_coord(m_pos, dt)
        r_pos_in_E, v_in_E = coord_v_in_dif_fr(r_pos, v, m_pos, 'Earth')
        MOON_pos.append(m_pos)
        coord.append(r_pos_in_E)
        V.append(v_in_E)
    r_pos, v = coord_v_in_dif_fr(r_pos, v, m_pos, 'Earth')
    while sqrt(r_pos[0] ** 2 + r_pos[1] ** 2) > 1.5 * R_E:
        r_pos, v = pos_and_velocity(r_pos, v, m_pos, 0, 0, m, dt)
        t += dt
        m_pos = moon_coord(m_pos, dt)
        MOON_pos.append(m_pos)
        coord.append(r_pos)
        V.append(v)
    while m >= (4.8 + 5.5) * 10 ** 3 + fuel[1] * dt:
        for ang in np.linspace(0, 2 * pi, 50):
            attack_p = [(R_E + 70 * 10 ** 3) * cos(ang), (R_E + 70 * 10 ** 3) * sin(ang)]
            print(cos_between_vect(attack_p, [attack_p[i] - r_pos[i] for i in range(2)]))
            if cos_between_vect(attack_p, [attack_p[i] - r_pos[i] for i in range(2)]) < 0.15:
                break
        fx = F[1] * (attack_p[0] - r_pos[0]) / sqrt((attack_p[0] - r_pos[0]) ** 2 + (attack_p[1] - r_pos[1]) ** 2)
        fy = F[1] * (attack_p[1] - r_pos[1]) / sqrt((attack_p[0] - r_pos[0]) ** 2 + (attack_p[1] - r_pos[1]) ** 2)
        # fx = F[1] * (- r_pos[0]) / sqrt(r_pos[0] ** 2 + r_pos[1] ** 2)
        # fy = F[1] * (- r_pos[1]) / sqrt(r_pos[0] ** 2 + r_pos[1] ** 2)
        r_pos, v = pos_and_velocity(r_pos, v, m_pos, fx, fy, m, dt)
        t += dt
        m -= fuel[1] * dt
        m_pos = moon_coord(m_pos, dt)
        MOON_pos.append(m_pos)
        coord.append(r_pos)
        V.append(v)
    return


if __name__ == '__main__':
    flight([ R_M + 50 * 10 ** 3, 0], [0, v_final], [0, - R_orb])
    fig = plt.figure(num=None, figsize=(12, 9), dpi=100)
    ax1 = fig.add_subplot(221)
    ax1.set_title(r'Движение ракеты и Луны')
    ax1.set_xlabel(r'$x$, км $\cdot 10^3$')
    ax1.set_ylabel(r'$y$, км $\cdot 10^3$')
    ax1.plot([Earth[i][0] * 10 ** (-6) for i in range(len(Earth))], [Earth[i][1] * 10 ** (-6) for i in range(len(Earth))])
    ax1.plot([coord[i][0] * 10 ** (-6) for i in range(len(coord))], [coord[i][1] * 10 ** (-6) for i in range(len(coord))])
    ax1.plot([MOON_pos[i][0] * 10 ** (-6) for i in range(len(MOON_pos))], [MOON_pos[i][1] * 10 ** (-6) for i in range(len(MOON_pos))])
    ax2 = fig.add_subplot(222)
    ax2.set_title(r'Движение ракеты в СО, связанной с Луной')
    ax2.set_xlabel(r'$x$, км')
    ax2.set_ylabel(r'$y$, км')
    ax2.plot([c_in_m_fr[i][0] * 10 ** (-3) for i in range(len(c_in_m_fr))], [c_in_m_fr[i][1] * 10 ** (-3) for i in range(len(c_in_m_fr))])
    ax3 = fig.add_subplot(223)
    ax3.set_title(r'Скорость ракеты в СО, связанной с Землёй')
    ax3.set_xlabel(r'$v_x$, км/c')
    ax3.set_ylabel(r'$v_y$, км/c')
    ax3.plot([V[i][0] for i in range(len(V))], [V[i][1] for i in range(len(V))])
    plt.show()
