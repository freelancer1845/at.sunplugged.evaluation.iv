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
    
    
    for cell in cellDataObjects:
        summaryDic.setdefault(columnHeadings[0], list()).append(cell.Id)
        summaryDic.setdefault(columnHeadings[1], list()).append(cell.Rp / cell.Area)
        summaryDic.setdefault(columnHeadings[2], list()).append(cell.Rs / cell.Area)
        summaryDic.setdefault(columnHeadings[3], list()).append(cell.MppA)
        summaryDic.setdefault(columnHeadings[4], list()).append(cell.Jsc)
        summaryDic.setdefault(columnHeadings[5], list()).append(cell.Voc)
        summaryDic.setdefault(columnHeadings[6], list()).append(cell.FF)
        summaryDic.setdefault(columnHeadings[7], list()).append(cell.Eff)
        summaryDic.setdefault(columnHeadings[8], list()).append(cell.FF * cell.Voc)
    

    df = pd.DataFrame(summaryDic)

    df.to_excel(writer, SHEET_TITLE, index = False)
    print(df.iloc[:,2:])
    
    statisticsFrame = df.iloc[:,1:].describe()
    statisticsFrame.loc[('mean','std','max','min'), :].to_excel(writer, SHEET_TITLE, startrow=len(cellDataObjects) + 2)
    
    
    if writer.engine == "xlwt":
        for col in range(0, 12):
            worksheet.col(col).width = 4000
    elif writer.engine == "xlsxwriter":
        worksheet.set_column(0, 12, width=15)
    
    