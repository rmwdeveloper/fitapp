import datetime 
from copy import copy
import tkinter as tk
import tkinter.messagebox as tkm
import sqlite3 as lite
import ttkcalendar as calendar
import fitDatabase as data

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
    #Repetitive, remove later
    """
    Toplevel window that holds the calendar
    """
    def __init__(self,parent = None):
        tk.Toplevel.__init__(self,parent)
        self.calendar = calendar.Calendar(self)
        self.calendar.grid()
        
class DateButton(tk.Button):
    #Repetitive, see about removing
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
            self.calendarWindow.protocol('WM_DELETE_WINDOW', self.remove_calendar_and_select_date)

    def remove_calendar_and_select_date(self):
        
        self.selectedDate = self.calendarWindow.calendar.selection
        
        self.parent.parent.dateLabel.display_date(self.selectedDate)
        self.dateString = str(self.selectedDate)
        self.cutDateString = self.dateString[:-9] #take off the 00:00:00 from the string
        self.parent.parent.displayFrame.displayArea.initialize_rows_list(self.cutDateString)
        self.parent.parent.deleteRowFrame.selected_date = self.cutDateString
        self.calendarWindow.destroy()
        self.calendarWindow = None


class MenuFrame(tk.Frame):
    """
    Frame that will be able to hold all the menu buttons for the
    viewDietWindow Toplevel. 
    """
    def __init__(self,parent = None):
        tk.Frame.__init__(self,parent,
                          height = 100,
                          width = 600,
                          relief = tk.RAISED,
                          borderwidth = 4)
        self.parent = parent

        tk.Label(self, text = 'Select Date').grid(column = 0, row = 0,sticky = tk.E)
        self.dateButton = DateButton(self)
        self.dateButton.grid(column = 1, row = 0,sticky = tk.E)

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
        self.parent.delete_range()

    def get_individual(self):
        """
        Calls the parent delete_individual()"""                      
        self.parent.delete_individual()
        

class DeleteRowFrame(tk.Frame):
    """
    Frame containing all of the entry's and buttons that will delete rows from the
    events database
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, relief = tk.GROOVE,
                          width = 200,
                          borderwidth = 2)
        self.parent = parent
        
        self.rows_list = []
        self.selected_date = None
        conn = lite.connect('fit.db')
        cursor = conn.cursor()
        
        for row in cursor.execute('SELECT * FROM food_journal ORDER BY id'):
            self.rows_list.append(row)
        conn.close()
    
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
                                      height = 1, command = lambda:self.deleteRangeButton.get_range())

        #Delete Individual Button
        self.deleteIndividualButton = DeleteRowButton(self)
        self.deleteIndividualButton.grid(column= 5, row = 0)
        self.deleteIndividualButton.config(text = 'Delete Individual',
                                    height = 1,command = lambda:self.deleteIndividualButton.get_individual())
    def resequentialize_visible_ids(self):
        """
        Resets the ordering of visible id's so there aren't any gaps.
        """
        conn = lite.connect('fit.db')
        cursor = conn.cursor()
        id_value = 1
        cursor.execute('SELECT visible_id FROM food_journal ORDER BY id')
        inner_cursor = conn.cursor()
        for i, row in enumerate(cursor):
            inner_cursor.execute('UPDATE food_journal SET id = ?', (1,))
            id_value += 1

    def delete_range(self):
        """
        Deletes a range of rows in the SQL events table. The range is determined by entries in the starting and ending
        DeleteRowEntry entries. 
        """
        try:
            starting_index = int(self.startingRowEntry.get())
            ending_index = int(self.endingRowEntry.get())
        except ValueError:        
            tkm.showerror('Entry Error','Enter integers for starting and ending row entries',parent = self.parent)    
            return None
        conn = lite.connect('fit.db')
        cursor = conn.cursor()
        cursor.execute("""DELETE  FROM food_journal WHERE(id >= (?))
                                  AND (id <= (?))""",(starting_index,ending_index))
        cursor.execute("""DELETE FROM SQLITE_SEQUENCE WHERE NAME = 'food_journal'""")
        
        conn.commit()
        conn.close
        self.parent.displayFrame.displayArea.initialize_rows_list(self.selected_date)
        self.parent.displayFrame.displayArea.textInDisplayArea.set(self.parent.displayFrame.displayArea.create_string_from_sql_entries(self.parent.displayFrame.displayArea.make_readable_entries(self.parent.displayFrame.displayArea.rows_list)))
        self.parent.displayFrame.displayArea.delete('1.0',tk.END)
        self.parent.displayFrame.displayArea.insert('1.0',self.parent.displayFrame.displayArea.textInDisplayArea.get())
   
    def delete_individual(self):
        """
        Deletes a single row in the SQL events table. The row is determined by entry in the individual
        DeleteRowEntry"""
        try:
            index = int(self.individualRowEntry.get())
        except ValueError:        
            tkm.showerror('Entry Error','Index entry should be an integer.',parent = self.parent)    
            return None
        
        conn = lite.connect('fit.db')
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM food_journal WHERE(id = (?))""",(index,))
            
        conn.commit()
        conn.close
        self.parent.displayFrame.displayArea.initialize_rows_list(self.selected_date)
        self.parent.displayFrame.displayArea.textInDisplayArea.set(self.parent.displayFrame.displayArea.create_string_from_sql_entries(self.parent.displayFrame.displayArea.make_readable_entries(self.parent.displayFrame.displayArea.rows_list)))
        self.parent.displayFrame.displayArea.delete('1.0',tk.END)
        self.parent.displayFrame.displayArea.insert('1.0',self.parent.displayFrame.displayArea.textInDisplayArea.get())
                      
class DisplayArea(tk.Text):
    """
    Display area for displaying information depending on what option is selected.
    """
    def __init__(self,parent):
        tk.Text.__init__(self, parent,
                           borderwidth = 3,
                           height = 50,
                         width = 120,
                         undo = True)
        self.parent = parent
        #Undo and redo numbers, don't perform if undo_number == redo_number
        self.undo_number = 0
        self.redo_number = 0
        top = self.winfo_toplevel()
        
        self.textInDisplayArea = tk.StringVar()
        rows_list = []
        self.rows_list = rows_list
        self.initialize_rows_list(datetime.date.today())
        self.textInDisplayArea.set(self.create_string_from_sql_entries(self.make_readable_entries(self.rows_list)))
          
    
    
    def initialize_rows_list(self,date):
        """
          Gets all the rows from the sql database to be put into the DisplayArea Text Widget, then makes a
          call to make_readable_entries with the new rows_list
        """
        self.rows_list = []
        conn = lite.connect('fit.db')
        cursor = conn.cursor()
        for row in cursor.execute('SELECT * FROM food_journal WHERE (date = ?) ORDER BY id', (date,)):
            self.rows_list.append(row)
        conn.close()
        self.reset_text_in_display_area()
    def reset_text_in_display_area(self):
        """
        Clears out text in display area widget and rewrites it with the new rows list
        """
        self.line_number = 1
        self.textInDisplayArea.set(self.create_string_from_sql_entries(self.make_readable_entries(self.rows_list)))
        self.delete('1.0',tk.END)
        self.insert('1.0',self.textInDisplayArea.get())
        
       
    def make_readable_entries(self,sql_rows_list):
        """
        Takes a list of SQL rows and makes a list of tuples with information added in to make it more readable.
        Excludes ID and Exercise ID.
        """
        conn = lite.connect('fit.db')
        cursor= conn.cursor()
        readable_entries_list = [[] for x in range(len(sql_rows_list))]
        for row_number in range(len(sql_rows_list)):
            readable_entries_list[row_number].append('id: '+ str(sql_rows_list[row_number][0]))
            readable_entries_list[row_number].append('Date: '+ str(sql_rows_list[row_number][1]))
            readable_entries_list[row_number].append('food_id: '+ str(sql_rows_list[row_number][2]))
            readable_entries_list[row_number].append('quantity: '+ str(sql_rows_list[row_number][3]))
            readable_entries_list[row_number].append('serving_size: '+ str(sql_rows_list[row_number][4]))
            readable_entries_list[row_number].append('serving_type: '+ str(sql_rows_list[row_number][5]))
        conn.close()
        return readable_entries_list

    def create_string_from_sql_entries(self, readable_list):
       """
       From a list of readable SQL entries, creates a single formatted string that can be added to a text object.
       """
       single_line_string_list = []
       one_list = []
       for row in readable_list:
              single_line_string_list.append(' '.join(row))
       
       for item in single_line_string_list:
              one_list.append(item)
       the_string = '\n'.join(one_list)
       
       return the_string
    
    
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
        
        self.displayArea = DisplayArea(self)
        self.displayArea.grid(row = 1, columnspan = 5) 
        

class ViewDietWindow(tk.Toplevel):
    """
    Toplevel window where user can view their eaten foods by day. 
    """
    def __init__(self, parent = None):
        tk.Toplevel.__init__(self, parent,
                             height = 600,
                             width = 600)
        self.menuFrame = MenuFrame(self)
        self.menuFrame.grid(column = 0, row = 0, sticky = tk.E+tk.W)
        self.menuFrame.columnconfigure(0,weight = 1)
        
        self.columnconfigure(0, weight = 1)
        
        self.dateLabel = DateLabel(self)
        self.dateLabel.grid(column = 0, row = 1)
        
        self.deleteRowFrame = DeleteRowFrame(self)
        self.deleteRowFrame.grid(column = 0, row = 2)
        
        self.displayFrame = DisplayFrame(self)
        self.displayFrame.grid(column = 0, row = 3)

        


        
        
