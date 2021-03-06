import pygame
import serial

port = input("Enter port number")

com = serial.Serial('/dev/ttyACM'+str(port),9600)
print("Connected...")

pygame.init()

done = False

r = 50.760/1000 # metres
R = 150.000/1000 # metres
wz = 0.5 #rps

clock = pygame.time.Clock()

pygame.joystick.init()
    
while done==False:

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done=True 

    joystick_count = pygame.joystick.get_count()


    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        name = joystick.get_name()
        
        axes = joystick.get_numaxes()
        
        vx = joystick.get_axis(3)
        vx = vx*abs(vx)
        vy = joystick.get_axis(4)
        vy = vy*abs(vy)
        ds = joystick.get_axis(5)

        buttons = joystick.get_numbuttons()

        k = joystick.get_button(0) ## 0 or 1 -> kick
        LB = joystick.get_button(4) ## 0 or 1 -> anti-clockwise rotation
        RB = joystick.get_button(5) ## 0 or 1 -> clockwise rotation

        if(LB == 0 and RB ==1):
            wz = -0.1
        if(LB == 1 and RB ==0):
            wz = 0.1
        if( ( LB ==0 and RB == 0 ) or ( LB==1 and RB == 1 ) ):
            wz = 0

        vx = vx*0.06 ## value from -0.2 to 0.2
        vy = -vy*0.06 ## value from -0.2 to 0.2    

        if ds < 0:
            ds = 0 ## value from 0 to 1
        ds = int(ds*255)
        
        w1 = ((vx/1.732)/r) - ((vy/3)/r) + ((wz*R)/r)
        w2 = ((vy/1.5)/r) + ((R*wz)/r)
        w3 = ((wz*R)/r) - ((vx/1.732)/r) - ((vy/3)/r)
        
        w1 = int(127*w1)
        w2 = int(127*w2)
        w3 = int(127*w3)

        print w1,w2,w3,ds,k # can be directly used as rpms
    s= str(w1) + '\t' + str(w2) + '\t' + str(w3) +'\t'+str(ds) +'\t'+str(k) +'\n'
    com.write(s.encode())    
    clock.tick(20)

    
pygame.quit ()


















