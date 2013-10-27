import os
import sys
import subprocess
import time

from youParse import crawl


# timer
startTime = time.time()

#playlist for test: http://www.youtube.com/playlist?list=PLWKPO_zqFsf3JQvXXNputD6nkmkRqItVu
playlistFile = "playlist.txt"

if len(sys.argv) > 1:
	url = sys.argv[1] #the url from command
	final_url = crawl(url)

	#open file and read it
	try:
		fRead = open(playlistFile, 'r')
		listDL = list(fRead)
		fRead.close()
	except:
		listDL = list()

	fWrite = open(playlistFile, 'a+')
	i = 0
	while i < len(final_url):  
		command = "youtube-dl -s --get-filename --get-id --get-title '"+final_url[i]+"'"
		videoInfo = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
		(out, err) = videoInfo.communicate()
		out = out.split('\n')
		print "===>>> Checking "+out[0]

		#look in file if the video has already been downloaded
		print "===>>>In progress... "+str(i/2+1)+"/"+str(len(final_url)/2)
		if (out[1]+'\n') in listDL:
			print "===>>> "+out[0]+' has been already downloaded'
		else:
			os.system("youtube-dl -i -c --console-title --no-post-overwrites -x --audio-format mp3 '"+final_url[i]+"'")
			fWrite.write(out[1]+'\n')#write id in file
			try:
				os.remove(out[2])#delete mp4
			except:
				print "===>>> "+out[2]+" file cannot be removed"	
			print "===>>> "+out[0]+' add to playlist file'
	
		i += 2

	fWrite.close()
	#print time of exec
	print time.time() - startTime
else:
	print "ERROR: please add playlist url"

