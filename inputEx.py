import datetime
import tkinter as tk
import tkinter.messagebox as tkm
import sqlite3 as lite
import fitDatabase as data
import copy 

#GUI variables
LABEL_WIDTH= 200
LABEL_HEIGHT = 110

#Date variables

#START ENTRY
class SetsEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief=tk.RAISED,
                          width=31
                          )
        self.parent = parent
        self.insert(0, 'Sets')
        self.grid(row =0, sticky=tk.E+tk.W)
        
    def get_entry(self):
        return self.get()
    

class RepsEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          )
        self.parent = parent
        self.insert(0, 'Reps')
        self.grid(row = 1, sticky= 'ew')

    def get_entry(self):
        return self.get()
    

class WeightEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          )
        self.parent = parent
        self.insert(0, 'Weight')
        self.grid(row = 2, sticky= 'ew')

    def get_entry(self):
        return self.get()

    
class DistanceEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          )
        self.parent = parent
        self.insert(0, 'Distance')
        self.grid(row = 0,sticky= 'ew')

    def get_entry(self):
        return self.get()

    
class TimeEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          )
        self.parent = parent
        self.insert(0, 'Time in minutes')
        self.grid(row = 1,sticky= 'ew')

    def get_entry(self):
        return self.get()


class EntryConfirmButton(tk.Button):
    def __init__(
                 self,parent,setsEntry = None,
                 repsEntry = None,weightEntry = None,
                 distanceEntry = None,timeEntry= None):
        tk.Button.__init__(
                           self, parent,
                           text = 'Enter', relief = tk.RIDGE,
                           border = 2, activeforeground = 'black',
                           activebackground = 'white',
                           command=lambda:self.get_entry(self.parent.exercise_type))
        self.parent = parent
        self.setsEntry = setsEntry
        self.repsEntry = repsEntry
        self.weightEntry = weightEntry
        self.distanceEntry = distanceEntry
        self.timeEntry = timeEntry
       
        self.grid(row = 4,sticky= 'ew')
        
    def append_to_tuple_list(self,exercise_type):
        """
           Appends a tuple of the entry to a dict in the InputExerciseWindow.
        """
        
        if exercise_type == 'strength training':
            try:
                sql_enterable_tuple = ((self.parent.parent.controller.displayFrame.
                                        saveButton.get_selected_date()),
                                       self.parent.parent.controller.displayFrame.
                                       saveButton.get_exercise_id(self.parent.
                                                                  cget('text')),
                                       
                                       
                                           int(self.setsEntry.get_entry()),
                                           int(self.repsEntry.get_entry()),
                                           float(self.weightEntry.get_entry()))
            except ValueError:
                tkm.showerror('Wrong Entry', 'Enter numbers for sets/reps/weight')
                return 
        if exercise_type == 'cardio':
            try:
                sql_enterable_tuple = (
                                       self.parent.parent.controller.displayFrame.
                                       saveButton.get_selected_date(),
                                       self.parent.parent.controller.displayFrame.
                                       saveButton.get_exercise_id(self.parent.
                                                                  cget('text')),
                                       float(self.distanceEntry.get_entry()),
                                       self.parent.distanceVar.get(),
                                       float(self.timeEntry.get_entry()))
            except ValueError:
                tkm.showerror('Wrong Entry', 'Enter numbers for distance and time')
                return 
        (self.parent.parent.controller.
         dict_of_tuples_to_be_entered_in_the_database[exercise_type].
         append(sql_enterable_tuple))
        self.parent.parent.controller.add_order.append(exercise_type)
   
    def get_entry(self, exercise_type):
        """
        Displays the entry to the DisplayArea
        """
        self.append_to_tuple_list(exercise_type)
        (self.parent.parent.controller.displayFrame.
         displayArea.display_entries_in_main_dict())
#END ENTRY
#START CARDIO
class WalkingLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Walking',
                               height = LABEL_HEIGHT+15,
                               width = LABEL_WIDTH)
                     
        self.parent = parent
        self.text = 'Walking'
        entries_dict = {}
        self.entries_dict= entries_dict
        walkingDistance = DistanceEntry(self)
        walkingTime = TimeEntry(self)
        #Distance Type Menu START
        self.distanceVar = tk.StringVar(self)
        mile = 'mile'
        feet = 'feet'
        
        self.distanceVar.set(mile)
        
        distanceMenu = tk.OptionMenu(self, self.distanceVar,
                                 mile,feet)
        distanceMenu.grid(column = 3, row = 0)
        #Distance Type Menu END
        
        walkingEnter = EntryConfirmButton(self,
                                          distanceEntry = walkingDistance,
                                          timeEntry = walkingTime)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')
class RunningLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Running',
                               height = LABEL_HEIGHT+15,
                               width = LABEL_WIDTH)
                     
        self.parent = parent
        self.text = 'Running'
        entries_dict = {}
        self.entries_dict= entries_dict
        runningDistance = DistanceEntry(self)
        runningTime = TimeEntry(self)
        #Distance Type Menu START
        self.distanceVar = tk.StringVar(self)
        mile = 'mile'
        feet = 'feet'
        
        self.distanceVar.set(mile)
        
        distanceMenu = tk.OptionMenu(self, self.distanceVar,
                                 mile,feet)
        distanceMenu.grid(column = 3, row = 0)
        #Distance Type Menu END
        
        runningEnter = EntryConfirmButton(self,
                                          distanceEntry = runningDistance,
                                          timeEntry = runningTime)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')

    
class SwimmingLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Swimming',
                               height = LABEL_HEIGHT+15,
                               width = LABEL_WIDTH)
                     
        self.parent = parent
        self.text = 'Swimming'
        entries_dict = {}
        self.entries_dict= entries_dict
        swimmingDistance = DistanceEntry(self)
        swimmingTime = TimeEntry(self)
        #Distance Type Menu START
        self.distanceVar = tk.StringVar(self)
        mile = 'mile'
        feet = 'feet'
        
        self.distanceVar.set(mile)
        
        distanceMenu = tk.OptionMenu(self, self.distanceVar,
                                 mile,feet)
        distanceMenu.grid(column = 3, row = 0)
        #Distance Type Menu END
        
        swimmingEnter = EntryConfirmButton(self,
                                           distanceEntry = swimmingDistance,
                                           timeEntry = swimmingTime)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')
   
class CardioFrame(tk.Frame):
    """
    Display Area for Cardio related exercise. 
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent,
                          borderwidth = 2,
                          relief = tk.RAISED,
                          height =  200,
                          width = 200)
        self.parent = parent
        self.controller = controller
        entries_dict = {}
        self.entries_dict = entries_dict
        children = []
        for F in (WalkingLabel,RunningLabel,SwimmingLabel):
            self.F = F(self)
            children.append(self.F)
            self.F.grid(padx = 4, sticky = tk.E + tk.W)
            self.F.exercise_type = 'cardio'
            self.F.grid_propagate(0)
#END CARDIO
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
        self.text = 'Deadlift'
        entries_dict = {}
        self.entries_dict= entries_dict
        deadLiftSets = SetsEntry(self)
        deadLiftReps = RepsEntry(self)
        deadLiftWeight = WeightEntry(self)
        deadLiftEnter = EntryConfirmButton(self,deadLiftSets,deadLiftReps,
                                           deadLiftWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class GoodMorningLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Good Morning',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        goodMorningSets = SetsEntry(self)
        goodMorningReps = RepsEntry(self)
        goodMorningWeight = WeightEntry(self)
        goodMorningEnter = EntryConfirmButton(self,goodMorningSets,
                                              goodMorningReps,goodMorningWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class BentOverRowBarbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bent Over Row(Barbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        bentOverRowBarbellSets = SetsEntry(self)
        bentOverRowBarbellReps = RepsEntry(self)
        bentOverRowBarbellWeight = WeightEntry(self)
        bentOverRowBarbellEnter = EntryConfirmButton(self,bentOverRowBarbellSets,
                                                     bentOverRowBarbellReps,
                                                     bentOverRowBarbellWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class BentOverRowDumbbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bent Over Row(Dumbbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        bentOverRowDumbbellSets = SetsEntry(self)
        bentOverRowDumbbellReps = RepsEntry(self)
        bentOverRowDumbbellWeight = WeightEntry(self)
        bentOverRowDumbbellEnter = EntryConfirmButton(self,bentOverRowDumbbellSets,
                                                      bentOverRowDumbbellReps,
                                                      bentOverRowDumbbellWeight)        

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


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
        entries_dict = {}
        self.entries_dict = entries_dict
        children = []
        for F in (DeadLiftLabel, GoodMorningLabel,BentOverRowBarbellLabel,
                  BentOverRowDumbbellLabel):
            self.F = F(self)
            children.append(self.F)
            self.F.exercise_type = 'strength training'
            self.F.grid(padx = 4, sticky = tk.E + tk.W)
            self.F.grid_propagate(0)
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
        entries_dict = {}
        self.entries_dict= entries_dict
        benchPressBarbellSets = SetsEntry(self)
        benchPressBarbellReps = RepsEntry(self)
        benchPressBarbellWeight = WeightEntry(self)
        benchPressBarbellEnter = EntryConfirmButton(self,benchPressBarbellSets,
                                                    benchPressBarbellReps,
                                                    benchPressBarbellWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')

    
class BenchPressInclineBarbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Incline)(Barbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        benchPressInclineBarbellSets = SetsEntry(self)
        benchPressInclineBarbellReps = RepsEntry(self)
        benchPressInclineBarbellWeight = WeightEntry(self)
        benchPressInclineBarbellEnter = EntryConfirmButton(self,
                                                    benchPressInclineBarbellSets,
                                                    benchPressInclineBarbellReps,
                                                    benchPressInclineBarbellWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class BenchPressDeclineBarbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Decline)(Barbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        benchPressDeclineBarbellSets = SetsEntry(self)
        benchPressDeclineBarbellReps = RepsEntry(self)
        benchPressDeclineBarbellWeight = WeightEntry(self)
        benchPressDeclineBarbellEnter = EntryConfirmButton(self,
                                                    benchPressDeclineBarbellSets,
                                                    benchPressDeclineBarbellReps,
                                                    benchPressDeclineBarbellWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')

class BenchPressDumbbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Dumbbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        benchPressDumbbellSets = SetsEntry(self)
        benchPressDumbbellReps = RepsEntry(self)
        benchPressDumbbellWeight = WeightEntry(self)
        benchPressDumbbellEnter = EntryConfirmButton(self,benchPressDumbbellSets,
                                                     benchPressDumbbellReps,
                                                     benchPressDumbbellWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class BenchPressInclineDumbbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Incline)(Dumbbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        benchPressInclineDumbbellSets = SetsEntry(self)
        benchPressInclineDumbbellReps = RepsEntry(self)
        benchPressInclineDumbbellWeight = WeightEntry(self)
        benchPressInclineDumbbellEnter = EntryConfirmButton(self,
                                                benchPressInclineDumbbellSets,
                                                benchPressInclineDumbbellReps,
                                                benchPressInclineDumbbellWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class BenchPressDeclineDumbbellLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Bench Press(Decline)(Dumbbell)',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
       
        entries_dict = {}
        self.entries_dict= entries_dict
        benchPressDeclineDumbbellSets = SetsEntry(self)
        benchPressDeclineDumbbellReps = RepsEntry(self)
        benchPressDeclineDumbbellWeight = WeightEntry(self)
        benchPressDeclineDumbbellEnter = EntryConfirmButton(self,
                                                    benchPressDeclineDumbbellSets,
                                                    benchPressDeclineDumbbellReps,
                                                    benchPressDeclineDumbbellWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


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
        children = []
        for F in (BenchPressBarbellLabel,
                  BenchPressInclineBarbellLabel,
                  BenchPressDeclineBarbellLabel,
                  BenchPressDumbbellLabel,
                  BenchPressInclineDumbbellLabel,
                  BenchPressDeclineDumbbellLabel):
            self.F = F(self)
            self.F.exercise_type = 'strength training'
            children.append(self.F)
            self.F.grid(padx = 4, sticky = tk.E + tk.W)
            self.F.grid_propagate(0)
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
        entries_dict = {}
        self.entries_dict= entries_dict
        squatSets = SetsEntry(self)
        squatReps = RepsEntry(self)
        squatWeight = WeightEntry(self)
        squatEnter = EntryConfirmButton(self,squatSets,squatReps,squatWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class FrontSquatLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Front Squat',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        frontSquatSets = SetsEntry(self)
        frontSquatReps = RepsEntry(self)
        frontSquatWeight = WeightEntry(self)
        frontSquatEnter = EntryConfirmButton(self,
                                             frontSquatSets,
                                             frontSquatReps,
                                             frontSquatWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class LegPressLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Leg Press',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        legPressSets = SetsEntry(self)
        legPressReps = RepsEntry(self)
        legPressWeight = WeightEntry(self)
        legPressEnter = EntryConfirmButton(self,
                                           legPressSets,
                                           legPressReps,
                                           legPressWeight)


    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class CalfRaiseLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Calf Raise',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        calfRaiseSets = SetsEntry(self)
        calfRaiseReps = RepsEntry(self)
        calfRaiseWeight = WeightEntry(self)
        calfRaiseEnter = EntryConfirmButton(self,calfRaiseSets,
                                            calfRaiseReps,calfRaiseWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')
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
        children = []
        for F in (SquatLabel,FrontSquatLabel,LegPressLabel,CalfRaiseLabel):
            self.F = F(self)
            children.append(self.F)
            self.F.exercise_type = 'strength training'
            self.F.grid(padx = 4, sticky = tk.E + tk.W)
            self.F.grid_propagate(0)
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
        entries_dict = {}
        self.entries_dict= entries_dict
        overheadPressSets = SetsEntry(self)
        overheadPressReps = RepsEntry(self)
        overheadPressWeight = WeightEntry(self)
        overheadPressEnter = EntryConfirmButton(self,overheadPressSets,
                                                overheadPressReps,
                                                overheadPressWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class ShrugsLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Shrugs',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        shrugsSets = SetsEntry(self)
        shrugsReps = RepsEntry(self)
        shrugsWeight = WeightEntry(self)
        shrugsEnter = EntryConfirmButton(self,shrugsSets,
                                         shrugsReps,shrugsWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class BehindNeckPressLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Behind Neck Press',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        behindNeckPressSets = SetsEntry(self)
        behindNeckPressReps = RepsEntry(self)
        behindNeckPressWeight = WeightEntry(self)
        behindNeckPressEnter = EntryConfirmButton(self,behindNeckPressSets,
                                                  behindNeckPressReps,
                                                  behindNeckPressWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class SeatedMilitaryPressLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Seated Military Press',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        seatedMilitaryPressSets = SetsEntry(self)
        seatedMilitaryPressReps = RepsEntry(self)
        seatedMilitaryPressWeight = WeightEntry(self)
        seatedMilitaryPressEnter = EntryConfirmButton(self,seatedMilitaryPressSets,
                                                      seatedMilitaryPressReps,
                                                      seatedMilitaryPressWeight)        

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class UprightRowLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Upright Row',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        uprightRowSets = SetsEntry(self)
        uprightRowReps = RepsEntry(self)
        uprightRowWeight = WeightEntry(self)
        uprightRowEnter = EntryConfirmButton(self,uprightRowSets,
                                             uprightRowReps,uprightRowWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')


class ChinupsLabel(tk.LabelFrame):
    def __init__(self,parent):
        tk.LabelFrame.__init__(self, parent,
                               borderwidth = 2,
                               relief = tk.RAISED,
                               text = 'Chinup',
                               height = LABEL_HEIGHT,
                               width = LABEL_WIDTH)
                             
        self.parent = parent
        entries_dict = {}
        self.entries_dict= entries_dict
        chinupsSets = SetsEntry(self)
        chinupsReps = RepsEntry(self)
        chinupsWeight = WeightEntry(self)
        chinupsEnter = EntryConfirmButton(self,chinupsSets,
                                          chinupsReps,chinupsWeight)

    def __str__(self):
        return self.cget('text')

    def __repr__(self):
        return self.cget('text')
        

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
        top = self.winfo_toplevel()
        children = []
        for F in (OverheadPressLabel,ShrugsLabel,
                  BehindNeckPressLabel,SeatedMilitaryPressLabel,
                  UprightRowLabel,ChinupsLabel):
            
            self.F = F(self)
            children.append(self.F)
            self.F.exercise_type = 'strength training'
            self.F.grid(padx = 4, sticky = tk.E + tk.W)
            self.F.grid_propagate(0)
#END SHOULDERS
#START DISPLAY
class ViewAllEntriesInDatabaseButton(tk.Button):
    """Opens a new window that allows user to view all exercises ever put
    into the database"""
    def __init__(self, parent):
        tk.Button.__init__(self, parent,
                           text = 'View All Entries',
                           relief = tk.RAISED,
                           border = 3,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command = self.open_window,
                           height = 2)
        self.parent = parent
        self.viewAllEntriesInDatabaseWindow = None
        
    def open_window(self):
        if self.viewAllEntriesInDatabaseWindow is None:
            self.viewAllEntriesInDatabaseWindow = ViewAllEntriesInDatabaseWindow(self)
            (self.viewAllEntriesInDatabaseWindow.protocol('WM_DELETE_WINDOW',
                                                          self.remove_window))

    def remove_window(self):
        self.viewAllEntriesInDatabaseWindow.destroy()
        self.viewAllEntriesInDatabaseWindow = None


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
        

    def get_selected_date(self):
        return self.parent.dateVar.get()

    def get_exercise_id(self,exercise_name):
       """
       Takes a string of an exercise name, looks it up in the exercise table, and
       returns it
       """
       exercise_name_as_tuple = (exercise_name,)
       exercise_id = []
       for row in data.cursor.execute("SELECT id FROM exercises WHERE name=?",
                                      exercise_name_as_tuple):
           exercise_id.append(row)
       if len(exercise_id) > 0:
           return exercise_id[0][0]
    
    def number_of_entries_for_same_exercise(self,entries_dict,exercise_name):
        """
        Returns the number of entries for the exercise in the entries dict.
        """
        return len(entries_dict[exercise_name])    

    def get_last_id_number(self,exercise_type):
        """
        Gets the latest ID number in the SQL table
        """
        if exercise_type =='strength training':
            
            id_number = []
            for row in data.cursor.execute('''SELECT max(visible_id) FROM
                                           events_weightlifting'''):
                
                id_number.append(row[0])
            if id_number[0] == None: #the table has just been created
                return 0
            return id_number[0]
        if exercise_type == 'cardio':
            id_number = []
            for row in data.cursor.execute('''SELECT max(visible_id) FROM
                                              events_cardio'''):
                id_number.append(row[0])
            if id_number[0] == None: #the table has just been created
                return 0
            return id_number[0]
                    
    def sequentialize_ids_in_sql_tuples(self,dict_of_list_of_tuples):
        """
        Adds in id's to sql tuples before they are entered into the database. 
        """
        copy_dict = {'strength training':[] , 'cardio':[]}
        
        for key in dict_of_list_of_tuples:
            
            id_number = self.get_last_id_number(key) + 1
            for tup in dict_of_list_of_tuples[key]:
                (copy_dict[key].append((id_number, id_number,tup[0],
                                        tup[1],tup[2],tup[3],tup[4])))
                id_number+=1
        return copy_dict
                  
    def save_entries(self):
        """
        Saves the entries in the DisplayArea as a dictionary with the following structure:
        {'exercise name':(sets, reps, weight)}
        """
        conn = lite.connect('fit.db')
        cursor= conn.cursor()
        selected_date = self.get_selected_date()
        if selected_date == 'Date':
            tkm.showerror('No Date Selected Error','Please Select A Date')
       
        sql_dict = self.sequentialize_ids_in_sql_tuples(
            self.parent.parent.dict_of_tuples_to_be_entered_in_the_database)
        
        sql_enterable_list_strength_training = sql_dict['strength training']
        sql_enterable_list_cardio = sql_dict['cardio']

        data.cursor.executemany('''INSERT INTO events_weightlifting
                                VALUES(?,?,?,?,?,?,?)''',
                                sql_enterable_list_strength_training)
        data.cursor.executemany('''INSERT INTO events_cardio
                                VALUES(?,?,?,?,?,?,?)''',
                                sql_enterable_list_cardio)
        
        data.conn.commit()
        conn.close()

        
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

    def move_tuple_to_garbage_dict(self):
        """
        Pops a tuple from the main dictionary in the
        InputExerciseWindow and appends it to a garbage dictionary. 
        """
        self.parent.parent.garbage_dict[self.parent.parent.add_order[-1]].append(
            self.parent.parent.dict_of_tuples_to_be_entered_in_the_database[self.parent.parent.add_order[-1]].pop())
        self.parent.parent.add_order_garbage.append(
            self.parent.parent.add_order.pop())
    
    def undo_last_entry(self):
        if len(self.displayAreaControlled.get('1.0',tk.END)) > 1:
            self.displayAreaControlled.undo_number += 1
            self.move_tuple_to_garbage_dict()
            self.displayAreaControlled.display_entries_in_main_dict()

   
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

    def move_tuple_to_main_dict(self):
        """
        Pops a tuple from the garbage dict in the InputExerciseWindow and appends it to the main
        dict. 
        """
        self.parent.parent.dict_of_tuples_to_be_entered_in_the_database[self.parent.parent.add_order_garbage[-1]].append(
            self.parent.parent.garbage_dict[self.parent.parent.add_order_garbage[-1]].pop())
        self.parent.parent.add_order.append(
            self.parent.parent.add_order_garbage.pop())

    def redo_last_entry(self):
        if self.displayAreaControlled.redo_number < self.displayAreaControlled.undo_number:
            self.displayAreaControlled.redo_number += 1
            self.move_tuple_to_main_dict()
            self.displayAreaControlled.display_entries_in_main_dict()

            
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
        top = self.winfo_toplevel()



       
    def display_entries_in_main_dict(self):
        """
        Displays the entry to the DisplayArea
        """
        self.delete('1.0', tk.END)
        for tup in self.parent.parent.dict_of_tuples_to_be_entered_in_the_database['strength training']:
            self.insert(tk.END,
                        'Exercise: '+self.parent.parent.get_exercise_from_id(tup[1])+'\n')
            self.insert(tk.END,
                        '--------------------' + '\n')
            self.insert(tk.END,
                        'Sets: '+ str(tup[2]) + ' Reps: '+ str(tup[3]) + ' Weight: '+str(tup[3]) + '\n')
        for tup in self.parent.parent.dict_of_tuples_to_be_entered_in_the_database['cardio']:
            self.insert(tk.END,
                        'Exercise: '+str(self.parent.parent.get_exercise_from_id(tup[1]))+'\n')
            self.insert(tk.END,
                        '--------------------' + '\n')
            self.insert(tk.END,
                        'Distance: '+ str(tup[2]) + ' ' + tup[3] + ' in '+str(tup[4]) + ' minutes'+ '\n')

          
    def display_inputs(self, inputs):
        """
        Inputs are the contents of a [Workout] Label when an entry is confirmed.
        Type is to be determined. 
        """
        self.insert('1.0', inputs)
    
    
class DisplayFrame(tk.Frame):
    """
    Containing frame for the text DisplayArea. The text DisplayArea
    displays the exercise name, sets, reps, and weight are visible
    when a user "enters" an exercise. 
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief = tk.SUNKEN,
                          width = 200,
                          borderwidth = 5)
        self.parent = parent
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
        
        self.dateVar.set(today)
        
        dateMenu = tk.OptionMenu(self, self.dateVar,
                                 today, yesterday, twodaysago,
                                 threedaysago,fourdaysago,
                                 fivedaysago,sixdaysago,
                                 sevendaysago)
        dateMenu.grid(column = 3, row = 0)
        #Date Menu END
        self.displayArea = DisplayArea(self)
        self.displayArea.grid(row = 1, columnspan = 5) 
        
        self.undoButton = UndoButton(self,self.displayArea)
        self.undoButton.grid(column = 0,row = 0)
        
        self.redoButton = RedoButton(self,self.displayArea)
        self.redoButton.grid(column = 2 ,row = 0)
        
        self.saveButton = SaveButton(self,self.displayArea)
        self.saveButton.grid(row = 0, column = 1)
        
        self.viewAllEntriesInDatabaseButton = ViewAllEntriesInDatabaseButton(self)
        self.viewAllEntriesInDatabaseButton.grid(column = 4, row = 0)
#END DISPLAY        
#START SELECTION FRAME AND CHILDREN
class SelectCardio(tk.Radiobutton):
    """
    Allows the user to select a group of exercises from
    Back, Shoulder, Chest, and Legs that will show up in the Input
    Exercise Window ready for entry
    """
    def __init__(self,parent,controller):
        tk.Radiobutton.__init__(self, parent,
                                command = lambda: controller.pass_to_parent(CardioFrame),
                                indicatoron = 0,
                                value = 'Cardio',
                                text = 'Display Cardio Exercises')
        self.parent = parent
class SelectBack(tk.Radiobutton):
    """
    Allows the user to select a group of exercises from
    Back, Shoulder, Chest, and Legs that will show up in the Input
    Exercise Window ready for entry
    """
    def __init__(self,parent,controller):
        tk.Radiobutton.__init__(self, parent,
                                command = lambda:
                                controller.pass_to_parent(BackFrame),
                                indicatoron = 0,
                                value = 'Back',
                                text = 'Display Back Exercises')
        self.parent = parent
        

class SelectShoulders(tk.Radiobutton):
    """
    Allows the user to select a group of exercises from
    Back, Shoulder, Chest, and Legs that will show up in the Input
    Exercise Window ready for entry
    """
    def __init__(self,parent,controller):
        tk.Radiobutton.__init__(self, parent,
                                command = lambda:
                                controller.pass_to_parent(ShouldersFrame),
                                indicatoron = 0,
                                value = 'shoulders',
                                text = 'Display Shoulder Exercises')
        self.parent = parent
        

class SelectChest(tk.Radiobutton):
    """
    Allows the user to select a group of exercises from
    Back, Shoulder, Chest, and Legs that will show up in the Input
    Exercise Window ready for entry
    """
    def __init__(self,parent,controller):
        tk.Radiobutton.__init__(self, parent,
                                command = lambda:
                                controller.pass_to_parent(ChestFrame),
                                indicatoron = 0,
                                value = 'chest',
                                text = 'Display Chest Exercises')
        self.parent = parent
        

class SelectLegs(tk.Radiobutton):
    """
    Allows the user to select a group of exercises from
    Back, Shoulder, Chest, and Legs that will show up in the Input
    Exercise Window ready for entry
    """
    def __init__(self,parent,controller):
        tk.Radiobutton.__init__(self, parent,
                                command =
                                lambda: controller.pass_to_parent(LegsFrame),
                                indicatoron = 0,
                                value = 'legs',
                                text = 'Display Legs Exercises')
        self.parent = parent
        
        
class SelectionFrame(tk.Frame):
    """
    Containing Frame that holds all the selection radiobuttons.
    """
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent, borderwidth = 3,
                          relief = tk.RAISED)
        self.parent = parent

        self.selectCardio= SelectCardio(self,self)
        self.selectCardio.grid(column = 0, row = 0)
        
        self.selectBack = SelectBack(self,self)
        self.selectBack.grid(column = 1, row = 0)
        
        self.selectShoulders = SelectShoulders(self,self)
        self.selectShoulders.grid(column = 2, row = 0)

        self.selectChest = SelectChest(self,self)
        self.selectChest.grid(column = 3, row = 0)
        
        self.selectLegs = SelectLegs(self,self)
        self.selectLegs.grid(column = 4, row = 0)
        

    def pass_to_parent(self, c):
        """
        Passes Frame to controller
        """
        return self.parent.show_frame(c)

#END SELECTION FRAME AND CHILDREN                            
class InputExerciseWindow(tk.Toplevel):
    "The window in which  exercise information can be added"
    def __init__(self, parent = None):
        tk.Toplevel.__init__(self,parent,
                             height = 400,
                             width = 400)
        container = tk.Frame(self,
                             relief = tk.RAISED,
                             borderwidth = 3)
        container.grid(column= 0, row = 0,
                       sticky = 'news',
                       pady=30)
        container.columnconfigure(0, weight = 1)
        container.rowconfigure(0, weight = 1)
        self.add_order = []
        self.add_order_garbage = []
        self.garbage_dict = {'strength training':[],
                             'cardio':[]}
        self.dict_of_tuples_to_be_entered_in_the_database = {'strength training': [],
                                                             'cardio': []}
        #initialize Database
        self.frames = {}
        for F in (CardioFrame,BackFrame,LegsFrame,ChestFrame,ShouldersFrame):
            
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(column = 0, row = 0, sticky = 'news')
            frame.parent = parent
        self.show_frame(CardioFrame)
        self.parent = parent
        self.title("Exercise Input")
        self.minsize(width = 1100, height = 766)

        #Widgets
        self.selectionFrame = SelectionFrame(self,self)
        self.selectionFrame.grid(column = 0, row = 0, sticky = tk.N + tk.W + tk.E)
        self.displayFrame = DisplayFrame(self)
        self.displayFrame.grid(column = 1, row = 0,columnspan = 4)

    def get_all_available_exercise_names(self):
        exercise_name_list = []
        for i in self.frames:
            for j in self.frames[i].children:
                exercise_name_list.append(self.frames[i].children[j])
    def get_exercise_from_id(self,exercise_id):
       """
       Takes an exercise ID  looks it up in the exercise table, and
       returns the exercise name
       """
       conn = lite.connect('fit.db')
       cursor= conn.cursor()
       exercise_id_as_tuple = (exercise_id,)
       exercise_name = []
       for row in cursor.execute('''SELECT name FROM exercises WHERE id=?''',
                                 exercise_id_as_tuple):
           exercise_name.append(row)
       if len(exercise_name) > 0:
           conn.close()
           return exercise_name[0][0]
       conn.close()
        
    def show_frame(self, c):
        """
        Show a frame for the given class.
        """
        frame = self.frames[c]
        frame.tkraise()
######END INPUT EXERCISE WINDOW######
#####################################
######BEGIN VIEW ALL ENTRIES IN DATABASE WINDOW#########

class DisplayStrengthButton(tk.Button):
    """
    Confirmation Button for deleting entries. 
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Strength',
                           relief = tk.RAISED,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command = lambda: self.set_display())
        self.parent = parent
    def set_display(self):
        self.parent.parent.displayed_database = 'strength training'
        self.parent.parent.rewrite_display()

class DisplayCardioButton(tk.Button):
    """
    Confirmation Button for deleting entries. 
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Cardio',
                           relief = tk.RAISED,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command = lambda: self.set_display())
        self.parent = parent
    def set_display(self):
        self.parent.parent.displayed_database = 'cardio'
        self.parent.parent.rewrite_display()
class SelectDatabaseFrame(tk.Frame):
    """
    Frame containing buttons that change what sqlite DB is being displayed to
    the display area.These buttnos will also affect what rows are deleted in
    the row/entry delete. 
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief = tk.GROOVE,
                          width = 200,
                          borderwidth = 2)
        self.parent = parent
        
        self.displayStrengthButton = DisplayStrengthButton(self).grid(column = 0,
                                                                      row = 0)
        self.displayCardioButton = DisplayCardioButton(self).grid(column = 1,
                                                                  row = 0)

        
class DeleteRowEntry(tk.Entry):
    """
    Allows user to specify either a single row or a range of rows to be deleted
    from the events table in the sql database.
    """
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          width = 15
                          )
        self.parent = parent
        self.insert(0, ' ')
        
    def get_entry(self):
        return self.get()

class DeleteRowButton(tk.Button):
    """
    Confirmation Button for deleting entries. 
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Enter',
                           relief = tk.RAISED,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'white')
        self.parent = parent


    def get_range(self):
        """
        Calls the parent delete_range()
        """
        self.parent.delete_range(self.parent.parent.displayed_database)

    def get_individual(self):
        """
        Calls the parent delete_individual()"""                      
        self.parent.delete_individual(self.parent.parent.displayed_database)
        

class DeleteRowFrame(tk.Frame):
    """
    Frame containing all of the entry's and buttons that will delete rows from
    the events database
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief = tk.GROOVE,
                          width = 200,
                          borderwidth = 2)
        self.parent = parent
        

    
        #Starting Row Entry
        self.startingRowEntry = DeleteRowEntry(self)
        self.startingRowEntry.grid(column = 0, row = 0)
        self.startingRowEntry.insert(0, 'Starting Row')

        #Ending Row Entry
        self.endingRowEntry = DeleteRowEntry(self)
        self.endingRowEntry.grid(column = 1, row = 0)
        self.endingRowEntry.insert(0, 'Ending Row')

        #Individual Row Entry
        self.individualRowEntry = DeleteRowEntry(self)
        self.individualRowEntry.grid(column = 4, row = 0)
        self.individualRowEntry.insert(0, 'Individual Row')

        #Delete Range Button
        self.deleteRangeButton = DeleteRowButton(self)
        self.deleteRangeButton.grid(column= 2, row = 0)
        self.deleteRangeButton.config(text = 'Delete Range',
                                      height = 1,
                                      command = lambda:self.deleteRangeButton.get_range())

        #Delete Individual Button
        self.deleteIndividualButton = DeleteRowButton(self)
        self.deleteIndividualButton.grid(column= 5, row = 0)
        self.deleteIndividualButton.config(text = 'Delete Individual',
                                    height = 1,
                                    command = lambda:self.deleteIndividualButton.get_individual())


    def delete_range(self,exercise_type):
        """
        Deletes a range of rows in the SQL events table. The range is determined
        by entries in the starting and ending DeleteRowEntry entries. 
        """
        if exercise_type == 'strength training':
            try:
                starting_index = int(self.startingRowEntry.get())
                ending_index = int(self.endingRowEntry.get())
            except ValueError:        
                tkm.showerror('Entry Error','''Enter integers for
                              starting and ending row entries''',
                              parent = self.parent)    
                return None
            conn = lite.connect('fit.db')
            cursor = conn.cursor()
            cursor.execute("""DELETE  FROM events_weightlifting
                               WHERE(visible_id >= (?))
                               AND (visible_id <= (?))""",
                           (starting_index,ending_index))
            cursor.execute("""DELETE FROM SQLITE_SEQUENCE
                            WHERE NAME = 'events_weightlifting'""")
            
            conn.commit()
            conn.close
            self.parent.rewrite_display()
        if exercise_type == 'cardio':
            try:
                starting_index = int(self.startingRowEntry.get())
                ending_index = int(self.endingRowEntry.get())
            except ValueError:        
                tkm.showerror('Entry Error','''Enter integers for
                               starting and ending row entries''',
                              parent = self.parent)    
                return None
            conn = lite.connect('fit.db')
            cursor = conn.cursor()
            cursor.execute("""DELETE  FROM events_cardio
                              WHERE(visible_id >= (?))
                                      AND (visible_id <= (?))""",
                             (starting_index,ending_index))
            cursor.execute("""DELETE FROM
                              SQLITE_SEQUENCE
                              WHERE NAME = 'events_cardio'""")
            conn.commit()
            conn.close
            self.parent.rewrite_display()
   
    def delete_individual(self,exercise_type):
        """
        Deletes a single row in the SQL events table. The row is determined by entry in the individual
        DeleteRowEntry"""
        if exercise_type == 'strength training':
            try:
                index = int(self.individualRowEntry.get())
            except ValueError:        
                tkm.showerror('Entry Error','''Index entry
                                               should be an integer.''',
                              parent = self.parent)    
                return None
            
            conn = lite.connect('fit.db')
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM events_weightlifting
                              WHERE(id = (?))""",(index,))
                
            conn.commit()
            conn.close
            self.parent.rewrite_display()
        if exercise_type == 'cardio':
            try:
                index = int(self.individualRowEntry.get())
            except ValueError:        
                tkm.showerror('Entry Error','''Index entry
                                               should be an integer.''',
                              parent = self.parent)    
                return None            
            conn = lite.connect('fit.db')
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM events_cardio
                              WHERE(id = (?))""",(index,))     
            conn.commit()
            conn.close
            self.parent.rewrite_display()


class EntriesDisplayArea(tk.Text):
    """
    Display area for the ViewAllEntriesInDatabaseWindow
    """
    def __init__(self,parent):
        tk.Text.__init__(self, parent,
                           borderwidth = 3,
                           height = 50,
                         width = 85,
                         wrap = tk.WORD)
        self.parent = parent
        self.textInDisplayArea = tk.StringVar()
        rows_list = []
        self.rows_list = rows_list
        self.initialize_rows_list(self.parent.displayed_database)
        self.textInDisplayArea.set(self.create_string_from_sql_entries(self.make_readable_entries(self.rows_list,self.parent.displayed_database)))
        self.insert('1.1', self.textInDisplayArea.get())


    def initialize_rows_list(self,exercise_type):
        """
          Gets all the rows from the sql database to be put into the 
        """
        if exercise_type == 'strength training':
            self.rows_list = []
            conn = lite.connect('fit.db')
            cursor = conn.cursor()
            for row in cursor.execute('SELECT * FROM events_weightlifting ORDER BY visible_id'):
                self.rows_list.append(row)
            conn.close()

        if exercise_type == 'cardio':
            self.rows_list = []
            conn = lite.connect('fit.db')
            cursor = conn.cursor()
            for row in cursor.execute('SELECT * FROM events_cardio ORDER BY visible_id'):
                self.rows_list.append(row)
            conn.close()

        

    def make_readable_entries(self,sql_rows_list,exercise_type):
        """
        Takes a list of SQL rows and makes a list of tuples with information added in to make it more readable.
        Excludes ID and Exercise ID.
        """
        if exercise_type == 'strength training':
            conn = lite.connect('fit.db')
            cursor= conn.cursor()
            readable_entries_list = [[] for x in range(len(sql_rows_list))]
            for row_number in range(len(sql_rows_list)):
                readable_entries_list[row_number].append('Entry ID: '+ str(sql_rows_list[row_number][1]))
                readable_entries_list[row_number].append('Date: '+ str(sql_rows_list[row_number][2]))
                readable_entries_list[row_number].append(
                    'Exercise: '+ self.parent.parent.parent.parent.parent.get_exercise_from_id(sql_rows_list[row_number][3]))
                readable_entries_list[row_number].append('Sets: '+ str(sql_rows_list[row_number][4]))
                readable_entries_list[row_number].append('Reps: '+ str(sql_rows_list[row_number][5]))
                readable_entries_list[row_number].append('Weight: '+ str(sql_rows_list[row_number][6]))
            conn.close()
            return readable_entries_list
        if exercise_type == 'cardio':
            conn = lite.connect('fit.db')
            cursor= conn.cursor()
            readable_entries_list = [[] for x in range(len(sql_rows_list))]
            for row_number in range(len(sql_rows_list)):
                readable_entries_list[row_number].append('Entry ID: '+ str(sql_rows_list[row_number][1]))
                readable_entries_list[row_number].append('Date: '+ str(sql_rows_list[row_number][2]))
                readable_entries_list[row_number].append(
                    'Exercise: '+ self.parent.parent.parent.parent.parent.get_exercise_from_id(sql_rows_list[row_number][3]))
                readable_entries_list[row_number].append('Sets: '+ str(sql_rows_list[row_number][4]))
                readable_entries_list[row_number].append('Reps: '+ str(sql_rows_list[row_number][5]))
                readable_entries_list[row_number].append('Weight: '+ str(sql_rows_list[row_number][6]))
            conn.close()
            return readable_entries_list

    def create_string_from_sql_entries(self, readable_list):
       """
       From a list of readable SQL entries, creates a single formatted string that can be added to a canvas object.
       """
       single_line_string_list = []
       one_list = []
       for row in readable_list:
              single_line_string_list.append(' '.join(row))
       
       for item in single_line_string_list:
              one_list.append(item)
       the_string = '\n'.join(one_list)
       
       return the_string


class EntriesDisplayFrame(tk.Frame):
    """
    Containing frame for the text DisplayArea
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief = tk.SUNKEN,
                          width = 200,
                          borderwidth = 2)
        self.parent = parent
        self.displayed_database = 'strength training'
        self.deleteRowFrame = DeleteRowFrame(self)
        self.deleteRowFrame.grid(row = 0, column = 0, sticky = 'w')

        self.selectDatabaseFrame = SelectDatabaseFrame(self).grid(row = 0, column = 0, sticky = 'e')
        
        self.entriesDisplayArea = EntriesDisplayArea(self)
        self.entriesDisplayArea.grid(row = 1, column = 0, sticky = 'ns')
        
        self.scrollVertical = tk.Scrollbar(self, orient = tk.VERTICAL,
                                           command = self.entriesDisplayArea.yview)
        
                                         
        self.entriesDisplayArea.config(yscrollcommand = self.scrollVertical.set)

        self.scrollVertical.grid(row=1,column=1,sticky = 'ns')
    def rewrite_display(self):
        self.entriesDisplayArea.initialize_rows_list(self.displayed_database)
        self.entriesDisplayArea.textInDisplayArea.set(self.entriesDisplayArea.create_string_from_sql_entries(self.entriesDisplayArea.make_readable_entries(self.entriesDisplayArea.rows_list,self.displayed_database)))
        self.entriesDisplayArea.delete('1.0',tk.END)
        self.entriesDisplayArea.insert('1.0',self.entriesDisplayArea.textInDisplayArea.get())

       
        
class ViewAllEntriesInDatabaseWindow(tk.Toplevel):
    """
    Window in which the user can view all of the entries entered ever
    entered into the database.
    """
    def __init__(self, parent = None):
        tk.Toplevel.__init__(self,parent,
                             height = 400,
                             width = 400)
        self.parent = parent
        
        self.entriesDisplayFrame = EntriesDisplayFrame(self)
        self.entriesDisplayFrame.grid(row = 0, column = 0)
