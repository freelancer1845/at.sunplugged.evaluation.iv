'''
Created on Jul 01, 2017

@author: Jascha Riedel
'''

from gui.fileIO import readFile
from evaluation import evaluateLightData
from evaluation import LightDataObject
from formattedOutput import writeDataTableLightTex
from formattedOutput import convertViaTex
from formattedOutput import createDiagramsTex
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
import re

def mainLoop():
    DialogFrame().mainloop()


class DialogFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Example")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)

        self.button = Button(self, text="Browse", command=self.load_file, width=10)
        self.button.grid(row=1, column=0, sticky=W)

    def load_file(self):
        dirname = askdirectory()
        if dirname:
            processDirLightPlots(dirname)
            return


def processDirLightPlots(dirname):
    print(os.getcwd())
    
    plots = []
    for file in os.listdir(dirname):
        if file.endswith('-1.txt'):
            dataName = 'e' + re.findall('[0-9]+(?=-1.txt)', file)[0]
            
            plots.append(LightDataObject(readFile(os.path.join(dirname, file)), 1, dataName))
            
    writeDataTableLightTex(plots, ['Voc', 'Isc', 'FF', 'Mpp', 'jsc', 'Rp', 'Rs', 'Eff'])
    createDiagramsTex(plots)
    convertViaTex()
    #multiPlotMethod(plots, 'figure.pdf')
    

def multiPlotMethod(dataObjects, fileName):
    if len(dataObjects) % 2 != 0:
        rows = len(dataObjects) + 1 / 2
    else:
        rows = len(dataObjects) / 2
    
    
    mainFigure = plt.figure(figsize=(10,rows * 4))
    outer = gridspec.GridSpec(int(rows), 2, wspace = 0.2, hspace=0.2)
    
    for i in range(0, len(dataObjects)):
        inner = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer[i], wspace=0.1, hspace=1.3, height_ratios=[8,1])
        
        axs = dataObjects[i].generatePlot((plt.Subplot(mainFigure, inner[0]), plt.Subplot(mainFigure, inner[1])))
        mainFigure.add_subplot(axs[0])
        mainFigure.add_subplot(axs[1])
    
    mainFigure.savefig(fileName)
