'''
Created on 18.07.2017

@author: jasch
'''

from tkinter import *
from tkinter.filedialog import askopenfilename
from databasereader import DatabaseConnection
from formattedOutput.ExcelOutput import saveCellDataObjects

class DatabaseReaderFrame(Frame):
    '''
    Access frame to read from the database and save the data into an Excel file
    '''
    DEFAULT_STRING_IDS_ENTRY = "Enter Ids (3, 5-60, 30)..."
    DEFAULT_DIRECTORY = r"C:\Users\jasch\SunpluggedJob\SPROD\SPROD.MDB"
    
    
    def __init__(self, mainWindow):
        '''
        Constructor
        '''
        Frame.__init__(self,master=mainWindow)
        
        self.mainWindow = mainWindow
        
        self.grid(sticky = NW, pady = 10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        
        self._createControls()
        
    def _createControls(self):
        btnSelectDatabase = Button(self, text='Select Database', command=self._selectDatabase)
        btnSelectDatabase.grid(row=0, column=0, sticky = W + E, pady = 5 , padx=2)
        
        self.etyDatabase = Entry(self)
        self.etyDatabase.delete(0, END)
        self.etyDatabase.insert(0, self.DEFAULT_DIRECTORY)
        self.etyDatabase.grid(row=0, column = 1, sticky =  W +E)
        
        btnExtractData = Button(self, text='Extract Data', command=self._extractData)
        btnExtractData.grid(row=1, column=0,sticky=W + E, pady = 5, padx=2)
        
        self.etyIds = Entry(self)
        self.etyIds.delete(0, END)
        self.etyIds.insert(0, self.DEFAULT_STRING_IDS_ENTRY)
        self.etyIds.grid(row=1, column=1, sticky=W + E)
        self.etyIds.bind('<FocusIn>', self._on_entry_click)
        self.etyIds.bind('<FocusOut>', self._on_focusout)
        self.etyIds.config(fg = 'grey')
        
    def _selectDatabase(self):
        databaseFile = askopenfilename()
        if databaseFile is not None:
            self.etyDatabase.configure(state=NORMAL)
            self.etyDatabase.delete(0, END)
            self.etyDatabase.insert(0, databaseFile)
            self.etyDatabase.configure(state='readonly')
    


    
    def _extractData(self):
        ids = self._getIdsFromEntry()
        with DatabaseConnection(self.etyDatabase.get()) as db:
            data = db.getDatabaseEntries(ids)
            for dataObject in data:
                self.mainWindow.addCellDataObject(dataObject)
                
            #print('Writing Excel File...')
            #saveCellDataObjects(r"output/excelOutput.xls", data)
        
    def _getIdsFromEntry(self):
        fieldInput = self.etyIds.get()
        parts = fieldInput.split(',')
        ids = []
        for part in parts:
            idString = part.strip()
            ranges = idString.split('-')
            if len(ranges) > 1:
                ids.append([x for x in range(int(ranges[0]), int(ranges[1])  + 1)])
            else:
                ids.append(int(ranges[0]))
        
        return list(flatten(ids))

    def _on_entry_click(self, event):
        """function that gets called whenever entry is clicked"""
        if self.etyIds.get() == self.DEFAULT_STRING_IDS_ENTRY:
            self.etyIds.delete(0, "end") # delete all the text in the entry
            self.etyIds.insert(0, '') #Insert blank for user input
            self.etyIds.config(fg = 'black')
           
    def _on_focusout(self, event):
        if self.etyIds.get() == '':
            self.etyIds.insert(0, self.DEFAULT_STRING_IDS_ENTRY)
            self.etyIds.config(fg = 'grey')

def flatten(L):
    for item in L:
        try:
            yield from flatten(item)
        except TypeError:
            yield item
        
        