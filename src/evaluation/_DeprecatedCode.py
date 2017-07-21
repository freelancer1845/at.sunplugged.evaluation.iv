'''
Created on 19.07.2017

@author: jasch
'''

"""

class DarkDataObject:
    '''
        A wrapper class for dark data.
    '''
    

    def createTableData(self):
        self.tableData.append(['Rs', self.Rs])
        self.tableData.append(['Rp', self.Rp])
        
    
    def __init__(self, data, area, texName):
        self.data = data
        self.area = area
        self.texName = texName
        self.Rs = self._findRs(data)
        self.Rp = self._findRp(data)
        self.tableData = []
        self.createTableData()
        
    def _findIsc(self, data, epsilon = 0.1):
        #epsilon only uses data for fitting where -epsilon < U < epsilon
        print(data)
        startRange = np.where(data[:, 0] > -epsilon)[0][0]
        endRange = np.where(data[:, 0] > epsilon)[0][0]
        
        if endRange <= startRange:
            return self._findIsc(data, epsilon * 10)
        
        polynom = np.poly1d(np.polyfit(data[startRange:endRange,0], data[startRange:endRange, 1], 1, 1))
        return polynom(0)
    
    def _findVoc(self, data, epsilon = 0.001):
        #epsilon only uses data for fitting where -epsilon < I < epsilon
        startRange = np.where(((data[:, 1] > -epsilon) == True) & (data[:,0] > 0))[0][0]
        endRange = np.where(((data[:, 1] > epsilon) == True) & (data[:,0] > 0))[0][0]
        if endRange <= startRange:
            return self._findVoc(data, epsilon * 10)
        
        polynom = np.poly1d(np.polyfit(data[startRange:endRange, 0],
                    data[startRange:endRange, 1], 1))
        #p.plot(data[:,0], data[:, 1], data[:,0], polynom(data[:,0]))
        #p.show()
        roots = polynom.r
        if roots[0] < data[0,0] or roots[0] > data[data[:,0].size-1,0]:
            return roots[1]
        else:
            return roots[0]
        
    def _findRp(self, data):
        p = 0.2 # percentage of data start to be fitted
        lowestVoltage = np.min(data[:,0])
        
    
        polyCoef = np.polyfit(data[(data[:,0] < lowestVoltage * (1-p)) == True, 0], data[(data[:,0] < lowestVoltage * (1-p)) == True, 1], 1)
        self.RpC = polyCoef[1]
        return polyCoef[0]
    
    def _findRs(self, data):
        p = 0.1 # percentage of data end to be fitted
        highestVoltage = np.max(data[:,0])
        
        
        polyCoef = np.polyfit(data[(data[:,0] > highestVoltage * (1-p)) == True, 0], data[(data[:,0] > highestVoltage * (1-p)) == True, 1], 1)
        self.RsC = polyCoef[1]
        return polyCoef[0]
    
    def generatePlot(self, axs):
        axs[0].plot(self.data[:,0], self.data[:,1], label='Data', zorder=100)
        axs[0].plot(self.data[:,0], self.Rp * self.data[:,0] + self.RpC)
        axs[0].plot(self.data[:,0], self.Rs * self.data[:,0] + self.RsC)
        axs[0].set_ylim((min(self.data[:,1]) - 0.1 * abs(min(self.data[:,1])) ,max(self.data[:,1]) + 0.1 * abs(max(self.data[:,1]))))
        axs[0].set_xlabel('U')
        axs[0].set_ylabel('I')
        axs[0].set_title(self.texName)
        axs[0].grid()
        axs[0].legend(fontsize=6)
        axs[0].axhline(y=0, color='k')
        axs[0].axvline(x=0, color='k')
        # Create the Table
        
        axs[1].axis('tight')
        axs[1].axis('off')
        table = axs[1].table(cellText=self.tableData,loc='center')
        return axs


class LightDataObject:
    '''
        A wrapper class for light data.
    '''
    def __init__(self, data, area, texName):
        self.data = data
        self.data.sort(axis=0)
        self.area = area
        self.texName = texName
        evaluation = self._evaluateLightData()
        self.Voc = evaluation[0]
        self.Isc = evaluation[1]
        self.FF = evaluation[2]
        self.MppX = evaluation[3][0]
        self.MppY = evaluation[3][1]
        self.Mpp = evaluation[3][2]
        self.jsc = evaluation[4]
        self.Rp = evaluation[5]
        self.Rs = evaluation[6]
        self.Eff = self.Mpp/area/(790/10000)
        self.tableData = []
        self.createTableData()
        
    def createTableData(self):
        self.tableData.append(['Voc', self.Voc])
        self.tableData.append(['Isc', self.Isc])
        self.tableData.append(['FF', self.FF])
        self.tableData.append(['Mpp', self.Mpp])
        self.tableData.append(['jsc', self.jsc])
        self.tableData.append(['Rp', self.Rp])
        self.tableData.append(['Rs', self.Rs])
        self.tableData.append(['Eff', self.Eff])
        
    def generatePlot(self, axs):
        #fig, axs = p.subplots(2, 1, gridspec_kw = {'height_ratios':[2.5, 1]})

        ymin = min(self.data[:,1]) - 0.1 * abs(min(self.data[:,1]))
        ymax = max(self.data[:,1]) + 0.1 * abs(max(self.data[:,1]))
        # Do the plot        
        axs[0].plot(self.data[:,0], self.data[:,1], label='Data', zorder=100)
        axs[0].plot(self.data[:,0], self.data[:,0] * self.data[:,1] * -1, label='Power')
        
        if self.Isc is not None and self.Rp is not None:
            axs[0].plot(self.data[:,0], 1 / self.Rp * self.data[:,0] + self.Isc, label='RP')
            axs[0].plot(0, self.Isc, 'x', label='Isc', zorder=200)
        if self.Voc is not None and self.Rs is not None:
            axs[0].plot(self.data[:,0], 1 / self.Rs * self.data[:,0] - self.Voc *  1 / self.Rs, label='RS')
            axs[0].plot(self.Voc, 0, 'x', label='Voc', zorder=200)
        
        if self.Mpp is not None:
            axs[0].plot(self.MppX, self.Mpp, 'x', label = 'Mpp', zorder=200)
            if self.Mpp > ymax:
                ymax = self.Mpp * 1.1
            
        axs[0].set_ylim(ymin, ymax)
        axs[0].set_xlabel('U')
        axs[0].set_ylabel('I')
        axs[0].set_title(self.texName)
        axs[0].grid()
        axs[0].legend(fontsize=6)
        axs[0].axhline(y=0, color='k')
        axs[0].axvline(x=0, color='k')
        # Create the Table
        
        axs[1].axis('tight')
        axs[1].axis('off')
        table = axs[1].table(cellText=self.tableData,loc='center')
        #fig.tight_layout(h_pad=1.4)
        #return fig, axs
        return axs
    
    
    def _findIsc(self, data, epsilon = 0.1):
        # epsilon only uses data for fitting where -epsilon < U < epsilon
        try:
            startRange = np.where(data[:, 0] > -epsilon)[0][0]
            endRange = np.where(data[:, 0] > epsilon)[0][0]
            if endRange <= startRange:
                return self._findIsc(data, epsilon * 10)
            
            polynom = np.poly1d(np.polyfit(data[startRange:endRange,0], data[startRange:endRange, 1], 1, 1))
        
            return polynom(0)
        except Exception as err:
            print('Error while calculating Isc for LightObject:', err)
            return None
    
    
    def _findVoc(self, data, epsilon = 0.001):
        # epsilon only uses data for fitting where -epsilon < I < epsilon
        try:
            startRange = np.where(((data[:, 1] > -epsilon) == True) & (data[:,0] > 0))[0][0]
            endRange = np.where(((data[:, 1] > epsilon) == True) & (data[:,0] > 0))[0][0]
            
            if endRange <= startRange:
                return self._findVoc(data, epsilon * 10)
            
            polynom = np.poly1d(np.polyfit(data[startRange:endRange, 0],
                        data[startRange:endRange, 1], 1))
            roots = polynom.r
            if roots[0] < data[0,0] or roots[0] > data[data[:,0].size-1,0]:
                return roots[1]
            else:
                return roots[0]
        except Exception as err:
            print('Error while calculating Voc for LightObject:', err)
            return None
    
    def _findMpp(self, data):
        '''
            Finds Mpp by interpolating U*I*-1 in a cubic way.
        '''
        try:
            data.sort(axis=0)
            uniqueData = np.array(data)
            for i in range(0, uniqueData[:,0].size):
                if (i < (uniqueData[:,0].size -2)):
                    if uniqueData[i,0] == uniqueData[i + 1,0]:
                        uniqueData[i,0] = uniqueData[i,0] - 1e-8
            
            iF = interp1d(uniqueData[:,0],uniqueData[:,1] * uniqueData[:,0] * -1, 'cubic')
            x = scipy.optimize.fmin(lambda x: iF(x) * -1, 0, disp=False)
            uIInterp = interp1d(uniqueData[:,0], uniqueData[:,1], 'cubic')
            return np.array([x[0], uIInterp(x[0]),  iF(x)[0]])
        except Exception as err:
            print('Error while calculating Voc for LightObject:', err)
            return None
    
    
    def _findRs(self, data):
        try:
            indexRange = 10 # Size of range around U = 0 that will be sampled for linear fit
            
            firstPositiveVoltage = np.where((data[:, 0] > 0) == True)[0][0]
            fitRange = range(firstPositiveVoltage-indexRange, firstPositiveVoltage+indexRange)
        
            return 1 / np.polyfit(data[fitRange, 0], data[fitRange, 1], 1)[0]
        except Exception as err:
            print('Error while calculating Rs for LightObject:', err)
            return None
    
    def _findRp(self, data):
        try:
            indexRange = 10 # Size of range around U = 0 that will be sampled for linear fit
            
            firstPositiveCurrent = np.where((data[:, 1] > 0) == True)[0][0]
            fitRange = range(firstPositiveCurrent-indexRange, firstPositiveCurrent+indexRange)
        
            return 1/np.polyfit(data[fitRange, 0], data[fitRange, 1], 1)[0]
        except Exception as err:
            print('Error while calculating Rp for LightObject:', err)
            return None
    
    def _evaluateLightData(self):
        '''
            Expects an array where each entry contains a U and I data point.
        '''
        
        Isc = self._findIsc(self.data)
        Voc = self._findVoc(self.data)
        jsc = Isc / self.area * -1
        MppPoint = self._findMpp(self.data)
        if MppPoint is not None and Voc is not None and Isc is not None:
            FF = -1 * MppPoint[2] / (Voc * Isc) * 100
        else:
            FF = None
        Rs = self._findRs(self.data)
        Rp = self._findRp(self.data)
        
       
        return Voc, Isc, FF, MppPoint, jsc , Rs, Rp