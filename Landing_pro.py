import math
import matplotlib.pyplot as plt

omega = 2.618e-6
R = 384405000 
R_earth = 6371000
R_moon = 1737000
height = 50000
moon_acceleration = 1.62
LM_mass = 15000
LM_fuel_mass = 8165 
LK_mass = 28000
Fuel_velocity = 3050
start_time = 250000
Gamma = 6.67e-11
Moon_mass = 7.35e22
####################################


def input_data():
    data_array =  []
    #data_array.append(135)
    #data_array.append(4000)
    #data_array.append(280)
    return data_array



def calculating_of_landing(data_array, M, g, Vp, m):
    x_0 = 0
    y_0 = 50000 + R_moon
    velocity_0_x = 1700
    velocity_0_y = 0
    a_x_0 = 0
    a_y_0 = 1.62
    array_of_estimations = []
    Mass = M + m
    time = 0
    for i in data_array:
        alpha = i[0]
        mass_of_fuel = i[1]
        time_of_using_fuel = i[2]
        consumption = mass_of_fuel/time_of_using_fuel
        if consumption > 14:
            print("CONSUMPTION is more than possible") 
        time = 0
        cos = math.cos(math.radians(alpha))
        sin = math.sin(math.radians(alpha))        
        #while True:
        #    a = []
        #    time = time + 0.5
    while x_0**2 + y_0**2 > R_moon**2:
        a = []
        delta_t = 1
        time = time + delta_t
        print("INERTION")
        a_x = -Gamma*Moon_mass*x_0/(x_0**2 + y_0**2)**(3/2)
        a_y = -Gamma*Moon_mass*y_0/(x_0**2 + y_0**2)**(3/2)
        velocity_x = velocity_0_x + a_x_0*delta_t
        velocity_y = velocity_0_y + a_y_0*delta_t
        x = x_0 + velocity_0_x*delta_t + a_x_0*(delta_t**2)*0.5
        y = y_0 + velocity_0_y*delta_t + a_y_0*(delta_t**2)*0.5 
        a_x_0 = a_x
        a_y_0 = a_y
        velocity_0_x = velocity_x
        velocity_0_y = velocity_y        
        x_0 = x
        y_0 = y
        if x**2 + y**2 < R_moon**2:
            break
        a.extend([x, y, velocity_0_x, velocity_0_y])
        array_of_estimations.append(a)      
        print(array_of_estimations)
        print(time)
    return array_of_estimations            

def graphic(array_of_estimations):
    x = []
    y = []
    Vx = []
    Vy = []
    for i in array_of_estimations:
        x.append(i[0])
        y.append(i[1])
        Vx.append(i[2])
        Vy.append(i[3])
    plt.plot(x, y, 'ro')
    plt.show()

def main():
    M = 6835
    g = 1.62
    Vp = 3050    
    m = 8165
    print(input_data())
    print(calculating_of_landing(input_data(), M, g, Vp, m))
    graphic(calculating_of_landing(input_data(), M, g, Vp, m))
    
main()