'''
Created on 13.07.2017

@author: Jascha Riedel
'''

import openpyxl

SHEET_DATA_TITLE = "DataSheet"
SHEET_RESULTS_TITLE = "Results"


def _createDataSheet(_sheet, dataObjects):
    currentColumn = 1
    for dataObject in dataObjects:
        _sheet.column_dimensions[currentColumn].width = 35
        
        nameCellX = _sheet.cell(row = 1, column = currentColumn)
        nameCellY = _sheet.cell(row = 1, column = currentColumn + 1)
        nameCellX.value = 'U-' + dataObject.texName
        nameCellY.value = 'I-' + dataObject.texName
        
        data = dataObject.data;
        currentRow = 2
        for point in data:
            _sheet.cell(row = currentRow, column = currentColumn).value = point[0]
            _sheet.cell(row = currentRow, column = currentColumn + 1).value = point[1]
            currentRow +=1
    
        currentColumn += 2


def _createResultsSheet(sheet, dataObjects, attribs):
    sheet.cell(row = 1, column = 1).value = 'Sample Name'
    currentColumn = 2
    for attrib in attribs:
        sheet.cell(row = 1, column = currentColumn).value = attrib
        currentColumn +=1
    
    currentRow = 2
    for dataObject in dataObjects:
        sheet.cell(row = currentRow, column = 1).value = dataObject.texName
        
        currentColumn = 2
        for attrib in attribs:
            value = getattr(dataObject, attrib)
            if value is None:
                value = "#NUM!"
            sheet.cell(row = currentRow, column = currentColumn).value = value
            currentColumn += 1
        
        currentRow += 1
    
    

def writeDataToExcelFile(excelFile, dataObjects, attribs):
    wb = openpyxl.Workbook()
    wb.active.title = SHEET_DATA_TITLE
    
    wb.create_sheet(title = SHEET_RESULTS_TITLE)
    
    _createDataSheet(wb.get_sheet_by_name(SHEET_DATA_TITLE), dataObjects)
    _createResultsSheet(wb.get_sheet_by_name(SHEET_RESULTS_TITLE), dataObjects, attribs)
    
    
    wb.save(excelFile)
