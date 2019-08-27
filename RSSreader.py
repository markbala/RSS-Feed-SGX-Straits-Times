# SGX Company Announcements and Straits Times RSS Feeds on Windows
# Feeds are updated every minute
# The MIT License (MIT)
# Copyright (c) 2017 Mark Balakrishnan
import feedparser, sys, random
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
from tkinter import *

stDatabase, sgxDatabase = [], []
def initialiseRSS():
	try:
		stFeed = feedparser.parse('http://www.straitstimes.com/news/singapore/rss.xml')
		sgxFeed = feedparser.parse('http://infopub.sgx.com/SitePages/RSSAnnouncementToday.aspx')
		for i in range(0,12):
			stDatabase.append(stFeed.entries[i].summary_detail.value.replace("<br /><br />"," "))
			sgxDatabase.append(sgxFeed.entries[i].title+" "+sgxFeed.entries[i].summary_detail.value)
	except:
		pass

def loop():
	try:
		stFeed = feedparser.parse('http://www.straitstimes.com/news/singapore/rss.xml')
		sgxFeed = feedparser.parse('https://links.sgx.com/SitePages/RSSAnnouncementToday.aspx')
		for i in range(0,5):
			if stFeed.entries[i].summary_detail.value.replace("<br /><br />"," ") in stDatabase:
				continue
			else:
				print('new ST update!')
				stDatabase.insert(0,stFeed.entries[i].summary_detail.value.replace("<br /><br />"," "))
				stDatabase.pop()
		for i in range(0,5):
			if sgxFeed.entries[i].title+" "+sgxFeed.entries[i].summary_detail.value in sgxDatabase:
				continue
			else:
				print('new SGX update!')
				sgxDatabase.insert(0,sgxFeed.entries[i].title+" "+sgxFeed.entries[i].summary_detail.value)
				sgxDatabase.pop()
		print('completed loop')
	except:
		print(sys.exc_info())
		print('Loop crashed. Restarting...')

q = 0
def updater():
	global q
	if q % 7 == 0:
		# only calls loop() every 10 * 7 = 70secs
		loop()
	if q % 2 == 0:
		# alternates between sgx and st news, going through the 10 most recent rss entries for each feed
		feed.config(text=sgxDatabase[random.randint(0,9)])
		feed.grid(row=0,column=2)
	else:
		feed.config(text=stDatabase[random.randint(0,9)])
		feed.grid(row=0,column=2)
	q += 1
	feed.after(10000,updater)

def StartMove(event):
	global xx, yy
	xx, yy = event.x, event.y

def StopMove(event):
    x, y = None, None

def OnMotion(event):
    x = (event.x_root - xx - feed.winfo_rootx() + feed.winfo_rootx())
    y = (event.y_root - yy - feed.winfo_rooty() + feed.winfo_rooty())
    root.geometry("+%s+%s" % (x, y))

root = Tk()
root.overrideredirect(1) #removes title/menu bar
root.wm_attributes("-topmost", 1) #always on top
root.wm_attributes('-alpha',0.9) #transparency level
feedFrame = Frame(root).grid(row=0,column=0)
quit = Button(feedFrame, text='quit', command=root.destroy).grid(column=0,row=0)
title = Label(feedFrame, text="RSS Feed: ",font=("Calibri",12), fg='red', bg='black').grid(column=1,row=0)
feed = Label(feedFrame, text='<RSS feed goes here>',font=("Calibri", 12), fg='yellow', bg='black')
feed.grid(column=2,row=0)
feed.bind("<ButtonPress-1>", StartMove)
feed.bind('<ButtonRelease-1>', StopMove)
feed.bind('<B1-Motion>', OnMotion)
initialiseRSS()
updater()
root.mainloop()
