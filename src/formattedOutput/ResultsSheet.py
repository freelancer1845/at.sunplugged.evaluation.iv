'''
Created on 18.07.2017

@author: Jascha Riedel
'''


columnHeadings = (
    'Sample Name',
    'Rp [ohmcm²]',
    'Rs [ohmcm²]',
    'Pmpp [W/cm²]',
    'jsc[A/cm²]',
    'Voc[V]',
    'FF[%]',
    'Eff[%]',
    'FFxVoc'
    )


def fillResultsSheet(sheet, cellDataObjects):
    
    for idx, heading in enumerate(columnHeadings, start=1):
        sheet.cell(row = 1, column = idx).value = heading
        
    for idx, dataObject in enumerate(cellDataObjects, start=1):
        sheet.cell(row = idx, column = 1).value = dataObject.Name
        sheet.cell(row = idx, column = 2).value = dataObject.Rp
        sheet.cell(row = idx, column = 3).value = dataObject.Rs
        sheet.cell(row = idx, column = 4).value = dataObject.Mpp / dataObject.Area
        sheet.cell(row = idx, column = 5).value = dataObject.Jsc
        sheet.cell(row = idx, column = 6).value = dataObject.Voc
        sheet.cell(row = idx, column = 7).value = dataObject.FF
        sheet.cell(row = idx, column = 8).value = dataObject.Eff
        sheet.cell(row = idx, column = 9).value = None
        
        
        
        
        
        
        
        
        
        
    