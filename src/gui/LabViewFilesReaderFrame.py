'''
Created on 19.07.2017

@author: Jascha Riedel
'''
from tkinter import *
from tkinter.filedialog import askopenfilenames
from gui.fileIO import readLabViewFile
from evaluation.lightevaluation import *
from evaluation import CellDataObject
from os import path as path
from gui.tkSimpleDialog import Dialog
import Config

class LabViewFilesReaderFrame(Frame):
    '''
    Frame containing controls to read LabView generated U-I data files and process them.
    '''


    
    
    def __init__(self, mainWindow):
        '''
        Parameters:
            mainWindow: To submit the CellDataObjects to the MainWindow
        '''
        Frame.__init__(self, master=mainWindow)
        
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
        names = askopenfilenames(filetypes = Config.FILE_TYPES_LIGHT)
        if names != None and len(names) != 0:
            d = AreaAndPowerInputDialog(self.master)
        for name in names:
            
            cellDataObject = CellDataObject.createFromData(path.basename(name).replace(".txt", ""),
                                                           readLabViewFile(name),
                                                           d.result[0],
                                                           d.result[1])
            cellDataObject.plotCellDataObject()
            self.mainWindow.addCellDataObject(cellDataObject)
            
            
    def _loadDarkData(self):
        names = askopenfilenames(filetypes = Config.FILE_TYPES_DARK)
        for name in names:
            print(name)


class AreaAndPowerInputDialog(Dialog):
    
    def body(self, master):
        Label(master, text="Area").grid(row=0)
        Label(master, text="PowerInput").grid(row=1)
        
        self.etyarea = Entry(master)
        self.etyPowerInput = Entry(master)
        
        self.etyarea.grid(row=0, column = 1)
        self.etyPowerInput.grid(row=1,column=1)
        
    def apply(self):
        try:
            self.result = float(self.etyarea.get()), float(self.etyPowerInput.get())
        except ValueError as err:
            print(err)
            
        
        
        
