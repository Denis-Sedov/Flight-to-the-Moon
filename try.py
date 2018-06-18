import copy
import math

G = 6.67 * 10**11


rm = 1738000 #м,Радиус Луны
gm = 1.62
Rm = 385000000 #м,Радиус орбиты луны
w0 = 0.00031 #рад/с
Mm = 7.35 * (10**22) #кг,масса луны

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
    t = t0
    w = w0
    h = rm
    g = gm

    while h < (H+rm)/2:

        #print(h)
        h += (v * dt + F / M * (dt ** 2) / 2 - g * (dt ** 2) / 2)

        M -= mu * dt

        Phi += W * dt
        g = gm /(h/rm) ** 2
        v += F / M * dt  - g * dt
        Phi = Phi % (2 * math.pi)
        if M <= 2335:
            mu = 0
            F = 0
        t += dt


    while h < H:
        h += (v * dt + F / M * (dt ** 2) / 2 * math.sin(math.radians(alpha)) - g * (dt ** 2) / 2)
        phi += w * dt + F / M * (dt ** 2) * math.cos(math.radians(alpha)) / h
        Phi += W * dt
        M -= mu * dt


        g = gm /(h/rm) ** 2
        v += F / M * dt * math.sin(math.radians(alpha)) - g * dt
        w += F / M * (dt ** 2) * math.cos(math.radians(alpha)) / h
        phi = phi % (2 * math.pi)
        Phi = Phi % (2 * math.pi)
        #print([h,F / M * math.sin(math.radians(alpha)),M,t])
        if M <= 2335:
            mu = 0
            F = 0
        t += dt
        #print(h*math.cos(phi),h*math.sin(phi),alpha)
        if h < rm:
            break
    if -1 < alpha < 1 and abs(H-h) <= 3:
        return [t,H*math.cos(phi),H*math.sin(phi),V*math.cos(phi),V*math.sin(phi),phi-Phi]
    else:
        for i in range(-45,45):
            return output(x,y,X,Y,Z,V, t0,(alpha + i))
def coordinates(x,y,X,Y,Z,V,t0,alpha,phi0):#пересчитывает координаты в общую СО
    H = math.hypot(X, math.hypot(Y, Z))
    W = V / H
    t = output(x,y,X,Y,Z,V,t0,alpha)[0]
    if output(x, y, X, Y, Z, V, t0, alpha)[5] > 0:
        Waitingtime = output(x, y, X, Y, Z, V, t0, alpha)[5]/(W - w0)
    else :
        Waitingtime = (2*math.pi - output(x, y, X, Y, Z, V, t0, alpha)[5]) / (W - w0)
    t += Waitingtime
    vx = output(x,y,X,Y,Z,V,t0,alpha)[3] + Rm * math.cos(w0*t + phi0) * w0
    vy = output(x,y,X,Y,Z,V,t0,alpha)[4] + Rm * math.sin(w0*t + phi0) * w0
    x0 = output(x,y,X,Y,Z,V,t0,alpha)[1] + Rm * math.cos(w0*t + phi0)#phi0 -угол положения луны в момент старта с Земли(между направлением на луну и осью Х)
    y0 = output(x,y,X,Y,Z,V,t0,alpha)[2] + Rm * math.sin(w0*t + phi0)

    return [t,x0,y0,vx,vy]
print (coordinates(1738000,0,1788000,0,0,1500,1000,45,0))