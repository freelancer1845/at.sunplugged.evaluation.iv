'''
Created on 19.07.2017

@author: Jascha Riede
'''
from tkinter import *
from tkinter.ttk import Treeview
from evaluation import CellDataObject

class CellDataObjectsTreeview(Treeview):
    '''
    classdocs
    '''

    COLUMN_HEADINGS = (
        ('#0', 'ID'),
        ('source', 'Source'),
        ('area', 'Area'),
        ('voc', 'Voc'),
        ('isc', 'Isc'),
        ('FF', 'FF'),
        ('eff', 'Eff')
        )
    
    
    def __init__(self):
        '''
        Constructor
        '''
        Treeview.__init__(self)
        
        self.cellDataObjects = {}
        
        self._createContextMenus()
        self._createColumns()
        
        
    def addCellDataObject(self, source, cellDataObject):
        if isinstance(cellDataObject, CellDataObject) is False:
            raise ValueError('This Treeview may only process CellDataObjects!')
        
        self.cellDataObjects[self.insert('',
                    'end',
                    text=cellDataObject.Id,
                    values=(source,
                            cellDataObject.Area,
                            cellDataObject.Voc,
                            cellDataObject.Isc,
                            cellDataObject.FF,
                            cellDataObject.Eff)
                    )] = cellDataObject
        
        
    
    def _createContextMenus(self):
        def _deleteSelected():
            selectedItems = self.selection()
            for selectedItem in selectedItems:
                self.delete(selectedItem)
                del self.cellDataObjects[selectedItem]
                        
            print('Current Items:')
            print(self.cellDataObjects)
        self.contextMenu = Menu(self.master, tearoff = 0)
        self.contextMenu.add_command(label = 'Delete', command=_deleteSelected)
        self.contextMenu.add_separator()
        
        def do_popup(event):
            # display the popup menu
            try:
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
        
        
