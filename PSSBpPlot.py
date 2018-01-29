from math import log10 as log,pow
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg, \
    NavigationToolbar2WxAgg

def InitPlot(self):
    dpio = 100
    self.fig = Figure((3.0, 3.0), dpi=dpio)
    self.axes = self.fig.add_subplot(111)

    self.canvas = FigureCanvasWxAgg(self.panelmain, -1, self.fig)
    self.fig.canvas.mpl_connect('button_press_event',self.OnPlotClick)
    
    self.xwatch = 0
	
def RedrawPlot(self,evt):
    freq = 2400 # w MHz
    lenf = 300/float(freq) # w m
    
    hb = self.infobox_btsheight_ninput.GetValue()
    hs = self.infobox_termheight_ninput.GetValue()
    hm = self.infobox_buldheight_ninput.GetValue()
    dist = self.infobox_distance_ninput.GetValue()
    opt = self.radiobox_loslist.GetSelection()

    self.infobox_termheight_ninput.SetBounds(max=hb)
    if (hs>=hb):
        self.OnNotification(0,"Terminal nie powinien znajdywac sie powyzej nadajnika")
        self.infobox_termheight_slider.SetValue(hb-1)
        return 0

    self.axes.cla()
    self.axes.set_xlabel("odleglosc [m]")
    self.axes.set_ylabel("tlumienie [dB]")
    
    if (opt == 0):
        if (hs>=hm):
	    self.axes.set_title("LOS1")
            hp = ((hb-hs)/float(2))-hm
            cf = (4 * pow(hp,2))/float(lenf)
            dist_scalar = 16.5
            #loss_equation = 23 + (20 * log(freq)) + (16.5 * log(dist)) + (22.1 * log(hb) - 10.3 * log(hs)) + 8.45 * log(hb-hm) - 5.31 * log(cf)
            loss_equation = 23 + (20 * log(freq)) + (22.1 * log(hb) - 10.3 * log(hs)) + 8.45 * log(hb-hm) - 5.31 * log(cf)
        else:
            self.axes.set_title("LOS2")
            dist_scalar = 18.1
            #loss_equation = 16.3 + (20 * log(freq)) + (18.1 * log(dist)) + (19.1 * log(hb) - 6.7 * log(hs)) + 12 * log(hb-hm) + 0.6 * log(hm-hs) - 16.2 * log((hb-hs)/float(2))
            loss_equation = 16.3 + (20 * log(freq)) + (19.1 * log(hb) - 6.7 * log(hs)) + 12 * log(hb-hm) + 0.6 * log(hm-hs) - 16.2 * log((hb-hs)/float(2))
    else:
        if (hs>=hm):
	    self.axes.set_title("NLOS1")
            dist_scalar = 21.8
            #loss_equation = 108.6 + (20 * log(freq)) + (21.8 * log(dist)) + (-35 * log(hb) + 16.6 * log(hs)) - 26.3 * log(hb-hm) + 23.9 * log((hb-hs)/float(2))
            loss_equation = 108.6 + (20 * log(freq)) + (-35 * log(hb) + 16.6 * log(hs)) - 26.3 * log(hb-hm) + 23.9 * log((hb-hs)/float(2))
        else:
	    self.axes.set_title("NLOS2")
            dist_scalar = 15.8
            #loss_equation = 83.1 + (20 * log(freq)) + (15.8 * log(dist)) + (19.1 * log(hb) - 20 * log(hs)) - 47.2 * log(hb-hm) + 0.3 * log(hm-hs) + 34.4 * log((hb-hs)/float(2))
            loss_equation = 83.1 + (20 * log(freq)) + (19.1 * log(hb) - 20 * log(hs)) + 47.2 * log(hb-hm) + 0.3 * log(hm-hs) + 34.4 * log((hb-hs)/float(2))

    loss = []
    xgen = range(1,int(dist*1000))
    for x in xgen:
        loss.append(loss_equation+(dist_scalar*log(x/float(1000))))
    #zmienic append na costam
        
    wyn = self.axes.plot(xgen,loss,'b+',linewidth=1)
    if (self.xwatch != 0):
        foundx = self.TakeClosest(xgen,self.xwatch)
        wyn = self.axes.plot((foundx,foundx),self.axes.get_ylim(),'r-',linewidth=1,alpha=0.8)
        if foundx < len(xgen):
            self.axes.text(0.03, 0.03, 'Odleglosc [m]: '+str(xgen.index(foundx))+'\nWartosc [dB]: '+str(round(loss[xgen.index(foundx)],2)), bbox=dict(facecolor='white', alpha=0.5, pad=10),transform=self.axes.transAxes)
    xmin = min(xgen)
    xmax = max(xgen)
    self.axes.set_xbound(lower=xmin, upper=xmax)
    self.canvas.draw()
    
    return 0

def OnPlotClick(self,event):
    if event.inaxes is not None:
        self.xwatch = event.xdata
        RedrawPlot(self,0)
        
