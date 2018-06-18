import copy
import math

G = 6.67 * 10**11


rm = 1738000 #м,Радиус Луны
gm = 1.62
Rm = 385000000 #м,Радиус орбиты луны
w0 = 0.00031 #рад/с
Mm = 7.35 * (10**22) #кг,масса луны

def Waitingtime(x,y,X,Y,Z,V,alpha):
    M0 = 4670
    H = math.hypot(X, math.hypot(Y, Z))
    phi = math.acos(x / rm)
    Phi = math.acos(x / H)
    W = V / H
    F = 15600
    u = 3050
    mu = F / u
    dt = 0.01
    v = 0
    M = M0
    t = 0
    w = w0
    h = rm
    g = gm
    while h < (H-rm)/2:
        h += v * dt + F / M * (dt ** 2) / 2 - g * (dt ** 2) / 2
        M -= mu * dt
        Phi += W * dt
        g = G * Mm / (h) ** 2
        v += (F / M * dt  - g * dt)
        Phi = Phi % (2 * math.pi)
        if M <= 2335:
            mu = 0
            F = 0
        t += dt
    while h < H:
        h += v * dt + F/M * (dt**2)/2 * math.sin(math.radians(alpha) - g * (dt**2)/2)
        phi += w * dt + F/M * (dt**2) * math.cos(math.radians(alpha)) / h
        Phi += W * dt
        M -= mu * dt
        alpha -= 1 * dt
        if alpha <= 0:
            alpha = 0
        g = G*Mm/(h)**2
        v += (F/M * dt * math.sin(math.radians(alpha)) - g * dt)
        w += F/M * (dt**2) * math.cos(math.radians(alpha)) / h
        phi = phi % (2*math.pi)
        Phi = Phi % (2 * math.pi)
        if M <= 2335:
            mu = 0
            F = 0
        #t += dt
        #print(h*math.cos(phi),h*math.cos(phi))
    if (phi - Phi) > 0:
        return (phi - Phi)/(W - w0)
    else :
        return (2*math.pi - (phi - Phi)) / (W - w0)
def output(x,y,X,Y,Z,V,t0,alpha):
    M0 = 4670
    dt = 0.01
    H = math.hypot(X, math.hypot(Y, Z))
    phi = math.acos(x / rm)
    Phi = math.acos(x / H)
    W = V / H
    v = 0
    F = 15600
    u = 3050
    mu = F/u
    M = M0
    t = Waitingtime(x,y,X,Y,Z,V,alpha)
    w = w0
    h = rm
    g = gm
    while h < (H-rm)/2:
        h += v * dt + F / M * (dt ** 2) / 2 - g * (dt ** 2) / 2
        M -= mu * dt
        Phi += W * dt
        g = G * Mm / (h) ** 2
        v += (F / M * dt * math.sin(math.radians(45)) - g * dt)
        Phi = Phi % (2 * math.pi)
        if M <= 2335:
            mu = 0
            F = 0
        t += dt
        print(h*math.cos(phi),h*math.sin(phi),alpha)
    while h < H:
        h += v * dt + F / M * (dt ** 2) / 2 * math.sin(math.radians(alpha) - g * (dt ** 2) / 2)
        phi += w * dt + F / M * (dt ** 2) * math.cos(math.radians(alpha)) / h
        Phi += W * dt
        M -= mu * dt
        alpha -= 1*dt

        g = G * Mm / (h) ** 2
        v += F / M * dt * math.sin(math.radians(45))
        w += F / M * (dt ** 2) * math.cos(math.radians(45)) / h
        phi = phi % (2 * math.pi)
        Phi = Phi % (2 * math.pi)
        if M <= 2335:
            mu = 0
            F = 0
        t += dt
        print(h*math.cos(phi),h*math.sin(phi),alpha)
    if -1 < alpha < 1  :
        return [t,H*math.cos(phi),H*math.sin(phi),math.hypot(v,w * H)*math.cos(phi),math.hypot(v,w * H)*math.sin(phi),Phi-phi]
    elif alpha >= 1:
        return output(x,y,X,Y,Z,V,t0,alpha-1)
    else:
        return output(x,y,X,Y,Z,V,t0,alpha+1)
def coordinates(x,y,X,Y,Z,V,t0,alpha,phi0):#пересчитывает координаты в общую СО
    t = output(x,y,X,Y,Z,V,t0,alpha)[0]
    vx = output(x,y,X,Y,Z,V,t0,alpha)[3]
    vy = output(x,y,X,Y,Z,V,t0,alpha)[4]
    x0 = x + Rm * math.cos(w0*t + phi0)#phi0 -угол положения луны в момент старта с Земли(между направлением на луну и осью Х)
    y0 = y + Rm * math.sin(w0*t + phi0)
    deltaphi = output(x,y,X,Y,Z,V,t0,alpha)[5]#неплохо,чтобы тут вышел ноль
    return [t,x0,y0,vx,vy,deltaphi]
print (coordinates(1738000,0,1788000,0,0,10000,100,45,0))