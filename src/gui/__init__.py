'''
Created on Jul 01, 2017

@author: Jascha Riedel
'''

from gui.fileIO import readLabViewFile
from formattedOutput import writeDataTableTex
from formattedOutput import convertViaTex
from formattedOutput import createDiagramsTex
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from tkinter.ttk import Treeview
from gui.DatabaseReaderFrame import DatabaseReaderFrame
from gui.MainWindow import MainWindow

def mainLoop():
    mainWindow = MainWindow()
    mainWindow.mainloop()
    #DialogFrame().mainloop()
    #DatabaseReader().mainloop()

