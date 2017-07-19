'''
Created on 19.07.2017

@author: jasch
'''
from tkinter import *
from tkinter.filedialog import askopenfilenames

class LabViewFilesReaderFrame(Frame):
    '''
    Frame containing controls to read LabView generated U-I data files and process them.
    '''


    
    
    def __init__(self, mainWindow):
        '''
        Parameters:
            mainWindow: To submit the CellDataObjects to the MainWindow
        '''
        Frame.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.grid(sticky=NW, pady=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        
        self._createControls()
    
    def _createControls(self):
        self.btnLoadLightFiles = Button(self, text='Load Light Data', command=self._loadLightData)
        self.btnLoadLightFiles.grid(row=0, column=0, columnspan=2, sticky=W + E)
        
        self.btnLoadDarkFiles = Button(self, text='Load Dark Data', command=self._loadDarkData)
        self.btnLoadDarkFiles.grid(row=1, column=0, columnspan=2, sticky=W + E)
        
    
    def _loadLightData(self):
        names = askopenfilenames()
        for name in names:
            print(name)
            
    def _loadDarkData(self):
        names = askopenfilenames()
        for name in names:
            print(name)
    
        
