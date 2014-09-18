import numpy
import matplotlib
import matplotlib.pyplot as plt
import fitDatabase as fitdb

def get_single_date(date):
    """
    Gets all food journal information from a single date.
    Date is in the format 'year-mo-da'. 
    """
    data_set = []
    for row in fitdb.cursor.execute('''SELECT * FROM food_journal WHERE (date = ?)
                                 ORDER BY id''', (date,)):
                              data_set.append(row)
    return data_set
def get_date_span(starting_date,ending_date):
    """
    Gets all food journal information from a single date inclusive. 
    """
    data_set = []
    for row in fitdb.cursor.execute('''SELECT * FROM food_journal WHERE date
                                       BETWEEN ? AND ?''',(starting_date,ending_date)):
        data_set.append(row)
    return data_set

t0 = get_date_span('2014-02-11','2014-02-11')              
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


def get_percentages(totals):
    """
    Gets percentages of macros eaten. Always protein%,fat%,carbs%.
    """
    sum_of_totals = sum(totals)
    percentages = [round(totals[0]/float(sum_of_totals)*100,1),
                   round(totals[1]/float(sum_of_totals)*100,1),
                   round(totals[2]/float(sum_of_totals)*100,1)]

    return percentages

def macronutrient_pie_chart(start,end= None):
    """
    Makes a macronutrient pie chart. Just having a start time makes a chart
    for a single day, including and end time makes it for a span of time. """
##    plt.figure(figsize = (6,6))
##    ax = plt.axes([0.1,0.1,0.8,0.8])
    labels = 'protein','fat','carbs'

    if end == None:
        percentages = get_percentages(get_macros(get_single_date(start)))
        title = ('Macronutrients for ' + start)
    else:
        percentages = get_percentages(get_macros(get_date_span(start,end)))
        title = ('Macronutrients for '+start+' through '+end)
    return plt.pie(percentages,labels = labels,autopct = '%1.1f%%',startangle = 90)
##    plt.title(title,bbox = {'facecolor':'0.8','pad':5})
    

##macronutrient_pie_chart('2014-02-09','2014-02-11')
    
