from wx import MessageDialog, OK, ID_OK, FD_OPEN, FD_FILE_MUST_EXIST, ID_CANCEL, FileDialog, SAVE
from os import getcwd
from bisect import bisect_left

def isfloat(text):
    try:
        inNumberfloat = float(text)
        return True
    except ValueError:
        pass
    return False
    
def OnNotification(self, event, text):
    dlg = MessageDialog(self,text,"Informacja od programu",OK)
    dlg.ShowModal()
    dlg.Destroy()
        
def OnExit(self):
    self.Close(True)

def OnSave(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = FileDialog(
            self, 
            message="Zapisz wykres jako...",
            defaultDir=getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=SAVE)
        
        if dlg.ShowModal() == ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=100)

def LabelOnHover(self,event,text):
    self.SetStatusText(text)
    
def StatusBoxOnLeave(self, event):
    self.SetStatusText("")

def SliderUpdate(self,event,slidid):
    if (slidid == 0):
        self.infobox_distance_ninput.SetValue(self.infobox_distance_slider.GetValue()/float(1000))
    elif (slidid == 1):
        self.infobox_btsheight_ninput.SetValue(self.infobox_btsheight_slider.GetValue())
    elif (slidid == 2):
        self.infobox_termheight_ninput.SetValue(self.infobox_termheight_slider.GetValue())
    elif (slidid == 3):
        self.infobox_buldheight_ninput.SetValue(self.infobox_buldheight_slider.GetValue())
    
def UpdateSlider(self,slidid):
    if (slidid == 0):
        self.infobox_distance_slider.SetValue(self.infobox_distance_ninput.GetValue())
    elif (slidid == 1):
        self.infobox_btsheight_slider.SetValue(self.infobox_btsheight_ninput.GetValue())
    elif (slidid == 2):
        self.infobox_termheight_slider.SetValue(self.infobox_termheight_ninput.GetValue())
    elif (slidid == 3):
        self.infobox_buldheight_slider.SetValue(self.infobox_buldheight_ninput.GetValue())

def TakeClosest(self,myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before