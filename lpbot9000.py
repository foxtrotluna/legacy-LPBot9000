
# LPBot9000 - by Luna Winters
# This bot will scape a youtube channel and if there are any new videos,
# post to a specified subreddit.
# Please don't run an LPBot on a subreddit without the moderators permission
#
#The MIT License (MIT)
#
#Copyright (c) 2014 Luna Winters
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
import time
import praw
import urllib.request
import json
import sys
import sendemail

api_key = '' #Youtube API key goes here
channel_id = '' #Youtube channel ID to watch goes here
user_agent = 'LPBot9000' #UserAgent of the bot
user_name = '' #Bots Username
password = '' #Bots password
subreddit = '' #Subreddit to post to

call_url = 'https://www.googleapis.com/youtube/v3/search?key='+api_key+'&channelId='+channel_id+'&part=snippet,id&order=date&maxResults=20'

r = praw.Reddit(user_agent=user_agent)
r.login(user_name,password)

##Can remove While loop and sleep and run as a cronjob instead.
while True:
	#Print current running time to console
	currenttime = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
	print ('LPBot9000 running at: ' + currenttime)

	try:
		posted_videos = open('videos.json','r+') #Read the current JSON formatted list of videos processed
		video_arr = json.loads(posted_videos.read()) #Read into array

		response = urllib.request.urlopen(call_url); #Call the API URL to get the 20 last videos
		data = json.loads(response.readall().decode('utf-8')) #Read the result into a JSON array
		for item in data['items']: #For each Item in the array
			video =  item['id'] #Grab the current video
			if 'videoId' in video: #If the video has an ID
				vid_id = video['videoId'] #Grab the video ID
				if vid_id not in video_arr: #If the videoID isn't in the JSON file of videos processed
					video_arr.append(vid_id) #Add this videoID to the processed array
					video_url = 'http://www.youtube.com/watch?v='+vid_id #Set the video URL
					title = item['snippet']['title'] #Grab the video title
					r.submit(subreddit,title,url=video_url) #Submit the video to reddit
					newvideo =  'new video ' + title # New video string
					sendemail.sendemail("LPBot9000 new Video",newvideo +' '+ video_url) #Send email to address
					print (newvideo) #Print the new video to console
		clear_vid = open('videos.json','w') #Re-open the posted videos file in Write mode
		clear_vid.close() #Close again to clear the file
		jdata = json.dumps(video_arr, indent=4, skipkeys=False, sort_keys=False) #Dump the json array
		posted_videos.seek(0) #Seek to the beginning of the posted_videos file
		posted_videos.write(jdata) #Write the json data

		posted_videos.close()
		print ('LPBot9000 finished at: ' + time.strftime("%b %d %Y %H:%M:%S",time.localtime())) #Print finished to console
	except Exception as e: #If error
		errortext = "Error running LPBot9000 \n{0}".format(e) #Format the error text
		sendemail.sendemail("LPBot9000 Error", errortext) #Email the error
		print (errortext) #Print the error text
		pass
	time.sleep(120) #Wait for 2 minutes
