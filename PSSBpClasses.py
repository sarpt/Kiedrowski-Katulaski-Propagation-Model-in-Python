#rTINFrame
import wx.lib.masked
import os

import PSSBpPageFuncs
import PSSBpPlot

# Create a new frame class, derived from the wxPython Frame.
class PSSBpFrame(wx.Frame):

    TakeClosest = PSSBpPageFuncs.TakeClosest
    LabelOnHover = PSSBpPageFuncs.LabelOnHover
    StatusBoxOnLeave = PSSBpPageFuncs.StatusBoxOnLeave
    OnNotification = PSSBpPageFuncs.OnNotification
    OnExit = PSSBpPageFuncs.OnExit
    OnSave = PSSBpPageFuncs.OnSave
    SliderUpdate = PSSBpPageFuncs.SliderUpdate
    
    InitPlot = PSSBpPlot.InitPlot
    RedrawPlot = PSSBpPlot.RedrawPlot
    OnPlotClick = PSSBpPlot.OnPlotClick
    

    def __init__(self, parent, id, title):

        # konstruktor klasy bazowej
        wx.Frame.__init__(self, parent, id, title)

        # minimialna wielkosc okna
        #self.SetSizeHints(450,300)

        # Status bar
        self.CreateStatusBar()

        # stworzenie menu
        self.initMenu()

        ### --- GLOWNY PANEL --- ###
        self.panelmain = wx.Panel(self, -1)

        self.radiobox_loslist = wx.RadioBox(self.panelmain, -1, "Widocznosc", wx.DefaultPosition, wx.DefaultSize,["LOS","NLOS"],2, wx.RA_SPECIFY_COLS)
        self.radiobox_loslist.Bind(wx.EVT_RADIOBOX,self.RedrawPlot)

        # Odleglosc
        self.infobox_distance = wx.StaticBox(self.panelmain,label="Odleglosc")
        
        self.infobox_distance_ntext = wx.StaticText(self.infobox_distance, -1,"l [km]:")
        self.infobox_distance_ntext.Bind(wx.EVT_ENTER_WINDOW,lambda evt, text="Odleglosc pomiedzy nadajnikiem a odbiornikiem w kilometrach":self.LabelOnHover(evt,text))
        self.infobox_distance_ntext.Bind(wx.EVT_LEAVE_WINDOW,self.StatusBoxOnLeave)
        
        self.infobox_distance_ninput = wx.lib.masked.NumCtrl(self.infobox_distance, -1,integerWidth=7, fractionWidth=3, allowNegative=False, min=0.200, max=8.300, value=0.200)
        self.infobox_distance_ninput.Bind(wx.lib.masked.EVT_NUM,self.RedrawPlot)
        
        distance_sizer = wx.FlexGridSizer(1, 2, 5, 5)
        distance_sizer.Add(self.infobox_distance_ntext,1,wx.EXPAND)
        distance_sizer.Add(self.infobox_distance_ninput,1,wx.EXPAND)
        
        self.infobox_distance_slider = wx.Slider(self.infobox_distance,minValue=200,maxValue=8300)
        self.infobox_distance_slider.Bind(wx.EVT_SLIDER,lambda evt, slidid=0:self.SliderUpdate(evt,slidid))
        
        distance_infobox_sizer = wx.StaticBoxSizer(self.infobox_distance, wx.VERTICAL)
        distance_infobox_sizer.Add(distance_sizer, 0, wx.ALIGN_CENTER)
        distance_infobox_sizer.Add(self.infobox_distance_slider, 0, wx.ALIGN_CENTER)

        # Wysokosc nadajnika
        self.infobox_btsheight = wx.StaticBox(self.panelmain,label="Wysokosc nadajnika")
        
        self.infobox_btsheight_ntext = wx.StaticText(self.infobox_btsheight, -1,"hb [m]:")
        self.infobox_btsheight_ntext.Bind(wx.EVT_ENTER_WINDOW,lambda evt, text="Wysokosc na ktorym znajduje sie nadajnik w metrach":self.LabelOnHover(evt,text))
        self.infobox_btsheight_ntext.Bind(wx.EVT_LEAVE_WINDOW,self.StatusBoxOnLeave)
        
        self.infobox_btsheight_ninput = wx.lib.masked.NumCtrl(self.infobox_btsheight, -1, integerWidth=3, fractionWidth=0, allowNegative=False, min=30, max=120, value=30)
        self.infobox_btsheight_ninput.Bind(wx.lib.masked.EVT_NUM,self.RedrawPlot)

        btsheight_sizer = wx.FlexGridSizer(1, 2, 5, 5)
        btsheight_sizer.Add(self.infobox_btsheight_ntext,1,wx.EXPAND)
        btsheight_sizer.Add(self.infobox_btsheight_ninput,1,wx.EXPAND)
        
        self.infobox_btsheight_slider = wx.Slider(self.infobox_btsheight, minValue=30, maxValue=120)
        self.infobox_btsheight_slider.Bind(wx.EVT_SLIDER,lambda evt, slidid=1:self.SliderUpdate(evt,slidid))
        
        btsheight_infobox_sizer = wx.StaticBoxSizer(self.infobox_btsheight, wx.VERTICAL)
        btsheight_infobox_sizer.Add(btsheight_sizer, 0, wx.ALIGN_CENTER)
        btsheight_infobox_sizer.Add(self.infobox_btsheight_slider, 0, wx.ALIGN_CENTER)

        # Wysokosc terminala
        self.infobox_termheight = wx.StaticBox(self.panelmain,label="Wysokosc odbiornika")
        
        self.infobox_termheight_ntext = wx.StaticText(self.infobox_termheight, -1,"hs [m]:")
        self.infobox_termheight_ntext.Bind(wx.EVT_ENTER_WINDOW,lambda evt, text="Wysokosc na ktorym znajduje sie odbiornik w metrach":self.LabelOnHover(evt,text))
        self.infobox_termheight_ntext.Bind(wx.EVT_LEAVE_WINDOW,self.StatusBoxOnLeave)
        
        self.infobox_termheight_ninput = wx.lib.masked.NumCtrl(self.infobox_termheight, -1, integerWidth=3, fractionWidth=0, allowNegative=False, min=3, max=48, value=3)
        self.infobox_termheight_ninput.Bind(wx.lib.masked.EVT_NUM,self.RedrawPlot)

        termheight_sizer = wx.FlexGridSizer(1, 2, 5, 5)
        termheight_sizer.Add(self.infobox_termheight_ntext,1,wx.EXPAND)
        termheight_sizer.Add(self.infobox_termheight_ninput,1,wx.EXPAND)
        
        self.infobox_termheight_slider = wx.Slider(self.infobox_termheight, minValue=3, maxValue=48)
        self.infobox_termheight_slider.Bind(wx.EVT_SLIDER,lambda evt, slidid=2:self.SliderUpdate(evt,slidid))
        
        termheight_infobox_sizer = wx.StaticBoxSizer(self.infobox_termheight, wx.VERTICAL)
        termheight_infobox_sizer.Add(termheight_sizer, 0, wx.ALIGN_CENTER)
        termheight_infobox_sizer.Add(self.infobox_termheight_slider, 0, wx.ALIGN_CENTER)

        # srednia wysokosc budynkow
        self.infobox_buldheight = wx.StaticBox(self.panelmain,label="Srednia wysokosc budynkow")
        
        self.infobox_buldheight_ntext = wx.StaticText(self.infobox_buldheight, -1,"hm [m]:")
        self.infobox_buldheight_ntext.Bind(wx.EVT_ENTER_WINDOW,lambda evt, text="Srednia wysokosc na ktorej znajduja sie dachy budynkow w okolicy trasy propagacjy":self.LabelOnHover(evt,text))
        self.infobox_buldheight_ntext.Bind(wx.EVT_LEAVE_WINDOW,self.StatusBoxOnLeave)
        
        self.infobox_buldheight_ninput = wx.lib.masked.NumCtrl(self.infobox_buldheight, -1, integerWidth=2, fractionWidth=0, allowNegative=False, min=11, max=15, value=11)
        self.infobox_buldheight_ninput.Bind(wx.lib.masked.EVT_NUM,self.RedrawPlot)

        buldheight_sizer = wx.FlexGridSizer(1, 2, 5, 5)
        buldheight_sizer.Add(self.infobox_buldheight_ntext,1,wx.EXPAND)
        buldheight_sizer.Add(self.infobox_buldheight_ninput,1,wx.EXPAND)
        
        self.infobox_buldheight_slider = wx.Slider(self.infobox_buldheight,minValue=11,maxValue=15)
        self.infobox_buldheight_slider.Bind(wx.EVT_SLIDER,lambda evt, slidid=3:self.SliderUpdate(evt,slidid))
        
        buldheight_infobox_sizer = wx.StaticBoxSizer(self.infobox_buldheight, wx.VERTICAL)
        buldheight_infobox_sizer.Add(buldheight_sizer, 0, wx.ALIGN_CENTER)
        buldheight_infobox_sizer.Add(self.infobox_buldheight_slider, 0, wx.ALIGN_CENTER)

        # LEFTSIZER

        leftsizer = wx.BoxSizer(wx.VERTICAL)
        leftsizer.Add(self.radiobox_loslist, flag=wx.ALIGN_CENTER)
        leftsizer.Add(distance_infobox_sizer, flag=wx.ALIGN_CENTER)
        leftsizer.Add(btsheight_infobox_sizer, flag=wx.ALIGN_CENTER)
        leftsizer.Add(termheight_infobox_sizer, flag=wx.ALIGN_CENTER)
        leftsizer.Add(buldheight_infobox_sizer, flag=wx.ALIGN_CENTER)

        # PLOT
        self.InitPlot()
        
        plotsizer = wx.BoxSizer()
        plotsizer.Add(self.canvas, 1, flag=wx.GROW)
        
        # MAIN SIZER

        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        mainsizer.Add(leftsizer, proportion=1, flag=wx.GROW)
        mainsizer.Add(plotsizer, proportion=5, flag=wx.GROW)

        self.panelmain.SetSizerAndFit(mainsizer)

        self.Fit()
        #self.SetDimensions(50,50,600,250)

    def initMenu(self):
        ### --- PASEK MENU --- ###

        # Stworzenie paska menu
        menuBar = wx.MenuBar()
        
        # Dodanie paska do frame'a
        self.SetMenuBar(menuBar) 

        ### --- MENU --- ###

        # Stworzenie menu, jako pojedynczego pionowego elementu
        filemenu= wx.Menu()

        # dodanie do menu elementow
        # wx.ID_ABOUT to wx.ID_EXIT standardowe ID od wx widgets ale moga byc jakies inne czy cos...
        menu_about = filemenu.Append(wx.ID_ABOUT, "&Info","Informacje na temat programu")
        filemenu.AppendSeparator()
        menu_exit = filemenu.Append(wx.ID_EXIT,"Wyjsci&e","Wyjscie z programu")
        filemenu.AppendSeparator()
        menu_save = filemenu.Append(wx.ID_EXIT, "&Zapisz","Zapisz wykres")
        
        # Dodanie menu do paska menu
        menuBar.Append(filemenu,"&Plik") 
        
        ### --- EVENT HANDLERY --- ###
        AboutText = "Program stworzony na potrzeby projektu z przedmiotu Projektowanie Systemow Sieci Bezprzewodowych - Projekt, przez Michala Michalskiego, W-4, Teleinformatyka, TIP"
        self.Bind(wx.EVT_MENU, lambda evt, text=AboutText:self.OnNotification(evt,text), menu_about)
        self.Bind(wx.EVT_MENU, self.OnExit, menu_exit)
        self.Bind(wx.EVT_MENU, self.OnSave, menu_save)

# Every wxWidgets application must have a class derived from wx.App
class PSSBpApp(wx.App):

    # wxWindows calls this method to initialize the application
    def OnInit(self):

        # Create an instance of our customized Frame class
        frame = PSSBpFrame(None, -1, "PSSBp")
        frame.Show(True)

        # Tell wxWindows that this is our main window
        self.SetTopWindow(frame)

        # Return a success flag
        return True
