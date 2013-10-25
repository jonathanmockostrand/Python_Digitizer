# Samira Ardani
# oct-24-2013
# My Digitizer

import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread
import matplotlib.cbook as cbook

class click_point:
    def __init__(self, point):
        self.point = point
        self.xs = list(point.get_xdata())
        self.ys = list(point.get_ydata())
        self.xx = []
        self.yy = []  
        
        self.cid = point.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print 'button=%d,x=%d, y=%d,xdata=%f, ydata=%f, '%(event.button, event.x,event.y, event.xdata,event.ydata)
        self.xx.append(event.x)
        self.yy.append(event.y)
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
         
        self.point.set_data(self.xs, self.ys)
        
#fig1 = imread("frame_0001.png")        
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Click to Specify a Point')
ax.plot(np.random.rand(10))
point, = ax.plot([0], [0])  # empty line
click_point = click_point(point)
#plt.imshow(fig1, zorder=0)
plt.show()

#click_point.xx
#click_point.yy
#click_point.xs
#click_point.ys
