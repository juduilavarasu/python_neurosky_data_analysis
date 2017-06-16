from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory
from module_session import Session
from module_dropbox import TransferData
from kivy.core.window import Window
from module_history import History
from kivy.garden.graph import MeshLinePlot
import time
import zipfile
import os
import numpy as np


#---------------------------------------------------------------
#
# Class:
# EEGRoot - Root screen
#
#---------------------------------------------------------------
class EEGRoot(BoxLayout):
	current_weather = ObjectProperty()
	
	def __init__(self, **kwargs):
		super(EEGRoot, self).__init__(**kwargs)




#---------------------------------------------------------------
#
# Class:
# OverviewForm - Main widget
#
#---------------------------------------------------------------
class SessionOverviewForm(BoxLayout):
	sessions_results = ObjectProperty()
	theta_graph = ObjectProperty()
	alpha2_graph = ObjectProperty()
	beta3_graph = ObjectProperty()
	label_theta_avg = ObjectProperty()
	label_alpha2_avg = ObjectProperty()
	label_beta3_avg = ObjectProperty()
#	active_profile = ObjectProperty(None)


	def __init__(self, **kwargs):
		super(SessionOverviewForm, self).__init__(**kwargs)
		access_token = ''
		self.transferData = TransferData(access_token)
		self.theta_plot = MeshLinePlot(color=[0, 0, 1, 1])
		self.alpha2_plot = MeshLinePlot(color=[0, 1, 0, 1])
		self.beta3_plot = MeshLinePlot(color=[1, 0, 0, 1])
		self.active_profile = 'raw'
		self.selected_session = None



	def get_session_list(self):
		self.cities = self.transferData.lfolder ('/Apps/BrainExpress')
		self.cities.reverse()
		self.sessions_results.item_strings = self.cities
		del self.sessions_results.adapter.data[:]	
		self.sessions_results.adapter.data.extend(self.cities)
		self.sessions_results._trigger_reset_populate()
		#self.sessions_results.scroll_view.bar_width = "20dp"
		self.sessions_results.container.parent.bar_width = "10dp"
		self.sessions_results.container.parent.scroll_type=['bars','content']

	def args_converter(self, index, data_item):
		tst = data_item.split("_") 
		date = tst[1].split("-")
		date2 = "20%s%s%s" % (date[2],date[0],date[1])

		city = data_item
		return {'session': (city, date2)}

	def analyse_history(self):
		# download all files
		self.get_session_list() # get the list
		for index, element in enumerate(self.cities):
			print 'downloading {} ({} of {})'.format(element, index, len(self.cities))
			if not os.path.exists('./' + element):
				self.transferData.download_file ('/Apps/BrainExpress/' + element,'./' + element)
		
		# analyse all files
		history = History()
		history.analyze()
		
	def test(self):
		print 'test'
		
	def analyze_session(self, session=None):
		relative_file_name = session[0]
		if session is None:
			return
		self.selected_session = session
		self.transferData.download_file ('/Apps/BrainExpress/' + relative_file_name,'./' + relative_file_name)
		
		# -------------------------------------------------------------------------
		# unzip
		# -------------------------------------------------------------------------
		filename = './' + relative_file_name
		zip_ref = zipfile.ZipFile(filename, 'r')
		zip_ref.extractall(filename[:-4])
		zip_ref.close()
		abs_filename = os.path.join(filename[:-4],"FreqValues.csv")

		# -------------------------------------------------------------------------
		# Read all csv files
		# -------------------------------------------------------------------------
		# Find date
		obj_session = Session ()
		obj_session.read_csv_file (abs_filename, session[1])
		
#		self.theta_graph.add_plot(self.theta_plot)
#		self.theta_graph.xmax = len(obj_session.values_theta)
#		self.theta_plot.points = [(i, j) for i, j in enumerate(obj_session.values_theta)] 

#		self.alpha2_graph.add_plot(self.alpha2_plot)
#		self.alpha2_graph.xmax = len(obj_session.values_alpha2)
#		self.alpha2_plot.points = [(i, j) for i, j in enumerate(obj_session.values_alpha2)] 

#		self.beta3_graph.add_plot(self.beta3_plot)
#		self.beta3_graph.xmax = len(obj_session.values_beta3)
#		self.beta3_plot.points = [(i, j) for i, j in enumerate(obj_session.values_beta3)] 

#		obj_session.plot_data ()
		if self.active_profile == 'raw':
			#obj_session.calc_smoothed_data ()
			self.theta_graph.add_plot(self.theta_plot)
			work_list = obj_session.values_theta
			self.theta_graph.xmax = len(work_list)
			self.theta_graph.ymax = max(work_list)
			self.theta_graph.ymin = min(work_list)
			self.theta_plot.points = [(i, j) for i, j in enumerate(work_list)] 
			self.label_theta_avg.text = str(np.mean(obj_session.values_theta))
	
			self.alpha2_graph.add_plot(self.alpha2_plot)
			work_list = obj_session.values_alpha2
			self.alpha2_graph.xmax = len(work_list)
			self.alpha2_graph.ymax = max(work_list)
			self.alpha2_graph.ymin = min(work_list)
			self.alpha2_plot.points = [(i, j) for i, j in enumerate(work_list)] 
			self.label_alpha2_avg.text = str(np.mean(obj_session.values_alpha2))
	
			self.beta3_graph.add_plot(self.beta3_plot)
			work_list = obj_session.values_beta3
			self.beta3_graph.xmax = len(work_list)
			self.beta3_graph.ymax = max(work_list)
			self.beta3_graph.ymin = min(work_list)
			self.beta3_plot.points = [(i, j) for i, j in enumerate(work_list)] 
			self.label_beta3_avg.text = str(np.mean(obj_session.values_beta3))
	#		obj_session.plot_data_5min()
#			obj_session.plot_smoothed_data ()
		if self.active_profile == 'smooth':
			obj_session.calc_smoothed_data ()
			self.theta_graph.add_plot(self.theta_plot)
			work_list = obj_session.s_theta[obj_session.SMOOTH:]
			self.theta_graph.xmax = len(work_list)
			self.theta_graph.ymax = max(work_list)
			self.theta_graph.ymin = min(work_list)
			self.theta_plot.points = [(i, j) for i, j in enumerate(work_list)] 
			self.label_theta_avg.text = str(np.mean(obj_session.values_theta))
	
			self.alpha2_graph.add_plot(self.alpha2_plot)
			work_list = obj_session.s_alpha2[obj_session.SMOOTH:]
			self.alpha2_graph.xmax = len(work_list)
			self.alpha2_graph.ymax = max(work_list)
			self.alpha2_graph.ymin = min(work_list)
			self.alpha2_plot.points = [(i, j) for i, j in enumerate(work_list)] 
			self.label_alpha2_avg.text = str(np.mean(obj_session.values_alpha2))
	
			self.beta3_graph.add_plot(self.beta3_plot)
			work_list = obj_session.s_beta3[obj_session.SMOOTH:]
			self.beta3_graph.xmax = len(work_list)
			self.beta3_graph.ymax = max(work_list)
			self.beta3_graph.ymin = min(work_list)
			self.beta3_plot.points = [(i, j) for i, j in enumerate(work_list)] 
			self.label_beta3_avg.text = str(np.mean(obj_session.values_beta3))
	#		obj_session.plot_data_5min()
#			obj_session.plot_smoothed_data ()
		self.transferData.remove_folder (filename[:-4])
		
 	def set_active(self, cb, value):
        #"this will be called everytime a checkbox status change"
		if cb.active:
			self.active_profile = value
			self.analyze_session(self.selected_session)
	
class SessionButton(ListItemButton):
	session = ListProperty()
		
		
#---------------------------------------------------------------
#
# Class:
# WeatherApp - Main class
#
#---------------------------------------------------------------
class EEGApp(App):
	pass
	
if __name__ == '__main__':
	EEGApp().run()
