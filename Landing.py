#import matplotlib.pyplot as plt
import math 
file = open("Moon.txt", "r")

def read():
    data_array = []
    for i in range(0, 5):
        row = file.readline().split()
        if len(row) > 0:
            for j in range(len(row)):
                row[j] = float(row[j])
                #row[j] = int(row[j])
            data_array.append(row)
    print(data_array)
    return data_array
        
def calculating(data_array, M, m, g, a, Vp):
    x_0 = 0
    y_0 = 50000
    velocity_0_x = 1700
    velocity_0_y = 0
    a_x_0 = 0
    a_y_0 = 0
    array_of_estimations = []
    Mass = M + m
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
        while True:
            a = []
            time = time + time_of_using_fuel
            if time > time_of_using_fuel:
                break 
            print(time)
            a_x =(consumption/(M+m-consumption*time))*Vp*cos
            a_y =(consumption/(M+m-consumption*time))*Vp*sin - g
            if math.sqrt(a_x**2 + a_y**2) > 29.43:
                print("Owerweight!")
                break
            a_x_0 = a_x
            a_y_0 = a_y
            if consumption == 0:
                velocity_x = velocity_0_x
                velocity_y = velocity_0_y - g*time                
                x = x_0 + velocity_0_x*time
                y = y_0 + velocity_0_y*time - 0.5*g*time**2                   
            else:
                velocity_x = velocity_0_x + Vp*cos*(math.log((Mass)/(Mass-consumption*time)))
                velocity_y = velocity_0_y + Vp*sin*(math.log((Mass)/(Mass-consumption*time))) - g*time                
                x = x_0 + velocity_0_x*time + Vp*cos*(time + (time - (Mass/consumption))*math.log((Mass)/(Mass-consumption*time)))
                y = y_0 + velocity_0_y*time + Vp*sin*(time + (time - (Mass/consumption))*math.log((Mass)/(Mass-consumption*time))) - 0.5*g*time**2    
            velocity_0_x = velocity_x
            velocity_0_y = velocity_y            
            x_0 = x
            y_0 = y
            if Mass < M:
                print("Run out of fuel!!!")
                break
            Mass = Mass-consumption*time
            a.extend([x, y, velocity_0_x, velocity_0_y])
            array_of_estimations.append(a)
    while y >= 0:
        a = []
        time = time + 0.1
        print(time)
        print("INERTION")
        velocity_x = velocity_0_x
        velocity_y = velocity_0_y - g*time
        x = x_0 + velocity_0_x*time
        y = y_0 + velocity_0_y*time - 0.5*g*time**2
        velocity_0_x = velocity_x
        velocity_0_y = velocity_y        
        x_0 = x
        y_0 = y
        if y < 0:
            break
        a.extend([x, y, velocity_0_x, velocity_0_y])
        array_of_estimations.append(a)      
    print(array_of_estimations)
    print(time)
    return array_of_estimations

def output(array_of_estimations):
    output = open("Moon_out.txt", "w")
    space = " "
    for i in array_of_estimations:
        for j in i:
            output.write(str(round(j, 3)) + (24-len(str(round(j,3))))* " ")
        output.write("\n")
    output.close()


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
    a = 1.62
    Vp = 3050    
    m = 8165
    data_array = read()
    array_of_estimations = calculating(data_array, M, m, g, a, Vp)
    output(array_of_estimations)
    #graphic(array_of_estimations)  

main()