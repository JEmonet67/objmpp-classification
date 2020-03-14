import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from PIL import Image
import numpy as np
from math import cos,sin


im = np.array(Image.open("/home/jerome/Stage_Classif_Organoid/Result/Organoid_2D/Ellipse_wMask_40_200_0.05_10_10000rep_10int_10ext.png"), dtype=np.uint8)
fig,ax=plt.subplots(1)
ax.imshow(im)

c = (780,1153)
w = 73.7
h = 95.87
teta = 77.5114   #1.3528 en radian 77.51 in degré
#Ells = Ellipse(xy=(1049,810),width=104.95*2,height=131.1875*2, angle=77.51)


X = np.linspace(0,im.shape[0],im.shape[0],dtype=int)
Y = np.linspace(0,im.shape[1],im.shape[1],dtype=int)
x=X*cos(teta) + Y*sin(teta)
y=(Y*cos(teta)-X*sin(teta))

x,y = np.meshgrid(X,Y)
z = ((x-c[0])**2/(h**2))+((y-c[1])**2/(w**2))-1
#z = ((((cos(teta)*(x-c[0]))+(sin(teta)*(y-c[1])))**2/h**2)
#+(((sin(teta)*(x-c[0]))-(cos(teta)*(y-c[1])))**2/w**2))

plt.contour(X,Y,z<1,[0])

#ax.add_artist(Ells)
#Ells.set_alpha(1)

plt.show()

