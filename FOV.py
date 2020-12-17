import matplotlib.pyplot as plt
import math
import numpy as np

#input variables for calculating gsd
effective_imaging_element_size = float(input("What is your effective imaging element size in micrometers?"))
focal_length = float(input("What is your focal length in millimeters?"))
horizontal_pixel = float(input("What is your hoirzontal pixel length"))
vertical_pixel = float(input("What is your vertical pixel length"))
altitude = float(input("What is your altitude in meters?"))

#convert pixel to mm 
Xsensor = effective_imaging_element_size*0.001*horizontal_pixel
Ysensor = effective_imaging_element_size*0.001*vertical_pixel
    
#solve for horizontal and vertical afov
HAFOV = 2*math.atan2(Xsensor,2*focal_length)
VAFOV = 2*math.atan2(Ysensor,2*focal_length)
print("your HAFOV is",HAFOV*(180/math.pi),"degrees")
print("your VAFOV is",VAFOV*(180/math.pi),"degrees")
   
#solve for horizontal and vertical fov
HFOV = 2*altitude*math.tan(HAFOV/2)
VFOV = 2*altitude*math.tan(VAFOV/2)

print("your HFOV is",HFOV,"meters")
print("your VFOV is",VFOV,"meters")



#Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Cartesian axes
ax.quiver(-1, 0, 0, 3, 0, 0, color='grey',linestyle='dashed')
ax.quiver(0, -1, 0, 0,3, 0, color='grey',linestyle='dashed')
ax.quiver(0, 0, -1, 0, 0, 3, color='grey',linestyle='dashed')

# Vector before rotation
ax.quiver(0, VFOV/2, -altitude, HFOV/2, 0, 0, color='red')
ax.quiver(0, VFOV/2, -altitude, -HFOV/2, 0, 0, color='red')
ax.quiver(-HFOV/2, 0, -altitude, 0, VFOV/2, 0, color='blue')
ax.quiver(-HFOV/2, 0, -altitude, 0, -VFOV/2, 0, color='blue')
ax.quiver(HFOV/2, 0, -altitude, 0, VFOV/2, 0, color='blue')
ax.quiver(HFOV/2, 0, -altitude, 0, -VFOV/2, 0, color='blue')
ax.quiver(0, -VFOV/2, -altitude, HFOV/2, 0, 0, color='red')
ax.quiver(0, -VFOV/2, -altitude, -HFOV/2, 0, 0, color='red')
ax.quiver(-HFOV/2, -VFOV/2, -altitude, HFOV, VFOV, 0, color='yellow',linestyle='dashed') #Diagnol





# Vector after rotation change based on output value from v2

ax.set_xlim([-150, 150])
ax.set_ylim([-150, 150])
ax.set_zlim([-altitude, 0])
plt.show()