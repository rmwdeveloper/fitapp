#!/usr/bin/env python
import tkinter as tk
import inputEx as inex
import inputDiet as indi
import viewDiet as vidi
import personalInfo as pein5
##import fitgraphs
##import matplotlib
##import matplotlib.pyplot as plt
##matplotlib.use('TkAgg')
##from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

    
class QuitButton(tk.Button):
    " Terminates the application"
    def __init__(self, parent):
        tk.Button.__init__(self, parent,
                           text    = 'Quit',
                           command = self.quit,
                           relief = tk.RAISED,
                           border = 3 )
        self.parent = parent
class TestAddFoodToDatabaseWindow(tk.Button):
    """
    Opens up the AddFoodToDatabase toplevel window.
    Meant only for testing purposes. 
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Add Food to Day',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'green',
                           command = self.open_window)
        self.parent = parent
        self.addFoodToDatabaseWindow = None

    def open_window(self):
        if self.addFoodToDatabaseWindow is None:
            self.addFoodToDatabaseWindow = indi.AddFoodToDayWindow()
            self.addFoodToDatabaseWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

    def remove_window(self):
        self.addFoodToDatabaseWindow.destroy()
        self.addFoodToDatabaseWindow = None
        

        
##class GraphDisplay(tk.Canvas):
##    """
##    Display area for displaying information depending on what option is selected.
##    """
##    def __init__(self,parent):
##        tk.Canvas.__init__(self, parent,
##                           borderwidth = 3,
##                           relief = tk.SUNKEN,
##                           height = 600,
##                           width = 600)
##        self.parent = parent

        
##class DisplayArea(tk.Canvas):
##    """
##    Display area for displaying information depending on what option is selected.
##    """
##    def __init__(self,parent):
##        tk.Canvas.__init__(self, parent,
##                           borderwidth = 3,
##                           relief = tk.SUNKEN,
##                           height = 600,
##                           width = 600)
####        self.parent = parent
####        self.figure = plt.figure(figsize = (6,6))
####        self.ax = plt.axes([0.1,0.1,0.8,0.8])
####        self.pie = fitgraphs.macronutrient_pie_chart('2014-02-11')
####        self.graphCanvas = FigureCanvasTkAgg(self.figure,self)
####        self.graphCanvas.show()
####        self.graphCanvas.get_tk_widget().grid(row = 0,sticky = 'news')
####        self.toolbar = NavigationToolbar2TkAgg(self.graphCanvas,self.parent)
####        self.toolbar.update()
####        self.graphCanvas._tkcanvas.grid(row = 0,sticky = 'news')
######        graphCanvas.mpl_connect('key_press_event',self.on_key_event)
######        button = tk.Button(master = self.parent, text = 'Quit', command = self.quit)
######        button.grid(sticky = tk.S)
##
##    def on_key_event(self,event):
##        print('you pressed %s'%event.key)
##        key_press_handler(event,graphCanvas,toolbar)
##    def _quit():
##        self.parent.quit()
##        self.parent.destroy()
##class DisplayCanvas(FigureCanvasTkAgg):
##    def __init__(self,figure,parent):
##        FigureCanvasTkAgg(self,figure,parent)
##        self.figure = figure
##        self.parent = parent
        
class DisplayFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          width = 100,
                          height = 100,
                          relief = tk.SUNKEN,
                          borderwidth = 3)
##        self.parent = parent
##        self.displayArea = DisplayArea(self)
        self.parent = parent
##        self.figure = plt.figure(figsize = (6,6))
##        self.ax = plt.axes([0.1,0.1,0.8,0.8])
##        self.pie = fitgraphs.macronutrient_pie_chart('2014-02-12')
##        self.graphCanvas = FigureCanvasTkAgg(self.figure,self.parent)
##        self.graphCanvas.show()
##        self.graphCanvas.get_tk_widget().grid(column = 0, row = 0)
##        
##        self.toolbar = NavigationToolbar2TkAgg(self.graphCanvas,self)
##        self.toolbar.update()
##        self.graphCanvas._tkcanvas.grid(column = 0, row = 0)
##        self.graphCanvas.mpl_connect('key_press_event',self.on_key_event)
##        button = tk.Button(master = self.parent, text = 'Quit', command = self.quit)
##        button.grid(sticky = tk.S,columnrow = 2)
##    def on_key_event(self,event):
##        print('you pressed %s'%event.key)
##        key_press_handler(event,graphCanvas,toolbar)
##    
        
        
        

class PersonalInfoButton(tk.Button):
    "When clicked, shows the personal info window."
    def __init__(self, parent):
        tk.Button.__init__(self,parent,
                           text = 'Enter Personal Information', 
                           relief = tk.RIDGE,
                           border = 3,
                           activeforeground = 'black',
                           activebackground = 'white',
                           width = 20,
                           command = self.open_window)
        self.parent = parent
        self.personalInfoWindow = None
    def open_window(self):
        if self.personalInfoWindow is None:
            self.personalInfoWindow = pein.PersonalInfoWindow(self)
            self.personalInfoWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

    def remove_window(self):
        self.personalInfoWindow.destroy()
        self.personalInfoWindow = None

        
class ViewExerciseButton(tk.Button):
    "When clicked, shows personal bests in the Display Area"
    def __init__(self, parent):
        tk.Button.__init__(self,parent,
                           text = 'View Exercise', 
                           relief = tk.RIDGE,
                           border = 3,
                           activeforeground = 'black',
                           activebackground = 'white')
        self.parent = parent
        

class ViewDietButton(tk.Button):
    "When clicked, shows diet info in the Display Area"
    def __init__(self, parent):
        tk.Button.__init__(self,parent,
                           text = 'View Diet', 
                           relief = tk.RIDGE,
                           border = 3,
                           activeforeground = 'black',
                           activebackground = 'white',
                           width = 10,
                           command = self.open_window)
        self.parent = parent
        self.viewDietWindow = None
    def open_window(self):
        if self.viewDietWindow is None:
            self.viewDietWindow = vidi.ViewDietWindow(self)
            self.viewDietWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

    def remove_window(self):
        self.viewDietWindow.destroy()
        self.viewDietWindow = None
        
        

class InputExerciseButton(tk.Button):
    "Opens a new window that allows for input of exercise information"
    def __init__(self, parent):
        tk.Button.__init__(self, parent,
                           text = 'Input Exercises',
                           relief = tk.RAISED,
                           border = 3,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command = self.open_window)
        self.parent = parent
        self.exerciseWindow = None
        

    def open_window(self):
        if self.exerciseWindow is None:
            self.exerciseWindow = inex.InputExerciseWindow(self)
            self.exerciseWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

    def remove_window(self):
        self.exerciseWindow.destroy()
        self.exerciseWindow = None
            
                                          
class InputDietButton(tk.Button):
    "Opens a new window that allows for input of diet information"
    def __init__(self, parent):
        tk.Button.__init__(self, parent,
                           text = 'Input Diet',
                           relief = tk.RAISED,
                           border = 3,
                           activeforeground = 'black',
                           activebackground = 'white',
                           width = 11,
                           command = self.open_window)
        self.parent = parent
        self.dietWindow = None
        
    def open_window(self):
        if self.dietWindow is None:
            self.dietWindow = indi.InputDietFoodJournalMain(self)
            self.dietWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

    def remove_window(self):
        self.dietWindow.destroy()
        self.dietWindow = None


class GraphsMenu(tk.Menubutton):
    def __init__(self, parent):
        tk.Button.__init__(self, parent,
                           text = 'Graphs',
                           relief = tk.RAISED,
                           border = 3,
                           activeforeground = 'black',
                           activebackground = 'white',
                           width = 11,
                           command = self.open_window)
        self.parent = parent
        self.dietWindow = None
        
    def open_window(self):
        if self.dietWindow is None:
            self.dietWindow = indi.InputDietFoodJournalMain(self)
            self.dietWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

    def remove_window(self):
        self.dietWindow.destroy()
        self.dietWindow = None
class HolderFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          height = 700,
                          width = 800)
        self.parent = parent

        self.personalInfoButton = PersonalInfoButton(self)
        self.personalInfoButton.grid(column = 0, row = 0, padx = 2, pady = 2,sticky = 'e')
        self.personalInfoButton.grid_propagate(0)
        
        self.viewExerciseButton = ViewExerciseButton(self)
        self.viewExerciseButton.grid(column = 0, row = 1, padx = 2, pady = 2)
        
        self.viewDietButton = ViewDietButton(self)
        self.viewDietButton.grid(column = 0, row = 2, padx = 2, pady = 2)
        
        self.inputExerciseButton = InputExerciseButton(self)
        self.inputExerciseButton.grid(column = 0, row = 3, padx = 2, pady = 2)
        
        self.inputDietButton = InputDietButton(self)
        self.inputDietButton.grid(column = 0, row = 4, padx = 2, pady = 2)
        
        self.graphsMenu = GraphsMenu(self)
        self.graphsMenu.grid(column = 0, row = 5)
        
class Application(tk.Frame):
    """
    Creates the topmost frame that contains the display area for
    graphs and all the buttons.
    """
    def __init__(self, parent):
        tk.Frame.__init__(self,parent,
                          height = 700,
                          width = 800)
        self.parent = parent
        top = self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        
        self.grid()
        self.grid_propagate(0)
        

        #Widgets
##        self.quitButton = QuitButton(self)
##        self.quitButton.grid( padx = 2 , pady = 2)
        
##        self.displayArea = DisplayArea(self)
##        self.displayArea.grid(column = 0, sticky = tk.NW)
        self.displayFrame = DisplayFrame(self)
        self.displayFrame.grid(column = 0, row = 1,sticky = 'news')

        self.holderFrame = HolderFrame(self)
        self.holderFrame.grid(column = 1, row = 0, sticky = 'news')

##        self.personalInfoButton = PersonalInfoButton(self)
##        self.personalInfoButton.grid(column = 0, row = 2, padx = 2, pady = 2,sticky = 'e')
##        self.personalInfoButton.grid_propagate(0)
##        
##        self.viewExerciseButton = ViewExerciseButton(self)
##        self.viewExerciseButton.grid(column = 5, row = 2, padx = 2, pady = 2)
##        
##        self.viewDietButton = ViewDietButton(self)
##        self.viewDietButton.grid(column = 5, row = 3, padx = 2, pady = 2)
##        
##        self.inputExerciseButton = InputExerciseButton(self)
##        self.inputExerciseButton.grid(column = 6, row = 2, padx = 2, pady = 2)
##        
##        self.inputDietButton = InputDietButton(self)
##        self.inputDietButton.grid(column = 6, row = 3, padx = 2, pady = 2)
##        
##        self.graphsMenu = GraphsMenu(self)
##        self.graphsMenu.grid(column = 2, row = 1)
        
        
if __name__ == "__main__":
    fit_app = Application(None)
    fit_app.master.title("Fitness Application")
    fit_app.mainloop()

