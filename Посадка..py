import math
G = 10*9.8
# максимальная перегрузка
Lf = 3000
vf = 300
# параметры, которых хотим добиться
R = 6356863
w = math.pi*5/180
# максимальное угловое ускорение
Cx = 0,85
Cy = 0,34*Cx
M = 465
Space = [1,85 * 0.00001, 1.5*0.0001, 3 * 0.0001, 1.03 * 0.001, 4 * 0.001, 7.26 * 0.001, 0.0136, 0.0251, 0.0469, 0.0889, 0.1216, 0.1665, 0.2279, 0.3119, 0.3648, 0.4135, 0.4671, 0.5258, 0.59, 0.6601, 0.7365, 0.8194, 0.9093]
# плотность для разных высот
Space_lst = [80000, 70000, 60000, 50000, 40000, 36000, 32000, 28000, 24000, 20000, 18000, 16000, 14000, 12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000]
# высота для соответствующей плотности
parameter0 = open('parameter.txt', 'r').read()
parameter = parameter0.split()
x0 = float(parameter[0])
y0 = float(parameter[1])
Vx0 = float(parameter[2])
Vy0 = float(parameter[3])
T = float(parameter[4])
def p(x, y):
    h = ((x*x +y*y)**0.5) - R
    i = 0
    while h < Space_lst[i]:
        i+=1
    delta = h - Space_lst[i]
# разница между высотой и ближайшим значением
    delta_h = Space_lst[i-1] - Space_lst[i]
# разница между ближайшими соседями
    otn = delta/delta_h
# относительное отклонение
    p = Space[i] + ((Space[i-1] - Space[i]) * otn)
    return p
# с помощью линейной апроксимации определяем давление на необходимой нам высоте
def normal(v, angle, p):
    Q = Cx * M * p * v * v * 0.5
    Qn = Q * math.cos(angle)
    N = Cy * M * p * v * v * 0.5
    Qi = N * math.cos(angle) + Q * math.sin(angle)
    Pz = N * math.sin(angle)
    F = (Qn * Qn + Qi * Qi + Pz * Pz) ** 0.5
    if F > G:
        return 0
    else:
        return 1
# определяем перегрузку в данный момент и проверяем, не превосходит ли она критической(0 - превосходит)
def a(angle, p, v):
    Q = Cx * M * p * v * v * 0.5
    Py = Cy * M * p * v * v * 0.5 * math.cos(angle)
    ai = Q * math.cos(angle)
    an = Py + Q * math.sin(angle)
    return (ai,an)
# угол отсчитываем от системы координат, в которой центр привязан к центру Земли, ось Y проведена через точку входа,
# а Х - перпендикулярно ей в полскости посадки (в плоскости YZ)
# определяем ускорение в данный момент
def elementary_d(x, y, Vx, Vy, angle, p):
    t = 0.01
    v = (Vx*Vx + Vy*Vy)**0.5
    ai,an = a(angle, p, v)
    x += Vx*t + ai * t * t * 0.5
    y += Vy*t + an * t * t * 0.5
    Vx += ai * t
    Vx += an * t
    return (x, y, Vx, Vy)
# определяем элементарное изменение положения коробля и его скорости
start_angle = Vx0/Vy0
angle0 = math.atan(start_angle)
lst_x = []
lst_y = []
lst_Vx = []
lst_Vy = []
t = 0.01
def model (x, y, Vx, Vy, angle, lst_x, lst_y,  lst_Vx, lst_Vy, T) :
# ввели праметр Т, который полагаем 0
    press = p(x, y)
    if (x + R)*(x + R) + (y + R)*(y + R) < Lf and Vx * Vx + Vy * Vy < 333:
        return True
# проверка на то, что мы уже добились цели и можно выходить из рекурсии
    possible = (-0.05, -0.04, -0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03, 0.04, 0.05)
# перебираем возможные углы, на которые мог повернуться корабль за элементарное время
    for i in possible:
        angle += i
        v = (Vx * Vx + Vy * Vy) ** 0.5
        if normal(v, angle, press) == 0:
            continue
# сразу отсекаем те, которые превосходят норму по перегрузке
        x_1, y_1, Vx_1, Vy_1 = elementary_d(x, y, Vx, Vy, angle, press)
        T += t
        lst_x += [x]
        lst_y += [y]
        lst_Vx += [Vx]
        lst_Vy += [Vy]
        if model(x_1, y_1, Vx_1, Vy_1, angle, lst_x, lst_y, lst_Vx, lst_Vy, T):
            return [lst_x, lst_y,  lst_Vx, lst_Vy, T]
        angle -= i
# используем рекурсию для определения оптимальной трактории (перебираем все возможные сценарии)
