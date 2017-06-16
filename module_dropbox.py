import dropbox
import os, os.path
import errno
import shutil
import sys




#---------------------------------------------------------------
#
# Class:
# Dropbox transfer
#
#---------------------------------------------------------------
class TransferData:
	def __init__(self, access_token):
		self.access_token = access_token
	
	def mkdir_p(self, path):
		try:
			os.makedirs(path)
		except OSError as exc: # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(path):
				pass
			else: raise

	def upload_file(self, file_from, file_to):
		#"""upload a file to Dropbox using API v2
		#"""
		dbx = dropbox.Dropbox(self.access_token)

		with open(file_from, 'rb') as f:
			dbx.files_upload(f, file_to, mode=dropbox.files.WriteMode.overwrite)

	def download_file(self, file_from, file_to):
        #"""download a file from Dropbox using API v2
        #"""
		dbx = dropbox.Dropbox(self.access_token)

		self.mkdir_p(os.path.dirname(file_to))
		
		with open(file_to, "wb") as f:
			metadata, res = dbx.files_download(path=file_from)
			f.write(res.content)
			
	def lfolder(self, path):
		files = []
		print self.access_token
		dbx = dropbox.Dropbox(self.access_token)
		for entry in dbx.files_list_folder(path).entries:
			print entry.name
			files.append(entry.name)
		return files
			
	def remove_folder(self,path):
		# check if folder exists
		if os.path.exists(path):
			# remove if exists
			shutil.rmtree(path)
