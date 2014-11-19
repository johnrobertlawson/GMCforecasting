import os
import time
import matplotlib as M
M.use('agg')
import matplotlib.pyplot as plt
import datetime
import numpy as N
import matplotlib.dates as mdates

class Meteogram(object):
    def __init__(self,datapath,outdir,forecastnames=False):
        self.fpath = datapath
        self.outdir = outdir

        self.init_time = datetime.datetime.now()
        if forecastnames:
            fore1 = raw_input("Who is the lead forecaster? ")
            forecasters = [fore1,]
            fore2 = raw_input("Who is the second forecaster,"
                                "if applicable? ")
            if len(fore2) > 2:
                forecasters.append(fore2)
        
        self.read_data()

    def read_data(self):
        names = ('Date','TimeLocal','MaxT','LikelyT','MinT',
                    'POPR','POPZ','WindLo','WindHi','ChanceLight')
        formats = ('S4','S4','i4','i4','i4',
                    'i4','i4','i4','i4','i4')
        self.data = N.loadtxt(self.fpath,dtype={'names':names,'formats':formats},
                                            skiprows=1,delimiter=',') 
        self.process_times()
        
    def process_times(self):
        raw_d = self.data['Date']
        raw_t = self.data['TimeLocal']
        # self.times = [datetime.datetime.strptime(d+'/'+t,'%m/%d/%H%M').timetuple()
        self.times = [datetime.datetime.strptime(d+'/'+t,'%m/%d/%H%M').replace(year=2014)
                            for d,t in zip(raw_d,raw_t)]
        # offset = 2208967200.0
        # self.times = [t.replace(year=2014) for t in self.times]

    def temp_range(self):
        upper = self.data['MaxT']-self.data['LikelyT']
        lower = self.data['LikelyT']-self.data['MinT']
        return upper,lower

    def plot(self):
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        # ax.xaxis.set_major_locator(mdates.DayLocator())

        # Error bars?
        # upper,lower = self.temp_range()
        # yerr = N.array([upper,lower])
        # temp = ax.errorbar(self.times,self.data['LikelyT'],yerr=yerr)
        
        # Fill-between plots
        # trange = ax1.fill_between(self.times,self.data['MaxT'],
                        # self.data['MinT'],alpha=0.5,color='red')
        ax1.set_ylim([10,50])
        tlike = ax1.plot(self.times,self.data['LikelyT'],color='red')
        for i,j in zip(self.times,self.data['LikelyT']):
            ax1.annotate(str(j)+' F',xy=(i,j),xytext=(0,0),
                    textcoords='offset points',color='red',
                    ha='center',va='center',
                    bbox={'alpha':0.9,'facecolor':'white'})

        # POP
        popr = ax2.plot(self.times,self.data['POPR'],color='blue')
        for i,j in zip(self.times,self.data['POPR']):
            ax2.annotate(str(j)+'%',xy=(i,j),xytext=(0,0),
                    textcoords='offset points',color='blue',
                    ha='center',va='center',
                    bbox={'alpha':0.9,'facecolor':'white'})
        popz = ax2.plot(self.times,self.data['POPZ'],color='green')
        for i,j in zip(self.times,self.data['POPZ']):
            ax2.annotate(str(j)+'%',xy=(i,j),xytext=(0,0),
                    textcoords='offset points',color='green',
                    ha='center',va='center',
                    bbox={'alpha':0.9,'facecolor':'white'})
        ax2.set_ylim([0,100])

        # Finish and save
        fig.autofmt_xdate()
        outfname = 'generate_{0}.pdf'.format(self.init_time.date())
        outpath = os.path.join(self.outdir,outfname)
        plt.savefig(outpath)
