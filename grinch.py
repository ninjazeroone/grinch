#!/usr/bin/python3

from bs4 import BeautifulSoup
from splinter import Browser
import time
import pause

def getTime():
	return time.time()

baseUrl = "https://steamgifts.com"

#Set your cookie here:
cookiePHPSESSID = ''


entered = []
def getPage():
	with Browser("phantomjs",user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0", custom_headers={'Cookie':cookiePHPSESSID}) as browser:
		url404 = "https://steamgifts.com/404"
		browser.visit(baseUrl)
		return browser.html
def enter(linkList, entered):
	enterlist = entered
	links = linkList
	with Browser("phantomjs",user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0", custom_headers={'Cookie':cookiePHPSESSID}) as browser:
		for i in links:
			if i not in enterlist:
				browser.visit(baseUrl + i)
				xpathEnter = '//div[@class="sidebar__entry-insert"]'
				xpathEntered = '//div[@class="sidebar__entry-insert is-hidden"]'
				if browser.is_element_present_by_xpath(xpathEntered):
					print(i + " entered already")
					enterlist.append(i)
				else:
					try:
						browser.find_by_xpath(xpathEnter).click()
						enterlist.append(i)
					except:
						print("Points is wasted")
						return enterlist
		return enterlist
def getLinks(page, targetNum, entered):
	resultHref = []
	soup = BeautifulSoup(page, "html.parser")
	titlesRaw = soup.find_all("a", class_ = "giveaway__heading__name")
	pointsRaw = soup.find_all("span", class_ = "giveaway__heading__thin")
	myPointsRaw = soup.find_all("span", class_ = "nav__points")
	myPoints = int(myPointsRaw[0].get_text())
	href = []
	for i in titlesRaw:
		x = i.get('href')
		href.append(x)
	titles = []
	points = []
	for i in titlesRaw:
		titles.append(i.get_text())
	for i in pointsRaw:
		if not "Cop" in i.get_text():
			x = i.get_text()
			x = x.replace("P", "")
			x = x.replace("(", "")
			x = x.replace(")", "")
			points.append(int(x))
	targetPoints = [i for i,x in enumerate(points) if x >= targetNum]
	for i in targetPoints:
		try:
			if href[i] not in entered:
				resultHref.append(href[i])
				print(href[i] + " " + str(points[i]))
			else:
				print(href[i] + " already entered, skipping")
		except:
			None
	return(resultHref)
def getPoints(page):
	soup = BeautifulSoup(page, "html.parser")
	myPointsRaw = soup.find_all("span", class_ = "nav__points")
	myPoints = myPointsRaw[0].get_text()
	return(myPoints)
def writeHTML():
	f.write("<b>Points:" + str(myPoints) + "</b><br />")
	for i in resultList:
		f.write(i + "<br />")
	f.close
while True:
	page = getPage()
	#Minimal points price for a game:
	targetPts = 10
	links = getLinks(page, targetPts, entered)
	points = getPoints(page)
	print("You have " + points + " points!")
	if not set(entered).issuperset(set(links)):	
		entered + enter(links, entered)
		if int(points) < targetPts:
			print("No points, sleeping")
			pause.until(getTime()+10800)
		else:
			time.sleep(10)
	else:
		print("No new giveaways, waiting")
		time.sleep(300)
