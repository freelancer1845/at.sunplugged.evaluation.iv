'''
Created on 19.07.2017

@author: Jascha Riede
'''
from tkinter import *
from tkinter.ttk import Treeview
from evaluation import CellDataObject
from logging import debug, warning
import gui.tkSimpleDialog
from evaluation.CellDataObject import CellDataObject





class CellDataObjectsTreeview(Treeview):
    '''
    classdocs
    '''

    # Column Id, Column Heading, CellDataObject Attribute, Type
    COLUMN_HEADINGS = (
        ('#0', 'ID', 'Id', 'str'),
        ('area', 'Area', 'Area', 'float'),
        ('voc', 'Voc', 'Voc', 'float'),
        ('isc', 'Isc', 'Isc', 'float'),
        ('FF', 'FF', 'FF', 'float'),
        ('eff', 'Eff', 'Eff', 'float')
        )
    
    
    def __init__(self):
        '''
        Constructor
        '''
        Treeview.__init__(self)
        
        self.cellDataObjects = {}
        
        self._createContextMenus()
        self._createColumns()
        
        
    def addCellDataObject(self, cellDataObject):
        if isinstance(cellDataObject, CellDataObject) is False:
            raise ValueError('This Treeview may only process CellDataObjects!')
        
        treeId = self.insert('',
                'end',
                text=cellDataObject.Id,
                values=(
                        cellDataObject.Area,
                        cellDataObject.Voc,
                        cellDataObject.Isc,
                        cellDataObject.FF,
                        cellDataObject.Eff
                        )
                    )    
        self.cellDataObjects[treeId] = cellDataObject                              
    
    
    def _createContextMenus(self):
        def _deleteSelected():
            selectedItems = self.selection()
            for selectedItem in selectedItems:
                self.delete(selectedItem)
                del self.cellDataObjects[selectedItem]
                        
        
        def _editSelected():
            selectedItems = self.selection()
            #if selectedItems
            d = EditDialog(self.master)
            if d.result is None:
                return;
            
            for selectedItem in selectedItems:
                cellDataObject = self.cellDataObjects[selectedItem]
                
                for idx,column in enumerate(self.COLUMN_HEADINGS):
                    if len(d.result[idx]) > 0:
                        if column[3] == "float":
                            setattr(cellDataObject, column[2], float(d.result[idx]))
                        else:
                            setattr(cellDataObject, column[2], d.result[idx])
                        
                        
                        
                self.cellDataObjects[selectedItem] = cellDataObject
                self.item(selectedItem, text=cellDataObject.Id,
                        values=(
                                cellDataObject.Area,
                                cellDataObject.Voc,
                                cellDataObject.Isc,
                                cellDataObject.FF,
                                cellDataObject.Eff
                                )
                          )
                
        
        
        def _addPrefixSelected():
            selectedItems = self.selection()
            
            d = PrefixDialog(self.master)
            if d.result is None:
                return;
            
            for selectedItem in selectedItems:
                cellDataObject = self.cellDataObjects[selectedItem]
                
                currentId = getattr(cellDataObject, CellDataObjectsTreeview.COLUMN_HEADINGS[0][2])
                
                setattr(cellDataObject, CellDataObjectsTreeview.COLUMN_HEADINGS[0][2], d.result + currentId)        
                self.cellDataObjects[selectedItem] = cellDataObject
                self.item(selectedItem,
                          text=cellDataObject.Id
                          )
            
            
            pass
        
        self.contextMenu = Menu(self.master, tearoff = 0)
        self.contextMenu.add_command(label = 'Delete', command=_deleteSelected)
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label = 'Edit', command=_editSelected)
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label = 'Add Prefix To Id', command=_addPrefixSelected)
        
        def do_popup(event):
            # display the popup menu
            if len(self.selection()) > 0:
                try:
                    
                    #self.contextMenu.entryconfig("Delete", state = DISABLED)
                    #self.contextMenu.entryconfig("Edit", state = DISABLED)
                    self.contextMenu.selection = self.set(self.identify_row(event.y))
                    self.contextMenu.post(event.x_root, event.y_root)
                finally:
                    # make sure to release the grab (Tk 8.0a1 only)
                    self.contextMenu.grab_release()
        
        self.bind("<Button-3>", do_popup)
        
        
    def _createColumns(self):
        
        self.heading(self.COLUMN_HEADINGS[0][0], text=self.COLUMN_HEADINGS[0][1])
        
        self['columns'] = [x[0] for x in self.COLUMN_HEADINGS[1:]]
        
        for col in self.COLUMN_HEADINGS[1:]:
            self.heading(col[0], text=col[1])
        
        


class EditDialog(gui.tkSimpleDialog.Dialog):




    def body(self, master):
        self.entries = {}
        for idx,column in enumerate(CellDataObjectsTreeview.COLUMN_HEADINGS):
            Label(master, text=column[1]).grid(row=idx)
            self.entries[column[1]] = Entry(master)
            self.entries[column[1]].grid(row=idx, column= 1)
            
        return self.entries[CellDataObjectsTreeview.COLUMN_HEADINGS[0][1]] # initial focus

    def apply(self):
        self.result = []
        for column in CellDataObjectsTreeview.COLUMN_HEADINGS:
            self.result.append(self.entries[column[1]].get())
        

class PrefixDialog(gui.tkSimpleDialog.Dialog):
    
    def body(self, master):
        
        Label(master, text="Prefix").grid(row = 0)
        self.entry = Entry(master)
        self.entry.grid(row = 0, column = 0)
        
    def apply(self):
        self.result = self.entry.get()
        