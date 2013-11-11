# ==============================================================================     
#  Python Digitizer
#  : This code is a tool to extract digitized data from a plot image or map
#
#  Final Group Project, OCNG 658
#  Fall 2013 semester
# ==============================================================================  
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons
import Tkinter,tkFileDialog 

def click_point(event):
    '''
    This is a function to deal with clicking the points
    '''
    print('Press', event.key)
    
    if event.key == 'a':
        print 'Xaxis = %f,  Yaxis = %f'  %(event.xdata, event.ydata)
        xaxis.append(event.xdata)
        yaxis.append(event.ydata)
            
    else:
        print 'Xdata = %f,  Ydata = %f'  %(event.xdata, event.ydata)
        xdata.append(event.xdata)
        ydata.append(event.ydata)


def calculation(xmin, xmax, ymin, ymax, xaxis, yaxis, logx, logy, xdata, ydata):
    '''
    This is a function to compute the coordinates of the actual data points
    '''
    
    # change the data as array for the calculation
    xaxis = np.array(xaxis)
    yaxis = np.array(yaxis)
    xdata = np.array(xdata)
    ydata = np.array(ydata)
    
    # make an empty list with same size of data      
    xpts  = np.zeros(np.size(xdata))
    ypts  = np.zeros(np.size(ydata))
    
    # check the coordinate system(linear or logscale)
    

    if logx == 1:
        xmin = np.log10(xmin)
        xmax = np.log10(xmax)
        
    if logy == 1:
        ymin = np.log10(ymin)
        ymax = np.log10(ymax)
    
        
    # calculate the point using linear interpolation        
    for i in range(len(xdata)):    
        xpts[i] = xmin + (xmax - xmin) * \
                 (xdata[i] - np.min(xaxis)) / (np.max(xaxis) - np.min(xaxis))
        ypts[i] = ymin + (ymax - ymin) * \
                 (ydata[i] - np.min(yaxis)) / (np.max(yaxis) - np.min(yaxis))   
    
    # change the coordinate system of result for logscale plot 
    if logx == 1:
        for i in range(len(xdata)): xpts[i] = 10**xpts[i]
                                                
    if logy == 1:
        for i in range(len(ydata)): ypts[i] = 10**ypts[i]
    
    return xpts, ypts
            
     

# make an empty list    
xaxis = []
yaxis = []
xdata = []
ydata = []

 
# Adjusting the window size: 
   
fig = plt.figure('Test Fig', figsize=(16, 9), facecolor='w', edgecolor='w')

################################################################################
# Import Bottun:# import the image by user 
################################################################################


iax = plt.axes([0.01,0.15,0.1,0.03])
import_button = Button(iax,'Import File',image = None, color = '0.95',hovercolor = '0.65')

def import_file(event):
 
    root = Tkinter.Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename()
    
    im = plt.subplot(111).imshow(np.flipud(plt.imread(str(file_path))), origin = 'lower')
    #plt.show() 
    
    frame1 = plt.gca()
    for xlabel_i in frame1.axes.get_xticklabels():
        xlabel_i.set_visible(False)
    for ylabel_i in frame1.axes.get_yticklabels():
        ylabel_i.set_visible(False)
        
import_button.on_clicked(import_file)

################################################################################
# Save Bottun:# save x and y data by user as a text file 
################################################################################


iax = plt.axes([0.01,0.05,0.1,0.03])
save_button = Button(iax,'Save File',image = None, color = '0.95',hovercolor = '0.65')

def save_file(event):
 
    root = Tkinter.Tk()
    root.withdraw()
    #file_path = tkFileDialog.asksaveasfile(a, title="Save File", filetypes=[("txt file", ".csv"), ("All files", ".*")]
    file_path = tkFileDialog.asksaveasfile()
    file_path.writelines('This is the output file of the digitizer\n')
    file_path.writelines('*- Column 0 = x data\n')
    file_path.writelines('*- Column 1 = y data\n')
    x,y= calculation(xmin, xmax, ymin, ymax, xaxis, yaxis, logx, logy, xdata, ydata)    
    np.savetxt(file_path,np.hstack([x]).reshape(-1,1),delimiter=' ',fmt=['%f']) 
    np.savetxt(file_path,np.hstack([y]).reshape(-1,1),delimiter=' ',fmt=['%f'])
      
    file_path.close()
    return()


        
save_button.on_clicked(save_file)
###############################################################################
# Openning a Matplotlib page:
###############################################################################


plt.show()

###############################################################################
# imput the axis information by user :
###############################################################################
xmin = input('Enter xmin:  ')
xmax = input('Enter xmax:  ')
ymin = input('Enter ymin:  ')
ymax = input('Enter ymax:  ')
logx = input('Log x-axis?  (1 = yes, 0 = no):  ');
logy = input('Log y-axis?  (1 = yes, 0 = no):  ');

###############################################################################
# get the axis points & data points by user:
############################################################################### 
print '1) Select the axis points, such as (xmin, ymin), (xmax, ymin), (xmin, ymax) or (xmax, ymax), by press button A (minimum 3 points)'
print '2) Select the data points by press any button (except A, shift, control, win key)'
fig.canvas.mpl_connect('key_press_event', click_point)

################################################################################
# Radio Buttons for choosing the scale:
################################################################################

rax = plt.axes([0.01, 0.3, 0.08, 0.1]) 
radio = RadioButtons(rax,('Linear','Log'))

def radio_click(label):
    
    if label== 'Linear': 
        plt.title( 'linear',loc = 'right')
        logx ==0
        logy ==0
        
    elif label==  'Log': 
        plt.title( 'log',loc='right')
        logx ==1
        logy ==1


radio.on_clicked(radio_click) 

###############################################################################
# Calculation button:
# Plots the results and prints the x and y value 
################################################################################         
x,y = calculation(xmin, xmax, ymin, ymax, xaxis, yaxis, logx, logy, xdata, ydata)
bax = plt.axes([0.01,0.19,0.1,0.03])

calc_button = Button(bax,'Calculate',image = None, color = '0.95',hovercolor = '0.65')
def calculate_button(event):
    x,y= calculation(xmin, xmax, ymin, ymax, xaxis, yaxis, logx, logy, xdata, ydata)
    print x,y
    plt.figure()
    plt.plot(x, y)
    plt.show()
      
calc_button.on_clicked(calculate_button)

###############################################################################            
################################################################################


    
