#############################################################################
## The following code utilizes data from StatsBomb Open Data repository on ##
## GitHub to create charts and heat maps of soccer passing, dribbling, and ## 
## shot data for players on FC Barcelona in La Liga                        ##
## Code for creating the pitch and charts is adapted from                  ##
## code written by Tuan Doan Nguyen on Towards Data Science                ##  
#############################################################################
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas

def draw_pitch(ax):
    #Pitch Outline & Centre Line
    Pitch = Rectangle([0,0], width = 120, height = 80, fill = False)

    #Left, Right Penalty Area and Midline
    LeftPenalty = Rectangle([0,22.3], width = 14.6, height = 35.3, fill = False)
    RightPenalty = Rectangle([105.4,22.3], width = 14.6, height = 35.3, fill = False)
    midline = ConnectionPatch([60,0], [60,80], "data", "data")

    #Left, Right 6-yard Box
    LeftSixYard = Rectangle([0,32], width = 4.9, height = 16, fill = False)
    RightSixYard = Rectangle([115.1,32], width = 4.9, height = 16, fill = False)

    #Prepare Circles
    centreCircle = plt.Circle((60,40),8.1,color="black", fill = False)
    centreSpot = plt.Circle((60,40),0.71,color="black")
    
    #Penalty spots and Arcs around penalty boxes
    leftPenSpot = plt.Circle((9.7,40),0.71,color="black")
    rightPenSpot = plt.Circle((110.3,40),0.71,color="black")
    leftArc = Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")
    
    element = [Pitch, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle, 
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    
    for i in element: ax.add_patch(i)

def show_heat(df, title):
    fig = plt.figure()
    fig.set_size_inches(7, 5)    
    ax = fig.add_subplot(1,1,1)
    draw_pitch(ax)
    
    plt.ylim(-2, 82)
    plt.xlim(-2, 122)
    plt.axis('off')
        
    sns.kdeplot(df.location_x, df.location_y, shade = 'True', color = 'green', n_levels = 10)        
    fig.suptitle('Heat Map of ' + title, fontsize=16)

    plt.show()

def show_chart(df, title):
    fig = plt.figure()
    fig.set_size_inches(7, 5)
    ax = fig.add_subplot(1,1,1)
    draw_pitch(ax)
    
    plt.ylim(-2, 82)
    plt.xlim(-2, 122)
    plt.axis('off')
        
    plt.scatter(df.location_x, df.location_y, c = 'green')
    fig.suptitle('Chart of ' + title, fontsize=16)

    plt.show()
        
def format_shots():
    #load and format shot data
    df = pandas.ExcelFile('C:/Users/Gautam Goel/shot_data.xlsx')
    df.sheet_names
    
    data = df.parse('Sheet1')
    list = data.values.tolist()
    
    goals, shots = [], []
    for row in list:
        if row[1] == 'Goal': goals.append(row[2:])
        else: shots.append(row[2:])
    
    return [goals, shots]

def format_passes():
    #load and format pass data (received)
    df1 = pandas.ExcelFile('C:/Users/Gautam Goel/pass_received.xlsx')
    df1.sheet_names
    
    data1 = df1.parse('Sheet1')
    list1 = data1.values.tolist()
    
    received = []
    for row in list1:
        if str(row[21]) == 'nan' and str(row[22]) == 'nan': received.append(row[-2:])
    
    #load and format pass data (made)
    df2 = pandas.ExcelFile('C:/Users/Gautam Goel/pass_made.xlsx')
    df2.sheet_names
    
    data2 = df2.parse('Sheet1')
    list2 = data2.values.tolist()
    
    made = []
    for row in list2:
        if str(row[21]) == 'nan' and str(row[22]) == 'nan': made.append(row[-2:])
    
    return [received, made]

def format_dribbles():
    #load and format shot data
    df = pandas.ExcelFile('C:/Users/Gautam Goel/dribble_data.xlsx')
    df.sheet_names
    
    data = df.parse('Sheet1')
    list = data.values.tolist()
    
    complete, incomplete = [], []
    for row in list:
        if row[1] == 'Complete': complete.append(row[2:])
        if row[1] == 'Incomplete': incomplete.append(row[2:])
    
    return [complete, incomplete]

def main():    
    categories = ['location_x', 'location_y']
    
    goals, shots = format_shots()
    df_goals = pandas.DataFrame(goals, columns = categories)
    df_shots = pandas.DataFrame(shots, columns = categories)
    
    received, made = format_passes()
    df_received = pandas.DataFrame(received, columns = categories)
    df_made = pandas.DataFrame(made, columns = categories)

    complete, incomplete = format_dribbles()
    df_complete = pandas.DataFrame(complete, columns = categories)
    df_incomplete = pandas.DataFrame(incomplete, columns = categories)

    #creates visuals for goals scored
    show_heat(df_goals, 'Goals Scored')
    #show_chart(df_goals, 'Goals Scored')
    
    #creates visuals for shots taken
    show_heat(df_shots, 'Shots Taken')
    #show_chart(df_shots, 'Shots Taken')
    
    #creates visuals for passes received
    show_heat(df_received, 'Passes Received')
    #show_chart(df_received, 'Passes Received')
    
    #creates visuals for passes made
    show_heat(df_made, 'Passes Made')
    #show_chart(df_made, 'Passes Made')
         
    #creates visuals for complete dribbles
    show_heat(df_complete, 'Dribbles Completed')
    #show_chart(df_complete, 'Dribbles Completed')
    
    #creates visuals for incomplete dribbles
    show_heat(df_incomplete, 'Dribbles Incompleted')
    #show_chart(df_incomplete, 'Dribbles Incompleted')
        
main()