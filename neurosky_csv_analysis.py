import numpy as np
import csv as csv
import pandas as pd
import matplotlib.pyplot as plt 
import os
import datetime as dt
import matplotlib.dates as mdates
import zipfile
from matplotlib.dates import WEDNESDAY

dates = []
averages_theta  = []
averages_alpha2 = []
averages_beta3  = []
old_date = []
old_n = 0

visit_dates = ['20160717', '20160720','20160801','20160803','20160824','20160829','20160909','20160921','20161005','20161012']

##-----------------------------------------------------------
## Main
##-----------------------------------------------------------
def main():
	print os.name
	if os.name == 'nt':
		indir = '/py/csv'
	if os.name == 'posix':
		indir = '/home/erfre/Dropbox/Apps/BrainExpress'
	print "date     N    delta  theta  alpha1 alpha2 beta1  beta2  beta3  beta4"

	# -------------------------------------------------------------------------
	# delete old extracted files
	# -------------------------------------------------------------------------
	for root, dirs, files in os.walk(indir):
	    for file in files:
			if os.path.splitext(os.path.join(root, file))[1] == '.csv':
				os.remove(os.path.join(root, file)) 
	
	abs_filenames = []
	dates2 = []
	
	# -------------------------------------------------------------------------
	# unzip
	# -------------------------------------------------------------------------
	for root, dirs, files in os.walk(indir):
	    for file in files:
			if file.endswith('.zip'):
				# ----------------
				# Extract zip file
				# ----------------
				zip_ref = zipfile.ZipFile(os.path.join(root, file), 'r')
				zip_ref.extractall(root)
				zip_ref.close()
				
				abs_filenames.append(os.path.join(root,"FreqValues.csv"))
	
	abs_filenames.sort()
	
	# -------------------------------------------------------------------------
	# Read all csv files
	# -------------------------------------------------------------------------
	for filename in abs_filenames:
		# Find date
		tst = filename.split("_") 
		date = tst[1].split("-")
		date2 = "20%s%s%s" % (date[2],date[0],date[1])
		# Read .csv file
		read_csv_file (filename, date2)
		
	plot_data ()
	plot_smoothed_data ()
			

##-----------------------------------------------------------
## Read .CSV file
##-----------------------------------------------------------
def read_csv_file(filename, date):
	global old_date
	global old_n
	readdata = csv.reader(open(filename))

	data = []

	for row in readdata:
		data.append(row)
  
	Header = data[0]
	data.pop(0)

	values_delta = []
	values_theta = []
	values_alpha1 = []
	values_alpha2 = []
	values_beta1 = []
	values_beta2 = []
	values_beta3 = []
	values_beta4 = []
	for i in range(len(data)):
		values_delta.append(int(data[i][0]))
		values_theta.append(int(data[i][1]))
		values_alpha1.append(int(data[i][2]))
		values_alpha2.append(int(data[i][3]))
		values_beta1.append(int(data[i][4]))
		values_beta2.append(int(data[i][5]))
		values_beta3.append(int(data[i][6]))
		values_beta4.append(int(data[i][7]))

	print date + " %04d" % len(data) + " %06d" % (np.mean(values_delta)) + " %06d" % (np.mean(values_theta)) + " %06d" % (np.mean(values_alpha1)) + " %06d" % (np.mean(values_alpha2)) + " %06d" % (np.mean(values_beta1))+ " %06d" % (np.mean(values_beta2))+ " %06d" % (np.mean(values_beta3))+ " %06d" % (np.mean(values_beta4))

	if np.array_equal(date,old_date):
		if len(data) > old_n:
			dates[-1]=old_date
			averages_theta[-1]=np.mean(values_theta)
			averages_alpha2[-1]=np.mean(values_alpha2)
			averages_beta3[-1]=np.mean(values_beta3)
			old_n = len(data)
		return
		
	old_date = date
	old_n = len(data)
	
	dates.append(old_date)
	averages_theta.append(np.mean(values_theta))
	averages_alpha2.append(np.mean(values_alpha2))
	averages_beta3.append(np.mean(values_beta3))

#	averages_theta.append(np.std(values_theta))
#	averages_alpha2.append(np.std(values_alpha2))
#	averages_beta3.append(np.std(values_beta3))
	
##-----------------------------------------------------------
## Plot data
##-----------------------------------------------------------
def plot_data():
	fig = plt.figure(figsize=(10, 6))
	plt.ylim(0, 80000) 
	fig.patch.set_facecolor('white')	


	len1 = len (averages_theta)
	x = [dt.datetime.strptime(d,'%Y%m%d').date() for d in dates]
	print x
	#plt.xlim(0, len1-1) 
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(WEDNESDAY))	
	plt.plot(x,averages_theta)
	plt.plot(x,averages_alpha2)
	plt.plot(x,averages_beta3)
#	plt.text (x[-1], averages_theta[-1]+2000, "theta", fontsize=10 )
	#plt.text (x[-1], averages_alpha2[-1]+2000, "alpha2", fontsize=10 )
	#plt.text (x[-1], averages_beta3[-1]+2000, "beta3", fontsize=10 )
	t = "theta: %d" % averages_theta[-1]
	plt.text (x[-1], averages_theta[-1], t, fontsize=10 )
	t = "alpha2: %d" % averages_alpha2[-1]
	plt.text (x[-1], averages_alpha2[-1], t, fontsize=10 )
	t = "beta3: %d" % averages_beta3[-1]
	plt.text (x[-1], averages_beta3[-1], t, fontsize=10 )
	plt.gcf().autofmt_xdate()
	for d in visit_dates:
		plt.axvline(dt.datetime.strptime(d,'%Y%m%d').date(),color='black', lw=2)
	plt.show()
	
##-----------------------------------------------------------
## Plot smoothed data
##-----------------------------------------------------------
def plot_smoothed_data():
	SMOOTH = 7
	s_averages_theta = []
	s_averages_alpha2 = []
	s_averages_beta3 = []
	fig = plt.figure(figsize=(10, 6))
	plt.ylim(0, 80000)
	fig.patch.set_facecolor('white')	

	len1 = len (averages_theta)
	x = [dt.datetime.strptime(d,'%Y%m%d').date() for d in dates]
	print x
	#plt.xlim(0, len1-1) 
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(WEDNESDAY))	

	#plt.xlim(SMOOTH, len1+2)
	avg = 0

	# theta
	for i in range(len1):
		avg = avg + averages_theta[i]
		if (i>=(SMOOTH-1)):
			s_averages_theta.append (avg / SMOOTH)
			avg = avg - averages_theta[i-(SMOOTH-1)]
		else:
			s_averages_theta.append (avg / (i+1))
	
	print s_averages_theta
	len2 = len (s_averages_theta)
	plt.subplot(311)
	plt.plot(x[2:],s_averages_theta[2:])
	plt.text (x[-1], s_averages_theta[-1]+2000, "theta", fontsize=10 )
	plt.text (x[-1], s_averages_theta[-1], s_averages_theta[-1], fontsize=10 )
	
	# alpha2
	avg = 0
	for i in range(len1):
		avg = avg + averages_alpha2[i]
		if (i>=(SMOOTH-1)):
			s_averages_alpha2.append (avg / SMOOTH)
			avg = avg - averages_alpha2[i-(SMOOTH-1)]
		else:
			s_averages_alpha2.append (avg / (i+1))
	
	print s_averages_alpha2
	len2 = len (s_averages_alpha2)
	plt.subplot(312)
	plt.plot(x[2:],s_averages_alpha2[2:])
	plt.text (x[-1], s_averages_alpha2[-1]+2000, "alpha2", fontsize=10 )
	plt.text (x[-1], s_averages_alpha2[-1], s_averages_alpha2[-1], fontsize=10 )


	avg = 0
	for i in range(len1):
		avg = avg + averages_beta3[i]
		if (i>=(SMOOTH-1)):
			s_averages_beta3.append (avg / SMOOTH)
			avg = avg - averages_beta3[i-(SMOOTH-1)]
		else:
			s_averages_beta3.append (avg / (i+1))
	
	print s_averages_beta3
	len2 = len (s_averages_beta3)
	plt.subplot(313)

	plt.plot(x[2:],s_averages_beta3[2:])
	plt.text (x[-1], s_averages_beta3[-1]+2000, "beta3", fontsize=10 )
	plt.text (x[-1], s_averages_beta3[-1], s_averages_beta3[-1], fontsize=10 )
	
	plt.gcf().autofmt_xdate()

#	for d1 in dates:
#		for d2 in visit_dates:
#			if (d2 == d1):
#				print dates.index(d1)
#				print d1
#				plt.axvline(dates.index(d1),color='black',  lw=2)

	
	plt.show()
	

##-----------------------------------------------------------
## Call main - if not called as module
##-----------------------------------------------------------
if __name__ == "__main__":
    main()











