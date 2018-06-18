#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import math 
import numpy as np
import math

#глобальные переменные
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
####################################

def LK(time): #здесь проводится манёвр посадки
    V_ship = input_data()[3]
    omega_LK = V_ship / (R_moon + height)
    phi = omega_LK * time
    x = (R_moon + height)*math.cos(phi)
    y = (R_moon + height)*math.sin(phi)
    LK_coord_in_moon = []
    LK_coord_in_moon.append(x)
    LK_coord_in_moon.append(y)
    print(LK_coord_in_moon)
    return LK_coord_in_moon        


def moon_coord(time):
    phi = omega*time
    x = R*math.cos(phi)
    y = R*math.sin(phi)
    moon_coord_in_earth = []
    moon_coord_in_earth.append(x)
    moon_coord_in_earth.append(y)
    return moon_coord_in_earth 

def in_earth_to_moon_coord(coord_in_earth):
    moon_coord_in_earth = moon_coord(start_time)
    coord_in_moon = []
    coord_in_moon.append(coord_in_earth[0] - moon_coord_in_earth[0])
    coord_in_moon.append(coord_in_earth[1] - moon_coord_in_earth[1])
    return coord_in_moon

def input_data():
    V_ship = 1701.452
    time = start_time 
    x_in_earth_coord = R - R_moon - height
    y_in_earth_coord = 0
    array_of_input_data = []
    array_of_input_data.extend([time, x_in_earth_coord, y_in_earth_coord, V_ship])
    return array_of_input_data

def main():
    a = moon_coord(start_time)
    b = input_data()
    c = LK(0)
    print(a)
    print(b)
    print(c)
    
main()


    
    
