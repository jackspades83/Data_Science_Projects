import os
import pandas as pd
import pickle
import tkinter as tk
from tkinter import *
from tkinter import ttk
import math

# Load the Df_tel file snapshot
df_tel = pd.read_csv("df_tel.csv")

# Change SeniorCitizen to object type for symmetry
df_tel.loc[:, "SeniorCitizen"] = df_tel.loc[:, "SeniorCitizen"].astype('object', errors='ignore').astype('object', errors='ignore')

# Load X_train file
X_train = pd.read_csv("X_train.csv")

# Creating a function which runs on Predict button left click event
def get_data(event):
    
    # Freeze button while get_data function is being executed
    predict["state"] = DISABLED
    
    # Define global variables since these will be needed in the main script as well
    global df_gui
    global pred_data
    
    # Initialising an empty dictionary for pred_data
    pred_data={}
    # Initialising a counter to go through all combo buttons
    idx=0
    
    # A loop to collect all categorical data given by user
    for col in list(df_tel.select_dtypes(include=['object']).columns)[:-1]:
        pred_data[str(col+'_'+cb[idx].get())] = 1
        idx+=1
    
    # Initialising a counter to go through all slider inputs
    idx=0
    
    # A loop to collect all continous data given by user
    for col in list(df_tel.select_dtypes(include=['int64', 'float64']).columns):
        pred_data[col] = slider[idx].get()
        idx+=1
    
    # Create and organise data in the form of X_test or how model has learnt to recieve data
    df_gui = pd.DataFrame(columns=X_train.columns)
    df_gui = pd.concat([df_gui, pd.DataFrame(pred_data, index=range(1))], axis=0).loc[:, X_train.columns].fillna(0)
    
    # Predict and convert output to No or Yes
    pred = 'No' if pickle_clf.predict(df_gui)==0 else 'Yes'
    
    # Paste prediction in textbox
    result['state']=NORMAL
    result.delete(0.0, 'end')
    result.insert(0.0, pred)
    result['state']=DISABLED
    
    # Unfreeze Predict button
    predict['state']=NORMAL
    
    return()

    # Load Pickle file if not loaded
if os.path.getsize('XGBBoost.pickle') > 0:
    # Load the Pickle file in the memory
    pickle_in = open('XGBBoost.pickle', 'rb')
    pickle_clf = pickle.load(pickle_in)

# Create Tkinter GUI window
window = tk.Tk()
var = tk.StringVar()

# Initialise position values and combobox list
x=10
y = 50
cb=[]

# Place the Combobox widgets based on all categorical data
for col in list(df_tel.select_dtypes(include=['object']).columns)[:-1]:
    ls_col = df_tel[col].unique()
    
    # Label
    txt = ttk.Label(window, text = "Select the "+col+" :", font = ("Times New Roman", 10))
    data = tuple(ls_col)
    cb.append(tk.ttk.Combobox(window, values=data))
    txt.place(x=x, y=y-22)
    cb[-1].place(x=x, y=y)
    if x+200<400:
        x+=200
    else:
        x=10
        y+=70
    cb[-1].current(0)

# Reinitialise position values and slider list
x=410
y=50
slider = []

# Place the Slider widgets based on all continous data
for col in list(df_tel.select_dtypes(include=['int64', 'float64']).columns)[:-1]:
    
    txt = ttk.Label(window, text = "Select the "+col+" :", font = ("Times New Roman", 10))
    txt.place(x=x, y=y-22)
    
    to = math.ceil(df_tel[col].max()/10)*10
    tickinterval = (to - 0)/10
    slider.append(Scale(window, from_=0, to=to, tickinterval=to/(to/10), length=230))
    slider[-1].set(round(df_tel[col].mean()/10)*10)
    slider[-1].place(x=x, y=y)
    y+=270

# Creating TotalCharges Slider outside loop to give it different settings
col = list(df_tel.select_dtypes(include=['int64', 'float64']).columns)[-1]
y=50

# Creating Text label
txt = ttk.Label(window, text = "Select the "+col+" :", font = ("Times New Roman", 10))
txt.place(x=x+200, y=y-22)

to = math.ceil(df_tel[col].max()/10)*10
tickinterval = (to - 0)/10

# Creating SLider
slider.append(Scale(window, from_=0, to=to, tickinterval=to/(to/10), length=500))
slider[-1].set(round(df_tel[col].mean()/10)*10)
slider[-1].place(x=x+200, y=y)

# Create and place results textbox
txt = ttk.Label(window, text = "Will the Customer Churn?", font = ("Times New Roman", 10))
txt.place(x=270, y=600)
result = Text(window, width=5, height=1, state=DISABLED)
result.place(x=420, y=600)

# Create, bind and place Predict Button
predict = ttk.Button(window, text="Predict")
predict.bind('<Button-1>', get_data)
predict.place(x=150, y=600)

# Create and place Close Button
close = ttk.Button(window, text="Close", command=window.destroy)
# close.bind('<Button-1>', close_window)
close.place(x=500,y=600)

# Set Window level parameters
window.title("Telcom Customer Churn Results Toolkit")
window.geometry("780x650+10+10")
window.lift()
mainloop()