#!/usr/bin/env python
import tkinter as tk
import pickle as pk
import inputEx as exerinput

    
class QuitButton(tk.Button):
    " Terminates the application"
    def __init__(self, parent):
        tk.Button.__init__(self, parent,
                           text    = 'Quit',
                           command = self.quit,
                           relief = tk.RAISED,
                           border = 3 )
        self.parent = parent
        self.initialize()
    def initialize(self):
        self.grid( padx = 2 , pady = 2)

        

class DisplayArea(tk.Canvas):
    """
    Display area for displaying information depending on what option is selected.
    """
    def __init__(self,parent):
        tk.Canvas.__init__(self, parent,
                           borderwidth = 3,
                           relief = tk.SUNKEN,
                           height = 600,
                           width = 600)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid(column = 0, sticky = tk.NW)

        

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
        self.initialize()

    def initialize(self):
        self.grid(column = 5, row = 2, padx = 2, pady = 2)

        

class ViewDietButton(tk.Button):
    "When clicked, shows diet info in the Display Area"
    def __init__(self, parent):
        tk.Button.__init__(self,parent,
                           text = 'View Diet', 
                           relief = tk.RIDGE,
                           border = 3,
                           activeforeground = 'black',
                           activebackground = 'white',
                           width = 10)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid(column = 5, row = 3, padx = 2, pady = 2)

        

class InputExerciseButton(tk.Button):
    "Opens a new window that allows for input of exercise information"
    def __init__(self, parent):
        tk.Button.__init__(self, parent,
                           text = 'Input Exercises',
                           relief = tk.RAISED,
                           border = 3,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command = self.openwindow)
        self.parent = parent
        self.initialize()
        self.exerciseWindow = None
        
    def initialize(self):
        self.grid(column = 6, row = 2, padx = 2, pady = 2)

    def openwindow(self):
        if self.exerciseWindow is None:
            self.exerciseWindow = exerinput.InputExerciseWindow(self)
            self.exerciseWindow.protocol('WM_DELETE_WINDOW', self.removewindow)

    def removewindow(self):
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
                           width = 11)
        self.parent = parent
        self.initialize()
    def initialize(self):
        self.grid(column = 6, row = 3, padx = 2, pady = 2)

class GraphsMenu(tk.Menubutton):
    def __init__(self,parent):
        tk.Menubutton.__init__(self,parent, text = 'Menu')
        self.parent = parent
        self.initialize()
    def initialize(self):
        self.grid()
    
    
        
    
class Application(tk.Frame):
    """
    Creates the topmost frame that contains the display area for
    graphs and all the buttons.
    """
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        top = self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        self.grid()

        #Widgets
        quitButton = QuitButton(self)
        displayArea = DisplayArea(self)
        viewExerciseButton = ViewExerciseButton(self)
        viewDietButton = ViewDietButton(self)
        inputExerciseButton = InputExerciseButton(self)
        inputDietButton = InputDietButton(self)
        graphsMenu = GraphsMenu(self)
        
        
        
        
    
        
        
        
if __name__ == "__main__":
    fit_app = Application(None)
    fit_app.master.title("Fitness Application")
    fit_app.mainloop()

