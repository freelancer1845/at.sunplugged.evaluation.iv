'''
Created on Jul 1, 2017

@author: Jascha Riedel
'''

import os
from enum import Enum
import subprocess
import shutil
import re
import numpy as np
from scipy.stats import describe
import scipy.stats
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def _createTexTableHeader(attribs):
    header = '\\begin{table}[!h]' + '\n'
    header += '\\tiny' + '\n'
    header += '\\begin{tabular}{l||r|r|r|r|r|r|r|r}'
    header += '\n'
    for attribute in attribs:
        header += ' & '
        header += attribute
    
    header += '\\\\'
    header += '\n'
    header += '\\hline'
    header += '\n'
    return header
    
def _formatValue(value):
    if abs(value) < 1E-3:
        valueString = '{:.2E}'.format(value)
    else:
        valueString = '{:.2f}'.format(value)
    return valueString
    
class _CellStyle(Enum):
    WORST = 1
    NORMAL = 2
    BEST = 3
    
    def texString(self, value):
        valueString = _formatValue(value)
        
        if self is _CellStyle.WORST:
            return '\\cellcolor{worst}$' + valueString + '$'
        elif self is _CellStyle.NORMAL:
            return  '$' + valueString + '$'
        elif self is _CellStyle.BEST:
            return '\\cellcolor{best}' + '$' + valueString + '$'
         


def _processDataObject(dataObjects, dataObject, attribs):
    dataRow = dataObject.texName
    for attrib in attribs:
        value = getattr(dataObject, attrib)
        others = np.array([getattr(otherObject, attrib) for otherObject in dataObjects])
        if attrib == 'Isc':
            value *= -1
            others *= -1
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


def _createSummaryRow(dataObjects, attribs):
    maxRow = 'Max'
    minRow = 'Min'
    meanRow = 'Mean'
    for attrib in attribs:
        data = np.array([getattr(dataObject, attrib) for dataObject in dataObjects])
        if attrib == 'Isc':
            data *= -1
        statistics = describe(data)
        maxValue = statistics[1][1]
        minValue = statistics[1][0]
        mean = statistics[2] 
        std = scipy.stats.tstd(data)
        maxRow += ' & ' + _formatValue(maxValue)
        minRow += ' & ' + _formatValue(minValue)
        meanRow += ' & ' + _formatValue(mean) + ' $(\\pm ' + _formatValue(std) + ')$'
    
    texReturn = '\\hline' + '\n' + '\\hline' + '\n'
    texReturn +=  maxRow + '\\\\' + '\n' + '\\hline' + '\n'
    texReturn += minRow + '\\\\' + '\n' + '\\hline'+ '\n'
    texReturn += meanRow + '\\\\' + '\n'
    return texReturn

def _createTaleEntires(dataObjects, attribs):
    tableTex = ''
    
    for dataObject in dataObjects:
        tableTex += _processDataObject(dataObjects, dataObject, attribs)
        tableTex += '\n'
    
    tableTex += _createSummaryRow(dataObjects, attribs)
    
    return tableTex

def _createTexTableFooter():
    return '\\end{tabular}' + '\n' + '\\end{table}' + '\n'


def writeDataTableTex(lightDataObjects, attribs):
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
    
def createDiagramsTex(dataObjects):
    _saveDataPlots(dataObjects)
    texScript = ''
    col = 0
    for dataObject in dataObjects:
        texScript += '\\includegraphics[width=10cm]{' + dataObject.texName + '.pdf}'
        if col == 1:
            texScript += '\n'
            col = 0
        else:
            col = 1
    
    texScript += '\n'
    
    if os.path.isdir('temp') is False:
        os.mkdir('temp')
    try:
        with open('temp/diagrams.tex', 'w') as outputFile:
            outputFile.write(texScript)
    except IOError as err:
        print(err)
    
    
    
    
def _saveDataPlots(dataObjects):
    for dataObject in dataObjects:
        figure = plt.figure()
        gs = GridSpec(2, 1, height_ratios=[3,1])
        gs.update(hspace=0.7)
        
        
        dataObject.generatePlot([figure.add_subplot(gs[0]), figure.add_subplot(gs[1])])
        figure.savefig('temp/' + dataObject.texName + '.pdf')
        figure.clear()
    
    
    
    
    
def convertViaTex(outputFileName):
    
    shutil.copy2('formattedOutput/template.tex', 'temp/template.tex')
    
    
    proc = subprocess.Popen(['pdflatex',  '-job-name=' + outputFileName,'--aux-directory=temp', '--output-directory=output' , 'template.tex'])
    proc.communicate()
    shutil.rmtree('temp', True)
    
