import datetime as date
import tkinter as tk
import tkinter.messagebox as tkm
import sqlite3 as lite
import fitDatabase as data
import copy
#BEGIN entries
#Variables
ENTRIES_FONT = ('Times', '12')
ENTRIES_WIDTH = 3

class HeightEntry(tk.Entry):
    """
    Entry for height in inches
    """
    def __init__(self,parent):
        tk.Entry.__init__(self,parent,
                          width = ENTRIES_WIDTH)
        self.parent = parent

class WeightEntry(tk.Entry):
    """
    Entry for weight in pounds
    """
    def __init__(self,parent):
        tk.Entry.__init__(self,parent,
                          width = ENTRIES_WIDTH)
        self.parent = parent

class AgeEntry(tk.Entry):
    """
    Entry for age in years
    """
    def __init__(self,parent):
        tk.Entry.__init__(self,parent,
                          width = ENTRIES_WIDTH)
        self.parent = parent
class BodyFatEntry(tk.Entry):
    """
    Entry for Body Fat % (optional)
    """
    def __init__(self,parent):
        tk.Entry.__init__(self,parent,
                          width = ENTRIES_WIDTH)
        self.parent = parent
class CalculateBodyFatCheck(tk.Checkbutton):
    """
    If user inputs checkbutton, allows user to opt for a bodyfat % calculation.
    """
    def __init__(self,parent):
        tk.Checkbutton.__init__(self,parent,
                                command = lambda:self.insert_body_fat(),
                                state = tk.DISABLED)
        self.parent = parent
       

        self.check = tk.IntVar()
        self.config(variable = self.check)
    def calculate_body_fat(self):
        gender = self.parent.gender.get()

        if gender == 'Male':
            body_weight = float(self.parent.weightEntry.get())
            lean_body_mass =  ((body_weight *1.082) +94.42) - (float(self.parent.waistEntry.get())*4.15)
            body_fat_percent =((body_weight - lean_body_mass)*100) / body_weight
            return round(body_fat_percent,1)
                                                              
    def insert_body_fat(self):
        if self.check.get():
            self.parent.bodyFatEntry.delete(0, tk.END)
            self.parent.bodyFatEntry.insert(0,
                                            str(self.calculate_body_fat()))
                                
class WaistEntry(tk.Entry):
    """
    Entry for Waist measurement in inches
    """
    def __init__(self,parent):
        tk.Entry.__init__(self,parent,
                          width = ENTRIES_WIDTH)
        self.parent = parent
        number_keypress_list = ['<KeyPress 0>','<KeyPress 1>',
                                '<KeyPress 2>','<KeyPress 3>',
                                '<KeyPress 4>','<KeyPress 5>',
                                '<KeyPress 6>','<KeyPress 7>',
                                '<KeyPress 8>','<KeyPress 9>']
        deletion_keypress_list = ['<KeyPress BackSpace>',
                                  '<KeyPress Delete>']
        for number_keypress in number_keypress_list:
            self.bind(number_keypress, self.enable_calculate_check_box)
        for deletion_keypress in deletion_keypress_list:
            self.bind(deletion_keypress, self.disable_calculate_check_box)
        
            
        
    def enable_calculate_check_box(self,event):
        self.parent.calculateBodyFatCheck.config(state = tk.NORMAL)
    def disable_calculate_check_box(self,event):
        if len(self.parent.waistEntry.get()) == 1:
            self.parent.calculateBodyFatCheck.config(state = tk.DISABLED)
        
class EnterButton(tk.Button):
    """
    Button that saves height, weight, and age to the sqlite database
    """
    def __init__(self,parent):
        tk.Button.__init__(self,parent,
                          text = 'Enter',
                          command = lambda:self.save_to_database())
        self.parent = parent

    def get_last_id_number(self):
        """
        Gets the latest ID number in the SQL table
        """
        id_number = []
        for row in data.cursor.execute('SELECT max(id) FROM personal_info'):
            id_number.append(row[0])
        if id_number[0] == None: #the table has just been created
            return 0
        return id_number[0]

    def save_to_database(self):

        sql_enterable_tuple = (self.get_last_id_number()+1,str(date.datetime.today())[:10],self.parent.heightEntry.get(),
                       self.parent.weightEntry.get(),self.parent.ageEntry.get(),self.parent.gender.get(),
                       self.parent.activityLevel.get(),self.parent.bodyFatEntry.get(),
                       self.parent.waistEntry.get())
        for index in range(len(sql_enterable_tuple)-2):
            if sql_enterable_tuple[index] == '':
                tkm.showerror('Required Entries', "You didn't fill in all non-optional entries")
                return None
                
        conn = lite.connect('fit.db')
        cursor = conn.cursor()   
                
        cursor.execute('''INSERT OR IGNORE INTO personal_info
                          VALUES (?,?,?,?,?,?,?,?,?)''',(
                       self.get_last_id_number()+1,
                       str(date.datetime.today())[:10],
                       self.parent.heightEntry.get(),
                       self.parent.weightEntry.get(),
                       self.parent.ageEntry.get(),
                       self.parent.gender.get(),
                       self.parent.activityLevel.get(),
                       self.parent.bodyFatEntry.get(),
                       self.parent.waistEntry.get()))
        conn.commit()
        conn.close()
        self.parent.parent.currentEntriesFrame.set_labels()
        self.parent.parent.calculationsHolderFrame.basalMetabolicRateFrame.set_radiobuttons()
        self.parent.parent.calculationsHolderFrame.basalMetabolicRateFrame.basalMetabolicRateDisplayLabel.update_label()
        self.parent.parent.calculationsHolderFrame.waistToHeightFrame.waistToHeightRatioDisplayLabel.update_label()
        self.parent.parent.calculationsHolderFrame.bodyMassFrame.fatBodyMassDisplayLabel.update_label()
        self.parent.parent.calculationsHolderFrame.bodyMassFrame.leanBodyMassDisplayLabel.update_label()
        self.parent.parent.calculationsHolderFrame.totalDailyEnergyExpenditureFrame.totalDailyEnergyExpenditureDisplayLabel.update_label()
        
        
        
class ActivityLevelDescriptionsButton(tk.Button):
    "Opens a new window with descriptions of activity levels"
    def __init__(self, parent):
        tk.Button.__init__(self, parent,
                           text = '?',
                           relief = tk.RAISED,
                           border = 3,
                           activeforeground = 'black',
                           activebackground = 'white',
                           width = 2,
                           command = self.openwindow)
        self.parent = parent
        self.activityDescriptions = None
        
    def openwindow(self):
        
        if self.activityDescriptions is None:
            self.activityDescriptions = ActivityLevelDescriptions(self)
            self.activityDescriptions.protocol('WM_DELETE_WINDOW', self.removewindow)

    def removewindow(self):
        self.activityDescriptions.destroy()
        self.activityDescriptions = None
class ActivityLevelDescriptions(tk.Toplevel):
    def __init__(self,parent):
        tk.Toplevel.__init__(self,parent)
        self.parent = parent
        tk.Label(self,text = 'Sedenary').grid(column = 0, row = 0)
    

class EntriesHolderFrame(tk.Frame):
    """
    Holds entries for height, weight, age, and activity level. 
    """
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
##                          ,height = 400, width = 300)
        self.parent = parent

        tk.Label(self, text= 'Height(in): ',
                 font = ENTRIES_FONT).grid(column = 0, row =0)
        self.heightEntry = HeightEntry(self)
        self.heightEntry.grid(column = 1, row = 0)

        tk.Label(self, text= 'Weight(lbs): ',
                 font = ENTRIES_FONT).grid(column = 0, row =1)
        self.weightEntry = HeightEntry(self)
        self.weightEntry.grid(column = 1, row = 1)

        tk.Label(self, text= 'Age(years): ',
                 font = ENTRIES_FONT).grid(column = 0, row =2)
        self.ageEntry = AgeEntry(self)
        self.ageEntry.grid(column = 1, row = 2)

        tk.Label(self, text= 'Activity Level ',
                 font = ENTRIES_FONT).grid(column = 0, row =3)
        self.activityLevel = tk.StringVar(self)
        sedentary = 'Sedentary'
        lightly_active = 'Lightly Active'
        moderately_active = 'Moderately Active'
        very_active = 'Very Active'
        extra_active = 'Extra Active'
        self.activityLevel.set('Lightly Active')
        self.activityLevelMenu = tk.OptionMenu(self,
                                               self.activityLevel,
                                               sedentary,lightly_active,
                                               moderately_active,
                                               very_active,extra_active)
        self.activityLevelMenu.grid(column = 1, row = 3)
        self.activityLevelDescriptionsButton = ActivityLevelDescriptionsButton(self)
        self.activityLevelDescriptionsButton.grid(column = 2, row = 3)

        self.gender = tk.StringVar()
        self.gender.set('Male')
        tk.Radiobutton(self,text ='Male', value ='Male',
                       variable = self.gender).grid(column = 0, row = 4)
        tk.Radiobutton(self,text ='Female', value ='Female',
                       variable = self.gender).grid(column = 1, row = 4)

        tk.Label(self, text= 'Bodyfat(%)(optional) ',
                 font = ENTRIES_FONT).grid(column = 0, row =5)
        self.bodyFatEntry = BodyFatEntry(self)
        self.bodyFatEntry.grid(column = 1, row = 5)

        tk.Label(self, text= 'Calculate ',font = ENTRIES_FONT).grid(column = 2, row =5)
        self.calculateBodyFatCheck = CalculateBodyFatCheck(self)
        self.calculateBodyFatCheck.grid(column = 3, row = 5)

        tk.Label(self, text= 'Waist(%)(optional) ',
                 font = ENTRIES_FONT).grid(column = 0, row =6)
        self.waistEntry = WaistEntry(self)
        self.waistEntry.grid(column = 1, row = 6)
        
        self.enterButton = EnterButton(self)
        self.enterButton.grid(column=0, row = 8)

class CurrentEntriesFrame(tk.Frame):
    """
    Holds entries for height, weight, age, and activity level. 
    """
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)

        self.parent = parent
        if not self.parent.is_database_empty():
            self.set_labels()
        


    def set_labels(self):
        """
        Sets the labels with the latest entry in the sqlite database. 
        """
        latest_entry = self.parent.get_latest_personal_info()
        tk.Label(self,
                 text= 'Height: ' + str(latest_entry[0])+ 'in',
                 font = ENTRIES_FONT).grid(column = 0, row =0)
        tk.Label(self, text= 'Weight: ' + str(latest_entry[1])+'lbs',
                 font = ENTRIES_FONT).grid(column = 0, row =1)
        tk.Label(self, text= 'Age: ' + str(latest_entry[2])+' years',
                 font = ENTRIES_FONT).grid(column = 0, row =2)
        if latest_entry[5] == '':
            tk.Label(self, text= 'Body Fat(percent): ' + '---'+'%',
                     font = ENTRIES_FONT).grid(column = 0, row =3)
        else:
            tk.Label(self,
                     text= 'Body Fat(percent): ' + str(latest_entry[5])+'%',
                     font = ENTRIES_FONT).grid(column = 0, row =3)
        if latest_entry[6] == '':
            tk.Label(self, text= 'Waist: ' + '---'+'in',
                     font = ENTRIES_FONT).grid(column = 0, row =4)
        else:
            tk.Label(self,
                     text= 'Waist: ' + str(latest_entry[6])+'in',
                     font = ENTRIES_FONT).grid(column = 0, row =4)
        
    
        
        
        
    
#END entries

#BEGIN displayed calculations
class BasalMetabolicRateDisplayLabel(tk.Label):
    """
    Label that changes dependent on entries and  inputted formula. 
    """
    def __init__(self,parent):
        tk.Label.__init__(self,parent)
        self.parent = parent
        if not self.parent.parent.parent.is_database_empty():
            self.update_label()

            
            
    def mifflin_stjeor(self):
        """
        Most accurate
        """
        latest_personal_info = self.parent.parent.parent.get_latest_personal_info()
        weight_in_kg = float(self.parent.parent.parent.lbs_to_kg(latest_personal_info[1]))
        height_in_cm = float(self.parent.parent.parent.in_to_cm(latest_personal_info[0]))
        if latest_personal_info[3] == 'Male':
            return round((10*weight_in_kg+6.25*height_in_cm-5*float(latest_personal_info[2])+5),0)
        return round((10*weight_in_kg+6.25*height_in_cm-5*float(latest_personal_info[2])-161),0)
    def katch_mcardle(self):
        """
        Accurate for leaner people(and those who know BMI)
        """
        latest_personal_info = self.parent.parent.parent.get_latest_personal_info()
        if latest_personal_info[5] == '':
            return None

        fat_free_mass = float(latest_personal_info[1]) -(float(latest_personal_info[5])/100) * float(latest_personal_info[1])
        return round(21.6 * self.parent.parent.parent.lbs_to_kg(fat_free_mass) + 370,0)
        
    def harris_benedict(self):
        """
        Skewed towards obese and young...overstates by 5%
        """
        latest_personal_info = self.parent.parent.parent.get_latest_personal_info()
        weight_in_kg = float(self.parent.parent.parent.lbs_to_kg(latest_personal_info[1]))
        height_in_cm = float(self.parent.parent.parent.in_to_cm(latest_personal_info[0]))
        
        if latest_personal_info[3] == 'Male':
            return round((66.5+(13.75*weight_in_kg)+(5.003*height_in_cm) - (4.676 * int(latest_personal_info[2]))),1)
    def average(self):
        if self.katch_mcardle() == None:
            return None
        return round((self.mifflin_stjeor() + self.katch_mcardle() + self.harris_benedict()) / 3.0,0)
    def update_label(self):
        """
        Updates the text of the label
        """

        if self.parent.selected_formula.get() == 'Mifflin St-Jeor':
            self.config(text = self.mifflin_stjeor())
        if self.parent.selected_formula.get() == 'Katch-McArdle':
            self.config(text = self.katch_mcardle())
        if self.parent.selected_formula.get() == 'Harris Benedict':
            self.config(text = self.harris_benedict())
        if self.parent.selected_formula.get() == 'Average':
            self.config(text = self.average())
        
        
class BasalMetabolicRateFrame(tk.Frame):
    """
    Holds radiobuttons and output label for BMR
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RAISED,
                          borderwidth = 3)
        self.parent = parent
        self.latest_personal_info = self.parent.parent.get_latest_personal_info()
        self.selected_formula = tk.StringVar()
        self.selected_formula.set('Mifflin St-Jeor')

        tk.Label(self, text = 'Basal Metabolic Rate').grid(column = 0, row = 0)
        self.basalMetabolicRateDisplayLabel=BasalMetabolicRateDisplayLabel(self)
        self.basalMetabolicRateDisplayLabel.grid(column = 1, row = 0)
        tk.Label(self,text = 'cals').grid(column = 2, row = 0)
        tk.Radiobutton(self,anchor = tk.W, text = 'Mifflin St-Jeor', value = 'Mifflin St-Jeor',
                       variable = self.selected_formula,
                       command = self.basalMetabolicRateDisplayLabel.update_label).grid(column = 0, row = 1)
        tk.Radiobutton(self,anchor = tk.W,  text = 'Harris Benedict', value = 'Harris Benedict',
                       variable = self.selected_formula,
                       command = self.basalMetabolicRateDisplayLabel.update_label).grid(column = 0, row = 2)

        self.katch_mcardle = tk.Radiobutton(self,
                                            anchor = tk.W,
                                            text = 'Katch-McArdle',
                                            value = 'Katch-McArdle',
                                            variable = self.selected_formula,
                       command = self.basalMetabolicRateDisplayLabel.update_label)
        self.katch_mcardle.grid(column = 0, row = 3)
  
        self.average = tk.Radiobutton(self,anchor = tk.W,  text = 'Average', value = 'Average',
                       variable = self.selected_formula,
                       command = self.basalMetabolicRateDisplayLabel.update_label)
        self.average.grid(column = 0, row = 4)
        if self.latest_personal_info[4] != None:
            self.katch_mcardle.config(state = tk.DISABLED)
            self.average.config(state = tk.DISABLED)
        
##            if self.latest_personal_info[4] == '':
##                self.katch_mcardle.config(state = tk.DISABLED)
##                self.average.config(state = tk.DISABLED)

    def set_radiobuttons(self):
        """
        If user inputs waist and bf, enables appropriate radiobuttons. Only woks with BF%
        """
        latest_personal_info = self.parent.parent.get_latest_personal_info()
        if latest_personal_info[4] != '':
            self.katch_mcardle.config(state = tk.NORMAL)
            self.average.config(state = tk.NORMAL)
        else:
            self.katch_mcardle.config(state = tk.DISABLED)
            self.average.config(state = tk.DISABLED)
            
        
        
        
        
class TotalDailyEnergyExpenditureDisplayLabel(tk.Label):
    """
    Label that changes dependent on entries and  inputted formula. 
    """
    def __init__(self,parent):
        tk.Label.__init__(self,parent)
        self.parent = parent
        if not self.parent.parent.parent.is_database_empty():
            self.update_label()

    def update_label(self):
        """
        Updates the text of the label
        """
        latest_personal_info = self.parent.parent.parent.get_latest_personal_info()
        if self.parent.selected_formula.get() == 'Calculated':
            if latest_personal_info[4] == 'Sedentary':
                self.config(text = str(float(self.parent.parent.basalMetabolicRateFrame.basalMetabolicRateDisplayLabel.cget('text'))*1.2))
            if latest_personal_info[4] == 'Lightly Active':
                self.config(text = str(float(self.parent.parent.basalMetabolicRateFrame.basalMetabolicRateDisplayLabel.cget('text'))*1.375))
            if latest_personal_info[4] == 'Moderately Active':
                self.config(text = str(float(self.parent.parent.basalMetabolicRateFrame.basalMetabolicRateDisplayLabel.cget('text'))*1.55))
            if latest_personal_info[4] == 'Very Active':
                self.config(text = str(float(self.parent.parent.basalMetabolicRateFrame.basalMetabolicRateDisplayLabel.cget('text'))*1.725))
            if latest_personal_info[4] == 'Extra Active':
                self.config(text = str(float(self.parent.parent.basalMetabolicRateFrame.basalMetabolicRateDisplayLabel.cget('text'))*1.375))
        
class TotalDailyEnergyExpenditureFrame(tk.Frame):
    """
    Holds radiobuttons and output lebel for TDEE
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RAISED,
                          borderwidth = 3)
        self.parent = parent

        self.selected_formula = tk.StringVar()
        self.selected_formula.set('Calculated')
        self.totalDailyEnergyExpenditureDisplayLabel=TotalDailyEnergyExpenditureDisplayLabel(self)
        self.totalDailyEnergyExpenditureDisplayLabel.grid(column = 1, row = 0)
        tk.Label(self,text = 'Total Daily Energy Expenditure').grid(column = 0, row = 0)
        tk.Label(self,text = 'cals').grid(column = 2, row = 0)
        tk.Radiobutton(self,anchor = tk.W, text = 'Calculated', value = 'Calculated',
                       variable = self.selected_formula,
                       command = self.totalDailyEnergyExpenditureDisplayLabel.update_label).grid(column = 0, row = 1)
        tk.Radiobutton(self,anchor = tk.W,  text = 'Simple Multiplier', value = 'Simple Multiplier',
                       variable = self.selected_formula,
                       command = self.totalDailyEnergyExpenditureDisplayLabel.update_label).grid(column = 0, row = 2)
        
class LeanBodyMassDisplayLabel(tk.Label):
    def __init__(self,parent):
        tk.Label.__init__(self,parent,
                          text = '---')
        self.parent = parent
        self.update_label()

    def update_label(self):
        """
        Updates the text of the label
        """
        latest_personal_info = self.parent.parent.parent.get_latest_personal_info()
        if latest_personal_info[5] == '':
            self.config(text ='---')
            return
        self.config(text = self.parent.parent.parent.calculate_lean_body_mass_subtraction())
class FatBodyMassDisplayLabel(tk.Label):
    def __init__(self,parent):
        tk.Label.__init__(self,parent,
                          text = '---')
        self.parent = parent
        self.update_label()

    def update_label(self):
        """
        Updates the text of the label
        """
        latest_personal_info = self.parent.parent.parent.get_latest_personal_info()
        if latest_personal_info[5] == '':
            self.config(text ='---')
            return

        self.config(text = self.parent.parent.parent.calculate_fat_body_mass())
class BodyMassFrame(tk.Frame):
    """
    Displays Lean Body Mass and Fat Body Mass
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RAISED,
                          borderwidth = 3)
        self.parent = parent

        tk.Label(self,text = 'Lean Body Mass(LBM)').grid(column = 0, row = 0)
        self.leanBodyMassDisplayLabel = LeanBodyMassDisplayLabel(self)
        self.leanBodyMassDisplayLabel.grid(column = 1, row = 0)
        tk.Label(self, text = 'lbs').grid(column = 2, row = 0)

        tk.Label(self,text = 'Fat Body Mass(FBM)').grid(column = 0, row = 1)
        self.fatBodyMassDisplayLabel = FatBodyMassDisplayLabel(self)
        self.fatBodyMassDisplayLabel.grid(column = 1, row = 1)
        tk.Label(self, text = 'lbs').grid(column = 2, row = 1)
        

class WaistToHeightRatioDisplayLabel(tk.Label):
    def __init__(self,parent):
        tk.Label.__init__(self,parent,
                          text = '---')
        self.parent = parent
        self.update_label()

    def update_label(self):
        """
        Updates the text of the label
        """

        self.config(text = self.parent.parent.parent.waist_to_height_ratio())
class MaximumFatMetabolismDisplayLabel(tk.Label):
    def __init__(self,parent):
        tk.Label.__init__(self,parent,
                          text = '---')
        self.parent = parent
        self.update_label()

    def update_label(self):
        """
        Updates the text of the label
        """

        pass
class MinimumRecommendedDailyCaloriesDisplayLabel(tk.Label):
    def __init__(self,parent):
        tk.Label.__init__(self,parent,
                          text = '---')
        self.parent = parent
        self.update_label()

    def update_label(self):
        """
        Updates the text of the label
        """

        pass         
class WaistToHeightFrame(tk.Frame):
    """
    Holds displays for waist to height ratio, maximum fat metabolism, and
    minimum recommended daily cals
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RAISED,
                          borderwidth = 3)
        self.parent = parent

        tk.Label(self, text = 'Waist-to-Height Ratio').grid(column = 0,
                                                            row= 0)
        self.waistToHeightRatioDisplayLabel = WaistToHeightRatioDisplayLabel(self)
        self.waistToHeightRatioDisplayLabel.grid(column = 1, row = 0)
        tk.Label(self, text = '%').grid(column = 2, row = 0)

        tk.Label(self, text = 'Maximum Fat Metabolism').grid(column = 0,
                                                             row= 1)
        self.maximumFatMetabolismDisplayLabel = MaximumFatMetabolismDisplayLabel(self)
        self.maximumFatMetabolismDisplayLabel.grid(column = 1, row = 1)
        tk.Label(self, text = 'cals').grid(column = 2, row = 1)

        tk.Label(self, text = 'Minimum Recommended Daily Calories').grid(column = 0,
                                                                         row= 2)
        self.minimumRecommendedDailyCaloriesDisplayLabel = MinimumRecommendedDailyCaloriesDisplayLabel(self)
        self.minimumRecommendedDailyCaloriesDisplayLabel.grid(column = 1,
                                                              row = 2)
        tk.Label(self, text = 'cals').grid(column = 2, row = 2)

        
class CalculationsHolderFrame(tk.Frame):
    """
    Holds displays for calculations (BMR, TDEE, LBM, BMI, waist-to-height ratio)
    """
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        
        self.basalMetabolicRateFrame = BasalMetabolicRateFrame(self)
        self.basalMetabolicRateFrame.grid(column = 0, row = 0,
                                          sticky = 'ew')

        self.totalDailyEnergyExpenditureFrame = TotalDailyEnergyExpenditureFrame(self)
        self.totalDailyEnergyExpenditureFrame.grid(column = 0, row = 1,
                                                   sticky = 'ew')

        self.bodyMassFrame = BodyMassFrame(self)
        self.bodyMassFrame.grid(column = 0, row = 2, stick = 'ew')

        self.waistToHeightFrame = WaistToHeightFrame(self)
        self.waistToHeightFrame.grid(column = 0, row = 3, sticky = 'ew')

#END displayed calculations
class PersonalInfoWindow(tk.Toplevel):
    """
    Window in which user enters personal information. 
    """
    def __init__(self, parent = None):
        tk.Toplevel.__init__(self,parent,
                             height = 400,
                             width = 400)
        self.entriesHolderFrame = EntriesHolderFrame(self)
        self.entriesHolderFrame.grid(column = 0, row = 0,sticky = 'n')

        self.currentEntriesFrame = CurrentEntriesFrame(self)
        self.currentEntriesFrame.grid(column = 0, row = 0,sticky = 's')

        self.calculationsHolderFrame = CalculationsHolderFrame(self)
        self.calculationsHolderFrame.grid(column = 1, row = 0,
                                          padx = 5,ipadx = 3,sticky= 'ns')
    def lbs_to_kg(self,pounds):
        return float(pounds)/2.2046
    def in_to_cm(self,inches):
        return int(inches)*2.54
    def kg_to_lbs(self,kg):
        return kg* 2.2046
    def cm_to_in(self,cm):
        return cm/2.54

    def is_database_empty(self):
        conn = lite.connect('fit.db')
        cursor = conn.cursor()
        
        for row in cursor.execute('SELECT COUNT(*) FROM personal_info'):
            if row[0] == 0: #Table is empty
                return True
        conn.commit()
        conn.close()
        return False
        
        
    def get_latest_personal_info(self):
        
        conn = lite.connect('fit.db')
        cursor = conn.cursor()
        for row in cursor.execute('SELECT * FROM personal_info WHERE id = (SELECT max(id) FROM personal_info)'):
            latest_in_database = row[2:]
        conn.commit()
        conn.close()
        latest_in_entries =(self.entriesHolderFrame.heightEntry.get(),
                            self.entriesHolderFrame.weightEntry.get(),
                            self.entriesHolderFrame.ageEntry.get(),
                            self.entriesHolderFrame.gender.get(),
                            self.entriesHolderFrame.activityLevel.get(),
                            self.entriesHolderFrame.bodyFatEntry.get(),
                            self.entriesHolderFrame.waistEntry.get())
        if self.is_database_empty():
            return latest_in_entries
##            return None
        
        latest_personal_info = []
        for index in range(len(latest_in_entries)):
            if latest_in_entries[index] != '':
                latest_personal_info.append(latest_in_entries[index])
            else:
                latest_personal_info.append(latest_in_database[index])
        print('latest personal info is..',str(latest_personal_info))
        return latest_personal_info
    def calculate_lean_body_mass_formula(self):
        latest_personal_info = self.get_latest_personal_info()
        height_in_cm = self.in_to_cm(latest_personal_info[0])
        weight_in_kg = self.lbs_to_kg(latest_personal_info[1])
        print(latest_personal_info)
        print(height_in_cm)
        print(weight_in_kg)
        if latest_personal_info[3] == 'Male':
            return self.kg_to_lbs(((0.32810 * weight_in_kg) + (0.33929 * height_in_cm) - 29.5336))
        return self.kg_to_lbs(((0.29569 * weight_in_kg) + (0.41813 * height_in_cm) - 43.2933))
    
     
                    
    def calculate_body_fat(self):
        gender = self.parent.gender.get()

        if gender == 'Male':
            body_weight = float(self.parent.weightEntry.get())
            lean_body_mass = self.calculate_lean_body_mass_formula()
            body_fat_percent =  ((body_weight - lean_body_mass)*100) / body_weight
            return round(body_fat_percent,1)
    def waist_to_height_ratio(self):
        latest_personal_info = self.get_latest_personal_info()
        if latest_personal_info[6] == '':
            return None
        return round((float(latest_personal_info[6])/ float(latest_personal_info[0]) *100),1)
    def calculate_fat_body_mass(self):
        latest_personal_info = self.get_latest_personal_info()
        if latest_personal_info[5] == '': # No Bodyfat entered
            return None 
        return (float(latest_personal_info[5])/100)*float(latest_personal_info[1])
    def calculate_lean_body_mass_subtraction(self):
        latest_personal_info = self.get_latest_personal_info()
        if self.calculate_fat_body_mass() == None:
            return None
        return float(latest_personal_info[1]) - float(self.calculate_fat_body_mass())
        
                    
    
        
