import numpy as np
import csv as csv
import pandas as pd
import matplotlib.pyplot as plt 
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.dates import WEDNESDAY
import sys



#---------------------------------------------------------------
#
# Class:
# Session
#
#---------------------------------------------------------------
class Session:

	def __init__(self):
		self.values_delta = []
		self.values_theta = []
		self.values_alpha1 = []
		self.values_alpha2 = []
		self.values_beta1 = []
		self.values_beta2 = []
		self.values_beta3 = []
		self.values_beta4 = []
		self.SMOOTH = 300
		self.s_theta = []
		self.s_alpha2 = []
		self.s_beta3 = []

	##-----------------------------------------------------------
	## Read .CSV file
	##-----------------------------------------------------------
	def read_csv_file(self,filename, date):
		readdata = csv.reader(open(filename))

		data = []

		for row in readdata:
			data.append(row)
	  
		Header = data[0]
		data.pop(0)

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
		
	##-----------------------------------------------------------
	## Plot data
	##-----------------------------------------------------------
#	def plot_data(self):
#		fig = plt.figure(figsize=(10, 6))
#		fig.patch.set_facecolor('white')	
#
#		len1 = len (self.values_theta)
#		ax = plt.subplot(311)
#		str = 'Theta, avg = {}'.format (np.mean(self.values_theta))
#		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
#		plt.plot(self.values_theta)
#		plt.xlim(0, len1)
#		plt.ylim(0, 500000)
#
#		ax = plt.subplot(312)
#		str = 'Alpha2, avg = {}'.format (np.mean(self.values_alpha2))
#		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
#		plt.plot(self.values_alpha2)
#		plt.xlim(0, len1)
#		plt.ylim(0, 200000)
#
#		ax = plt.subplot(313)
#		str = 'Beta3, avg = {}'.format (np.mean(self.values_beta3))
#		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
#		plt.plot(self.values_beta3)
#		plt.xlim(0, len1)
#		plt.ylim(0, 50000)

#		plt.show()

	def plot_data_5min(self):
		SECONDS = 300

		fig = plt.figure(figsize=(10, 6))
		fig.patch.set_facecolor('white')	

		len1 = len (self.values_theta[0:SECONDS])

		ax = plt.subplot(321)
		str = 'Theta start, avg = {}'.format (np.mean(self.values_theta[0:SECONDS]))
		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
		plt.plot(self.values_theta[0:SECONDS])
		plt.xlim(0, len1)
		plt.ylim(0, 500000)

		ax = plt.subplot(323)
		str = 'Alpha2 start, avg = {}'.format (np.mean(self.values_alpha2[0:SECONDS]))
		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
		plt.plot(self.values_alpha2[0:SECONDS])
		plt.xlim(0, len1)
		plt.ylim(0, 200000)

		ax = plt.subplot(325)
		str = 'Beta3 start, avg = {}'.format (np.mean(self.values_beta3[0:SECONDS]))
		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
		plt.plot(self.values_beta3[0:SECONDS])
		plt.xlim(0, len1)
		plt.ylim(0, 50000)

		ax = plt.subplot(322)
		str = 'Theta end, avg = {}'.format (np.mean(self.values_theta[-SECONDS:]))
		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
		plt.plot(self.values_theta[-SECONDS:])
		plt.xlim(0, len1)
		plt.ylim(0, 500000)

		ax = plt.subplot(324)
		str = 'Alpha2 end, avg = {}'.format (np.mean(self.values_alpha2[-SECONDS:]))
		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
		plt.plot(self.values_alpha2[-SECONDS:])
		plt.xlim(0, len1)
		plt.ylim(0, 200000)

		ax = plt.subplot(326)
		str = 'Beta3 end, avg = {}'.format (np.mean(self.values_beta3[-SECONDS:]))
		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
		plt.plot(self.values_beta3[-SECONDS:])
		plt.xlim(0, len1)
		plt.ylim(0, 50000)
		plt.show()
		
	##-----------------------------------------------------------
	## Plot smoothed data
	##-----------------------------------------------------------
	def plot_smoothed_data(self):
		SMOOTH = 300
		s_theta = []
		s_alpha2 = []
		s_beta3 = []
		fig = plt.figure(figsize=(10, 6))
		fig.patch.set_facecolor('white')	

		len1 = len (self.values_theta)

		# theta
		avg = 0
		for i in range(len1):
			avg = avg + self.values_theta[i]
			if (i>=(SMOOTH-1)):
				s_theta.append (avg / SMOOTH)
				avg = avg - self.values_theta[i-(SMOOTH-1)]
			else:
				s_theta.append (avg / (i+1))
		
		len2 = len (s_theta)
		ax = plt.subplot(311)
		str = 'Theta, avg = {}'.format (np.mean(self.values_theta))
		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)

		plt.xlim(0, len2-SMOOTH)
		plt.plot(s_theta[SMOOTH:])
		
		# alpha2
		avg = 0
		for i in range(len1):
			avg = avg + self.values_alpha2[i]
			if (i>=(SMOOTH-1)):
				s_alpha2.append (avg / SMOOTH)
				avg = avg - self.values_alpha2[i-(SMOOTH-1)]
			else:
				s_alpha2.append (avg / (i+1))
		
		len2 = len (s_alpha2)
		ax = plt.subplot(312)
		str = 'Alpha2, avg = {}'.format (np.mean(self.values_alpha2))
		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
		plt.xlim(0, len2-SMOOTH)
		plt.plot(s_alpha2[SMOOTH:])


		avg = 0
		for i in range(len1):
			avg = avg + self.values_beta3[i]
			if (i>=(SMOOTH-1)):
				s_beta3.append (avg / SMOOTH)
				avg = avg - self.values_beta3[i-(SMOOTH-1)]
			else:
				s_beta3.append (avg / (i+1))
		
		len2 = len (s_beta3)
		ax = plt.subplot(313)
		str = 'Beta3, avg = {}'.format (np.mean(self.values_beta3))
		ax.text(.5,.9,str, horizontalalignment='center', transform=ax.transAxes)
		plt.xlim(0, len2-SMOOTH)
		plt.plot(s_beta3[SMOOTH:])
		plt.show()




	def calc_smoothed_data(self):

		len1 = len (self.values_theta)

		# theta
		avg = 0
		for i in range(len1):
			avg = avg + self.values_theta[i]
			if (i>=(self.SMOOTH-1)):
				self.s_theta.append (avg / self.SMOOTH)
				avg = avg - self.values_theta[i-(self.SMOOTH-1)]
			else:
				self.s_theta.append (avg / (i+1))
		
		
		# alpha2
		avg = 0
		for i in range(len1):
			avg = avg + self.values_alpha2[i]
			if (i>=(self.SMOOTH-1)):
				self.s_alpha2.append (avg / self.SMOOTH)
				avg = avg - self.values_alpha2[i-(self.SMOOTH-1)]
			else:
				self.s_alpha2.append (avg / (i+1))
		


		avg = 0
		for i in range(len1):
			avg = avg + self.values_beta3[i]
			if (i>=(self.SMOOTH-1)):
				self.s_beta3.append (avg / self.SMOOTH)
				avg = avg - self.values_beta3[i-(self.SMOOTH-1)]
			else:
				self.s_beta3.append (avg / (i+1))
		
	
