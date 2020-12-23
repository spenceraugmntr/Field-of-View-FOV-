import matplotlib.pyplot as plt
import math as m
import numpy as np

#input variables for calculating gsd
effective_imaging_element_size = float(input("What is your effective imaging element size in micrometers?"))
focal_length = float(input("What is your focal length in millimeters?"))
horizontal_pixel = float(input("What is your hoirzontal pixel length?"))
vertical_pixel = float(input("What is your vertical pixel length?"))
altitude = float(input("What is your altitude in meters?"))

#convert pixel to mm 
Xsensor = effective_imaging_element_size*0.001*horizontal_pixel
Ysensor = effective_imaging_element_size*0.001*vertical_pixel
    
#solve for horizontal and vertical afov
HAFOV = 2*m.atan2(Xsensor,2*focal_length)
VAFOV = 2*m.atan2(Ysensor,2*focal_length)
print("your HAFOV is",HAFOV*(180/m.pi),"degrees")
print("your VAFOV is",VAFOV*(180/m.pi),"degrees")
   
#solve for horizontal and vertical fov
vx = 2*altitude*m.tan(HAFOV/2)
vy = 2*altitude*m.tan(VAFOV/2)

print("your HFOV is",vx,"meters")
print("your VFOV is",vy,"meters")


#New Projected Vector At NADIR
v1 = ([vx],[vy],[altitude])  
print("Your new projected pixel vector at NADIR =", v1)

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
phi = float(input("What is your roll angle in degrees?"))*m.pi/180 
theta = float(input("What is your pitch angle in degrees?"))*m.pi/180
psi =float(input("What is your yaw angle in degrees?"))*m.pi/180 
print("phi =", phi)
print("theta  =", theta)
print("psi =", psi)
  
#Obtaining rotation matrix based on order rotated, change order depending on rotation
R = Rz(psi) * Ry(theta) * Rx(phi)
print("Your Euler Rotation Matrix =", np.round(R, decimals=2)) 

#New projected vector after Euler Rotation
v2 = R * v1
print("Your pixel projection after the Euler rotation =", np.round(v2, decimals=2))

HFOV = v2[0]
print("Your HFOV is", HFOV, "meters")
VFOV = v2[1]
print("Your VFOV is", VFOV, "meters")

#Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#Intial vectors
ax.quiver(vx/2, vy/2, 0, -vx, 0, 0, color='red')
ax.quiver(vx/2, vy/2, 0, 0, -vy, 0, color='blue')
ax.quiver(-vx/2, -vy/2, 0, vx, 0, 0, color='red')
ax.quiver(-vx/2, -vy/2, 0, 0, vy, 0, color='blue')

#Final Vector after rotation
ax.quiver(HFOV/2, VFOV/2, -altitude, -HFOV, 0, 0, arrow_length_ratio=0, color='red')
ax.quiver(HFOV/2, VFOV/2, -altitude, 0, -VFOV, 0, arrow_length_ratio=0, color='blue')
ax.quiver(-HFOV/2, -VFOV/2, -altitude, HFOV, 0, 0, arrow_length_ratio=0, color='red')
ax.quiver(-HFOV/2, -VFOV/2, -altitude, 0, VFOV, 0, arrow_length_ratio=0, color='blue')

#Points
ax.quiver(0, 0, 0, 0, 0, -altitude, arrow_length_ratio=0, color='green', linestyle='dashed')
ax.quiver(0, 0, 0, HFOV/2, VFOV/2, -altitude, arrow_length_ratio=0, color='green', linestyle='dashed')
ax.quiver(0, 0, 0, -HFOV/2, VFOV/2, -altitude, arrow_length_ratio=0, color='green', linestyle='dashed')
ax.quiver(0, 0, 0, HFOV/2, -VFOV/2, -altitude, arrow_length_ratio=0, color='green', linestyle='dashed')
ax.quiver(0, 0, 0, -HFOV/2, -VFOV/2, -altitude, arrow_length_ratio=0, color='green', linestyle='dashed')



#axis limits
ax.set_xlim([-HFOV, HFOV])
ax.set_ylim([-HFOV, HFOV])
ax.set_zlim([-altitude, 0])
plt.savefig("fov.png")
plt.show()