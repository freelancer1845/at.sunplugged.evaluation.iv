'''
Created on 25.07.2017

@author: Jascha Riedel
'''

import pandas as pd
import collections

SUMMARAY_HEADINGS_AND_ATTRIBS = (
    ['Area', 'Area'],
    ['Voc', 'Voc'],
    ['Isc', 'Isc'],
    ['Jsc[A/cm^2]', 'Jsc'],
    ['R_p', 'Rp'],
    ['R_s', 'Rs'],
    ['Pmpp[W/cm^2]', 'MppA'],
    ['jsc[A/cm^2]', 'Jsc'],
    ['FF', 'FF'],
    ['Eff[%]', 'Eff']
    )

DATA_HEADINGS = (
    'Voltage',
    'Current',
    'Abs(U)',
    'Abs(I)',
    'j[A/cm^2]',
    'Abs(j)',
    'P[W/cm^2]'
    )

PLOT_TITLES = (
    'U - I Chart',
    'Voltage [V]',
    'Current [I]'
    )

#PLOT_SPECIAL_COLUMNS = {
#    'Rs': get_col_index('X')
#    }




def createCellDataSheet(writer, cellDataObject):
    
    if writer.engine == "xlwt":
        worksheet = writer.book.add_sheet(cellDataObject.Id)
    elif writer.engine == "xlsxwriter":
        worksheet = writer.book.add_worksheet(cellDataObject.Id)
    
    
    writer.sheets[cellDataObject.Id] = worksheet
    summaryDict = {}
    for attrib in SUMMARAY_HEADINGS_AND_ATTRIBS:
        summaryDict[attrib[0]] = [getattr(cellDataObject, attrib[1])]
    df = pd.DataFrame(summaryDict)
    
    df.to_excel(writer, cellDataObject.Id, startrow = 0, startcol = 2, index = False)
    
    worksheet.write(0, 0, 'Sample Name')
    worksheet.write(1, 0, cellDataObject.Id)
    
    
    
    dataDict = collections.OrderedDict()
    
    dataDict[DATA_HEADINGS[0]] = cellDataObject.data[:,0]
    dataDict[DATA_HEADINGS[1]] = cellDataObject.data[:,1]
    dataDict[DATA_HEADINGS[2]] = abs(cellDataObject.data[:,0])
    dataDict[DATA_HEADINGS[3]] = abs(cellDataObject.data[:,1])
    dataDict[DATA_HEADINGS[4]] = cellDataObject.data[:,1] / cellDataObject.Area
    dataDict[DATA_HEADINGS[5]] = abs(cellDataObject.data[:,1] / cellDataObject.Area)
    dataDict[DATA_HEADINGS[6]] = cellDataObject.data[:,1] * cellDataObject.data[:,0] / cellDataObject.Area
    
    df = pd.DataFrame(dataDict)
    df.to_excel(writer, cellDataObject.Id, startrow = 3, startcol = 0, index = False)
    
    
    if writer.engine == "xlwt":
        for col in range(0, 12):
            worksheet.col(col).width = 4000
    elif writer.engine == "xlsxwriter":
        worksheet.set_column(0, 12, width=15)
    
   
    
    if writer.engine == "xlwt":
        print('Charts are not supported for Excel 2003...')
    elif writer.engine == 'xlsxwriter':
        _createChart(writer, worksheet, cellDataObject)
        
    
def _createChart(writer, worksheet, cellDataObject):
    chart = writer.book.add_chart({'type': 'scatter'})
        
    chart.add_series({
            'name': [cellDataObject.Id, 3, 1],
            'values': [cellDataObject.Id, 3,1,len(cellDataObject.data[:,0]) + 3, 1],
            'categories': [cellDataObject.Id, 3, 0, len(cellDataObject.data[:,0]) + 3, 0]
        })
    
    chart.set_x_axis({'name': 'Voltage'})
    chart.set_y_axis({'name': 'Current'})
    
    
    
    
    
    worksheet.insert_chart('I7', chart)


    
    
