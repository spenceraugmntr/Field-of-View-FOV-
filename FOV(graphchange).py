import matplotlib.pyplot as plt
import math as m
import numpy as np
from math import sqrt

#input variables for calculating gsd
effective_imaging_element_size = 15
focal_length = 1400
horizontal_pixel = 1280
vertical_pixel = 720
altitude = 7620

#convert pixel to mm 
Xsensor = effective_imaging_element_size*0.001*horizontal_pixel
Ysensor = effective_imaging_element_size*0.001*vertical_pixel
pixel_vector = ([Xsensor],[Ysensor],[0])  
print(pixel_vector)

#solve for horizontal and vertical FOV
HFOV = 2*m.atan2(Xsensor,2*focal_length)
VFOV = 2*m.atan2(Ysensor,2*focal_length)
print("your HFOV is",HFOV*(180/m.pi),"degrees")
print("your VFOV is",VFOV*(180/m.pi),"degrees")
   
#solve for horizontal and vertical Dimension at NADIR
Horizontal_Dim = 2*altitude*m.tan(HFOV/2)
Vertical_Dim = 2*altitude*m.tan(VFOV/2)
vector_NADIR = ([Horizontal_Dim],[Vertical_Dim],[-altitude])
print("your Horizontal Dimension is",Horizontal_Dim,"meters")
print("your Vertical Dimension is",Vertical_Dim,"meters")
print("your Vector at NADIR is", vector_NADIR)

#Euler Rotation Matrices
def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, m.cos(theta),-m.sin(theta)],
                   [ 0, m.sin(theta), m.cos(theta)]])
  
def Ry(theta):
  return np.matrix([[ m.cos(theta), 0, m.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-m.sin(theta), 0, m.cos(theta)]])
  
def Rz(theta):
  return np.matrix([[ m.cos(theta), -m.sin(theta), 0 ],
                   [ m.sin(theta), m.cos(theta) , 0 ],
                   [ 0           , 0            , 1 ]])

#Euler Rotation Input Values for Inertial Sensor
phi = 30*m.pi/180 
theta = 40*m.pi/180
psi = 5*m.pi/180 
print("phi =", phi)
print("theta  =", theta)
print("psi =", psi)
  
#Obtaining rotation matrix based on order rotated, change order depending on rotation
R = Rz(psi) * Ry(theta) * Rx(phi)
print("Your Euler Rotation Matrix =", np.round(R, decimals=2)) 

#New projected vector after Euler Rotation
vector_rotation = R * vector_NADIR
print("Your pixel projection after the Euler rotation =", np.round(vector_rotation, decimals=2))

#Assigning direction values using Euler matrix
if vector_rotation[0] < 0:
    direction_x = -1
else:
    direction_x = 1
print("your x direction is",direction_x)

if vector_rotation[1] < 0:
    direction_y = -1
else:
    direction_y = 1
print("your y direction is",direction_y)                

#Solving for magnitude of vectors
#If just a theta or psi rotation
if ((phi == 0) and (-m.pi/2 <= theta <= m.pi/2) and (-2*m.pi <= psi <= 2*m.pi)):
    x_middle = abs(m.tan(theta)*altitude)*direction_x
    x_hyp_middle = sqrt(x_middle**2 + altitude**2)
    y_middle = abs(x_hyp_middle*m.tan(VFOV/2))*direction_y
    vector_middle = ([x_middle],[y_middle],[-altitude])
    print("your new middle vector =", vector_middle)
    
    x_1 = abs(m.tan(theta+(HFOV/2))*altitude)*direction_x
    x_hyp1 = sqrt(x_1**2 + altitude**2)
    y_1 = abs(x_hyp1*m.tan(VFOV/2))*direction_y
    vector_first = ([x_1],[y_1],[-altitude])
    print("your new first vector =", vector_first)
    
    x_2 = abs(m.tan(theta-(HFOV/2))*altitude)*direction_x
    x_hyp2 = sqrt(x_2**2 + altitude**2)
    y_2 = abs(x_hyp2*m.tan(VFOV/2))*direction_y
    vector_second = ([x_2],[y_2],[-altitude])
    print("your new second vector =", vector_second)
    
    #3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #Initial vectors
    ax.quiver(0, 0, 0, vector_NADIR[0], vector_NADIR[1], vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, Horizontal_Dim/2, Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, -Horizontal_Dim/2, -Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, -Horizontal_Dim/2, Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, Horizontal_Dim/2, -Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    #showing 3 points just for theta rotation
    ax.quiver(0, 0, 0, vector_middle[0], vector_middle[1], vector_middle[2], arrow_length_ratio=0, color='blue')
    ax.quiver(0, 0, 0, vector_first[0], vector_first[1], vector_first[2], arrow_length_ratio=0, color='blue')
    ax.quiver(0, 0, 0, vector_second[0], vector_second[1], vector_second[2], arrow_length_ratio=0, color='blue')
    #changing y to negative
    ax.quiver(0, 0, 0, vector_middle[0], -1*y_middle, vector_middle[2], arrow_length_ratio=0, color='blue')
    ax.quiver(0, 0, 0, vector_first[0], -1*y_1, vector_first[2], arrow_length_ratio=0, color='blue')
    ax.quiver(0, 0, 0, vector_second[0], -1*y_2, vector_second[2], arrow_length_ratio=0, color='blue')
    #axis limits
    ax.set_xlim([-8000, 8000])
    ax.set_ylim([-8000, 8000])
    ax.set_zlim([-8000, 0])
    plt.savefig("fov.png")
    plt.show()
    
    #2D plot
    plt.plot([vector_second[0],vector_middle[0],vector_first[0]],[vector_second[1],vector_middle[1],vector_first[1]])
    plt.plot([x_middle,x_1,x_2],[y_middle*-1,y_1*-1,y_2*-1])
    plt.plot([x_2,x_2],[y_2*-1,y_2])
    plt.plot([x_1,x_1],[y_1*-1,y_1])    
    
    
#If just a phi or psi rotation
elif ((-m.pi/2 <= phi <= m.pi/2) and (theta == 0) and (-2*m.pi <= psi <= 2*m.pi)):
    y_middle = abs(m.tan(phi)*altitude)*direction_y
    y_hyp_middle = sqrt(y_middle**2 + altitude**2)
    x_middle = abs(y_hyp_middle*m.tan(HFOV/2))*direction_x
    vector_middle = ([x_middle],[y_middle],[-altitude])
    print("your new middle vector =", vector_middle)
    
    y_1 = abs(m.tan(phi+(HFOV/2))*altitude)*direction_y
    y_hyp1 = sqrt(y_1**2 + altitude**2)
    x_1 = abs(y_hyp1*m.tan(HFOV/2))*direction_x
    vector_first = ([x_1],[y_1],[-altitude])
    print("your new first vector =", vector_first)
    
    y_2 = abs(m.tan(phi-(HFOV/2))*altitude)*direction_y
    y_hyp2 = sqrt(y_2**2 + altitude**2)
    x_2 = abs(y_hyp2*m.tan(HFOV/2))*direction_x
    vector_second = ([x_2],[y_2],[-altitude])
    print("your new second vector =", vector_second)    

    #3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #Initial vectors
    ax.quiver(0, 0, 0, vector_NADIR[0], vector_NADIR[1], vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, Horizontal_Dim/2, Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, -Horizontal_Dim/2, -Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, -Horizontal_Dim/2, Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, Horizontal_Dim/2, -Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    #showing 3 points just for theta rotation
    ax.quiver(0, 0, 0, -1*x_middle, vector_middle[1], vector_middle[2], arrow_length_ratio=0, color='blue')
    ax.quiver(0, 0, 0, -1*x_1, vector_first[1], vector_first[2], arrow_length_ratio=0, color='blue')
    ax.quiver(0, 0, 0, -1*x_2, vector_second[1], vector_second[2], arrow_length_ratio=0, color='blue')
    #changing y to negative
    ax.quiver(0, 0, 0, vector_middle[0], vector_middle[1], vector_middle[2], arrow_length_ratio=0, color='blue')
    ax.quiver(0, 0, 0, vector_first[0], vector_first[1], vector_first[2], arrow_length_ratio=0, color='blue')
    ax.quiver(0, 0, 0, vector_second[0], vector_second[1], vector_second[2], arrow_length_ratio=0, color='blue')
    #axis limits
    ax.set_xlim([-8000, 8000])
    ax.set_ylim([-8000, 8000])
    ax.set_zlim([-8000, 0])
    plt.savefig("fov.png")
    plt.show()

    #2D plot
    plt.plot([vector_second[0],vector_middle[0],vector_first[0]],[vector_second[1],vector_middle[1],vector_first[1]])
    plt.plot([x_middle,x_1,x_2],[y_middle*-1,y_1*-1,y_2*-1])
    plt.plot([x_2,x_2],[y_2*-1,y_2])
    plt.plot([x_1,x_1],[y_1*-1,y_1]) 


#Compound rotation of theta,phi,psi
elif ((-m.pi/2 <= phi <= m.pi/2) and (-m.pi/2 <= theta <= m.pi/2) and (-2*m.pi <= psi <= 2*m.pi)):
    x_middle = abs(m.tan(theta)*altitude)*direction_x
    x_1 = abs(m.tan(theta+(HFOV/2))*altitude)*direction_x
    x_2 = abs(m.tan(theta-(HFOV/2))*altitude)*direction_x
    
    y_middle = abs(m.tan(phi)*altitude)*direction_y
    y_1 = abs(m.tan(phi+(HFOV/2))*altitude)*direction_y
    y_2 = abs(m.tan(phi-(HFOV/2))*altitude)*direction_y
    
    vector_middle = ([x_middle],[y_middle],[-altitude])
    vector_first = ([x_1],[y_1],[-altitude])
    vector_second = ([x_2],[y_2],[-altitude])

    print("your new middle vector =", vector_middle)        
    print("your new first vector =", vector_first)
    print("your new second vector =", vector_second)
    
    #3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    #Initial vectors
    ax.quiver(0, 0, 0, vector_NADIR[0], vector_NADIR[1], vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, Horizontal_Dim/2, Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, -Horizontal_Dim/2, -Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, -Horizontal_Dim/2, Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    ax.quiver(0, 0, 0, Horizontal_Dim/2, -Vertical_Dim/2, vector_NADIR[2], arrow_length_ratio=0, color='red')
    
    ax.quiver(0, 0, 0, vector_middle[0], vector_middle[1], vector_middle[2], arrow_length_ratio=0, color='blue')
    ax.quiver(0, 0, 0, vector_first[0], vector_first[1], vector_first[2], arrow_length_ratio=0, color='blue')
    ax.quiver(0, 0, 0, vector_second[0], vector_second[1], vector_second[2], arrow_length_ratio=0, color='blue')
    
    #axis limits
    ax.set_xlim([-8000, 8000])
    ax.set_ylim([-8000, 8000])
    ax.set_zlim([-8000, 0])
    plt.savefig("fov.png")
    plt.show()

    #2D plot
    plt.plot([vector_second[0],vector_middle[0],vector_first[0]],[vector_second[1],vector_middle[1],vector_first[1]])
    plt.plot([x_middle,x_1,x_2],[y_middle*-1,y_1*-1,y_2*-1])
    plt.plot([x_2,x_2],[y_2*-1,y_2])
    plt.plot([x_1,x_1],[y_1*-1,y_1]) 
    
else:
    print("something went wrong not sure what")
    







#middle point
# x_new = m.tan(theta)*altitude
# x_hyp = sqrt(x_new**2 + altitude**2)
# print("x_new =", x_new)
# print("x_hyp =", x_hyp)

#point 1 (add the FOV)
# x_new1 = m.tan(theta+(HFOV/2))*altitude
# x_hyp1 = sqrt(x_new1**2 + altitude**2)
# print("x_new1 =", x_new1)
# print("x_hyp1 =", x_hyp1)

# #point 2 (subtract FOV)
# x_new2 = m.tan(theta-(HFOV/2))*altitude
# x_hyp2 = sqrt(x_new2**2 + altitude**2)
# print("x_new2 =", x_new2)
# print("x_hyp2 =", x_hyp2)



#Plot

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# #showing 3 points
# ax.quiver(0, 0, 0, vector_middle[0], vector_middle[1], vector_middle[2], arrow_length_ratio=0, color='red')
# ax.quiver(0, 0, 0, vector_first[0], vector_first[1], vector_first[2], arrow_length_ratio=0, color='red')
# ax.quiver(0, 0, 0, vector_second[0], vector_second[1], vector_second[2], arrow_length_ratio=0, color='red')
# #changing y to negative
# ax.quiver(0, 0, 0, vector_middle[0], -1*y_middle, vector_middle[2], arrow_length_ratio=0, color='blue')
# ax.quiver(0, 0, 0, vector_first[0], -1*y_1, vector_first[2], arrow_length_ratio=0, color='blue')
# ax.quiver(0, 0, 0, vector_second[0], -1*y_2, vector_second[2], arrow_length_ratio=0, color='blue')


#Intial vectors
#ax.quiver(0, 0, 0, v[0], v[1], -altitude, arrow_length_ratio=0, color='green')
#ax.quiver(0, 0, -altitude, vx/2, vy/2, 0, arrow_length_ratio=0, color='black')
#ax.quiver(0, 0, -altitude, -vx/2, -vy/2, 0, arrow_length_ratio=0, color='black')
#ax.quiver(0, 0, -altitude, -vx/2, vy/2, 0, arrow_length_ratio=0, color='black')
#ax.quiver(0, 0, -altitude, vx/2, -vy/2, 0, arrow_length_ratio=0, color='black')
#ax.quiver(0, 0, 0, v[0], v[1], v[2], arrow_length_ratio=0, color='black')

#ax.quiver(vx/2, vy/2, -altitude, -vx, 0, 0, arrow_length_ratio=0, color='red')
#ax.quiver(vx/2, vy/2, -altitude, 0, -vy, 0, arrow_length_ratio=0, color='blue')
#ax.quiver(-vx/2, -vy/2, -altitude, vx, 0, 0, arrow_length_ratio=0, color='red')
#ax.quiver(-vx/2, -vy/2, -altitude, 0, vy, 0, arrow_length_ratio=0, color='blue')

#Final Vector after rotation
#ax.quiver(0, 0, 0, rv1[0], rv1[1], -altitude, arrow_length_ratio=0, color='black')
#ax.quiver(0, 0, 0, rv3[0], rv3[1], -altitude, arrow_length_ratio=0, color='black')
#ax.quiver(0, 0, 0, rv4[0], rv4[1], -altitude, arrow_length_ratio=0, color='black')
#ax.quiver(0, 0, 0, rv5[0], rv5[1], -altitude, arrow_length_ratio=0, color='black')

#ax.quiver(0, 0, 0, -13.9644, 0, -altitude, arrow_length_ratio=0, color='green')
#ax.quiver(0, 0, 0, -66, 0, -altitude, arrow_length_ratio=0, color='green')
#ax.quiver(0, 0, 0, -119, 0, -altitude, arrow_length_ratio=0, color='green')
#ax.quiver(0, 0, 0, -14, 29, -altitude, arrow_length_ratio=0, color='blue')
#ax.quiver(0, 0, 0, -14, -29, -altitude, arrow_length_ratio=0, color='blue')
#ax.quiver(0, 0, 0, -66, 29, -altitude, arrow_length_ratio=0, color='blue')
#ax.quiver(0, 0, 0, -66, -29, -altitude, arrow_length_ratio=0, color='blue')
#ax.quiver(0, 0, 0, -119, 29, -altitude, arrow_length_ratio=0, color='blue')
#ax.quiver(0, 0, 0, -119, -29, -altitude, arrow_length_ratio=0, color='blue')

#ax.quiver(rv5[0], rv5[1], -altitude, rv1[0], rv1[1], 0, arrow_length_ratio=0, color='green')
#ax.quiver(rv5[0], rv5[1], -altitude, rv2[0], rv2[1], 0, arrow_length_ratio=0, color='green')
#ax.quiver(rv5[0], rv5[1], -altitude, rv3[0], rv3[1], 0, arrow_length_ratio=0, color='green')
#ax.quiver(rv5[0], rv5[1], -altitude, rv4[0], rv4[1], 0, arrow_length_ratio=0, color='green')
#ax.quiver(0, 0, 0, vector_final[0], vector_final[1], vector_final[2], arrow_length_ratio=0, color='black')

#break down above vector into respective x,y,z components
#ax.quiver(0, 0, 0, vector_final[0], vector_final[1], vector_final[2], arrow_length_ratio=0, color='black')
#ax.quiver(0, 0, vector_final[2], vector_final[0], 0, 0, arrow_length_ratio=0, color='black')
#ax.quiver(0, 0, vector_final[2], 0, vector_final[1], 0, arrow_length_ratio=0, color='black')
#ax.quiver(0,vector_final[1], vector_final[2], vector_final[0], 0, 0, arrow_length_ratio=0, color='black')
#ax.quiver(vector_final[0], 0, vector_final[2], 0, vector_final[1], 0, arrow_length_ratio=0, color='black')


# #axis limits
# ax.set_xlim([6300, 6500])
# ax.set_ylim([-40, 40])
# ax.set_zlim([-8000, 0])
# plt.savefig("fov.png")
# plt.show()