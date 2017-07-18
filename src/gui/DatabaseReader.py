'''
Created on 17.07.2017

@author: jasch
'''
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Treeview

class DatabaseReader(Frame):
    '''
        Window to read from the database.
    '''


    
    
    def __init__(self):
        '''
        Constructor
        '''
        Frame.__init__(self)
        self.master.title("SPROD Database exporter")
        
        
        self.initalizeGrid()
        
        self.createControls()
       
       
        #self.master.minsize(width=1000, height=600)
        self.pack(expand = True, fill = 'both')
    
    def initalizeGrid(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(sticky=N + W)
    
    
    def createControls(self):
        self.createHeaderLabel()
        self.createDatabaseLoadButton()
        self.createTableViews()
        
    
    def createHeaderLabel(self):
        self.headerLabel = Label(self, text='Databse Reader for SPROD Microsoft Access Database')
        self.headerLabel.grid(row=0, column=0, columnspan=2, pady=40, sticky=N +E+W)
    
   
    
    
    def createDatabaseLoadButton(self):
        
        self.databaseLoadButton = Button(self, text="Load Database", command=self.handlerLoadDatabase)
        self.databaseLoadButton.grid(row=1, column=0, sticky = N + W)
        
        self.databaseLoadFileDir = Entry(self)
        self.databaseLoadFileDir.grid(row=1, column=1, sticky= N + E)
        
    
    def createMainList(self):
        self.mainList = Treeview(self)
        self.mainList.grid(row = 2, column = 0, columnspan = 2, sticky = N + W)
        
        
    
    def createTableViews(self):
        self.createMainList()
    
    
    def handlerLoadDatabase(self):
        databasedir = askopenfilename()
        self.databaseLoadFileDir.configure(state=NORMAL)
        self.databaseLoadFileDir.delete(0, END)
        self.databaseLoadFileDir.insert(0, databasedir)
        self.databaseLoadFileDir.configure(state='readonly')
        
