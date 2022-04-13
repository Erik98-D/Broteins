#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from datetime import datetime
import time
import pandas as pd



class Compear():
    def __init__(self,string1,string2):
        self.str1 = string1.get().upper()
        self.str2 = string2.get().upper()
        self.minnumber = 3 #give by Lorenso
        self.strsplit = []
        
        #Assuming heare everithing is alphabet letters only
        
        #dictionary definition
        """ migth be not good since we need to change the code a lot for this 
            but can be use to split the short string instead that the 1st 
        if len(self.str1)<len(self.str2):
            print("str2 bigger...")
            for i in range(len(self.str1)-self.minnumber):
                self.strsplit.append(self.str1[i:i+self.minnumber])
        else:
            print("str1 is bigger or same size...")
            for i in range(len(self.str2)-self.minnumber):
                self.strsplit.append(self.str2[i:i+self.minnumber])
        """
        #split 1st string in the minnumber (3) exmp in "ABCD" 
        # out "ABC" and "BCD"
        for i in range(len(self.str1)-self.minnumber+1):
            self.strsplit.append(self.str1[i:i+self.minnumber])
            
        r=0
        df=pd.DataFrame(columns=["Match","Iidx", "Fidx","Origiidx","Origfidx"])
        
        #here we find all the exact matches and we save them to a df
        for i in range(len( self.strsplit)):
            while(r<len(self.str2)-self.minnumber and r!=-1):
                r=self.str2.find(self.strsplit[i],r)
                if r != -1:
                    df=df.append({"Match":self.strsplit[i],
                    "Iidx":r,"Fidx":r+self.minnumber-1,"Origiidx":i,"Origfidx":i+self.minnumber-1},ignore_index=True)
                    r+=1

            r=0
        print("Untill heart the df hass all the 3 exact matches")
        self.df=df
        print(df)
        
        
    def extend_final_idx(self):
        for i in range(self.df.shape[0]):
            iidx=self.df.iloc[i][1]
            fidx=self.df.iloc[i][2] #final index location
            oidx=self.df.iloc[i][3]
            ad=self.minnumber
            #sumand=0
            f=(oidx+1)+ad #add one to companeste chacking
            g=(fidx+2)
            while(f<len(self.str1)):
                
                if(self.str1[oidx:f]==self.str2[iidx:g]):
                    self.df.loc[i,"Fidx"]=g-1
                    self.df.loc[i,"Origfidx"]=f-1
                    self.df.loc[i,"Match"]=self.str1[oidx:f]
                    f+=1
                    if g<len(self.str2):
                        g+=1
                else:
                    break
            
        print("Matches with extended index are:")
        print(self.df)
    def extend_initial_idx(self):
        return self.str1


# In[2]:


class GUI():
    def __init__(self):
        """
        GUI is a class that creat the user interface to compate two strings
        
         Attributes:
        -----------
        None

        Methods:
        --------
        Constructor will crate the gui and the following methods will help to set info and generete outputs
            defname()
            manualname()
            mesagefinish()
            cleanscrean()
            proteincompare()
            chektext()
            startgui()
            printinfo()

        
        
        
        """
        
        
        #initialise window
        self.window=Tk()
        self.window.geometry("1000x650") 
        
        #set up labels 
        l1=Label(self.window,text="String 1:")
        l2=Label(self.window,text="String 2:")
        l3=Label(self.window,text="Output Name:")
        #place lables 
        l1.place(x=20,y=125)
        l2.place(x=20,y=350)
        l3.place(x=20,y=550)
        
        #define entrys 
        #Entery text boxes
        self.String1=StringVar()
        self.e1=Entry(self.window,textvariable=self.String1)
        self.e1.place(x=100,y=50,width=800,height=200)
        self.String2=StringVar()
        self.e2=Entry(self.window,textvariable=self.String2)
        self.e2.place(x=100,y=275,width=800,height=200)
        self.outText=StringVar()
        self.e3=Entry(self.window,textvariable=self.outText)
        self.e3.place(x=100,y=550,width=400,height=25)

        ##defauld output name 
        self.name=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"_output"
        
        
        # Output Name set up 
        self.v = IntVar()
        self.v.set(1) #Def name option selected by default
        l4=Label(self.window, text="Output Name")
        l4.place(x=550,y=500)
        
        #Radiobuttons
        self.R1 = Radiobutton(self.window, text="Default name", variable=self.v, value=1,command=self.defname)
        self.R1.place(x=550,y=525)
        self.R2 = Radiobutton(self.window, text="Manual name", variable=self.v, value=2,command=self.manualname)
        self.R2.place(x=550,y=550)
        
        #progress bar
        self.bar=Progressbar(self.window,orient=HORIZONTAL,length=300)
        self.bar.place(x=200,y=500)
        l4=Label(self.window,text="Progress:")
        l4.place(x=140,y=500)
        
        #run button
        self.b1=Button(self.window,text="Run",width=25,state='disabled',command=self.proteincompare) #run button
        self.b1.place(x=700,y=525)
        
        self.e1.bind("<Key>",self.chektext)
        self.e2.bind("<Key>",self.chektext)
        
        if (self.v.get()==1):
            self.e3.config(state='disabled') #need it for initialise disable
            self.outText.set(self.name)
        elif(self.v.get()==2):
            self.outText.set(self.e3.get())
        else:
            self.e3.insert(0,"Error")

    def defname(self):
        """
            set the output text to a default name and disable the entery for the name
        """
        self.e3.delete(0,END)
        self.e3.insert(0,self.name) 
        self.e3.config(state='disabled')
        
    def manualname(self):
        """
            set the output text to the entery 3 and enable it
        """
        self.e3.config(state='normal')
        self.e3.delete(0,END)

    def mesagefinish(self):     #mesage box and call the function to clean the input info
        """
            Creater a message boc indicating the comparation has ended
        """
        messagebox.showinfo("Sucess", "Comparation complete")
        self.cleanscrean()

    def cleanscrean(self): #clan all the inputs
        """
        clear all inputs and create a new default name
        """
        self.e1.delete(0,END)
        self.e2.delete(0,END)
        self.bar['value']=0
        self.v.set(1)
        self.name=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"_output"
        self.outText.set(self.name)
        self.defname()
        

    def proteincompare(self): #function to compare strings update bar and call msg finish
        """
        here we compare the proteins and update the task bar
        """
        a=Compear(self.String1,self.String2)
        a.extend_final_idx()
        x=0
        while (x<10):
            self.bar['value']+=10
            time.sleep(1)
            x+=1
            self.window.update_idletasks()

        self.mesagefinish()


    def chektext(self,event):
        """
            Check if we have text to enable or disable the buton run
        """
        if (self.e1.get()!="" and self.e2.get()!=""):
            self.b1.config(state='normal')
        elif (self.e1.get()=="" or self.e2.get()==""):
            self.b1.config(state='disabled')

    def startgui(self):
        """
            Needed to run the GUI
        """
        self.window.mainloop()
        
    def printinfo(self):
        """
        Print info use for testing
        """
        print("Output name : "+str(self.outText.get())+"\n")
        print("Default Name: "+str(self.name)+"\n")
        print("String1     : "+str(self.String1.get())+"\n")
        print("String2     : "+str(self.String2.get())+"\n")


# In[3]:


a=GUI()


# In[4]:


a.startgui()


# In[11]:


#a.printinfo()


# In[5]:


#help(GUI)


# In[6]:


from docx import Document
from docx.text.run import Font, Run


# In[7]:


document = Document('Test.docx')


# In[10]:


for p in document.paragraphs:
    print(p.text)


# In[ ]:


    


