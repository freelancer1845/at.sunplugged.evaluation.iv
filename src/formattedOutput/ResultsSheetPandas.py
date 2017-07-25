'''
Created on 25.07.2017

@author: Jascha Riedel
'''

import collections
import pandas as pd

SHEET_TITLE = 'Summary'


columnHeadings = (
    r'Sample Name',
    r'Rp [ohmcm2]',
    r'Rs [ohmcm2]',
    r'Pmpp [W/cm2]',
    r'jsc[A/cm2]',
    r'Voc[V]',
    r'FF[%]',
    r'Eff[%]',
    r'FFxVoc'
    )


def createResultsSheet(writer, cellDataObjects):
    
    
    if writer.engine == "xlwt":
        worksheet = writer.book.add_sheet(SHEET_TITLE)
    elif writer.engine == "xlsxwriter":
        worksheet = writer.book.add_worksheet(SHEET_TITLE)
    
    writer.sheets[SHEET_TITLE] = worksheet
    
    
    summaryDic = collections.OrderedDict()
    
    summaryDic[columnHeadings[0]] = [getattr(cell, 'Id') for cell in cellDataObjects]
    summaryDic[columnHeadings[1]] = [getattr(cell, 'Rp') for cell in cellDataObjects]
    summaryDic[columnHeadings[2]] = [getattr(cell, 'Rs') for cell in cellDataObjects]
    summaryDic[columnHeadings[3]] = [getattr(cell, 'MppA') for cell in cellDataObjects]
    summaryDic[columnHeadings[4]] = [getattr(cell, 'Jsc') for cell in cellDataObjects]    
    summaryDic[columnHeadings[5]] = [getattr(cell, 'Voc') for cell in cellDataObjects]   
    summaryDic[columnHeadings[6]] = [getattr(cell, 'FF') for cell in cellDataObjects]    
    summaryDic[columnHeadings[7]] = [getattr(cell, 'Eff') for cell in cellDataObjects]    
    summaryDic[columnHeadings[8]] = [None for cell in cellDataObjects]    
    
    df = pd.DataFrame(summaryDic)

    df.to_excel(writer, SHEET_TITLE, index = False)
    if writer.engine == "xlwt":
        for col in range(0, 12):
            worksheet.col(col).width = 4000
    elif writer.engine == "xlsxwriter":
        worksheet.set_column(0, 12, width=15)
    
    