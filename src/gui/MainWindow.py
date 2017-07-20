'''
Created on 19.07.2017

@author: Jascha Riedel
'''

from tkinter import *
from gui.LabViewFilesReaderFrame import LabViewFilesReaderFrame
from gui.DatabaseReaderFrame import DatabaseReaderFrame
from gui.CellDataObjectsTreeview import CellDataObjectsTreeview
from tkinter.filedialog import asksaveasfilename
from formattedOutput import saveCellDataObjects


class MainWindow(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Example")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=W + E + N + S)


        
        LabViewFilesReaderFrame(self).grid(row=1, column= 0, sticky =N + W + E)
        
        DatabaseReaderFrame(self).grid(row=2, column = 0, sticky = N + W + E)
        
        self.btnExtractData = Button(text='Save Data in Excel File', command=self._handleSaveData)
        self.btnExtractData.grid(row=3, column = 0, sticky = N + W + E)
        
        self.cellDataTreeView = CellDataObjectsTreeview()
        self.cellDataTreeView.grid(row=4, column=0, sticky = N+W+E)
        
        
        


    def addCellDataObject(self, cellDataObject):
        self.cellDataTreeView.addCellDataObject(cellDataObject)
        
    def _handleSaveData(self):
        print('saving data...')
        cellObjects = [v for k,v in self.cellDataTreeView.cellDataObjects.items()]
        fileName = asksaveasfilename()
        if fileName is not None:
            saveCellDataObjects(fileName, cellObjects)
            print('Data saved.')
            
        

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