import datetime
from copy import copy
import tkinter as tk
import tkinter.messagebox as tkm
import sqlite3 as lite
import ttkcalendar as calendar
import fitDatabase as data
import fit as fit
##################################################
###########START Add Food To Day##################
##################################################
#Add Food To Day Variables
FOOD_LISTING_FRAME_HEIGHT = 800
FOOD_LISTING_FRAME_WIDTH = 700
FOOD_LISTING_FRAME_BORDERWIDTH = 3
TAB_FRAME_HEIGHT = 75
TAB_FRAME_WIDTH = 400
TAB_FRAME_BORDERWIDTH = 3
class SaveMealButton(tk.Button):
    """
    Button that saves the meal to the recipes and recipe_ingrediet_listing sql database.
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Save',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'green',
                           command = lambda:self.save_meal())
        self.parent = parent
    def get_last_id_number(self):
        """
        Gets the latest ID number in the SQL table
        """
        id_number = []
        for row in data.cursor.execute('SELECT max(id) FROM foods'): 
            id_number.append(row[0])
        for row in data.cursor.execute('SELECT max(id) FROM recipes'): 
            id_number.append(row[0])
        if id_number[0] == None: #the table has just been created
            id_number[0] = 0
        if id_number[1] == None:
            id_number[1] = 0

####            return 0
        return max(id_number) #returns the latest id number from foods or recipes
    def get_last_id_recipe_ingredient_listing(self):
        """
        Gets latest id for recipe_listing table, which has its own unique primary id keys
        """
        id_number = []
        for row in data.cursor.execute('SELECT max(id) FROM recipe_ingredient_listing'): 
            id_number.append(row[0])
        if id_number[0] == None: #the table has just been created
            return 0
        return id_number[0]
        
    
        
    
    def create_sql_enterable_list_of_tuples(self):
        """
        Creates  a tuple from the checked items that will be inputted
        to the database.
        """
        recipe_id = self.get_last_id_number()
        recipe_ingredient_listing_id = self.get_last_id_recipe_ingredient_listing()+1
        
        list_of_sql_enterable_tuples = []
        for group in self.parent.to_display:
           
            if group[0].get():
                try:
                    
##                    list_of_sql_enterable_tuples.append((int(group[1]),float(group[2].get()),
##                                                        float(group[3].get().split(' ')[0]),
##                                                        str(group[3].get().split(' ')[1])))
                    list_of_sql_enterable_tuples.append((recipe_ingredient_listing_id,
                                                         recipe_id,
                                                         int(group[1]),float(group[2].get()),
                                                         float(group[3].get().split(' ')[0]),
                                                         str(group[3].get().split(' ')[1])))
                                                         
                    recipe_ingredient_listing_id +=1
                except ValueError:
                    tkm.showerror('Missing Entry','Fill in a quantity')
                    return
                
        return list_of_sql_enterable_tuples
    def save_meal(self):
        """
        Appends the checked and their values to a dictionary in
        InputFoodJournalMain in the toSave dictionary. The
        dictionary has the following format:
        {<mealName> : (sql enterable tuple),}
        """
        id_number = self.get_last_id_number() + 1
        data.cursor.execute('INSERT INTO recipes VALUES(?,?,?,?,?)',(id_number,
                                                                   self.parent.infoFrame.nameEntry.get(),
                                                                   self.parent.infoFrame.descriptionEntry.get(),
                                                                   self.parent.infoFrame.servingsEntry.get(),
                                                                     1))
                                                                   
                            
        sql_enterable_list = self.create_sql_enterable_list_of_tuples()
        for row in sql_enterable_list:
            data.cursor.execute('''INSERT INTO recipe_ingredient_listing VALUES(?,?,?,?,?,?)''',(row[0],row[1],row[2],
                                                                                                 row[3],row[4],row[5]))
        data.conn.commit()
        
                           
class InfoFrame(tk.Frame):
    """
    Frame that holds entries for a recipe. 
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent

        tk.Label(self,text = 'Name: ').grid(row = 0, column = 0)
        self.nameEntry = NameEntry(self)
        self.nameEntry.grid(row = 0, column=1)
        
        tk.Label(self,text = 'Description: ').grid(row = 1, column = 0)
        self.descriptionEntry = DescriptionEntry(self)
        self.descriptionEntry.grid(row = 1,column=1)

        tk.Label(self,text='Servings: ').grid(row=2,column=0)
        self.servingsEntry = ServingsPerContainerEntry(self)
        self.servingsEntry.grid(row=2,column=1)
        
class AddMealToDatabaseWindow(tk.Toplevel):
    """
    Toplevel window where user adds foods/recipes to the database. 
    """
    def __init__(self, parent):
        tk.Toplevel.__init__(self,parent,
                             height = 400,
                             width = 400)
        self.parent = parent
        #Widgets
        self.scrollableCanvas = tk.Canvas(self,relief = tk.FLAT,
                          height = FOOD_LISTING_FRAME_HEIGHT,
                          width = FOOD_LISTING_FRAME_WIDTH,
                          borderwidth = FOOD_LISTING_FRAME_BORDERWIDTH,
                          scrollregion = (0,0,FOOD_LISTING_FRAME_WIDTH,
                                          FOOD_LISTING_FRAME_HEIGHT*2))
        self.scrollableCanvas.grid(row = 2, column = 0, sticky = 'news')
        self.infoFrame = InfoFrame(self)
        self.infoFrame.grid(row = 0, column = 0, sticky = 'news')
        self.foodListingFrame = FoodListingFrame(self.scrollableCanvas)
        self.foodListingFrame.grid(row = 1, column = 0, sticky = 'news')
        self.scrollableCanvas.create_window(0,0,anchor = tk.NW,
                                            window = self.foodListingFrame)
        self.scrollY = tk.Scrollbar(self,orient = tk.VERTICAL,
                                    command = self.scrollableCanvas.yview)
        self.scrollY.grid(row = 2, column = 1, sticky = 'ns')
        self.scrollableCanvas.config(yscrollcommand = self.scrollY.set)
                    
        self.saveMealButton = SaveMealButton(self)
        self.saveMealButton.grid(row=0, column=0)
##        self.tabFrame = TabFrame(self)
##        self.tabFrame.grid(row = 0, column = 0,sticky = 'e')

        self.update_rows()
    def update_rows(self):
        conn = lite.connect('fit.db')
        c = conn.cursor()
        c.execute('SELECT * FROM foods')
        self.to_display = []
        self.foodListingFrame.destroy()
        self.foodListingFrame = FoodListingFrame(self.scrollableCanvas)
        self.foodListingFrame.grid(row = 1, column = 0,sticky = 'news')
        self.scrollableCanvas.create_window(0,0,anchor = tk.NW,
                                            window = self.foodListingFrame)
        for i, row in enumerate(c):
            
            if row[13] == 1:

                #variables for accessing data
                self.check = tk.IntVar()
                self.entry1 = tk.StringVar()
                
                tk.Checkbutton(self.foodListingFrame, variable=self.check).grid(row=i+1, column=0, sticky=tk.W)
                tk.Label(self.foodListingFrame, text=row[1]+' ' + row[2]).grid(row=i+1, column=1, padx=5, sticky=tk.W)
                tk.Label(self.foodListingFrame, text= 'Quantity: ').grid(row = i+1, column = 2, padx = 5, sticky = tk.W)
                tk.Entry(self.foodListingFrame, textvariable=self.entry1).grid(row=i+1, column=3, padx=10, sticky=tk.W)
                tk.Label(self.foodListingFrame, text= 'of: ').grid(row = i+1, column = 4, padx = 5, sticky = tk.W)

                self.servingVar = tk.StringVar()
                serving = str(row[3])+ ' ' + str(row[4])
                self.servingVar.set(str(row[3])+ ' ' + str(row[4]))
                tk.OptionMenu(self.foodListingFrame,self.servingVar, serving).grid(row = i+1, column = 5, padx = 5, sticky = tk.W)
                
                self.to_display.append((self.check,row[0] ,self.entry1, self.servingVar))
##        for item in self.to_display:
##            if item[0].get() == False:

        
        c.close()
        self.update()
        self.title('Add Meal To Database')
######START ADD MEAL TO DATABASE BUTTON######
class AddMealToDatabaseButton(tk.Button):
    """
    Opens up the AddMealToDatabase toplevel window. 
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Add Meal to Database',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'green',
                           command = self.open_window)
        self.parent = parent
        self.addMealToDatabaseWindow = None

    def open_window(self):
        if self.addMealToDatabaseWindow is None:
            self.addMealToDatabaseWindow = AddMealToDatabaseWindow(self)
            self.addMealToDatabaseWindow.protocol('WM_DELETE_WINDOW',
                                                  self.remove_window)

    def remove_window(self):
        self.addMealToDatabaseWindow.destroy()
        self.addMealToDatabaseWindow = None


######END ADD MEAL TO DATABASE BUTTON######
######START ADD FOOD TO DATABASE BUTTON######
class AddFoodToDatabaseButton(tk.Button):
    """
    Opens up the AddFoodToDatabase toplevel window. 
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Add Food to Database',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'green',
                           command = self.open_window)
        self.parent = parent
        self.addFoodToDatabaseWindow = None

    def open_window(self):
        if self.addFoodToDatabaseWindow is None:
            self.addFoodToDatabaseWindow = AddFoodToDatabaseWindow(self)
            self.addFoodToDatabaseWindow.protocol('WM_DELETE_WINDOW',
                                                  self.remove_window)

    def remove_window(self):
        self.addFoodToDatabaseWindow.destroy()
        self.addFoodToDatabaseWindow = None

######END ADD FOOD TO DATABASE BUTTON######
######START FOOD LISTING FRAME######
class FoodListingFrame(tk.Frame):
    """
    Frame that holds all of all of the future subframes for food entry.
    Foods that the user has added to the database will show up in this
    frame in rows, each row having a checkbox, the name of the food, and
    entries for quantity and serving size. 
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RIDGE,
                          highlightbackground='green',
                          height = FOOD_LISTING_FRAME_HEIGHT,
                          width = FOOD_LISTING_FRAME_WIDTH,
                          borderwidth = FOOD_LISTING_FRAME_BORDERWIDTH)
        self.parent = parent        
######END FOOD LISTING FRAME######
######START TAB BUTTONS AND FRAME######
class AddCheckedButton(tk.Button):
    """
    Adds the checked rows to the database.
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Add Checked',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'green',
                           command = lambda: self.store_for_entry())
        self.parent = parent
   
    def get_last_id_number(self):
        """
        Gets the latest ID number in the SQL table
        """
        id_number = []
        for row in data.cursor.execute('SELECT max(id) FROM foods'): 
            id_number.append(row[0])
        for row in data.cursor.execute('SELECT max(id) FROM recipes'): 
            id_number.append(row[0])
        if id_number[0] == None: #the table has just been created
            id_number[0] = 0
        if id_number[1] == None:
            id_number[1] = 0

####            return 0
        return max(id_number) #returns the latest id number from foods or recipes
    
    def create_sql_enterable_list_of_tuples(self,type_):
        """
        Creates  a tuple from the checked items that will be inputted
        to the database.
        """
        if type_ == 'Foods':
            list_of_sql_enterable_tuples = []
            for group in self.parent.parent.to_display:
                if group[0].get():
                    try:
                        list_of_sql_enterable_tuples.append((str(self.parent.parent.parent.parent.parent.titleAndDateFrame.dateLabel.cget('text')),
                                                             int(group[1]),float(group[2].get()),
                                                             float(group[3].get().split(' ')[0]),
                                                             str(group[3].get().split(' ')[1])))
                    except ValueError:
                        tkm.showerror('Missing Entry','Fill in a quantity')
                        return
            return list_of_sql_enterable_tuples
        if type_ == 'Meals':
            list_of_sql_enterable_tuples = []
            for group in self.parent.parent.to_display:
                
                if group[0].get():
                    list_of_sql_enterable_tuples.append((str(self.parent.parent.parent.parent.parent.titleAndDateFrame.dateLabel.cget('text')),
                                                             int(group[1]),float(group[2].get()),
                                                             1, group[3].get()))
                    
                    
##                    try:
##                        list_of_sql_enterable_tuples.append((str(self.parent.parent.parent.parent.parent.titleAndDateFrame.dateLabel.cget('text')),
##                                                             int(group[1]),float(group[2].get()),
##                                                             float(group[3].get().split(' ')[0]),
##                                                             str(group[3].get().split(' ')[1])))
##                    except ValueError:
##                        tkm.showerror('Missing Entry','Fill in a quantity')
##                        return
                
            return list_of_sql_enterable_tuples
    def calculate_nutrition_for_meal(self):
        """
        For a a given id in the recipes table, goes through every ingredient in the recipes_ingredient_listing, 
        """
    def store_for_entry(self):
        """
        Appends the checked and their values to a dictionary in
        InputFoodJournalMain in the toSave dictionary. The
        dictionary has the following format:
        {<mealName> : (sql enterable tuple),}
        """
        
        sql_enterable_list = self.create_sql_enterable_list_of_tuples(self.parent.parent.selection)
        if sql_enterable_list == None:
            return
     
        for tup in range(len(sql_enterable_list)):
            self.parent.parent.parent.parent.parent.toSave[self.parent.parent.parent.mealName].append(sql_enterable_list[tup])

           
            
        self.parent.parent.parent.parent.parent.update_rows(self.parent.parent.parent.mealName)
##        self.parent.parent.parent.parent.parent.parent.update_idletasks()
class DeleteFromDatabaseButton(tk.Button):
    """
    Deletes the Checked Buttons from the SQL database 'foods'
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Delete',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'green',
                           command = lambda:self.delete_sql_entries())
        self.parent = parent
    def delete_sql_entries(self):
        """
        Deletes sql_entries from an sql database
        """
        if self.parent.parent.selection == 'Foods':
        
            conn = lite.connect('fit.db')
            cursor = conn.cursor()

            entries_to_delete = []
            for group in self.parent.parent.to_display:
                if group[0].get():
                    entries_to_delete.append(group[1])
            for entry in entries_to_delete:
                
                cursor.execute("""UPDATE foods set to_display = 0
                                  WHERE(id = (?))""",(entry,))
            conn.commit()
            conn.close
            
        if self.parent.parent.selection == 'Meals':
        
            conn = lite.connect('fit.db')
            cursor = conn.cursor()

            entries_to_delete = []
            for group in self.parent.parent.to_display:
                if group[0].get():
                    entries_to_delete.append(group[1])
            for entry in entries_to_delete:
                
                cursor.execute("""UPDATE recipes set to_display = 0
                                  WHERE(id = (?))""",(entry,))
            conn.commit()
            conn.close
        self.parent.parent.update_rows()
                        
class RecentButton(tk.Button):
    """
    Button that makes the FoodListingFrame list the most recent foods. 
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Recent',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'purple',
                           command =
                           lambda:self.populate_listing_with_foods_in_database())
        self.parent = parent
    def populate_listing_with_foods_in_database(self):
        """
        Function that populates the frame with all the foods
        that are in the database. Here is the format for each entry :
        <check button> <food name>      <Quantity entry>   of <serving size entry>
        """
        list_of_entries = []
        
        conn = lite.connect('fit.db')
        cursor = conn.cursor()
        for row in cursor.execute('SELECT * FROM foods ORDER BY id'):
            list_of_entries.append(row)

class FrequentButton(tk.Button):
    """
    Button that makes the FoodListingFrame list the most frequently
    eaten foods. 
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Frequent',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'purple')
        self.parent = parent
class FoodsButton(tk.Button):
    """
    Button that makes the FoodListingFrame
    list foods entered by the user.
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Foods',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'purple',
                           command = lambda: self.display_foods())
        self.parent = parent
    def display_foods(self):
        """
        Sets the food listed in AddFoodToDayWindow to items from the recipes table
        """
        self.parent.parent.selection = 'Foods'
        self.parent.parent.update_rows()
        
class MealsButton(tk.Button):
    """
    Button that makes the FoodListingFrame
    list meals entered by the user.
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Meals',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'purple',
                           command = lambda: self.display_meals())
        self.parent = parent
    def display_meals(self):
        """
        Sets the food listed in AddFoodToDayWindow to items from the recipes table
        """
        self.parent.parent.selection = 'Meals'
        self.parent.parent.update_rows()
        

class TabFrame(tk.Frame):
    """
    Frame that holds all of the tab buttons that change how foods are
    listed on the FoodListingFrame (RecentTab/FrequentTab/ MyFoodsTab
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RIDGE,
                          highlightbackground='green',
                          height = TAB_FRAME_HEIGHT,
                          width = TAB_FRAME_WIDTH,
                          borderwidth = TAB_FRAME_BORDERWIDTH)
        self.parent = parent
        
        self.addCheckedButton = AddCheckedButton(self)
        self.addCheckedButton.grid(row = 0, column = 0,
                                   sticky = 'w', padx = 5)
        self.recentButton = RecentButton(self)
        self.recentButton.grid(row = 0, column = 1)
        
        self.frequentButton = FrequentButton(self)
        self.frequentButton.grid(row = 0, column = 2)
        
        self.mealsButton = MealsButton(self)
        self.mealsButton.grid(row = 0, column = 3)
        self.foodsButton = FoodsButton(self)
        self.foodsButton.grid(row = 0, column = 4)
        
        self.deleteFromDatabaseButton = DeleteFromDatabaseButton(self)
        self.deleteFromDatabaseButton.grid(row = 0, column = 5)
######END TAB LISTINGS AND FRAME######
######START SIDEBAR FRAME AND BUTTONS######
class QuickAddCaloriesButton(tk.Button):
    """
    Button to quickly add calories for the selected day. 
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           text = 'Recent',
                           relief = tk.RIDGE,
                           border = 2,
                           activeforeground = 'black',
                           activebackground = 'purple')
        self.parent = parent


class SideBarFrame(tk.Frame):
    """
    Frame that holds the date selection and quick add calories, and Save
    button. 
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RIDGE,
                          highlightbackground='green',
                          height = FOOD_LISTING_FRAME_HEIGHT-500,
                          width = FOOD_LISTING_FRAME_WIDTH-600,
                          borderwidth = FOOD_LISTING_FRAME_BORDERWIDTH)
        self.parent = parent
        
######END SIDEBAR FRAME AND BUTTONS######

class AddFoodToDayWindow(tk.Toplevel):
    """Toplevel window in which user can input foods. These are the foods that are
       saved to a particular day. 
    """
    def __init__(self, parent):
        tk.Toplevel.__init__(self,parent,
                             height = 400,
                             width = 400)
        self.parent = parent
        
        #Widgets
        self.addFoodToDatabaseButton = AddFoodToDatabaseButton(self)
        self.addFoodToDatabaseButton.grid(row = 0, column = 0, sticky = 'w')

        self.addMealToDatabaseButton = AddMealToDatabaseButton(self)
        self.addMealToDatabaseButton.grid(row = 0, column = 0)
        self.scrollableCanvas = tk.Canvas(self,relief = tk.FLAT,
                          height = FOOD_LISTING_FRAME_HEIGHT,
                          width = FOOD_LISTING_FRAME_WIDTH,
                          borderwidth = FOOD_LISTING_FRAME_BORDERWIDTH,
                          scrollregion = (0,0,FOOD_LISTING_FRAME_WIDTH,
                                          FOOD_LISTING_FRAME_HEIGHT*2))
        self.scrollableCanvas.grid(row = 1, column = 0, sticky = 'news')

        self.foodListingFrame = FoodListingFrame(self.scrollableCanvas)
        self.foodListingFrame.grid(row = 0, column = 0, sticky = 'news')
        self.scrollableCanvas.create_window(0,0,anchor = tk.NW,
                                            window = self.foodListingFrame)
        self.scrollY = tk.Scrollbar(self,orient = tk.VERTICAL,
                                    command = self.scrollableCanvas.yview)
        self.scrollY.grid(row = 1, column = 1, sticky = 'ns')
        self.scrollableCanvas.config(yscrollcommand = self.scrollY.set)
                    
##        self.foodListingFrame = FoodListingFrame(self.scrollableCanvas)
##        self.foodListingFrame.grid(row = 0, column = 0,sticky = tk.N)
        
        self.tabFrame = TabFrame(self)
        self.tabFrame.grid(row = 0, column = 0,sticky = 'e')
##        self.sideBarFrame = SideBarFrame(self)
##        self.sideBarFrame.grid(row = 1, column = 2)
        self.title('Add Food To Day Window')
        self.selection = 'Foods'

       
        self.update_rows()
    def calculate_recipe_nutrition(self):
        """
        For a a given id in the recipes table, goes through every ingredient in the recipes_ingredient_listing, 
        """
        
    def update_rows(self):
        """
        Displays in the window dependent on selection (either foods, or recipes
        """
        if self.selection == 'Foods':
            
            conn = lite.connect('fit.db')
            c = conn.cursor()
            c.execute('SELECT * FROM foods')
            self.to_display = []
            self.foodListingFrame.destroy()
            self.foodListingFrame = FoodListingFrame(self.scrollableCanvas)
            self.foodListingFrame.grid(row = 0, column = 0,sticky = tk.N)
            self.scrollableCanvas.create_window(0,0,anchor = tk.NW,
                                                window = self.foodListingFrame)
            for i, row in enumerate(c):
                
                if row[13] == 1:

                    #variables for accessing data
                    self.check = tk.IntVar()
                    self.entry1 = tk.StringVar()
                    
                    tk.Checkbutton(self.foodListingFrame, variable=self.check).grid(row=i+1, column=0, sticky=tk.W)
                    tk.Label(self.foodListingFrame, text=row[1]+' ' + row[2]).grid(row=i+1, column=1, padx=5, sticky=tk.W)
                    tk.Label(self.foodListingFrame, text= 'Quantity: ').grid(row = i+1, column = 2, padx = 5, sticky = tk.W)
                    tk.Entry(self.foodListingFrame, textvariable=self.entry1).grid(row=i+1, column=3, padx=10, sticky=tk.W)
                    tk.Label(self.foodListingFrame, text= 'of: ').grid(row = i+1, column = 4, padx = 5, sticky = tk.W)

                    self.servingVar = tk.StringVar()
                    serving = str(row[3])+ ' ' + str(row[4])
                    self.servingVar.set(str(row[3])+ ' ' + str(row[4]))
                    tk.OptionMenu(self.foodListingFrame,self.servingVar, serving).grid(row = i+1, column = 5, padx = 5, sticky = tk.W)
                    
                    self.to_display.append((self.check,row[0] ,self.entry1, self.servingVar))
            
            c.close()
            self.update()
        if self.selection == 'Meals':
            conn = lite.connect('fit.db')
            c = conn.cursor()
            c.execute('SELECT * FROM recipes')
            self.to_display = []
            self.foodListingFrame.destroy()
            self.foodListingFrame = FoodListingFrame(self.scrollableCanvas)
            self.foodListingFrame.grid(row = 0, column = 0,sticky = tk.N)
            self.scrollableCanvas.create_window(0,0,anchor = tk.NW,
                                                window = self.foodListingFrame)
            for i, row in enumerate(c):
                if row[4] == 1:
                    self.check = tk.IntVar()
                    self.entry1 = tk.StringVar()
                    
                    tk.Checkbutton(self.foodListingFrame, variable=self.check).grid(row=i+1, column=0, sticky=tk.W)
                    tk.Label(self.foodListingFrame, text=row[1]+' ' + row[2]).grid(row=i+1, column=1, padx=5, sticky=tk.W)
                    tk.Label(self.foodListingFrame, text= 'Quantity: ').grid(row = i+1, column = 2, padx = 5, sticky = tk.W)
                    tk.Entry(self.foodListingFrame, textvariable=self.entry1).grid(row=i+1, column=3, padx=10, sticky=tk.W)
    ##                tk.Label(self.foodListingFrame, text= 'of: ').grid(row = i+1, column = 4, padx = 5, sticky = tk.W)
                    tk.Label(self.foodListingFrame, text= 'of: ').grid(row = i+1, column = 4, padx = 5, sticky = tk.W)


                    self.servingVar = tk.StringVar()
    ##                serving = str(row[3])+ ' ' + str(row[4])
                    serving = 'Serving'
                    self.servingVar.set(serving)
                    tk.OptionMenu(self.foodListingFrame,self.servingVar, serving).grid(row = i+1, column = 5, padx = 5, sticky = tk.W)
                    
                    self.to_display.append((self.check,row[0] ,self.entry1, self.servingVar))
            
            c.close()
            self.update()
            

        
##################################################
###########END Add Food To Day####################
##################################################
##################################################
###########START Input Diet Food Journal##########
##################################################
#Input Diet Food Journal Variables
TITLE_FRAME_HEIGHT = 100
TITLE_FRAME_WIDTH = 400
TITLE_FRAME_BORDERWIDTH = 3

MEAL_HEADING_HEIGHT = 40
MEAL_HEADING_WIDTH = 725
MEAL_HEADING_BORDERWIDTH = 3
MEAL_HEADING_FONT = ('Times', '13')
MEAL_HEADINGS_PADX = 18
MEAL_HEADINGS_BLANK_SPACE_PADX = 28

MEAL_BODY_HEIGHT = 150
MEAL_BODY_WIDTH = 400
MEAL_BODY_BORDERWIDTH = 3

UPDATE_ROWS_BLANK_SPACE_PADX = 20
UPDATE_ROWS_LABEL_FONT = ('Times', '9')
UPDATE_ROWS_LABEL_HEIGHT = 5
UPDATE_ROWS_LABEL_WRAPLENGTH = 90
UPDATE_ROWS_LABEL_WRAPLENGTH_2 =30
UPDATE_ROWS_LABEL_PADX = 25
UPDATE_ROWS_LABEL_PADY = 4
#START Title Date Frame, Calendar ,and Label
class TitleLabel(tk.Label):
    """
    Label that says 'Your Food Journal for:
    """
    def __init__(self,parent):
        tk.Label.__init__(self,parent,
                          font = ('Helvetica', '25'),
                          text = 'Your Food Journal for: ')
        self.parent= parent
class DateLabel(tk.Label):
    """
    Label that says the date. 
    """
    def __init__(self,parent):
        tk.Label.__init__(self,parent,
                          font = ('Helvetica', '25'),
                          text = datetime.date.today())
        self.parent= parent
        
    def display_date(self,date):
        """
        Displays the date in the label. 
        """
        date_string = str(date)
        shaved_date_string = date_string[:-9]
        self.config(text = shaved_date_string)
        
                          
class CalendarWindow(tk.Toplevel):
    """
    Toplevel window that holds the calendar
    """
    def __init__(self,parent = None):
        tk.Toplevel.__init__(self,parent)
        self.calendar = calendar.Calendar(self)
        self.calendar.grid()
        self.title('Calendar')
        
        
class DateButton(tk.Button):
    """
    Button that brings up the calendar
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           relief = tk.FLAT,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command = self.open_calendar)
        self.parent = parent
        self.calendar_image = tk.PhotoImage(file ='images/Calendar.gif')
        self.config(image = self.calendar_image)
        self.calendarWindow = None
        self.selectedDate = None
    
    def open_calendar(self):
        """
        Opens the calendar. 
        """
        if self.calendarWindow is None:
            self.calendarWindow = CalendarWindow()
            self.calendarWindow.protocol('WM_DELETE_WINDOW',
                                         self.remove_calendar_and_select_date)

    def remove_calendar_and_select_date(self):
        
        
        self.selectedDate = self.calendarWindow.calendar.selection
        self.parent.dateLabel.display_date(self.selectedDate)
        self.calendarWindow.destroy()
        self.calendarWindow = None
            
class SaveButton(tk.Button):
    """
    Button that saves all entries for the selected day to the database.
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           relief = tk.FLAT,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command = lambda:self.save_entries())
        self.parent = parent
        self.save_image = tk.PhotoImage(file = 'images/save.gif')
        self.config(image = self.save_image)

    def get_last_id_number(self):
        """
        Gets the latest ID number in the SQL table
        """
        id_number = []
        for row in data.cursor.execute('''SELECT max(id)
                                       FROM food_journal'''):
            id_number.append(row[0])
        if id_number[0] == None: #the table has just been created
            return 0
        return id_number[0]
    
    def create_sql_enterable_list_of_tuples(self):
        """
        Creates  a tuple from the checked items that will be
        inputted to the database.
        """
        list_of_sql_enterable_tuples = []
        id_number = self.get_last_id_number() + 1
        for key in self.parent.parent.toSave:
            
            for tup in self.parent.parent.toSave[key]:
                list_of_sql_enterable_tuples.append((id_number,
                                                     tup[0],tup[1],
                                                     tup[2],tup[3]
                                                     ,tup[4]))
                id_number += 1
        return list_of_sql_enterable_tuples
    
    def save_entries(self):
        """
        Saves the entry in the Food database.
        """
        conn = lite.connect('fit.db')
        cursor= conn.cursor()
        sql_enterable_list = self.create_sql_enterable_list_of_tuples()
        #Input into DB
        for row in sql_enterable_list:
            data.cursor.execute('INSERT INTO food_journal VALUES (?,?,?,?,?,?)', row)
        data.conn.commit()
        conn.close()
        self.parent.parent.destroy()
        self.parent.parent.parent.dietWindow = None
        
    
    
                
class TitleAndDateFrame(tk.Frame):
    """
    Frame that has the label frame as well as the date menu. 
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RAISED,
                          highlightbackground='green',
                          height = TITLE_FRAME_HEIGHT,
                          width = TITLE_FRAME_WIDTH,
                          borderwidth = TITLE_FRAME_BORDERWIDTH)
        self.parent = parent
        
        self.titleLabel = TitleLabel(self)
        self.titleLabel.grid(column = 0, row = 0)
        
        self.dateLabel = DateLabel(self)
        self.dateLabel.grid(column = 1, row = 0)
        
        self.dateButton = DateButton(self)
        self.dateButton.grid(column = 2, row = 0)

        self.saveButton = SaveButton(self)
        self.saveButton.grid(column = 3, row = 0)
#END Title Date Frame, Calendar ,and Label

class AddFoodButton(tk.Button):
    """Opens a new window that allows the user to add food to a particular day
    (AddFoodToDayWindow(tk.Toplevel)"""
    def __init__(self, parent):
        tk.Button.__init__(self, parent,
                           text = 'Add Food/Meal',
                           relief = tk.RIDGE,
                           borderwidth = 5,
                           activeforeground = 'black',
                           activebackground = 'white',
                           width = 11,
                           command = self.open_window)
        self.parent = parent
        self.addFoodToDayWindow = None
        
    def open_window(self):
        if self.addFoodToDayWindow is None:
            self.addFoodToDayWindow = AddFoodToDayWindow(self.parent)
            self.addFoodToDayWindow.protocol('WM_DELETE_WINDOW', self.remove_window)

    def remove_window(self):
        self.addFoodToDayWindow.destroy()
        self.addFoodToDayWindow = None
class DeleteCheckedButton(tk.Button):
    """
    Delete all the rows in the toSave dict that are checked. Also changes the row numbers the other entries. 
    """
    def __init__(self, parent):
        tk.Button.__init__(self, parent,
                           text = 'Delete',
                           relief = tk.RIDGE,
                           borderwidth = 4,
                           activeforeground = 'black',
                           activebackground = 'white',
                           width = 4,
                           command = self.deleteEntries)
        self.parent = parent
    def deleteEntries(self):
        for row in self.parent.parent.to_delete:
            if row[0].get():
                for entry_index in range(len(self.parent.parent.toSave[self.parent.mealName]) -1,-1,-1):
                    if self.parent.parent.toSave[self.parent.mealName][entry_index] == row[1]:
                        self.parent.parent.toSave[self.parent.mealName].remove(self.parent.parent.toSave[self.parent.mealName][entry_index])
                        break
        self.parent.parent.update_rows(self.parent.mealName)
    
##START meal Label and Body
class MealHeadingFrame(tk.Frame):
    """
    Frame that holds all the title information for breakfast.
    "<Meal Name>      Calories       Carbs      Fat     Protein   Sodium    Sugar"
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RAISED,
                          highlightbackground='green',
                          height = MEAL_HEADING_HEIGHT,
                          width = MEAL_HEADING_WIDTH,
                          borderwidth = MEAL_HEADING_BORDERWIDTH)
        self.parent = parent
        self.mealName = None
        
        #All the labels
        self.mealNameLabel = tk.Label(self, font = MEAL_HEADING_FONT,
                                 text = self.mealName)
        self.mealNameLabel.grid(column = 0, row = 0)

        self.blankSpaceLabel = tk.Label(self, font = MEAL_HEADING_FONT,
                                 text = '          ')
        self.blankSpaceLabel.grid(column = 1, row = 0,
                                  padx = MEAL_HEADINGS_BLANK_SPACE_PADX)
        
        self.caloriesLabel = tk.Label(self, font = MEAL_HEADING_FONT,
                                 text = 'Calories')
        self.caloriesLabel.grid(column = 2, row = 0,padx = MEAL_HEADINGS_PADX)

        self.carbsLabel = tk.Label(self, font = MEAL_HEADING_FONT,
                                 text = 'Carbs')
        self.carbsLabel.grid(column = 3, row = 0,
                             padx = MEAL_HEADINGS_PADX)

        self.fatLabel = tk.Label(self, font = MEAL_HEADING_FONT,
                                 text = 'Fat')
        self.fatLabel.grid(column = 4, row = 0,
                           padx = MEAL_HEADINGS_PADX)

        self.proteinLabel = tk.Label(self, font = MEAL_HEADING_FONT,
                                 text = 'Protein')
        self.proteinLabel.grid(column = 5, row = 0,
                               padx = MEAL_HEADINGS_PADX)

        self.fiberLabel = tk.Label(self, font = MEAL_HEADING_FONT,
                                 text = 'Fiber')
        self.fiberLabel.grid(column = 6, row = 0,
                             padx = MEAL_HEADINGS_PADX)

        self.sugarLabel = tk.Label(self, font = MEAL_HEADING_FONT,
                                 text = 'Sugar')
        self.sugarLabel.grid(column = 7, row = 0,
                             padx = MEAL_HEADINGS_PADX)

        self.deleteCheckedButton = DeleteCheckedButton(self)
        self.deleteCheckedButton.grid(column = 8, row = 0,
                                      padx = MEAL_HEADINGS_PADX-18)

class MealBodyFrame(tk.Frame):
    """
    Frame that holds all of the buttons and strings for breakfast. 
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.FLAT,
                          height = MEAL_BODY_HEIGHT,
                          width = MEAL_BODY_WIDTH,
                          borderwidth = MEAL_BODY_BORDERWIDTH)
        self.parent = parent
        self.mealName = None
        self.addToMealNameButton = AddFoodButton(self)
        self.addToMealNameButton.grid(column = 0, row = 0)
        
##END meal Label and Body
class InputDietFoodJournalMain(tk.Toplevel):
    """
    Toplevel window where the user can view all the foods they
    entered for the day and then save that information to the database. 
    """
    def __init__(self,parent = None):
        tk.Toplevel.__init__(self,parent,
                           height = 800,
                           width = 400)
        self.parent = parent
        self.title('Food Journal')
        self.toSave = {'Breakfast': [], 'Lunch':[], 'Dinner':[], 'Snacks':[]}
        self.mealWidgetsDictionary = {'Breakfast': {'Heading':[],'Body':[],'Canvas':[]},
                                      'Lunch':{'Heading':[],'Body':[],'Canvas':[]},
                                      'Dinner':{'Heading':[],'Body':[],'Canvas':[]},
                                      'Snacks':{'Heading':[],'Body':[],'Canvas':[]}}
        
        
        
        self.titleAndDateFrame = TitleAndDateFrame(self)
        self.titleAndDateFrame.grid(column = 0,row = 0, sticky = 'we')
        self.titleAndDateFrame.columnconfigure(0, weight = 1)
        
        #Breakfast start
        self.breakfastHeadingFrame = MealHeadingFrame(self)
        self.breakfastHeadingFrame.mealName = 'Breakfast'
        self.breakfastHeadingFrame.mealNameLabel.config(text = self.breakfastHeadingFrame.mealName)
        self.mealWidgetsDictionary['Breakfast']['Heading']= self.breakfastHeadingFrame
        self.breakfastHeadingFrame.grid(column =0, row = 1)
        self.breakfastHeadingFrame.grid_propagate(0)
        self.breakfastBodyCanvas = tk.Canvas(self,height = MEAL_BODY_HEIGHT,
                                             width = MEAL_BODY_WIDTH,
                                             scrollregion = (0,0,MEAL_BODY_WIDTH,MEAL_BODY_HEIGHT*5))
        self.mealWidgetsDictionary['Breakfast']['Canvas'] = self.breakfastBodyCanvas
        self.breakfastBodyCanvas.parent = self
        self.breakfastBodyCanvas.grid(column = 0 , row = 2, sticky = 'we')
        self.breakfastBodyFrame = MealBodyFrame(self.breakfastBodyCanvas)
        self.breakfastBodyFrame.mealName = 'Breakfast'
        self.mealWidgetsDictionary['Breakfast']['Body'] = self.breakfastBodyFrame
        self.breakfastBodyCanvas.create_window(0, 0 ,
                                               anchor = tk.NW,
                                               window = self.breakfastBodyFrame)
        #scroll breakfast start
        self.scrollBreakfast = tk.Scrollbar(self, orient = tk.VERTICAL,
                                           command = self.breakfastBodyCanvas.yview)                                 
        self.breakfastBodyCanvas.config(yscrollcommand = self.scrollBreakfast.set)
        self.scrollBreakfast.grid(row=2,column=1,sticky = 'ns')
        
        #scrollbreakfast end
        #Breakfast end
        
        #Lunch Start
        self.lunchHeadingFrame = MealHeadingFrame(self)
        self.mealWidgetsDictionary['Lunch']['Heading']= self.lunchHeadingFrame

        self.lunchHeadingFrame.mealName = 'Lunch'
        self.lunchHeadingFrame.mealNameLabel.config(text = self.lunchHeadingFrame.mealName)
        self.lunchHeadingFrame.grid(column =0, row = 3)
        self.lunchBodyCanvas = tk.Canvas(self, height = MEAL_BODY_HEIGHT,
                                         width = MEAL_BODY_WIDTH,
                                         scrollregion = (0, 0, MEAL_BODY_WIDTH, MEAL_BODY_HEIGHT*5))
        self.mealWidgetsDictionary['Lunch']['Canvas'] = self.lunchBodyCanvas

        self.lunchBodyCanvas.parent = self
        self.lunchBodyFrame = MealBodyFrame(self.lunchBodyCanvas)
        self.lunchBodyFrame.mealName = 'Lunch'
        self.mealWidgetsDictionary['Lunch']['Body'] = self.lunchBodyFrame
        self.lunchBodyCanvas.create_window(0,0,
                                           anchor = tk.NW,
                                           window = self.lunchBodyFrame)
        self.lunchBodyCanvas.grid(column =0, row = 4, sticky = 'we')
        
        #scroll lunch start
        self.scrollLunch = tk.Scrollbar(self, orient = tk.VERTICAL,
                                           command = self.lunchBodyCanvas.yview)                                 
        self.lunchBodyCanvas.config(yscrollcommand = self.scrollLunch.set)
        self.scrollLunch.grid(row=4,column=1,sticky = 'ns')
        #scroll lunch end
        #Lunch end
        #Dinner start
        self.dinnerHeadingFrame = MealHeadingFrame(self)
        self.mealWidgetsDictionary['Dinner']['Heading']= self.dinnerHeadingFrame
        self.dinnerHeadingFrame.mealName = 'Dinner'
        self.dinnerHeadingFrame.mealNameLabel.config(text = self.dinnerHeadingFrame.mealName)

        self.dinnerHeadingFrame.grid(column =0, row = 5)
        self.dinnerBodyCanvas = tk.Canvas(self, height = MEAL_BODY_HEIGHT,
                                         width = MEAL_BODY_WIDTH,
                                         scrollregion = (0, 0, MEAL_BODY_WIDTH, MEAL_BODY_HEIGHT*5))
        self.mealWidgetsDictionary['Dinner']['Canvas'] = self.dinnerBodyCanvas
        self.dinnerBodyCanvas.parent = self
        self.dinnerBodyFrame = MealBodyFrame(self.dinnerBodyCanvas)
        self.dinnerBodyFrame.mealName = 'Dinner'
        self.mealWidgetsDictionary['Dinner']['Body'] = self.dinnerBodyFrame
        
        self.dinnerBodyCanvas.create_window(0,0,anchor = tk.NW,
                                            window = self.dinnerBodyFrame)
        self.dinnerBodyCanvas.grid(column =0, row = 6, sticky = 'we')
        #scroll dinner start
        self.scrollDinner = tk.Scrollbar(self, orient = tk.VERTICAL,
                                           command = self.dinnerBodyCanvas.yview)                                 
        self.dinnerBodyCanvas.config(yscrollcommand = self.scrollDinner.set)
        self.scrollDinner.grid(row=6,column=1,sticky = 'ns')
        #scroll dinner end
        #Dinner end
        #Snacks start
        self.snacksHeadingFrame = MealHeadingFrame(self)
        self.mealWidgetsDictionary['Snacks']['Heading']= self.snacksHeadingFrame
        self.snacksHeadingFrame.mealName = 'Snacks'
        self.snacksHeadingFrame.mealNameLabel.config(text = self.snacksHeadingFrame.mealName)
        self.snacksHeadingFrame.grid(column =0, row = 7)
        self.snacksBodyCanvas = tk.Canvas(self,
                                        height = MEAL_BODY_HEIGHT,
                                         width = MEAL_BODY_WIDTH,
                                         scrollregion = (0, 0, MEAL_BODY_WIDTH, MEAL_BODY_HEIGHT*5))
        self.mealWidgetsDictionary['Snacks']['Canvas'] = self.snacksBodyCanvas
        self.snacksBodyCanvas.parent = self
        self.snacksBodyFrame = MealBodyFrame(self.snacksBodyCanvas)
        self.snacksBodyFrame.mealName = 'Snacks'
        
        self.snacksBodyCanvas.grid(column =0, row = 8, sticky = 'we')
        self.snacksBodyCanvas.create_window(0,0,anchor = tk.NW,
                                            window = self.snacksBodyFrame)
        self.mealWidgetsDictionary['Snacks']['Body'] = self.snacksBodyFrame
        #scroll snacks  start
        self.scrollSnacks = tk.Scrollbar(self, orient = tk.VERTICAL,
                                           command = self.snacksBodyCanvas.yview)                                 
        self.snacksBodyCanvas.config(yscrollcommand = self.scrollSnacks.set)
        self.scrollSnacks.grid(row=8,column=1,sticky = 'ns')
        #scroll snacks end
        #Snacks End
    def calculate_recipe_nutrition(self,recipe_id):
        foods_quantity_list_of_lists = []
        data_list = []
        for row in data.cursor.execute('''SELECT * FROM recipe_ingredient_listing WHERE recipe_id = ?''',(recipe_id,)):
            foods_quantity_list_of_lists.append([row[2],row[3]])
        for item in foods_quantity_list_of_lists:
            for row in data.cursor.execute('''SELECT * FROM foods WHERE id = ?''',(item[0],)):
                data_list.append(row)
        price = 0
        calories = 0
        fat = 0
        carbs = 0
        fiber = 0
        sugar = 0
        protein = 0

        for recipe_ingredient_number in range(len(data_list)):
            
            calories+=data_list[recipe_ingredient_number][7]*foods_quantity_list_of_lists[recipe_ingredient_number][1]
            fat+=data_list[recipe_ingredient_number][8]*foods_quantity_list_of_lists[recipe_ingredient_number][1]
            carbs+=data_list[recipe_ingredient_number][9]*foods_quantity_list_of_lists[recipe_ingredient_number][1]
            fiber+=data_list[recipe_ingredient_number][10]*foods_quantity_list_of_lists[recipe_ingredient_number][1]
            sugar+=data_list[recipe_ingredient_number][11]*foods_quantity_list_of_lists[recipe_ingredient_number][1]
            protein+=data_list[recipe_ingredient_number][12]*foods_quantity_list_of_lists[recipe_ingredient_number][1]
        nutrition_of_recipe = [calories,fat,carbs,fiber,sugar,protein] #nutr for entire recipe, all servings
        return nutrition_of_recipe
        
        
            
    def update_rows(self,mealName):
        """
        Appends rows of labels and checkbuttons to the <mealName>bodyFrames if they are in the toSave dict. 
        """
        
        self.to_delete = []

        conn = lite.connect('fit.db')
        c = conn.cursor()
        totals = [0,0,0,0,0,0] #cals carbs fat protein fiber sugars
        food_ids = []
        recipe_ids = []
        for row in c.execute('''SELECT * FROM foods'''):
            food_ids.append(row[0])
        for row in c.execute('''SELECT * FROM recipes'''):
            recipe_ids.append(row[0])
        
        self.mealWidgetsDictionary[mealName]['Body'].destroy()
        self.mealWidgetsDictionary[mealName]['Body'] = MealBodyFrame(self.mealWidgetsDictionary[mealName]['Canvas'])
        self.mealWidgetsDictionary[mealName]['Body'].mealName = mealName
        self.mealWidgetsDictionary[mealName]['Canvas'].create_window(0, 0
                                               , anchor = tk.NW,
                                               window = self.mealWidgetsDictionary[mealName]['Body'])
        

        for i,tup in enumerate(self.toSave[mealName]):
            if tup[1] in food_ids:
            
                self.deleteCheck = tk.IntVar()
                for name,description in c.execute('''SELECT name,
                                                  description
                                                  FROM foods WHERE id = ?''',(tup[1],)):
                    
                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'], text = name +' '+description,
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH).grid(column = 0,
                             row = i+1,pady = UPDATE_ROWS_LABEL_PADY)
                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                     text = str(tup[2]*tup[3])+' '+ tup[4],
                     font = ('Times','9'),height = UPDATE_ROWS_LABEL_HEIGHT,
                     wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                     column = 1, row = i+1)

                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'],text ='      ').grid(
                             column = 2, row = i+1,
                             padx = UPDATE_ROWS_BLANK_SPACE_PADX)


                    
                for calories, carbs,fat,protein,fiber,sugars in c.execute('''SELECT
                                       calories,carbs,fat,
                                       protein,fiber,sugars
                                       FROM foods WHERE id = ?''',(tup[1],)):
                   
                  

                    totals[0]+=calories*tup[2]
                    totals[1]+=carbs*tup[2]
                    totals[2]+=fat*tup[2]
                    totals[3]+=protein*tup[2]
                    totals[4]+=fiber*tup[2]
                    totals[5]+=sugars*tup[2]
                    print(totals)
                    
                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                             text = str(calories * tup[2]),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                             column = 3,row = i+1,
                             padx = UPDATE_ROWS_LABEL_PADX)
                             
                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                             text = str(carbs * tup[2]),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                             column = 4,row = i+1,
                             padx = UPDATE_ROWS_LABEL_PADX)
                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                             text = str(fat * tup[2]),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                             column = 5, row = i+1,
                             padx = UPDATE_ROWS_LABEL_PADX)
                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                             text = str(protein * tup[2]),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                            column = 6, row = i+1,
                            padx = UPDATE_ROWS_LABEL_PADX)
                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                             text = str(fiber * tup[2]),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                             column = 7, row = i+1,
                             padx = UPDATE_ROWS_LABEL_PADX+1)
                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'], text = str(sugars * tup[2]),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                             column = 8, row = i+1,
                             padx = UPDATE_ROWS_LABEL_PADX+1)
                    tk.Checkbutton(self.mealWidgetsDictionary[mealName]['Body'],
                           variable = self.deleteCheck).grid(
                               column = 9, row = i+1)
                self.to_delete.append([self.deleteCheck, tup])
##                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'],text ='       ').grid(
##                             column = 2, row = i+1,
##                             padx = UPDATE_ROWS_BLANK_SPACE_PADX)
##            tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
##                     text = 'Totals', font = ('Times','9'),
##                     height = UPDATE_ROWS_LABEL_HEIGHT,
##                     wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
##                         column = 0, row = i+2)
##            tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
##                     text = str(tup[2]*tup[3])+' '+ tup[4],
##                     font = ('Times','9'),height = UPDATE_ROWS_LABEL_HEIGHT,
##                     wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
##                     column = 1, row = i+1)
            


       
            if tup[1] in recipe_ids:
                self.deleteCheck = tk.IntVar()
                recipe_nutrition = []
                for name,description,id_ in c.execute('''SELECT name,
                                                  description,id
                                                  FROM recipes WHERE id = ?''',(tup[1],)):
                    
                    
                    tk.Label(self.mealWidgetsDictionary[mealName]['Body'], text = name +' '+description,
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH).grid(column = 0,
                             row = i+1,pady = UPDATE_ROWS_LABEL_PADY)
                    recipe_nutrition.append(self.calculate_recipe_nutrition(id_)) 
                for recipe_index in range(len(recipe_nutrition)): 
                    for nutrient_index in range(len(recipe_nutrition[recipe_index])):
                        recipe_nutrition[recipe_index][nutrient_index] = recipe_nutrition[recipe_index][nutrient_index] * tup[2]#adjust for quantity
                
                for nutrient in recipe_nutrition: #For each nutrient, in the recipe, add to the totals
                    
                    calories = nutrient[0]
                    totals[0] += calories
                    fat = nutrient[1]
                    totals[2] += fat
                    
                    carbs = nutrient[2]
                    totals[1] += carbs
                    fiber = nutrient[3]
                    totals[4] += fiber
                    sugars = nutrient[4]
                    totals[5] += sugars
                    protein = nutrient[5]
                    totals[3]+= protein
                
                
                tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                             text = str(calories),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                             column = 3,row = i+1,
                             padx = UPDATE_ROWS_LABEL_PADX)
                             
                tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                             text = str(carbs ),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                             column = 4,row = i+1,
                             padx = UPDATE_ROWS_LABEL_PADX)
                tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                             text = str(fat ),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                             column = 5, row = i+1,
                             padx = UPDATE_ROWS_LABEL_PADX)
                tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                             text = str(protein),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                            column = 6, row = i+1,
                            padx = UPDATE_ROWS_LABEL_PADX)
                tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                             text = str(fiber ),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                             column = 7, row = i+1,
                             padx = UPDATE_ROWS_LABEL_PADX+1)
                tk.Label(self.mealWidgetsDictionary[mealName]['Body'], text = str(sugars),
                             font = UPDATE_ROWS_LABEL_FONT,
                             height = UPDATE_ROWS_LABEL_HEIGHT,
                             wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                             column = 8, row = i+1,
                             padx = UPDATE_ROWS_LABEL_PADX)
                tk.Label(self.mealWidgetsDictionary[mealName]['Body'],text ='    ').grid(
                         column = 2, row = i+1,
                         padx = UPDATE_ROWS_BLANK_SPACE_PADX) 
                tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                         text = str(tup[2]*tup[3])+' '+ tup[4],
                         font = ('Times','9'),height = UPDATE_ROWS_LABEL_HEIGHT,
                         wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                         column = 1, row = i+1)
                tk.Checkbutton(self.mealWidgetsDictionary[mealName]['Body'],
                           variable = self.deleteCheck).grid(
                               column = 9, row = i+1)
            tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                     text = 'Totals', font = ('Times','9'),
                     height = UPDATE_ROWS_LABEL_HEIGHT,
                     wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                         column = 0, row = i+2)
            for j in range(0,len(totals)):
                tk.Label(self.mealWidgetsDictionary[mealName]['Body'],
                     text = totals[j], font = ('Times','9'),
                     height = UPDATE_ROWS_LABEL_HEIGHT,
                     wraplength = UPDATE_ROWS_LABEL_WRAPLENGTH_2).grid(
                        column = j+3, row = i+2)
##        tk.Checkbutton(self.mealWidgetsDictionary[mealName]['Body'],
##                       variable = self.deleteCheck).grid(
##                           column = 9, row = i+1)
            self.to_delete.append([self.deleteCheck, tup])
       
        c.close()
        
        
##################################################
###########START Add Food To Database#############
##################################################
#Add Food To Database Variables
FOOD_DESCRIPTION_FRAME_HEIGHT = 100
FOOD_DESCRIPTION_FRAME_WIDTH = 400
FOOD_DESCRIPTION_FRAME_BORDERWIDTH = 3
FOOD_DESCRIPTION_ENTRY_WIDTH = 36
FOOD_DESCRIPTION_TEXT_WIDTH = 27
FOOD_DESCRIPTION_TEXT_HEIGHT = 2

SERVING_SIZE_AND_PRICE_FRAME_HEIGHT = 140
SERVING_SIZE_AND_PRICE_FRAME_WIDTH = 400
SERVING_SIZE_AND_PRICE_FRAME_BORDERWIDTH = 3
SERVING_SIZE_AND_PRICE_LABEL_HEIGHT = 2
SERVING_SIZE_AND_PRICE_LABEL_WIDTH = 15
SERVING_SIZE_AND_PRICE_LABEL_BORDERWIDTH = 3
SERVING_SIZE_AND_PRICE_LABEL_FONT = ('Times', '12')
SERVING_SIZE_AND_PRICE_LABEL_STICKY = tk.W
SERVING_SIZE_AND_PRICE_ENTRY_WIDTH = 10

NUTRITION_FACTS_FRAME_HEIGHT = 350
NUTRITION_FACTS_FRAME_WIDTH = 400
NUTRITION_FACTS_FRAME_BORDERWIDTH = 3
NUTRITION_FACTS_LABEL_HEIGHT = 2
NUTRITION_FACTS_LABEL_WIDTH = 15
NUTRITION_FACTS_LABEL_BORDERWIDTH = 3
NUTRITION_FACTS_LABEL_FONT = ('Times', '12')
NUTRITION_FACTS_LABEL_STICKY = tk.W
NUTRITION_FACTS_ENTRY_WIDTH = 10

#START FOOD DESCRIPTION FRAME  
class NameEntry(tk.Entry):
    """
    Entry for the name of a food. 
    """
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          width = FOOD_DESCRIPTION_ENTRY_WIDTH
                          )
        self.parent = parent
        
    def get_entry(self):
        return self.get()

class DescriptionEntry(tk.Entry):
    """
    Entry for a description of a food.
    """
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          width = FOOD_DESCRIPTION_ENTRY_WIDTH)
        self.parent = parent
        
    def get_entry(self):
        return self.get()

    
class FoodDescriptionFrame(tk.Frame):
    """
    Frame that holds the labels and entry fields for food name and description 
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RAISED,
                          highlightbackground='green',
                          height = FOOD_DESCRIPTION_FRAME_HEIGHT,
                          width = FOOD_DESCRIPTION_FRAME_WIDTH,
                          borderwidth = FOOD_DESCRIPTION_FRAME_BORDERWIDTH)
        self.parent = parent

        self.nameLabel = tk.Label(self, font = NUTRITION_FACTS_LABEL_FONT,
                                  text = 'Name/Brand: ',
                                   height = NUTRITION_FACTS_LABEL_HEIGHT,
                                   width = NUTRITION_FACTS_LABEL_WIDTH)
        self.nameLabel.grid( column = 0, row = 0, padx = 10)
        self.nameEntry = NameEntry(self)
        self.nameEntry.grid(column = 1, row = 0, sticky = 'w')

        self.descriptionLabel = tk.Label(self, font = NUTRITION_FACTS_LABEL_FONT,
                                   text = 'Description: ',
                                   height = NUTRITION_FACTS_LABEL_HEIGHT,
                                   width = NUTRITION_FACTS_LABEL_WIDTH)
        self.descriptionLabel.grid( column = 0, row = 1, padx = 10)
        self.descriptionEntry = DescriptionEntry(self)
        self.descriptionEntry.grid(column = 1, row = 1,sticky = 'w')

#END FOOD DESCRIPTION FRAME
#START SERVING SIZE AND PRICE FRAME
class ServingSizeEntry(tk.Entry):
    """
    Entry for food serving size. 
    """
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          width = SERVING_SIZE_AND_PRICE_ENTRY_WIDTH
                          )
        self.parent = parent
        
    def get_entry(self):
        return self.get()

class ServingsPerContainerEntry(tk.Entry):
    """
    Entry for food serving size. 
    """
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          width = SERVING_SIZE_AND_PRICE_ENTRY_WIDTH
                          )
        self.parent = parent
        
    def get_entry(self):
        return self.get()

class PricePerEntry(tk.Entry):
    """
    Price of the food entry. 
    """
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          width = SERVING_SIZE_AND_PRICE_ENTRY_WIDTH
                          )
        self.parent = parent
        
    def get_entry(self):
        return self.get()



class ServingSizeAndPriceFrame(tk.Frame):
    """
    Frame that holds all the information regarding serving size and price
    """
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,
                          relief = tk.RAISED,
                          highlightbackground='green',
                          height = SERVING_SIZE_AND_PRICE_FRAME_HEIGHT,
                          width = SERVING_SIZE_AND_PRICE_FRAME_WIDTH,
                          borderwidth = SERVING_SIZE_AND_PRICE_FRAME_BORDERWIDTH)
        self.parent = parent

        #Serving type START

        
        self.servingVar = tk.StringVar(self)
        teaspoon = 'teaspoon'
        tablespoon = 'tablespoon'
        fluid_oz = 'fl.oz'
        cup = 'cup'
        pint = 'liquidpint'
        quart = 'quart'
        gallon = 'gallon'
        gram = 'gram'
        unit = 'unit'
        pound = 'pound'
        oz = 'oz'
        
        self.servingVar.set("Serving Measurement")
        
        servingTypeMenu = tk.OptionMenu(self, self.servingVar,
                                 teaspoon, tablespoon, fluid_oz,
                                        cup, pint, quart, gallon, gram, unit,
                                        pound,oz)
        servingTypeMenu.grid(column = 2, row = 0, sticky = 'w')

        
        #Serving Type END
        self.servingSizeLabel = tk.Label(self, font = SERVING_SIZE_AND_PRICE_LABEL_FONT,
                                         text = 'Serving Size: ',
                                   height = SERVING_SIZE_AND_PRICE_LABEL_HEIGHT,
                                   width = SERVING_SIZE_AND_PRICE_LABEL_WIDTH)
        self.servingSizeLabel.grid( column = 0, row = 0, padx = 10)
        self.servingSizeEntry = ServingSizeEntry(self)
        self.servingSizeEntry.grid(column = 1, row = 0, sticky = 'w')

        self.servingsPerContainerLabel = tk.Label(self,
                                                  font = SERVING_SIZE_AND_PRICE_LABEL_FONT,
                                                  text = 'Servings Per Container: ',
                                   height = SERVING_SIZE_AND_PRICE_LABEL_HEIGHT,
                                   width = SERVING_SIZE_AND_PRICE_LABEL_WIDTH)
        self.servingsPerContainerLabel.grid( column = 0, row = 1,padx = 10)
        self.servingsPerContainerEntry= ServingsPerContainerEntry(self)
        self.servingsPerContainerEntry.grid(column = 1, row = 1)

        self.pricePerEntryLabel = tk.Label(self,
                                           font = SERVING_SIZE_AND_PRICE_LABEL_FONT,
                                           text = 'Price: ',
                                   height = SERVING_SIZE_AND_PRICE_LABEL_HEIGHT,
                                   width = SERVING_SIZE_AND_PRICE_LABEL_WIDTH)
        self.pricePerEntryLabel.grid( column = 0, row = 2, padx = 10)
        self.pricePerEntry= PricePerEntry(self)
        self.pricePerEntry.grid(column = 1, row = 2)
        
        
#END SERVING SIZE AND PRICE FRAME
#START NUTRITION FACTS FRAME
class AddToDatabaseButton(tk.Button):
    """
    Clicking this button saves the entry to the database. 
    """
    def __init__(self,parent):
        tk.Button.__init__(self, parent,
                           relief = tk.FLAT,
                           activeforeground = 'black',
                           activebackground = 'white',
                           command = lambda: self.save_entries())
        self.parent = parent
        self.save_image = tk.PhotoImage(file = 'images/save.gif')
        self.config(image = self.save_image)
    def get_selected_serving_type(self):
        """
        Get whatever serving type the user has selected. 
        """
        return self.parent.parent.servingSizeAndPriceFrame.servingVar.get()
    def get_description(self):
        """
        Remove \n's from a string. 
        """
        s = self.parent.parent.foodDescriptionFrame.descriptionEntry.get_entry()
        to_be_removed = ('\\')
        word_list = []
        copy_string = copy(s)
        splitted_string = copy_string.split('\n')
        return splitted_string
        joined_string = (' ').join(splitted_string)
        return joined_string

    def get_last_id_number(self):
        """
        Gets the latest ID number in the SQL table
        """
        id_number = []
        for row in data.cursor.execute('SELECT max(id) FROM foods'): 
            id_number.append(row[0])
        for row in data.cursor.execute('SELECT max(id) FROM recipes'): 
            id_number.append(row[0])
        if id_number[0] == None: #the table has just been created
            id_number[0] = 0
        if id_number[1] == None:
            id_number[1] = 0

####            return 0
        return max(id_number) #returns the latest id number from foods or recipes
        
    def get_sql_enterable_tuple(self):
        """
        Makes an sql enterable tuple from all the fields.
        """
        t0 = self.get_selected_serving_type()

        try:
            enterable_tuple = (self.get_last_id_number() + 1,
                               self.parent.parent.foodDescriptionFrame.nameEntry.get_entry(),
                               self.parent.parent.foodDescriptionFrame.descriptionEntry.get_entry(),
                               float(self.parent.parent.servingSizeAndPriceFrame.servingSizeEntry.get_entry()),
                               self.get_selected_serving_type(),
                               float(self.parent.parent.servingSizeAndPriceFrame.servingsPerContainerEntry.get_entry()),
                               float(self.parent.parent.servingSizeAndPriceFrame.pricePerEntry.get_entry()),
                               float(self.parent.parent.nutritionFactsFrame.caloriesEntry.get_entry()),
                               float(self.parent.parent.nutritionFactsFrame.totalFatEntry.get_entry()),
                               float(self.parent.parent.nutritionFactsFrame.totalCarbsEntry.get_entry()),
                               float(self.parent.parent.nutritionFactsFrame.dietaryFiberEntry.get_entry()),
                               float(self.parent.parent.nutritionFactsFrame.sugarsEntry.get_entry()),
                               float(self.parent.parent.nutritionFactsFrame.proteinEntry.get_entry()),
                               1
                               )
        except ValueError:
            tkm.showerror('Missing Entry', 'All the fields are required.')
            return
        return enterable_tuple
    def save_entries(self):
        """
        Saves the entry in the Food database.
        """
        conn = lite.connect('fit.db')
        cursor= conn.cursor()
        
        sql_enterable_list = self.get_sql_enterable_tuple()
        
        #Input into DB
        if sql_enterable_list == None:
            conn.close()
            return
        data.cursor.execute('INSERT  INTO foods VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',sql_enterable_list)
        data.conn.commit()
        conn.close()
        self.parent.parent.parent.parent.update_rows()
                           
class NutritionEntry(tk.Entry):
    """
    Entry for various nutrient values. 
    """
    def __init__(self, parent):
        tk.Entry.__init__(self, parent,
                          relief = tk.RAISED,
                          width = NUTRITION_FACTS_ENTRY_WIDTH
                          )
        self.parent = parent
        
    def get_entry(self):
        return self.get()

class NutritionFactsFrame(tk.LabelFrame):
    """
    Frame that holds all the information regarding serving size and price
    """
    def __init__(self,parent):
        tk.LabelFrame.__init__(self,parent,
                          relief = tk.RAISED,
                          highlightbackground='green',
                          text = 'Amount Per Serving: ',
                          height = NUTRITION_FACTS_FRAME_HEIGHT,
                          width = NUTRITION_FACTS_FRAME_WIDTH,
                          borderwidth = NUTRITION_FACTS_FRAME_BORDERWIDTH)
        self.parent = parent

        self.caloriesLabel = tk.Label(self, font = NUTRITION_FACTS_LABEL_FONT,
                                      text = 'Calories: ',
                                   height = NUTRITION_FACTS_LABEL_HEIGHT,
                                   width = NUTRITION_FACTS_LABEL_WIDTH)
        self.caloriesLabel.grid( column = 0, row = 0, padx = 10)
        self.caloriesEntry = NutritionEntry(self)
        self.caloriesEntry.grid(column = 1, row = 0, sticky = 'w')


        self.totalFatLabel = tk.Label(self, font = NUTRITION_FACTS_LABEL_FONT,
                                      text = 'Total Fat (grams): ',
                                   height = NUTRITION_FACTS_LABEL_HEIGHT,
                                   width = NUTRITION_FACTS_LABEL_WIDTH)
        self.totalFatLabel.grid( column = 0, row = 1, padx = 10)
        self.totalFatEntry = NutritionEntry(self)
        self.totalFatEntry.grid(column = 1, row = 1, sticky = 'w')


        
        self.totalCarbsLabel = tk.Label(self, font = NUTRITION_FACTS_LABEL_FONT,
                                        text = 'Total Carbs(grams): ',
                                   height = NUTRITION_FACTS_LABEL_HEIGHT,
                                   width = NUTRITION_FACTS_LABEL_WIDTH)
        self.totalCarbsLabel.grid( column = 0, row = 2, padx = 10)
        self.totalCarbsEntry = NutritionEntry(self)
        self.totalCarbsEntry.grid(column = 1, row = 2, sticky = 'w')

        self.dietaryFiberLabel = tk.Label(self, font = NUTRITION_FACTS_LABEL_FONT,
                                          text = 'Dietary Fiber(grams): ',
                                   height = NUTRITION_FACTS_LABEL_HEIGHT,
                                   width = NUTRITION_FACTS_LABEL_WIDTH)
        self.dietaryFiberLabel.grid( column = 0, row = 3, padx = 10)
        self.dietaryFiberEntry = NutritionEntry(self)
        self.dietaryFiberEntry.grid(column = 1, row = 3, sticky = 'w')

        self.sugarsLabel = tk.Label(self, font = NUTRITION_FACTS_LABEL_FONT,
                                    text = 'Sugars(grams): ',
                                   height = NUTRITION_FACTS_LABEL_HEIGHT,
                                   width = NUTRITION_FACTS_LABEL_WIDTH)
        self.sugarsLabel.grid( column = 0, row = 4, padx = 10)
        self.sugarsEntry = NutritionEntry(self)
        self.sugarsEntry.grid(column = 1, row = 4, sticky = 'w')

        self.proteinLabel = tk.Label(self, font = NUTRITION_FACTS_LABEL_FONT,
                                     text = 'Protein(grams): ',
                                   height = NUTRITION_FACTS_LABEL_HEIGHT,
                                   width = NUTRITION_FACTS_LABEL_WIDTH)
        self.proteinLabel.grid( column = 0, row = 5, padx = 10)
        self.proteinEntry = NutritionEntry(self)
        self.proteinEntry.grid(column = 1, row = 5, sticky = 'w')

        self.addToDatabaseButton = AddToDatabaseButton(self)
        self.addToDatabaseButton.grid(column = 2, row = 3, padx = 10, pady = 10,
                                      sticky = 'news')

        
        
#END NUTRITION FACTS FRAME
class AddFoodToDatabaseWindow(tk.Toplevel):
    """
    Toplevel window where user adds foods/recipes to the database. 
    """
    def __init__(self, parent = None):
        tk.Toplevel.__init__(self, parent,
                             height = 800,
                             width = 400)
        self.parent = parent
        self.foodDescriptionFrame = FoodDescriptionFrame(self)
        self.foodDescriptionFrame.grid(column = 0, row = 0, sticky = 'w')
        
        self.foodDescriptionFrame.grid_propagate(0)
        
        self.servingSizeAndPriceFrame = ServingSizeAndPriceFrame(self)
        self.servingSizeAndPriceFrame.grid(column = 0, row = 1, sticky = 'w')
        
        self.servingSizeAndPriceFrame.grid_propagate(0)

        self.nutritionFactsFrame = NutritionFactsFrame(self)
        self.nutritionFactsFrame.grid(column = 0, row = 2, sticky = 'w')
        
        self.nutritionFactsFrame.grid_propagate(0)

        self.minsize(400, 550)
        self.maxsize(400, 550)
        self.title('Add Food To Database Window')
        

#END SERVING SIZE AND PRICE FRAME        
##################################################
###########END Add Food To Database###############
##################################################

        

        
