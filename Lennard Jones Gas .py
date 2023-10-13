import math
import sys
from ctypes.wintypes import RGB
import pygame
import random
# 100 px = 1 nm
t = 0.0049
# 1 px = 264580 nm
# 1 A = 0.1 nm

epsilon = 0.185  # kj/mol
sigma = 3   # nm
mass = 39.948  # u

# F newton
angle = - math.pi / 6
F_new = random.uniform(0.1,0.2)
F_newton = [F_new * math.cos(angle), F_new * math.sin(angle)]

black = (0, 0, 0)
pygame.init()
pygame.display.set_caption("Lennard Jones")
Alliance=pygame.image.load("Alliance.png")
pygame.display.set_icon(Alliance)
screen = pygame.display.set_mode((1000, 600))
color_circle1 = RGB(167, 0, 240)
color_circle2 = RGB(255, 128, 100)
paused = False
pos1 = [random.randint(50,950), random.randint(50,550)]
pos2 = [random.randint(50,950), random.randint(50,550)]

F_total1 = [0, 0]
F_total2 = [0, 0]
# direction
d_lj = [1, 1]

# velocity
v1 = [0, 0]
v2 = [0, 0]
#
FN=[0,0]




def position():
    if math.sqrt((pos1[0] - pos2[0])**2+ (pos1[1] - pos2[1])**2) /100  < sigma:
        if pos2[0]>pos1[0]:
            d_lj[0]=-1
        else:
            d_lj[0]=1
        if pos1[1]<pos2[1]:
            d_lj[1]=-1
        else:
            d_lj[1]=1

    if math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2) /100  > sigma :
        if pos1[0] < pos2[0]:
            d_lj[0] = 1
        else:
            d_lj[0]=-1
        if pos1[1] > pos2[1]:
            d_lj[1]=-1
        else :
            d_lj[1]=1




    if pos1[0] > 950 or pos1[0] < 50:
        FN[0] =F_newton[0]
        v1[0]= -v1[0]


    if pos1[1] < 50 or pos1[1] > 550:
        FN[1] = F_newton[1]
        v1[1]=-v1[1]

    if pos2[0] > 950 or pos2[0] < 50:
        v2[0] = -v2[0]

    if pos2[1] < 50 or pos2[1] > 550:
        v2[1] = -v2[1]


    v1[0] = velocity(F_total1[0] / mass, v1[0])
    v2[0] = velocity(F_total2[0] / mass, v2[0])
    v1[1] = velocity(F_total1[1] / mass, v1[1])
    v2[1] = velocity(F_total2[1] / mass, v2[1])


    F_total1[0] =  F_newton[0] + d_lj[0] * f_lj(abs(pos1[0]-pos2[0]) ,abs(pos1[1]-pos2[1])) - FN[0]
    F_total2[0] = -1 * d_lj[0] * f_lj(abs(pos1[0]-pos2[0]),abs(pos1[1]-pos2[1]))
    F_total1[1] =  F_newton[1] + d_lj[1] * f_lj(abs(pos1[1]-pos2[1]) ,abs(pos1[0]-pos2[0])) - FN[1]
    F_total2[1] = -1 * d_lj[1] * f_lj(abs(pos1[1]-pos2[1]) ,abs(pos1[0]-pos2[0]))

    pos1[0] = cons_acc_motion(F_total1[0] / mass, v1[0], pos1[0])
    pos1[1] = cons_acc_motion(F_total1[1] / mass, v1[1], pos1[1])
    pos2[0] = cons_acc_motion(F_total2[0] / mass, v2[0], pos2[0])
    pos2[1] = cons_acc_motion(F_total2[1] / mass, v2[1], pos2[1])


def velocity(a, v0):
    return a * t + v0


def f_lj(r0,r1):
    return abs(4800 * epsilon / r0* (((100*sigma / math.sqrt(r0**2+r1**2)) ** 12 )-( 0.5 * (100*sigma / math.sqrt(r0**2+r1**2)) ** 6)))


def cons_acc_motion(a, v0, x0):
    return ( 1 / 2 * a * (t ** 2) + v0 * t )*100 + x0


def render():
    screen.fill(black)
    pygame.draw.circle(screen, color_circle1, (pos1[0], pos1[1]), 50, 0)
    pygame.draw.circle(screen, color_circle2, (pos2[0], pos2[1]), 50, 0)
    pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                paused = not paused
    if not paused:
        position()
        render()
