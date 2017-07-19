'''
Created on Jul 01, 2017

@author: Jascha Riedel
'''

from gui.fileIO import readFile
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

class DialogFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Example")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=W + E + N + S)
        
        self.outputFileNamePrefix = Label(self, text="Output file prefix + dark/light")
        self.outputFileNamePrefix.grid(row=1, column=0, sticky=W)

        self.suffixLightLabel = Label(self, text="Suffix for Light Datafiles")
        self.suffixLightLabel.grid(row=2, column=0, sticky=W)
        
        self.suffixDarkLabel = Label(self, text="Suffix for Dark Datafiles")
        self.suffixDarkLabel.grid(row=3, column=0, sticky=W)
        
        self.etyOutputFileNamePrefix = Entry(self)
        self.etyOutputFileNamePrefix.delete(0, END)
        self.etyOutputFileNamePrefix.insert(0, 'output')
        self.etyOutputFileNamePrefix.grid(row=1, column=1, sticky=W)
        
        self.etySuffixLight = Entry(self)
        self.etySuffixLight.delete(0, END)
        self.etySuffixLight.insert(0, '-1.txt')
        self.etySuffixLight.grid(row=2, column=1, sticky=E)
        
        self.etySuffixDark = Entry(self)
        self.etySuffixDark.delete(0, END)
        self.etySuffixDark.insert(0, '-0.txt')
        self.etySuffixDark.grid(row=3, column=1, sticky=E)
        
        self.areaFieldLabel = Label(self, text="Cell Area")
        self.areaFieldLabel.grid(row=4, column=0, sticky=W)
        
        self.etyAreaField = Entry(self)
        self.etyAreaField.delete(0, END)
        self.etyAreaField.insert(0, 1)
        self.etyAreaField.grid(row=4, column=1, sticky=E)
        
        
        self.button = Button(self, text="Browse/Evaluate", command=self.load_file, width=10)
        self.button.grid(row=5, column=0, sticky=W)
        
        self.button = Button(self, text="Generate Tex Output", command=self.generateOutput, width=20)
        self.button.grid(row=5, column=1)
        
        self.button = Button(self, text="Clear", command=self.clear, width=10)
        self.button.grid(row=5, column=2, sticky=E)
        
        self.fileList = Treeview(self)
        self.fileList.grid(row=6, column=0, columnspan=3, sticky=W)
        self.fileList['columns'] = ('Type')
        self.fileList.heading("#0", text='Name')
        self.fileList.heading('Type', text='Type')
        
        
        self.lightDataObjects = []
        self.darkDataObjects = []
        
        DatabaseReaderFrame(self.master).grid(row=7, column = 0, columnspan=3, sticky = W + E)
        

    def load_file(self):
        dirname = askdirectory()
        if dirname:
            self.processDirLightPlots(dirname)
            return
        
    def clear(self):
        self.fileList.delete(*self.fileList.get_children())
        self.lightDataObjects.clear()
        self.darkDataObjects.clear()

    def generateOutput(self):
        if (len(self.lightDataObjects) > 0):
            attribs = ['Voc', 'Isc', 'FF', 'Mpp', 'jsc', 'Rp', 'Rs', 'Eff']
            writeDataTableTex(self.lightDataObjects, attribs)
            createDiagramsTex(self.lightDataObjects)
            convertViaTex(self.etyOutputFileNamePrefix.get() + 'light')
            writeExcelOutput('output/excel' + self.etyOutputFileNamePrefix.get() + '.xlsx', self.lightDataObjects, attribs)
        
        if (len(self.darkDataObjects) > 0):
            writeDataTableTex(self.darkDataObjects, ['Rp', 'Rs'])
            createDiagramsTex(self.darkDataObjects)
            convertViaTex(self.etyOutputFileNamePrefix.get() + 'dark')
            pass

    def processDirLightPlots(self, dirname):
        print(os.getcwd())
        
        
        for file in os.listdir(dirname):
            
            
            area = float(self.etyAreaField.get())
            if file.endswith('-1.txt'):
                dataName = 'e' + re.findall('[0-9]+(?=-1.txt)', file)[0]
                dataName = file[0:(len(file) - 6)]
                try:
                    self.lightDataObjects.append(LightDataObject(readFile(os.path.join(dirname, file)), area, dataName))
                    self.fileList.insert('', 'end', file, text=file, values=('Light'))
                except Exception as e:
                    self.fileList.insert('', 'end', file, text=file, values=('ERROR'))
                    print('Failed to calculate light data for "' + dataName + '"... Ignoring it', e)
                    raise e
            elif file.endswith('-0.txt'):
                dataName = 'e' + re.findall('[0-9]+(?=-0.txt)', file)[0]
                try:
                    self.darkDataObjects.append(DarkDataObject(readFile(os.path.join(dirname, file)), area, dataName))
                    self.fileList.insert('', 'end', file, text=file, values=('Dark'))
                except Exception as e:
                    self.fileList.insert('', 'end', file, text=file, values=('ERROR'))
                    print('Failed to calculate dark data for "' + dataName + '"... Ignoring it', e)
                    raise e
         

        

def multiPlotMethod(dataObjects, fileName):
    if len(dataObjects) % 2 != 0:
        rows = len(dataObjects) + 1 / 2
    else:
        rows = len(dataObjects) / 2
    
    
    mainFigure = plt.figure(figsize=(10, rows * 4))
    outer = gridspec.GridSpec(int(rows), 2, wspace=0.2, hspace=0.2)
    
    for i in range(0, len(dataObjects)):
        inner = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer[i], wspace=0.1, hspace=1.3, height_ratios=[8, 1])
        
        axs = dataObjects[i].generatePlot((plt.Subplot(mainFigure, inner[0]), plt.Subplot(mainFigure, inner[1])))
        mainFigure.add_subplot(axs[0])
        mainFigure.add_subplot(axs[1])
    
    mainFigure.savefig(fileName)
