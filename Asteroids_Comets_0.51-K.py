#!/usr/bin/python3
'''#----------------------------------------------------------------------
Name:        Asteroids_Comets.py
 Purpose:     To display current Asteroid/Comet Information
             

Author:      John Duchek

Created:     Nov, 2007
Last Updated: August 25, 2017

Copyright: in the public domain
Version 0.51
converted to tkinter
placed in the public domain

Version 0.50 - several asteroid pages
adding NEO and Trans observable.
Version       0.44
44 corrects comet and asteroid http. Note the bright asteroids have 2011 in name and will need to be changed yearly
.43 displays brightest to dimmest, and gives all the info in grid style (no clicking)
.42 displays current magnitude in list.
.40provides user adjustable date
.35 provides automatic data updates

----------------------------------------------------------------------
 http://www.minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt - comets
 http://www.minorplanetcenter.net/iau/Ephemerides/Bright/2011/Soft03Bright.txt - bright asteroids
 http://www.minorplanetcenter.net/iau/Ephemerides/CritList/Soft03CritList.txt  - observable critical list numbered minor planets
 http://www.minorplanetcenter.net/iau/Ephemerides/Distant/Soft03Distant.txt - observable distant minor planets (including Centaurs & Transneptuniasns)
 http://www.minorplanetcenter.net/iau/Ephemerides/Unusual/Soft03Unusual.txt - unusual minor planets (including NEOs)
'''

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from ephem import *
import urllib.request
version = 0.50


john=Observer()

#---------------SITES------comment out those not in use-------
my_site="Karamar"
john.long, john.lat ,john.elev = '-90.379025','38.47362',147.9
#-------------------------------------------------------------
#my_site="Carrizozo"
#john.long,john.lat,john.elev='-105.77175','33.60763',1849
#---------------Common Variables------------------------------
john_timezone=-6
john.temp=15 #deg C
john.pressure=1010 #mB
local = localtime(john.date)
#------------------------------
urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt', 'Soft03Cmt.txt')
urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/Ephemerides/Bright/2011/Soft03Bright.txt', 'Soft03Bright.txt')
urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/Ephemerides/CritList/Soft03CritList.txt', 'Soft03CritList.txt')
urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/Ephemerides/Distant/Soft03Distant.txt ', 'Soft03Distant.txt')
urllib.request.urlretrieve('http://www.minorplanetcenter.net/iau/Ephemerides/Unusual/Soft03Unusual.txt', 'Soft03Unusual.txt')

#---------------------make a window-------------------------
win=tk.Tk()
win.title("Asteroids & Comets "+" at "+my_site+", "+str(localtime(john.date))[0:10])
#win.resizable(False, False) #force window to remain at one size
#-----------------------------------------------------
john.date=now()
tabControl=ttk.Notebook(win)
site=ttk.Frame(tabControl)
bright_a=ttk.Frame(tabControl)
critical_a=ttk.Frame(tabControl)
distant_a=ttk.Frame(tabControl)
unusual_a=ttk.Frame(tabControl)
comets=ttk.Frame(tabControl)

tabControl.add(site,text='Site Info')
site_info=ttk.LabelFrame(site,text="Site Info")
site_info.grid(column=0,row=0,padx=8,pady=8)

tabControl.add(bright_a,text='Bright A')
tabControl.add(critical_a,text='Critical A')
tabControl.add(distant_a,text='Distant A')
tabControl.add(unusual_a,text='Unusual A')
tabControl.add(comets,text='Comets')
#tabControl.select(2) #Choose which tab you want to come up as default (1->6)

brighta=ttk.Treeview(bright_a)
criticala=ttk.Treeview(critical_a)
distanta=ttk.Treeview(distant_a)
unusuala=ttk.Treeview(unusual_a)
comet=ttk.Treeview(comets)
tabControl.pack(expand=1,fill="both")
def partition(theList, start, end,name,ra,dec,Constellation,altitude):

    pivot = theList[end]    
    pivot1=name[end]
    pivot2=ra[end]
    pivot3=dec[end]
    pivot4=Constellation[end]
    pivot5=altitude[end]
            
            
            
            # place the pivot at the end
    bottom = start-1                         # begin "outside"                           
    top = end                                # place other side for partitioning                            

    done = 0
    while not done:                             # begin                    
        while not done:                        
            bottom = bottom + 1                   

            if bottom == top:                   # has we reached the end?       
                done = 1                        # if so, exit!    
                break
            if theList[bottom] > pivot:         # move values '>' "above"
                theList[top] = theList[bottom]
                name[top]=name[bottom]
                ra[top]=ra[bottom]
                dec[top]=dec[bottom]
                Constellation[top]=Constellation[bottom]
                altitude[top]=altitude[bottom]
                
                break
            
        while not done:                        
            top = top-1                        
            
            if top == bottom:                   # if end is reached, exit!        
                done = 1                       
                break
            if theList[top] < pivot:            # do the opposite of the above      
                theList[bottom] = theList[top]  # '<' are moved "below" 
                name[bottom]=name[top]
                ra[bottom]=ra[top]
                dec[bottom]=dec[top]
                Constellation[bottom]=Constellation[top]
                altitude[bottom]=altitude[top]
                                
                break                          

    theList[top] = pivot 
    name[top]=pivot1
    ra[top]=pivot2
    dec[top]=pivot3
    Constellation[top]=pivot4
    altitude[top]=pivot5
    
    
    return top  
def quicksort(theList, start, end,name,ra,dec,Constellation,altitude):
    if start < end:                             # verifies the list is not empty
        split = partition(theList, start, end,name,ra,dec,Constellation,altitude)      # partition the sublist
        quicksort(theList, start, split-1,name,ra,dec,Constellation,altitude)          # sort both halves.
        quicksort(theList, split+1, end,name,ra,dec,Constellation,altitude)            # recursion 
    else:
        return
#------------------site info -----------------------
john.date=now()
col=0
row=0
ttk.Label(site,text="Site : "+my_site).grid(column=0,row=0,sticky=tk.W,padx=5,pady=0)
ttk.Label(site,text="Date : "+str(localtime(john.date))[0:10]).grid(column=col,row=row+2,sticky=tk.W,padx=5,pady=0)
ttk.Label(site,text="Sidereal Time :  "+str(john.sidereal_time())).grid(column=col,row=row+3,sticky=tk.W,padx=5,pady=0)
ttk.Label(site,text="Local Time :  "+str(localtime(john.date)).split()[1][:10]).grid(column=col,row=row+4,sticky=tk.W,padx=5,pady=0)
ttk.Label(site,text="Universal Time :  "+str(john.date).split()[1][:10]).grid(column=col,row=row+5,sticky=tk.W,padx=5,pady=0)
ttk.Label(site,text="Version :  "+str(version)).grid(column=col,row=row+7,sticky=tk.W,padx=5,pady=0)
col=1
row=0
ttk.Label(site,text="Latitude : "+str(john.lat)).grid(column=col,row=row,sticky=tk.W,padx=5,pady=0)
ttk.Label(site,text="Longitude : "+str(john.long)).grid(column=col,row=row+1,sticky=tk.W,padx=5,pady=0)
ttk.Label(site,text="Elevation : "+str(john.elev)+ " M").grid(column=col,row=row+2,sticky=tk.W,padx=5,pady=0)
#-------------------Bright Asteroids---------------------------
brighta["columns"]=("one","two","three","four","five","six")
brighta['show']='headings' # remove left column
brighta.column("one",width=150)

brighta.column("two",width=120)
brighta.column("three",width=120)
brighta.column("four",width=120)
brighta.column("five",width=120)
brighta.column("six",width=120)

brighta.heading("one", text="Name")
brighta.heading("two", text="Magnitude" )
brighta.heading("three", text="Right Ascension")
brighta.heading("four", text="Declination")
brighta.heading("five", text="Constellation")
brighta.heading("six", text="Altitude")

f=open("Soft03Bright.txt",'r')
name=[0]
mag=[0]
ra=[0]
dec=[0]
Constellation=[0]
altitude=[0]

while True:
            line=f.readline()
            if len(line)==0: #length 0 indicates EOF
                break
            if line[0:6]!='# From': #removes alternate lines
                #grid.AppendRows(numRows=1)
                asteroid=readdb(line)
                
                asteroid.compute(john)
                name.append(asteroid.name)
                mag.append(asteroid.mag)
                ra.append(asteroid.ra)
                dec.append(asteroid.dec)
                Constellation.append(constellation(asteroid)[1])
                altitude.append(asteroid.alt) 
quicksort(mag,0,len(mag)-1,name,ra,dec,Constellation,altitude) 

for item in range (1,len(mag)): 
    brighta.insert("" , item, values=(str(name[item]),str(mag[item]),str(ra[item])[0:12],
    str(dec[item])[0:12],Constellation[item],str(altitude[item])[0:2]))

brighta.pack()


#-------------------Critical Asteroids--------------------------
criticala["columns"]=("one","two","three","four","five","six")
criticala['show']='headings' # remove left column
criticala.column("one",width=150)

criticala.column("two",width=120)
criticala.column("three",width=120)
criticala.column("four",width=120)
criticala.column("five",width=120)
criticala.column("six",width=120)

criticala.heading("one", text="Name")
criticala.heading("two", text="Magnitude" )
criticala.heading("three", text="Right Ascension")
criticala.heading("four", text="Declination")
criticala.heading("five", text="Constellation")
criticala.heading("six", text="Altitude")

f=open("Soft03CritList.txt",'r')
name=[0]
mag=[0]
ra=[0]
dec=[0]
Constellation=[0]
altitude=[0]

while True:
            line=f.readline()
            if len(line)==0: #length 0 indicates EOF
                break
            if line[0:6]!='# From': #removes alternate lines
                #grid.AppendRows(numRows=1)
                asteroid=readdb(line)
                
                asteroid.compute(john)
                name.append(asteroid.name)
                mag.append(asteroid.mag)
                ra.append(asteroid.ra)
                dec.append(asteroid.dec)
                Constellation.append(constellation(asteroid)[1])
                altitude.append(asteroid.alt) 
quicksort(mag,0,len(mag)-1,name,ra,dec,Constellation,altitude) 

for item in range (1,len(mag)): 
    criticala.insert("" , item, values=(str(name[item]),str(mag[item]),str(ra[item])[0:12],
    str(dec[item])[0:12],Constellation[item],str(altitude[item])[0:2]))

criticala.pack()

#-------------------Unusual Asteroids---------------------------
unusuala["columns"]=("one","two","three","four","five","six")
unusuala['show']='headings' # remove left column
unusuala.column("one",width=150)

unusuala.column("two",width=120)
unusuala.column("three",width=120)
unusuala.column("four",width=120)
unusuala.column("five",width=120)
unusuala.column("six",width=120)

unusuala.heading("one", text="Name")
unusuala.heading("two", text="Magnitude" )
unusuala.heading("three", text="Right Ascension")
unusuala.heading("four", text="Declination")
unusuala.heading("five", text="Constellation")
unusuala.heading("six", text="Altitude")

f=open("Soft03Unusual.txt",'r')
name=[0]
mag=[0]
ra=[0]
dec=[0]
Constellation=[0]
altitude=[0]

while True:
            line=f.readline()
            if len(line)==0: #length 0 indicates EOF
                break
            if line[0:6]!='# From': #removes alternate lines
                #grid.AppendRows(numRows=1)
                asteroid=readdb(line)
                
                asteroid.compute(john)
                name.append(asteroid.name)
                mag.append(asteroid.mag)
                ra.append(asteroid.ra)
                dec.append(asteroid.dec)
                Constellation.append(constellation(asteroid)[1])
                altitude.append(asteroid.alt) 
quicksort(mag,0,len(mag)-1,name,ra,dec,Constellation,altitude) 

for item in range (1,len(mag)): 
    unusuala.insert("" , item, values=(str(name[item]),str(mag[item]),str(ra[item])[0:12],
    str(dec[item])[0:12],Constellation[item],str(altitude[item])[0:2]))

unusuala.pack()


#-------------------Distant Asteroids---------------------------
distanta["columns"]=("one","two","three","four","five","six")
distanta['show']='headings' # remove left column
distanta.column("one",width=150)

distanta.column("two",width=120)
distanta.column("three",width=120)
distanta.column("four",width=120)
distanta.column("five",width=120)
distanta.column("six",width=120)

distanta.heading("one", text="Name")
distanta.heading("two", text="Magnitude" )
distanta.heading("three", text="Right Ascension")
distanta.heading("four", text="Declination")
distanta.heading("five", text="Constellation")
distanta.heading("six", text="Altitude")

f=open("Soft03Distant.txt",'r')
name=[0]
mag=[0]
ra=[0]
dec=[0]
Constellation=[0]
altitude=[0]

while True:
            line=f.readline()
            if len(line)==0: #length 0 indicates EOF
                break
            if line[0:6]!='# From': #removes alternate lines
                #grid.AppendRows(numRows=1)
                asteroid=readdb(line)
                
                asteroid.compute(john)
                name.append(asteroid.name)
                mag.append(asteroid.mag)
                ra.append(asteroid.ra)
                dec.append(asteroid.dec)
                Constellation.append(constellation(asteroid)[1])
                altitude.append(asteroid.alt) 
quicksort(mag,0,len(mag)-1,name,ra,dec,Constellation,altitude) 

for item in range (1,len(mag)): 
    distanta.insert("" , item, values=(str(name[item]),str(mag[item]),str(ra[item])[0:12],
    str(dec[item])[0:12],Constellation[item],str(altitude[item])[0:2]))

distanta.pack()


#-------------------Comets--------------------------------------
comet["columns"]=("one","two","three","four","five","six")
comet['show']='headings' # remove left column
comet.column("one",width=150)

comet.column("two",width=120)
comet.column("three",width=120)
comet.column("four",width=120)
comet.column("five",width=120)
comet.column("six",width=120)

comet.heading("one", text="Name")
comet.heading("two", text="Magnitude" )
comet.heading("three", text="Right Ascension")
comet.heading("four", text="Declination")
comet.heading("five", text="Constellation")
comet.heading("six", text="Altitude")

f=open("Soft03Cmt.txt",'r')
name=[0]
mag=[0]
ra=[0]
dec=[0]
Constellation=[0]
altitude=[0]

while True:
            line=f.readline()
            if len(line)==0: #length 0 indicates EOF
                break
            if line[0:6]!='# From': #removes alternate lines
                #grid.AppendRows(numRows=1)
                asteroid=readdb(line)
                
                asteroid.compute(john)
                name.append(asteroid.name)
                mag.append(asteroid.mag)
                ra.append(asteroid.ra)
                dec.append(asteroid.dec)
                Constellation.append(constellation(asteroid)[1])
                altitude.append(asteroid.alt) 
quicksort(mag,0,len(mag)-1,name,ra,dec,Constellation,altitude) 

for item in range (1,len(mag)): 
    comet.insert("" , item, values=(str(name[item]),str(mag[item]),str(ra[item])[0:12],
    str(dec[item])[0:12],Constellation[item],str(altitude[item])[0:2]))

comet.pack()

def quicksort(theList, start, end,name,ra,dec,Constellation,altitude):
    if start < end:                             # verifies the list is not empty
        split = partition(theList, start, end,name,ra,dec,Constellation,altitude)      # partition the sublist
        quicksort(theList, start, split-1,name,ra,dec,Constellation,altitude)          # sort both halves.
        quicksort(theList, split+1, end,name,ra,dec,Constellation,altitude)            # recursion 
    else:
        return



if __name__ == "__main__":
    win.mainloop()  
