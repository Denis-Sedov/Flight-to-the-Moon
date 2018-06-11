import math
import matplotlib.pyplot as plt
G = 10*9.8
# максимальная перегрузка
Lf = 10000
vf = 300
# параметры, которых хотим добиться
R = 6356863
mu = 398600
w = math.pi*5/180
# максимальное угловое ускорение
Cx = 0.85
Cy = 0.34*Cx
M = (465)**(-1)
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
# считываем данные
T = 0
# запускаем отсчёт времени с нуля
def p(x, y):
    '''с помощью линейной апроксимации определяет давление на необходимой нам высоте'''
    h = ((x*x +y*y)**0.5) - R
    i = 0
    while h < Space_lst[i]:
        i+=1
        if i > 23:
            break
    delta = h - Space_lst[i]
# разница между высотой и ближайшим значением
    delta_h = Space_lst[i-1] - Space_lst[i]
# разница между ближайшими соседями
    otn = delta/delta_h
# относительное отклонение
    p = Space[i] + ((Space[i-1] - Space[i]) * otn)
    return p
def normal(Vx, Vy, angle, p):
    '''определяет перегрузку в данный момент и проверяет, не превосходит ли она критической(0 - превосходит)'''
    v = (Vx*Vx + Vy*Vy)**0.5
    N = Cy * M * p * v * v * 0.5
    Py = N * math.cos(angle)
    Q = Cx * M * p * v * v * 0.5
    Fx = Q*(Vx/v) + Py*(Vy/v)
    Fy = Q * (Vy/v) - Py * (Vx/v)
    Pz = N * math.sin(angle)
    F = (Fx * Fx + Fy * Fy + Pz * Pz) ** 0.5
    if F > G:
        return 0
    else:
        return 1
def a(angle, p, Vx, Vy, x, y):
    '''определяем ускорение в данный момент( угол отсчитывает от системы координат, в которой центр привязан к центру Земли, ось Y проведена через точку входа, а Х - перпендикулярно ей в полскости посадки (в плоскости YZ)'''
    v = (Vx*Vx + Vy*Vy)**0.5
    r = (x * x + y * y) ** 0.5
    N = Cy * M * p * v * v * 0.5
    Py = N * math.cos(angle)
    Q = Cx * M * p * v * v * 0.5
    ax = -Q * (Vx/v) - Py * (Vy/v) - mu * x/(r ** 3)
    ay = - Q * (Vy/v) + Py * (Vx/v) - mu * y/(r ** 3)
    return (ax,ay)
def elementary_d(x, y, Vx, Vy, angle, p, T):
    '''определяет элементарное изменение положения коробля и его скорости'''
    t = 20
    T += t
    ai,an = a(angle, p, Vx, Vy, x, y)
    x += Vx*t + ai * t * t * 0.5
    y += Vy*t + an * t * t * 0.5
    Vx += ai * t
    Vx += an * t
    return (x, y, Vx, Vy, T)
start_angle = Vy0/Vx0
angle0 = math.atan(start_angle)
lst_x = []
lst_y = []
lst_Vx = []
lst_Vy = []
T_lst = []
def model (x, y, Vx, Vy, angle, lst_x, lst_y, lst_Vx, lst_Vy, T_lst, T) :
# ввели праметр Т, который полагаем 0
    '''Определяет оптимальную тракторию, используя рекурсивный перебор всех возможных вариантов'''
    if x*x + y*y < (Lf + R)*(Lf + R) and Vx * Vx + Vy * Vy < 90000:
        return True
# проверка на то, что мы уже добились цели и можно выходить из рекурсии
    possible = (-0.5, -0.25, 0, 0.25, 0.5)
    press = p(x,y)
# перебираем возможные углы, на которые мог повернуться корабль за элементарное время
    for i in possible:
        angle += i
        if normal(Vx, Vy, angle, press) == 0:
            continue
# сразу отсекаем те, которые превосходят норму по перегрузке
        x_1, y_1, Vx_1, Vy_1, T = elementary_d(x, y, Vx, Vy, angle, press, T)
        if T > 6000:
            continue
        if Vy_1 > 0:
            continue
# ограничиваем по времени и скорости, чтобы не проводить рассчет полета в открытом космосе
        if model(x_1, y_1, Vx_1, Vy_1, angle, lst_x, lst_y, lst_Vx, lst_Vy, T_lst, T):
            T_lst += [T]
            lst_x += [x_1]
            lst_y += [y_1]
            lst_Vx += [Vx_1]
            lst_Vy += [Vy_1]
            return [lst_x, lst_y,  lst_Vx, lst_Vy, T_lst]
        angle -= i
print(model (x0, y0, Vx0, Vy0, angle0, lst_x, lst_y, lst_Vx, lst_Vy, T_lst, T)[4])
plt.plot(model (x, y, Vx, Vy, angle, lst_x, lst_y, lst_Vx, lst_Vy, T_lst, T)[0], model (x, y, Vx, Vy, angle, lst_x, lst_y, lst_Vx, lst_Vy, T_lst, T)[1])