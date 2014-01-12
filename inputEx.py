import datetime
import tkinter as tk
import inputExLogic as inexlo

#GUI variables
LABEL_WIDTH= 200
LABEL_HEIGHT = 110

#Date variables


#START ENTRY
class SetsEntry(tk.Entry):
    
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          width = 31
                          )
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.insert(0, 'Sets')
        self.grid(row = 0,sticky= tk.E+tk.W)
        
    def get_entry(self):
        return self.get()


class RepsEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          )
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.insert(0, 'Reps')
        self.grid(row = 1,sticky= 'ew')

    def get_entry(self):
        return self.get()


class WeightEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          )
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.insert(0, 'Weight')
        self.grid(row = 2,sticky= 'ew')

    def get_entry(self):
        return self.get()


class EntryConfirmButton(tk.Button):
    def __init__(self,parent,setsEntry,repsEntry,weightEntry):
        tk.Button.__init__(self, parent,
                           text = 'Enter',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command = lambda:self.get_entry())
        self.parent = parent
        self.setsEntry = setsEntry
        self.repsEntry = repsEntry
        self.weightEntry = weightEntry
        self.initialize()

    def initialize(self):
        self.grid(row = 3,sticky= 'ew')

    def get_entry(self):
        """
        Displays the entry to the DisplayArea
        """
        entries = []
        entries.append(self.setsEntry.get_entry())
        entries.append(self.repsEntry.get_entry())
        entries.append(self.weightEntry.get_entry())
        self.parent.parent.controller.displayFrame.displayArea.insert(tk.END,'Exercise: '+self.parent.cget('text')+'\n')
        self.parent.parent.controller.displayFrame.displayArea.insert(tk.END,'--------------------' + '\n')
        self.parent.parent.controller.displayFrame.displayArea.insert(tk.END,'Sets: '+ entries[0] + ' Reps: '+ entries[1] + ' Weight: '+entries[2] + '\n')
        self.parent.parent.controller.displayFrame.displayArea.edit_separator() 
#END ENTRY        
#START BACK    
class DeadLiftLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Deadlift',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        deadLiftSets = SetsEntry(self)
        deadLiftReps = RepsEntry(self)
        deadLiftWeight = WeightEntry(self)
        deadLiftEnter = EntryConfirmButton(self,deadLiftSets,deadLiftReps,deadLiftWeight)


class GoodMorningLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Good Morning',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    
    def initialize(self):
        self.grid(padx = 4, pady = 4)
        self.grid_propagate(0)
        goodMorningSets = SetsEntry(self)
        goodMorningReps = RepsEntry(self)
        goodMorningWeight = WeightEntry(self)
        goodMorningEnter = EntryConfirmButton(self,goodMorningSets,goodMorningReps,goodMorningWeight)


class BentOverRowBarbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bent Over Row(Barbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    
    def initialize(self):
        self.grid()
        self.grid_propagate(0)
        bentOverRowBarbellSets = SetsEntry(self)
        bentOverRowBarbellReps = RepsEntry(self)
        bentOverRowBarbellWeight = WeightEntry(self)
        bentOverRowBarbellEnter = EntryConfirmButton(self,bentOverRowBarbellSets,bentOverRowBarbellReps,bentOverRowBarbellWeight)


class BentOverRowDumbbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bent Over Row(Dumbbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    
    def initialize(self):
        self.grid(padx = 4, pady = 4)
        self.grid_propagate(0)
        bentOverRowDumbbellSets = SetsEntry(self)
        bentOverRowDumbbellReps = RepsEntry(self)
        bentOverRowDumbbellWeight = WeightEntry(self)
        bentOverRowDumbbellEnter = EntryConfirmButton(self,bentOverRowDumbbellSets,bentOverRowDumbbellReps,bentOverRowDumbbellWeight)        


class BackFrame(tk.Frame):
    """
    Display Area for Chest Labels and Frames
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,
                          borderwidth = 2,
                          relief = tk.RAISED,
                          height =  200,
                          width = 200)
        self.parent = parent
        self.controller = controller
        self.initialize()
        entries_dict = {}
        self.entries_dict = entries_dict

    def initialize(self):
        self.grid(column= 0, row = 0,
                       sticky = tk.N)
        self.deadLiftLabel = DeadLiftLabel(self)
        self.goodMorningLabel = GoodMorningLabel(self)
        self.bentOverRowBarbellLabel = BentOverRowBarbellLabel(self)
        self.bentOverRowDumbbellLabel = BentOverRowDumbbellLabel(self)

    def __iter__(self):
        return iter(self._iterable)
#END BACK
#START CHEST
class BenchPressBarbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Barbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4, pady = 4)
        self.grid_propagate(0)
        benchPressBarbellSets = SetsEntry(self)
        benchPressBarbellReps = RepsEntry(self)
        benchPressBarbellWeight = WeightEntry(self)
        benchPressBarbellEnter = EntryConfirmButton(self,benchPressBarbellSets,benchPressBarbellReps,benchPressBarbellWeight)


class BenchPressInclineBarbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Incline)(Barbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    
    def initialize(self):
        self.grid(padx = 4, pady = 4)
        self.grid_propagate(0)
        benchPressInclineBarbellSets = SetsEntry(self)
        benchPressInclineBarbellReps = RepsEntry(self)
        benchPressInclineBarbellWeight = WeightEntry(self)
        benchPressInclineBarbellEnter = EntryConfirmButton(self,benchPressInclineBarbellSets,benchPressInclineBarbellReps,benchPressInclineBarbellWeight)


class BenchPressDeclineBarbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Decline)(Barbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    
    def initialize(self):
        self.grid(padx = 4, pady = 4)
        self.grid_propagate(0)
        benchPressDeclineBarbellSets = SetsEntry(self)
        benchPressDeclineBarbellReps = RepsEntry(self)
        benchPressDeclineBarbellWeight = WeightEntry(self)
        benchPressDeclineBarbellEnter = EntryConfirmButton(self,benchPressDeclineBarbellSets,benchPressDeclineBarbellReps,benchPressDeclineBarbellWeight)


class BenchPressDumbbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Dumbbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    
    def initialize(self):
        self.grid(padx = 4, pady = 4)
        self.grid_propagate(0)
        benchPressDumbbellSets = SetsEntry(self)
        benchPressDumbbellReps = RepsEntry(self)
        benchPressDumbbellWeight = WeightEntry(self)
        benchPressDumbbellEnter = EntryConfirmButton(self,benchPressDumbbellSets,benchPressDumbbellReps,benchPressDumbbellWeight)


class BenchPressInclineDumbbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Incline)(Dumbbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4, pady = 4)
        self.grid_propagate(0)
        benchPressInclineDumbbellSets = SetsEntry(self)
        benchPressInclineDumbbellReps = RepsEntry(self)
        benchPressInclineDumbbellWeight = WeightEntry(self)
        benchPressInclineDumbbellEnter = EntryConfirmButton(self,benchPressInclineDumbbellSets,benchPressInclineDumbbellReps,benchPressInclineDumbbellWeight)


class BenchPressDeclineDumbbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Decline)(Dumbbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4, pady = 4)
        self.grid_propagate(0)
        benchPressDeclineDumbbellSets = SetsEntry(self)
        benchPressDeclineDumbbellReps = RepsEntry(self)
        benchPressDeclineDumbbellWeight = WeightEntry(self)
        benchPressDeclineDumbbellEnter = EntryConfirmButton(self,benchPressDeclineDumbbellSets,benchPressDeclineDumbbellReps,benchPressDeclineDumbbellWeight)


class ChestFrame(tk.Frame):
    """
    Display Area for Chest Labels and Frames
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,
                          borderwidth = 2,
                          relief = tk.RAISED,
                          height =  200,
                          width = 200)
        self.parent = parent
        self.controller = controller
        self.initialize()

    def initialize(self):
        self.grid(column = 0, row = 0)
        self.benchPressBarbellLabel = BenchPressBarbellLabel(self)
        self.benchPressInclineBarbellLabel = BenchPressInclineBarbellLabel(self)
        self.benchPressDeclineBarbellLabel = BenchPressDeclineBarbellLabel(self)
        self.benchPressDumbbellLabel = BenchPressDumbbellLabel(self)
        self.benchPressInclineDumbbellLabel = BenchPressInclineDumbbellLabel(self)
        self.benchPressDeclineDumbbellLabel = BenchPressDeclineDumbbellLabel(self)
        
    def __iter__(self):
        return iter(self._iterable)
#END CHEST
#START LEGS
class SquatLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Squat',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        squatSets = SetsEntry(self)
        squatReps = RepsEntry(self)
        squatWeight = WeightEntry(self)
        squatEnter = EntryConfirmButton(self,squatSets,squatReps,squatWeight)


class FrontSquatLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Front Squat',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        frontSquatSets = SetsEntry(self)
        frontSquatReps = RepsEntry(self)
        frontSquatWeight = WeightEntry(self)
        frontSquatEnter = EntryConfirmButton(self,frontSquatSets,frontSquatReps,frontSquatWeight)


class LegPressLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Leg Press',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        legPressSets = SetsEntry(self)
        legPressReps = RepsEntry(self)
        legPressWeight = WeightEntry(self)
        legPressEnter = EntryConfirmButton(self,legPressSets,legPressReps,legPressWeight)


class CalfRaiseLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Calf Raise',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        calfRaiseSets = SetsEntry(self)
        calfRaiseReps = RepsEntry(self)
        calfRaiseWeight = WeightEntry(self)
        calfRaiseEnter = EntryConfirmButton(self,calfRaiseSets,calfRaiseReps,calfRaiseWeight)


class LegsFrame(tk.Frame):
    """
    Display Area for Legs Labels and Frames
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,
                          borderwidth = 2,
                          relief = tk.RAISED,
                          height =  200,
                          width = 200)
        self.parent = parent
        self.controller = controller
        self.initialize()

    def initialize(self):
        self.grid(column = 0, row = 0)
        self.squatLabel = SquatLabel(self)
        self.frontSquatLabel = FrontSquatLabel(self)
        self.legPressLabel = LegPressLabel(self)
        self.calfRaiseLabel = CalfRaiseLabel(self)
     
    def __iter__(self):
        return iter(self._iterable)   
#END LEGS
#START SHOULDERS
class OverheadPressLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Overhead Press',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        overheadPressSets = SetsEntry(self)
        overheadPressReps = RepsEntry(self)
        overheadPressWeight = WeightEntry(self)
        overheadPressEnter = EntryConfirmButton(self,overheadPressSets,overheadPressReps,overheadPressWeight)


class ShrugsLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Shrugs',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        shrugsSets = SetsEntry(self)
        shrugsReps = RepsEntry(self)
        shrugsWeight = WeightEntry(self)
        shrugsEnter = EntryConfirmButton(self,shrugsSets,shrugsReps,shrugsWeight)


class BehindNeckPressLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Behind Neck Press',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        behindNeckPressSets = SetsEntry(self)
        behindNeckPressReps = RepsEntry(self)
        behindNeckPressWeight = WeightEntry(self)
        behindNeckPressEnter = EntryConfirmButton(self,behindNeckPressSets,behindNeckPressReps,behindNeckPressWeight)


class SeatedMilitaryPressLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Seated Military Press',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        seatedMilitaryPressSets = SetsEntry(self)
        seatedMilitaryPressReps = RepsEntry(self)
        seatedMilitaryPressWeight = WeightEntry(self)
        seatedMilitaryPressEnter = EntryConfirmButton(self,seatedMilitaryPressSets,seatedMilitaryPressReps,seatedMilitaryPressWeight)        


class UprightRowLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Upright Row',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        uprightRowSets = SetsEntry(self)
        uprightRowReps = RepsEntry(self)
        uprightRowWeight = WeightEntry(self)
        uprightRowEnter = EntryConfirmButton(self,uprightRowSets,uprightRowReps,uprightRowWeight)


class ChinupsLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Chinup',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        self.initialize()
        entries_dict = {}
        self.entries_dict= entries_dict
        
    def initialize(self):
        self.grid(padx = 4,  sticky = tk.E + tk.W)
        self.grid_propagate(0)
        chinupsSets = SetsEntry(self)
        chinupsReps = RepsEntry(self)
        chinupsWeight = WeightEntry(self)
        chinupsEnter = EntryConfirmButton(self,chinupsSets,chinupsReps,chinupsWeight)

        
class ShouldersFrame(tk.Frame):
    """
    Display Area for Legs Labels and Frames
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,
                          borderwidth = 2,
                          relief = tk.RAISED,
                          height =  200,
                          width = 200)
        self.parent = parent
        self.controller = controller
        self.initialize()

    def initialize(self):
        self.grid(column = 0, row = 0)
        self.overheadPressLabel = OverheadPressLabel(self)
        self.shrugsLabel = ShrugsLabel(self)
        self.behindNeckPressLabel = BehindNeckPressLabel(self)
        self.seatedMilitaryPressLabel = SeatedMilitaryPressLabel(self)
        self.uprightRowLabel = UprightRowLabel(self)
        self.chinupsLabel= ChinupsLabel(self)

    def __iter__(self):
        return iter(self._iterable)
#END SHOULDERS
#START DISPLAY
class SaveButton(tk.Button):
    """
    Saves entries in the DisplayArea. 
    """
    def __init__(self,parent,displayAreaControlled):
        tk.Button.__init__(self, parent,
                           text = 'Save',
                           relief = tk.RIDGE,
                           border = 2,
                           height =  2,
                           width = 17,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command =lambda: self.save_entries())
        self.parent = parent
        self.displayAreaControlled=displayAreaControlled
        self.initialize()

    def initialize(self):
        self.grid()

    def save_entries(self):
        """
        Saves the entries in the DisplayArea as a dictionary with the following structure:
        {'exercise name':(sets, reps, weight)}
        """
        #Testing Vals
        str1= self.displayAreaControlled.get('1.0',tk.END)
        print(str1)
        ##

        entries_dict = {}
        

class UndoButton(tk.Button):
    """
    Undo's the last entry in the DisplayArea 
    """
    def __init__(self,parent,displayAreaControlled):
        tk.Button.__init__(self, parent,
                           text = 'Undo Last Entry',
                           relief = tk.RIDGE,
                           border = 2,
                           height =  2,
                           width = 17,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command =lambda: self.undo_last_entry())
        self.parent = parent
        self.displayAreaControlled=displayAreaControlled
        self.initialize()

    def initialize(self):
        self.grid(column = 0,row = 0, ipady= 2,sticky =  tk.W + tk.N)

    def undo_last_entry(self):
        
        if len(self.displayAreaControlled.get('1.0',tk.END)) > 1:
            self.displayAreaControlled.edit_undo()
            self.displayAreaControlled.undo_number += 1
            
        
class RedoButton(tk.Button):
    """
    Redo's the last entry in the DisplayArea 
    """
    def __init__(self,parent,displayAreaControlled):
        tk.Button.__init__(self, parent,
                           text = 'Redo Last Entry',
                           relief = tk.RIDGE,
                           border = 2,
                           height =  2,
                           width = 17,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command =lambda: self.redo_last_entry())
        self.parent = parent
        self.displayAreaControlled=displayAreaControlled
        self.initialize()

    def initialize(self):
        self.grid(column = 0 ,row = 0, ipady= 2, sticky = tk.E + tk.N)

    def redo_last_entry(self):
        if self.displayAreaControlled.redo_number < self.displayAreaControlled.undo_number:
            self.displayAreaControlled.edit_redo()
            self.displayAreaControlled.redo_number += 1


                      
class DisplayArea(tk.Text):
    """
    Display area for displaying information depending on what option is selected.
    """
    def __init__(self,parent):
        tk.Text.__init__(self, parent,
                           borderwidth = 3,
                           height = 50,
                         width = 70,
                         undo = True)
        self.parent = parent
        #Undo and redo numbers, don't perform if undo_number == redo_number
        self.undo_number = 0
        self.redo_number = 0
        self.initialize()

    def display_inputs(self, inputs):
        """
        Inputs are the contents of a [Workout] Label when an entry is confirmed.
        Type is to be determined. 
        """
        self.insert('1.0', inputs)
    
    def initialize(self):
        top = self.winfo_toplevel()
        self.grid(row = 1)
        
        
class DisplayFrame(tk.Frame):
    """
    Containing frame for the text DisplayArea
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief = tk.SUNKEN,
                          width = 70,
                          borderwidth = 5)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid(column = 1, row = 0, sticky = tk.N)
        

        #Date Menu START
        self.dateVar = tk.StringVar(self)
        today = datetime.date.today()
        yesterday = datetime.date.today() - datetime.timedelta(1)
        twodaysago = datetime.date.today() - datetime.timedelta(2)
        threedaysago = datetime.date.today() - datetime.timedelta(3)
        fourdaysago = datetime.date.today() - datetime.timedelta(4)
        fivedaysago = datetime.date.today() - datetime.timedelta(5)
        sixdaysago = datetime.date.today() - datetime.timedelta(6)
        sevendaysago = datetime.date.today() - datetime.timedelta(7)
        
        self.dateVar.set("Date")
        
        dateMenu = tk.OptionMenu(self, self.dateVar,
                                 today, yesterday, twodaysago,
                                 threedaysago,fourdaysago,
                                 fivedaysago,sixdaysago,
                                 sevendaysago)

        dateMenu.grid()

        
        #Date Menu END

        
        displayArea = DisplayArea(self)
        self.displayArea = displayArea
        undoButton = UndoButton(self,displayArea)
        self.undoButton = undoButton
        redoButton = RedoButton(self,displayArea)
        self.redoButton = redoButton
        saveButton = SaveButton(self,displayArea)
        self.saveButton = saveButton

    
        
        
        
#END DISPLAY        
#START SELECTION FRAME AND CHILDREN
class SelectBack(tk.Radiobutton):
    """
    Allows the user to select a group of exercises from
    Back, Shoulder, Chest, and Legs that will show up in the Input
    Exercise Window ready for entry
    """
    def __init__(self,parent,controller):
        tk.Radiobutton.__init__(self, parent,
                                command = lambda: controller.pass_to_parent(BackFrame),
                                indicatoron = 0,
                                value = 'Back',
                                text = 'Display Back Exercises')
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid(column = 0, row = 0)

    def pass_to_parent(self,c):
        return self.parent.pass_to_parent(c)


class SelectShoulders(tk.Radiobutton):
    """
    Allows the user to select a group of exercises from
    Back, Shoulder, Chest, and Legs that will show up in the Input
    Exercise Window ready for entry
    """
    def __init__(self,parent,controller):
        tk.Radiobutton.__init__(self, parent,
                                command = lambda: controller.pass_to_parent(ShouldersFrame),
                                indicatoron = 0,
                                value = 'shoulders',
                                text = 'Display Shoulder Exercises')
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid(column = 1, row = 0)

    def showShoulders(self):
        print('test')


class SelectChest(tk.Radiobutton):
    """
    Allows the user to select a group of exercises from
    Back, Shoulder, Chest, and Legs that will show up in the Input
    Exercise Window ready for entry
    """
    def __init__(self,parent,controller):
        tk.Radiobutton.__init__(self, parent,
                                command = lambda: controller.pass_to_parent(ChestFrame),
                                indicatoron = 0,
                                value = 'chest',
                                text = 'Display Chest Exercises')
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid(column = 2, row = 0)

    def showChest(self):
        print('test')


class SelectLegs(tk.Radiobutton):
    """
    Allows the user to select a group of exercises from
    Back, Shoulder, Chest, and Legs that will show up in the Input
    Exercise Window ready for entry
    """
    def __init__(self,parent,controller):
        tk.Radiobutton.__init__(self, parent,
                                command = lambda: controller.pass_to_parent(LegsFrame),
                                indicatoron = 0,
                                value = 'legs',
                                text = 'Display Legs Exercises')
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid(column = 3, row = 0)

    def showLegs(self):
        print('test')


class SelectionFrame(tk.Frame):
    """
    Containing Frame that holds all the selection radiobuttons.
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent, borderwidth = 3,
                          relief = tk.RAISED)
        self.parent = parent
        self.initialize()

    def pass_to_parent(self, c):
        """
        Passes Frame to controller
        """
        return self.parent.show_frame(c)

    def initialize(self):
        self.grid(column = 0, row = 0, sticky = tk.N + tk.W + tk.E)
        selectBack = SelectBack(self,self)
        selectChest = SelectChest(self,self)
        selectShoulders = SelectShoulders(self,self)
        selectLegs = SelectLegs(self,self)
#END SELECTION FRAME AND CHILDREN                            
                           
class InputExerciseWindow(tk.Toplevel):
    "The window in which  exercise information can be added"
    def __init__(self, parent = None):
        tk.Toplevel.__init__(self,parent,
                             height = 400,
                             width = 400)
        container = tk.Frame(self,
                             relief = tk.RAISED,
                             borderwidth = 5)
        container.grid(column= 0, row = 0,
                       sticky = 'news',
                       pady=30)
        container.columnconfigure(0, weight = 1)
        container.rowconfigure(0, weight = 1)

        self.frames = {}
        for F in (BackFrame,LegsFrame,ChestFrame,ShouldersFrame):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(column = 0, row = 0, sticky = 'news')
            

        self.show_frame(LegsFrame)
        self.parent = parent
        self.title("Exercise Input")
        self.initialize()

    def show_frame(self, c):
        """
        Show a frame for the given class.
        """
        frame = self.frames[c]
        frame.tkraise()
    
    def initialize(self):
        
        self.grid()
##        entries_dict = {}
##        self.entries_dict= entries_dict
        
        #Widgets
        selectionFrame = SelectionFrame(self,self)
        displayFrame = DisplayFrame(self)
        self.displayFrame = displayFrame
        
