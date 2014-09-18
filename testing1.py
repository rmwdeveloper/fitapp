import numpy
import matplotlib as matplotlib
##import matplotlib.pyplot as pyplot
from pylab import *


import fitDatabase as fitdb
data_set = []
for row in fitdb.cursor.execute('''SELECT * FROM food_journal WHERE (date = ?)
                             ORDER BY id''', ('2014-02-11',)):
                          data_set.append(row)

one_day_food_journal= [(8, '2014-02-11', 6, 2.0, 1.0, 'cup'),
                       (9, '2014-02-11', 7, 1.0, 1.0, 'cup'),
                       (10, '2014-02-11', 8, 1.0, 1.0, 'cup')]
def get_carbs(data_set):
    total_carbs = 0
    for row in data_set:
        total_serving = row[3]*row[4]
        
        for q in fitdb.cursor.execute('''SELECT * FROM
                                               foods WHERE (id = ?)
                                              ORDER BY id''', (row[2],)):
            carbs = total_serving * q[9]
            total_carbs += carbs
    return total_carbs
def get_fat(data_set):
    total_fat = 0
    for row in data_set:
        total_serving = row[3]*row[4]
        
        for q in fitdb.cursor.execute('''SELECT * FROM
                                               foods WHERE (id = ?)
                                              ORDER BY id''', (row[2],)):
            fat = total_serving * q[8]
            total_fat += fat
    return total_fat
def get_protein(data_set):
    total_protein = 0
    for row in data_set:
        total_serving = row[3]*row[4]
        for q in fitdb.cursor.execute('''SELECT * FROM
                                               foods WHERE (id = ?)
                                              ORDER BY id''', (row[2],)):
            protein = total_serving * q[12]
            total_protein += protein
    return total_protein
def get_macros(data_set):
    return (get_protein(data_set),get_fat(data_set),get_carbs(data_set))

totals = get_macros(one_day_food_journal)
def get_percentages(totals):
    """
    Gets percentages of macros eaten. Always protein%,fat%,carbs%.
    """
    sum_of_totals = sum(totals)
    percentages = [round(totals[0]/float(sum_of_totals)*100,1),
                   round(totals[1]/float(sum_of_totals)*100,1),
                   round(totals[2]/float(sum_of_totals)*100,1)]
##    percentages =  (totals[0]/float(sum_of_totals),
##                   totals[1]/float(sum_of_totals),
##                   totals[2]/float(sum_of_totals))
    return percentages
percentages = get_percentages(totals)

#Make figure and axes aspect equal/square...
matplotlib.pyplot.figure(1,figsize=(6,6))
ax = matplotlib.pyplot.axes([0.1,0.1,0.8,0.8])
explode = (0,0.05,0)
#Make the Labels..
#Make the pie chart
##labels1 =((totals[0],str(percentages[0])+'%'),
##                      (totals[1],str(percentages[1]) +'%'),
##                      (totals[2],str(percentages[2])+'%'))
labels1 = 'protein','fat','carbs'
matplotlib.pyplot.pie(percentages,explode = explode, labels = labels1,
                      autopct = '%1.1f%%',startangle= 90)
title('Macronutrients for 2014-02-11',bbox = {'facecolor':'0.8','pad':5})
matplotlib.pyplot.show()
