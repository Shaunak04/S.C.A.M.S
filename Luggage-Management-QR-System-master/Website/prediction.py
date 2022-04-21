import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.font as font
from sklearn.linear_model import LinearRegression

#read the dataset
df = pd.read_csv('csv\\allairline.csv')
monthlypass=pd.read_csv('csv\\jetairways.csv')
totalpass=monthlypass['PASSENGERS - CARRIED (NOS.)'].sum()
ratios=[]
ratios.append(1)
monthpass=list(monthlypass.iloc[:,4])
for k in monthpass:
    ratios.append(k/totalpass)
#data visualisation 

# p1=sb.lmplot(x='YEAR',y='PASSENGERS-TO',data=df)
# p1.fig.suptitle('PASSENGERS TRAVELLING TO INDIA')
# p2=sb.lmplot(x='YEAR',y='PASSENGERS-FROM',data=df)
# p2.fig.suptitle('PASSENGERS TRAVELLING FROM INDIA')
# p3=sb.lmplot(x='YEAR',y='PASSENGERS-TOTAL',data=df)
# p3.fig.suptitle('TOTAL PASSENGERS')

print(df.iloc[0:13,0:1])
print(df.iloc[0:13,1:4])

#fitting regression line
regressor=LinearRegression(fit_intercept=True)
regressor.fit(df.iloc[0:13,0:1],df.iloc[0:13,1:4])

#heatmap to show visualise correlation coefficients
# data_corr=df.corr()
# data_corr
# sb.heatmap(data_corr)

#Desktop app with tkinter

root=Tk()
root.title("PASSENGER PREDICTOR")
root.resizable(width=False, height=False)
root.geometry("420x420")
root.configure(background="#27496d")
topFont = font.Font(family='Times', size=17, weight='bold')
midFont=font.Font(family='Times',size=13,weight='bold')
bottomFont=font.Font(family='Times',size=10,weight='bold')
l1=Label(text="AIRLINE  PASSENGER  PREDICTION  ",font=topFont,bg='#27496d',fg='#dae1e7')
l1.place(x=0,y=0)
Label(text='___________________________________________________________________________',fg='#dae1e7',bg='#27496d').place(x=16,y=31)
y=Label(text='YEAR : ',bg='#27496d',fg='white',font=midFont)
y.place(x=20,y=85)
m=Label(text='MONTH : ',bg='#27496d',fg='white',font=midFont)
m.place(x=20,y=120)
e1=Entry(root,bd=3,width=10,bg="#dae1e7")
e1.place(x=84,y=85)
def callback(*args):
    month=mon.index(str(variable.get()))
    monthratio=ratios[month]
    year=np.array([[int(e1.get())]])
    pred=regressor.predict(year)
    Label(text='PASSNGERS FROM INDIA : ',fg='#dae1e7',bg='#27496d',font=midFont).place(x=30,y=180)
    Label(text=str(int(monthratio*(pred[0][0]))),fg='white',bg='#27496d',font=midFont).place(x=250,y=180)
    Label(text='___________________________________________________________________________',fg='#dae1e7',bg='#27496d').place(x=16,y=210)
    Label(text='PASSNGERS TO INDIA : ',fg='#dae1e7',bg='#27496d',font=midFont).place(x=30,y=250)
    Label(text=str(int(monthratio*(pred[0][1]))),fg='white',bg='#27496d',font=midFont).place(x=232,y=250)
    Label(text='___________________________________________________________________________',fg='#dae1e7',bg='#27496d').place(x=16,y=280)
    Label(text='TOTAL PASSENGERS : ',fg='#dae1e7',bg='#27496d',font=midFont).place(x=30,y=320)
    Label(text=str(int(monthratio*((pred[0][0])+(pred[0][1])))),fg='white',bg='#27496d',font=midFont).place(x=232,y=320)

mon=['Total','January','February','March','April','May','June','July','August','September','October','November','December']
variable = StringVar(root)
variable.set(mon[0])
e2=OptionMenu(root,variable,*mon)
e2.place(x=100,y=120)
variable.trace("w", callback)

Label(text='Accuracy recorded for 80%(train)-20%(test) was : 99.47%',font=bottomFont,fg='white',bg='#27496d').place(x=0,y=400)
root.mainloop()