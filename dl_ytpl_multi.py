import os
import sys
import subprocess
import threading
import time

from youParse import crawl


# Requirement:  youtube-dl installed:
# - http://rg3.github.io/youtube-dl/
# - https://github.com/rg3/youtube-dl
# playlist for test (short videos in it): 
# http://www.youtube.com/playlist?list=PLWKPO_zqFsf3JQvXXNputD6nkmkRqItVu

# Execute this script in the directory in which songs have to be downloaded 
# e.g: Create a 'Myplaylist' directory and from the terminal:
# cd /PathToMyPlaylist/Myplaylist  <= to be in the right directory
# python /PathToTheScriptFolder/playlist_downloader/dl_ytpl_multi.py http://youtubePlaylistAdress.com/343424324... 

# It creates a playlist.txt file, do not delete or edit this file if you don't want to 
# download the same video each time you run the script (it records all downloaded viedos)
# from a given playlist

class OneDownloader(threading.Thread):

	def __init__(self, url_temp):
		threading.Thread.__init__(self)
		self.url_temp = url_temp
		self.result = "none"
		self.filename = ""

	def run(self):
		"""
		DL one song in a list and return new index of the list that need to be downloaded
		"""
		command = "youtube-dl -s --skip-download --get-filename --get-id --get-title '"+self.url_temp+"'"
		videoInfo = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
		(out, err) = videoInfo.communicate()
		out = out.split('\n')
		print "===>>> Checking "+out[0]

		#look in file if the video has already been downloaded
		hasAlreadyBeenDownloaded = False
		j = 0
		a = out[1]
		while j < len(listDL):
			b = listDL[j]
			if listDL[j].find('\n'):
				b = listDL[j].split('\n')[0]
			hasAlreadyBeenDownloaded |= (a == b)
			j += 1

		if not hasAlreadyBeenDownloaded:
			os.system("youtube-dl -i -c --console-title --no-post-overwrites -x --audio-format mp3 '"+self.url_temp+"'")
			self.result = out[1]+'\n'
			self.filename = out[2]
			print "===>>> " + out[0] + ' add to playlist file'
		else:
			print "===>>> " + out[0] + ' has been already downloaded'

###########################
#
# Beginning of the prog
#
###########################
# timer
startTime = time.time()

playlistFile = "playlist.txt"

fWrite = open(playlistFile, 'a')
if len(sys.argv) > 1:
	url = sys.argv[1] # the url from command
	final_url = crawl(url)

	#open file and read it
	fRead = open(playlistFile, 'r')
	listDL = list(fRead)
	fRead.close()

	i = 0
	threads = []
	while i < len(final_url): 
		thread = OneDownloader(final_url[i])
		i += 2
		thread.start()
		threads.append(thread)

	print "===>>> Number of Thread alive "+`threading.activeCount()`

	resultThread = []
	filenameThread = []
	j = 0
	for thread in threads:
		thread.join()
		print "THREAD TERMINATE " + `j`
		resultThread.append(thread.result)
		filenameThread.append(thread.filename)
		j += 1

	i = 0
	while i < len(resultThread):
		id_file = resultThread[i]
		if id_file != "none":
			fWrite.write(id_file)
		if filenameThread[i] != "": # remove video files
			try:
				os.remove(filenameThread[i])
			except:
				print filenameThread[i]+" cannot be removed !!!"   
		i += 1

	#print time of exec
	fWrite.close()
	print time.time() - startTime
else:
	print "ERROR: please add playlist url"

fWrite.close()