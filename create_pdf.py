import os

from plotting.plot import Meteogram

datapath = os.path.abspath('./datafiles')
datafile = 'TexasTech.csv'
outdir = os.path.abspath('./output/')
fpath = os.path.join(datapath,datafile)

MET = Meteogram(fpath,outdir)
MET.plot()

