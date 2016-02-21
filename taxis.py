import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams

start=time.time()
csv=pd.read_csv('yellow_tripdata_2015-06.csv')
#csv=pd.read_csv('yellow_tripdata_2015-06.csv', nrows=100000)

#-----pre-processing-----#
#csv=csv[csv.tip_amount>=0.0]# delete values smaller than zero->error in the data
#csv=csv[csv.tip_amount<50.0]# delete very large tip
#csv=csv[csv.payment_type==1]
#csv=csv[csv.pickup_latitude<=40.93]#delete missing coordinates
#csv=csv[csv.pickup_latitude>=40.48]
#csv=csv[csv.pickup_longitude<=-73.69]
#csv=csv[csv.pickup_longitude>=-74.26]
#csv=csv[csv.dropoff_longitude!=0.0]
#csv=csv[csv.dropoff_latitude!=0.0]
print "number of valid data points: %s" % (len(csv))


tips=csv['tip_amount'].as_matrix()#store some columns as np.array
passengers=csv['passenger_count'].as_matrix()
distances=csv['trip_distance'].as_matrix()
x=csv['pickup_longitude'].as_matrix()
y=csv['pickup_latitude'].as_matrix()
mean=np.mean(tips)#compute average tip
stddev=np.std(tips)#compute standard deviation
#plt.figure()

#-----plot of pick-up points-----#
#http://www.danielforsyth.me/mapping-nyc-taxi-data/

pd.options.display.mpl_style = 'default' #Better Styling  
new_style = {'grid': False} #Remove grid  
matplotlib.rc('axes', **new_style)  
#matplotlib.rc('xtick',labelsize=30)
#matplotlib.rc('ytick',labelsize=30)
rcParams['figure.figsize'] = (17.5, 17) #Size of figure  
rcParams['figure.dpi'] = 250

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 25}

matplotlib.rc('font', **font)
P=csv.plot(kind='scatter', x='pickup_longitude', y='pickup_latitude',color='white',xlim=(-74.26,-73.69),ylim=(40.48, 40.93),s=.02,alpha=0.3)
P.set_axis_bgcolor('black') #Background Color
plt.savefig('test.png')

#-----1d histogram of tips-----#
'''
plt.hist(tips,bins=200)
plt.yscale('log',nonposy='clip')
plt.ylim(ymin=0.1)
plt.xlabel('amount tips [$]')
plt.ylabel('counts')
plt.savefig('tips_histogram.png')
'''

#-----various 2d histograms with hexagonal binning-----#

#-----plot of different minimum count thresholds-----#
'''
gsize=100

fig, ax= plt.subplots(nrows=2,ncols=2)
histogram=ax[0,0].hexbin(x,y,C=tips,reduce_C_function=np.mean,gridsize=gsize,mincnt=0)
#fig.colorbar(histogram1)
histogram=ax[0,1].hexbin(x,y,C=tips,reduce_C_function=np.mean,gridsize=gsize,mincnt=10)
histogram=ax[1,0].hexbin(x,y,C=tips,reduce_C_function=np.mean,gridsize=gsize,mincnt=100)
histogram=ax[1,1].hexbin(x,y,C=tips,reduce_C_function=np.mean,gridsize=gsize,mincnt=1000)
#print histogram.get_array()
#fig.colorbar(histogram)
plt.savefig('hexbin%s.pdf' % (gsize))
'''
#-----plot of tip amount-----#
'''
gsize=300
tips_threshold=stddev
fig= plt.figure()
ax=fig.add_subplot(111)
histogram=plt.hexbin(x,y,C=tips,reduce_C_function=np.mean,gridsize=gsize,mincnt=50)
histogram.set_array(np.where(histogram.get_array()-mean>=tips_threshold,12.5,0))
#histogram.set_array(histogram.get_array()-mean)
plt.xlabel('pickup_latitude')
plt.ylabel('pickup_longitude')
#cbar=plt.colorbar(histogram)
#cbar.set_label('average tip per bin [$]')
#plt.savefig('hexbin%s.pdf' % (gsize))
ax.text(-73.9, 40.89,'blue: tip below threshold \n red: tip above threshold')
plt.savefig('binary_plot%s.pdf' % (gsize))
'''
#-----plot of passenger counts-----#
'''
pfig=plt.figure()
gsize=300
p_histogram=plt.hexbin(x,y,C=passengers,reduce_C_function=np.mean,gridsize=gsize,mincnt=100)
plt.xlabel('pickup_latitude')
plt.ylabel('pickup_longitude')
p_cbar=plt.colorbar(p_histogram)
p_cbar.set_label('average passenger count per bin')
plt.savefig('passengers%s.pdf' % (gsize))
'''
#-----plot of travel distance-----#
'''
dfig=plt.figure()
gsize=300
d_histogram=plt.hexbin(x,y,C=distances,reduce_C_function=np.mean,gridsize=gsize,mincnt=100)
plt.xlabel('pickup_latitude')
plt.ylabel('pickup_longitude')
d_cbar=plt.colorbar(d_histogram)
d_cbar.set_label('average trip distance per bin [miles]')
plt.savefig('distances%s.pdf' % (gsize))
'''

end=time.time()
comptime=end-start
print "average tip: %s" % (mean)
print "standard deviation: %s" % (stddev)
print "computation time: %ss" % (comptime)


#plt.show()
