import sqlite3 as lite
import inputEx as inex

#Table with all available exercises
exercise_name_list = ['Walking',
'Running',
'Swimming',
'Behind Neck Press',
'Upright Row',
'Shrugs',
'Overhead Press',
'Chinup',
'Seated Military Press',
'Front Squat',
'Calf Raise',
'Leg Press',
'Squat',
'Bench Press(Incline)(Barbell)',
'Bench Press(Decline)(Dumbbell)',
'Bench Press(Barbell)',
'Bench Press(Dumbbell)',
'Bench Press(Decline)(Barbell)',
'Bench Press(Incline)(Dumbbell)',
'Bent Over Row(Dumbbell)',
'Good Morning',
'Bent Over Row(Barbell)',
'Deadlift']

 #Creation of exercises table
def create_insert_list(exercise_name_list):
    exercises_and_ids = []
    id_number = 1
    for exercise_name in exercise_name_list:
        exercises_and_ids.append(( id_number, exercise_name,))
        id_number += 1
    return exercises_and_ids

id_and_exercise_list  = create_insert_list(exercise_name_list)    
conn = lite.connect('fit.db')
cursor= conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS exercises ( id int UNIQUE , name text)''')

cursor.executemany('INSERT OR IGNORE INTO exercises VALUES (?,?)',id_and_exercise_list)
cursor.execute('''CREATE TABLE IF NOT EXISTS events_weightlifting( id INTEGER PRIMARY KEY AUTOINCREMENT, visible_id int, date text, exercise_id int,
                  sets int, reps int, weight real)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS events_cardio( id INTEGER PRIMARY KEY AUTOINCREMENT, visible_id int, date text, exercise_id int,
                  distance real, distance_type text, time real)''')



#food table meant for individual ingredients and food, prepackaged prepared foods included 
cursor.execute('''CREATE TABLE IF NOT EXISTS foods (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, description text, serving_size real,
                  serving_size_type text, servings_per_container real, price real, calories real,fat real, carbs real, fiber real, sugars real,
                  protein real,to_display int)''')
#food_journal table for recording what is eaten in a particular day
cursor.execute('''CREATE TABLE IF NOT EXISTS food_journal (id INTEGER PRIMARY KEY AUTOINCREMENT, date text, food_id int, quantity real,
               serving_size real, serving_type text)''')
#meals table for prepared meals
cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, description text, servings int,to_display int)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS recipe_ingredient_listing (id INTEGER PRIMARY KEY AUTOINCREMENT, recipe_id int, foods_id int,
                  quantity real, serving_size real, serving_type text)''') 
conn.commit()
cursor.execute('''CREATE TABLE IF NOT EXISTS personal_info (id INTEGER PRIMARY KEY AUTOINCREMENT, date text,height int,weight int, age int,gender text,activity_level text,body_fat real, waist int)''') 
conn.commit()



