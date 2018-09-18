# Visualisation of Parkes beam pattern: Shows position of beams for a given HDF file
# Input: fname (location of HDF dataset)
# V.A. Moss (vmoss.astro@gmail.com)

__author__ = "V.A. Moss"
__date__ = "$18-sep-2018 17:00:00$"
__version__ = "0.1"

import os 
import sys
import tables as tb
import numpy as np
from matplotlib import *
import matplotlib
matplotlib.rcParams["interactive"] = True
from numpy import *
from pylab import *
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['serif'],'size':14})
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage,AnnotationBbox
from matplotlib._png import read_png
import urllib.request, urllib.parse, urllib.error
import datetime
from astropy.io import ascii

# Read the position from the observation record
fname = '2017-09-19_0109-P953_GASS_246.2+39.9+312_0.hdf'

# VLSR
# This function gets the velocity of the observatory for a given position and date/time
def freq2vlsr(ra,dec,fname):

	x = datetime.datetime.strptime(fname.split('-P')[0],'%Y-%m-%d_%H%M')
	date = x.strftime('%Y%b%d:%H:%M').lower()
	path = 'www.narrabri.atnf.csiro.au/cgi-bin/obstools/velo.cgi?radec=%s,%s&velo=0&frame=lsr&type=radio&date=%s&freq1=1420.405752&freq2=&telescope=parkes' % (ra,dec,date)
	path1 = path.replace(':','%3A')
	path2 = 'http://'+path1.replace(',','%2C')

	# Get from online
	f = urllib.request.urlopen(path2)
	for line in f: 
		line = line.decode('utf-8')
		if 'Observatory velocity' in line:
			vel = float(line.split('</td><td>')[1].split()[0])

	return vel

def showmb():

	# Make image
	sfig = 'beams_all.png'
	arr_lena = read_png(sfig)
	imagebox = OffsetImage(arr_lena, zoom=0.35)
	ab = AnnotationBbox(imagebox, [0.095,0.08],
	                    xybox=(0., 0.),
	                    xycoords='axes fraction',
	                    boxcoords="offset points",
	                    frameon=False
	                    )
	gca().add_artist(ab)

# Get the positional information
d = ascii.read('P953 Observation Record - Sheet1.csv')

# Get the position
srcname = fname.split('/')[-1]
src = srcname.split('.hdf')[0]
mask = (d['File'] == srcname)
dsub = d[mask]
ra,dec = dsub['RA'][0],dsub['Dec'][0]
print('Input file: %s\nPosition: %s, %s' % (srcname,ra,dec))

# Open the data file
t = tb.open_file('%s' % fname)

# Setup the figure
figure(figsize=(8,8))
cmap = cm.Spectral_r

# Plot each position traced
alph=0.025
sz = 300
scatter(t.root.scan_pointing.cols.mb01_raj[:],t.root.scan_pointing.cols.mb01_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(0/12.),facecolor=cm.Spectral(0/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb02_raj[:],t.root.scan_pointing.cols.mb02_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(1/12.),facecolor=cm.Spectral(1/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb03_raj[:],t.root.scan_pointing.cols.mb03_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(2/12.),facecolor=cm.Spectral(2/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb04_raj[:],t.root.scan_pointing.cols.mb04_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(3/12.),facecolor=cm.Spectral(3/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb05_raj[:],t.root.scan_pointing.cols.mb05_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(4/12.),facecolor=cm.Spectral(4/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb06_raj[:],t.root.scan_pointing.cols.mb06_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(5/12.),facecolor=cm.Spectral(5/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb07_raj[:],t.root.scan_pointing.cols.mb07_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(6/12.),facecolor=cm.Spectral(6/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb08_raj[:],t.root.scan_pointing.cols.mb08_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(7/12.),facecolor=cm.Spectral(7/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb09_raj[:],t.root.scan_pointing.cols.mb09_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(8/12.),facecolor=cm.Spectral(8/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb10_raj[:],t.root.scan_pointing.cols.mb10_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(9/12.),facecolor=cm.Spectral(9/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb11_raj[:],t.root.scan_pointing.cols.mb11_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(10/12.),facecolor=cm.Spectral(10/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb12_raj[:],t.root.scan_pointing.cols.mb12_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(11/12.),facecolor=cm.Spectral(11/12.),alpha=alph)
scatter(t.root.scan_pointing.cols.mb13_raj[:],t.root.scan_pointing.cols.mb13_dcj[:],s=sz,marker='o',edgecolor=cm.Spectral(12/12.),facecolor=cm.Spectral(12/12.),alpha=alph)

# Show a legend of the multi-beam colours
showmb()

figsave = '\_'.join(srcname.split('_'))
title(figsave)
grid(True,alpha=0.2)
xlabel('Right Ascension (deg)')
ylabel('Declination (deg)')

savefig('%s_beampos.pdf' % src,bbox_inches='tight',transparent=True)


