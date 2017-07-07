'''
Created on Jul 1, 2017

@author: Jascha Riedel
'''

import os
from enum import Enum
import subprocess
import shutil
import re

def _createTexTableHeader(attribs):
    header = '\\begin{tabular}{l||r|r|r|r|r|r|r|r}'
    header += os.linesep
    for attribute in attribs:
        header += ' & '
        header += attribute
    
    header += '\\\\'
    header += os.linesep
    header += '\\hline'
    header += os.linesep
    return header
    
class _CellStyle(Enum):
    WORST = 1
    NORMAL = 2
    BEST = 3
    
    def texString(self, value):
        if self is _CellStyle.WORST:
            return '\\cellcolor{worst}$' + '{:.2E}'.format(value) + '$'
        elif self is _CellStyle.NORMAL:
            return  '$' + '{:.2E}'.format(value) + '$'
        elif self is _CellStyle.BEST:
            return '\\cellcolor{best}' + '$' + '{:.2E}'.format(value) + '$'
         
    

def _processDataObject(dataObjects, dataObject, attribs):
    dataRow = dataObject.texName
    for attrib in attribs:
        value = getattr(dataObject, attrib)
        others = [getattr(otherObject, attrib) for otherObject in dataObjects]
        minValue = min(others)
        maxValue = max(others)
        if (value <= minValue):
            cellStyle = _CellStyle.WORST
        elif (value >= maxValue):
            cellStyle = _CellStyle.BEST
        else:
            cellStyle = _CellStyle.NORMAL
        
        dataRow += ' & '
        dataRow += cellStyle.texString(value)
    
    dataRow += '\\\\'    
    return dataRow


def _createTaleEntires(dataObjects, attribs):
    tableTex = ''
    
    for dataObject in dataObjects:
        tableTex += _processDataObject(dataObjects, dataObject, attribs)
        tableTex += os.linesep
    
    return tableTex

def _createTexTableFooter():
    return '\\end{tabular}' + os.linesep


def writeDataTableLightTex(lightDataObjects, attribs):
    lightDataObjects.sort(key=lambda x: int(re.findall('[0-9]+', x.texName)[0]))
    
    texScript = _createTexTableHeader(attribs)
    texScript += _createTaleEntires(lightDataObjects, attribs)
    texScript += _createTexTableFooter()
    if os.path.isdir('temp') is False:
        os.mkdir('temp')
    try:
        with open('temp/datatable.tex', 'w') as outputFile:
            outputFile.write(texScript)
    except IOError as err:
        print(err)
    
    
def convertViaTex():
    
    shutil.copy2('formattedOutput/template.tex', 'temp/template.tex')
    
    
    proc = subprocess.Popen(['pdflatex', '--aux-directory=temp', '--output-directory=output' , 'template.tex'])
    proc.communicate()
    shutil.rmtree('temp', True)
    
