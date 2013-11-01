# Group project
# oct-31-2013
# My Digitizer

import matplotlib.pyplot as plt
import numpy as np
import wx.lib.scrolledpanel as scp
from scipy.misc import imread
import matplotlib.cbook as cbook
from matplotlib.widgets import Button, RadioButtons
import Tkinter as TK


                                                                
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
        
fig1 = imread("frame_0001.png")        
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Click to Specify a Point')
#ax.plot(np.random.rand(10))
point, = ax.plot([0], [0])  # empty line
click_point = click_point(point)
plt.imshow(fig1, zorder=0)

#############################################################################
# Determining the location of each GUI item:
rax = plt.axes([0.01, 0.3, 0.08, 0.1])
bax = plt.axes([0.01,0.02,0.1,0.03])

#adding a GUI item and a function which is activated by an clicking events:

calc_button = Button(bax,'Calculate',image = None, color = '0.95',hovercolor = '0.65')
def calculate():
    frame = TK.Frame
    scroll = TK.Scrollbar
    scroll.pack(side=RIGHT,fill = Y)
calc_button.on_clicked(calculate)
        
radio = RadioButtons(rax,('Linear','Log'))
def radio_click(label):
    
    if label == 'Linear': plt.text= 'linear'#l0.set_visible(not l0.get_visible())
    elif label == 'Log': plt.text=  'log'#l1.set_visible(not l1.get_visible())
    
radio.on_clicked(radio_click) 
   
plt.show()
#click_point.xx
#click_point.yy
#click_point.xs
#click_point.ys
