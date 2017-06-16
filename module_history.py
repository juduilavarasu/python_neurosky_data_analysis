import numpy as np
import csv as csv
import pandas as pd
import matplotlib.pyplot as plt 
import os
import datetime as dt
import matplotlib.dates as mdates
import zipfile
from matplotlib.dates import WEDNESDAY
import sys


class History:


	def __init__(self):

		self.dates = []
		self.averages_theta  = []
		self.averages_alpha2 = []
		self.averages_beta3  = []
		self.old_date = []
		self.old_n = 0

		self.visit_dates = ['20160717', '20160720','20160801','20160803','20160824','20160829','20160909','20160921','20161005','20161012']

	##-----------------------------------------------------------
	## Main
	##-----------------------------------------------------------
	def analyze(self):
		print os.name
		indir = './'
		print "date     N    delta  theta  alpha1 alpha2 beta1  beta2  beta3  beta4"

		# -------------------------------------------------------------------------
		# unzip
		# -------------------------------------------------------------------------
		abs_filenames = []
		dates2 = []

		for root, dirs, files in os.walk(indir):
			for file in files:
				if file.endswith('.zip'):
					# ----------------
					# Extract zip file
					# ----------------
					print 'extract ' + os.path.join(root, file) + ' to'
					print os.path.join(root, file[:-4])
					zip_ref = zipfile.ZipFile(os.path.join(root, file), 'r')
					zip_ref.extractall(os.path.join(root, file[:-4]))
					zip_ref.close()
					
					abs_filenames.append(os.path.join(root,file[:-4],"FreqValues.csv"))
		
		abs_filenames.sort()
		
		#sys.exit ()
		
		# -------------------------------------------------------------------------
		# Read all csv files
		# -------------------------------------------------------------------------
		for filename in abs_filenames:
			# Find date
			tst = filename.split("_") 
			date = tst[1].split("-")
			date2 = "20%s%s%s" % (date[2],date[0],date[1])
			# Read .csv file
			self.read_csv_file (filename, date2)
			
		self.plot_data ()
		self.plot_smoothed_data ()
				

	##-----------------------------------------------------------
	## Read .CSV file
	##-----------------------------------------------------------
	def read_csv_file(self,filename, date):
		global old_date
		global old_n
		readdata = csv.reader(open(filename))

		data = []

		for row in readdata:
			data.append(row)
	  
		Header = data[0]
		data.pop(0)

		self.values_delta = []
		self.values_theta = []
		self.values_alpha1 = []
		self.values_alpha2 = []
		self.values_beta1 = []
		self.values_beta2 = []
		self.values_beta3 = []
		self.values_beta4 = []
		for i in range(len(data)):
			self.values_delta.append(int(data[i][0]))
			self.values_theta.append(int(data[i][1]))
			self.values_alpha1.append(int(data[i][2]))
			self.values_alpha2.append(int(data[i][3]))
			self.values_beta1.append(int(data[i][4]))
			self.values_beta2.append(int(data[i][5]))
			self.values_beta3.append(int(data[i][6]))
			self.values_beta4.append(int(data[i][7]))

		print date + " %04d" % len(data) + " %06d" % (np.mean(self.values_delta)) + " %06d" % (np.mean(self.values_theta)) + " %06d" % (np.mean(self.values_alpha1)) + " %06d" % (np.mean(self.values_alpha2)) + " %06d" % (np.mean(self.values_beta1))+ " %06d" % (np.mean(self.values_beta2))+ " %06d" % (np.mean(self.values_beta3))+ " %06d" % (np.mean(self.values_beta4))

		if np.array_equal(date,self.old_date):
			if len(data) > self.old_n:
				self.dates[-1]=self.old_date
				self.averages_theta[-1]=np.mean(self.values_theta)
				self.averages_alpha2[-1]=np.mean(self.values_alpha2)
				self.averages_beta3[-1]=np.mean(self.values_beta3)
				self.old_n = len(data)
			return
			
		self.old_date = date
		self.old_n = len(data)
		
		self.dates.append(self.old_date)
		self.averages_theta.append(np.mean(self.values_theta))
		self.averages_alpha2.append(np.mean(self.values_alpha2))
		self.averages_beta3.append(np.mean(self.values_beta3))

	#	averages_theta.append(np.std(values_theta))
	#	averages_alpha2.append(np.std(values_alpha2))
	#	averages_beta3.append(np.std(values_beta3))
		
	##-----------------------------------------------------------
	## Plot data
	##-----------------------------------------------------------
	def plot_data(self):
		fig = plt.figure(figsize=(10, 6))
		plt.ylim(0, 80000) 
		fig.patch.set_facecolor('white')	


		len1 = len (self.averages_theta)
		x = [dt.datetime.strptime(d,'%Y%m%d').date() for d in self.dates]
		#print x
		#plt.xlim(0, len1-1) 
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
		plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(WEDNESDAY))	
		ax = plt.subplot(311)
		#ax.set_title ("Theta")
		plt.plot(x,self.averages_theta)
		t = "theta: %d" % self.averages_theta[-1]
		plt.text (x[-1], self.averages_theta[-1], t, fontsize=10 )
		ax = plt.subplot(312)
		#ax.set_title ("Alpha2")
		plt.plot(x,self.averages_alpha2)
		t = "alpha2: %d" % self.averages_alpha2[-1]
		plt.text (x[-1], self.averages_alpha2[-1], t, fontsize=10 )
		ax = plt.subplot(313)
		#ax.set_title ("Beta3")
		plt.plot(x,self.averages_beta3)
		t = "beta3: %d" % self.averages_beta3[-1]
		plt.text (x[-1], self.averages_beta3[-1], t, fontsize=10 )
		plt.gcf().autofmt_xdate()
		for d in self.visit_dates:
			plt.axvline(dt.datetime.strptime(d,'%Y%m%d').date(),color='black', lw=2)
		plt.show()
		
	##-----------------------------------------------------------
	## Plot smoothed data
	##-----------------------------------------------------------
	def plot_smoothed_data(self):
		SMOOTH = 7
		s_averages_theta = []
		s_averages_alpha2 = []
		s_averages_beta3 = []
		fig = plt.figure(figsize=(10, 6))
		plt.ylim(0, 80000)
		fig.patch.set_facecolor('white')	

		len1 = len (self.averages_theta)
		x = [dt.datetime.strptime(d,'%Y%m%d').date() for d in self.dates]
		#print x
		#plt.xlim(0, len1-1) 
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
		plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(WEDNESDAY))	

		#plt.xlim(SMOOTH, len1+2)
		avg = 0

		# theta
		for i in range(len1):
			avg = avg + self.averages_theta[i]
			if (i>=(SMOOTH-1)):
				s_averages_theta.append (avg / SMOOTH)
				avg = avg - self.averages_theta[i-(SMOOTH-1)]
			else:
				s_averages_theta.append (avg / (i+1))
		
		#print s_averages_theta
		len2 = len (s_averages_theta)
		plt.subplot(311)
		plt.plot(x[2:],s_averages_theta[2:])
		t = "theta: %d" % s_averages_theta[-1]
		plt.text (x[-1], s_averages_theta[-1], t, fontsize=10 )
		
		# alpha2
		avg = 0
		for i in range(len1):
			avg = avg + self.averages_alpha2[i]
			if (i>=(SMOOTH-1)):
				s_averages_alpha2.append (avg / SMOOTH)
				avg = avg - self.averages_alpha2[i-(SMOOTH-1)]
			else:
				s_averages_alpha2.append (avg / (i+1))
		
		#print s_averages_alpha2
		len2 = len (s_averages_alpha2)
		plt.subplot(312)
		plt.plot(x[2:],s_averages_alpha2[2:])
		t = "alpha2: %d" % s_averages_alpha2[-1]
		plt.text (x[-1], s_averages_alpha2[-1], t, fontsize=10 )


		avg = 0
		for i in range(len1):
			avg = avg + self.averages_beta3[i]
			if (i>=(SMOOTH-1)):
				s_averages_beta3.append (avg / SMOOTH)
				avg = avg - self.averages_beta3[i-(SMOOTH-1)]
			else:
				s_averages_beta3.append (avg / (i+1))
		
		#print s_averages_beta3
		len2 = len (s_averages_beta3)
		plt.subplot(313)

		plt.plot(x[2:],s_averages_beta3[2:])
		t = "beta3: %d" % s_averages_beta3[-1]
		plt.text (x[-1], s_averages_beta3[-1], t, fontsize=10 )
		
		plt.gcf().autofmt_xdate()

	#	for d1 in dates:
	#		for d2 in visit_dates:
	#			if (d2 == d1):
	#				print dates.index(d1)
	#				print d1
	#				plt.axvline(dates.index(d1),color='black',  lw=2)

		
		plt.show()
	












