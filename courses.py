import urllib.request
import re
from bs4 import BeautifulSoup
import json

class DalCourse:
	__Weekdays = ["M","T","W","R","F"]

	def __init__(self):
		self.title = "title"
		self.date = "date"
		self.link = "web"
		self.registerID = 0
		self.courseType = "Lec"
		self.credit = 0
		self.time = "NONE"
		self.address = "DALHOUSIE"
		self.maxStudent = 0
		self.current = 0
		self.available = 0
		self.wList = 0
		self.percentage = "%0"
		self.weekdays = [False, False, False, False, False]
		self.Labs = []

	def getWeekDays(self):
		i = 0
		days = ""
		for day in self.weekdays:
			if day == True:
				days += self.__Weekdays[i] + " "
			i += 1
		return days

	def setLabs(self, info):
		self.Labs = []
		lab = DalCourse()
		lab.title = self.title + " " + info[5].string
		lab.date = self.date
		lab.link = ""
		lab.registerID = int(info[3].string)
		lab.courseType = info[7].string
		lab.credit = 0
		lab.time = info[23].string
		lab.address = info[25].string
		lab.maxStudent = int(info[27].string)
		lab.current = int(info[29].string)
		lab.available = int(info[31].string)
		if info[33].string != '\xa0':
			lab.wList = int(info[33].string)
		else:
			lab.wList = 0
		lab.percentage = info[35].font.string.split('\n')[0]
		lab.professor = "Staff"
		for i in range(13,22):
			if info[i].string != "\xa0" and info[i] != "\n":
				lab.weekdays[int((i - 13)/2)] = True
		self.Labs.append(lab)

	def toDict(self):
		courseDict = dict()
		courseDict["title"] = self.title
		courseDict["date"] = self.date
		courseDict["link"] = self.link
		courseDict["registerID"] = self.registerID
		courseDict["courseType"] = self.courseType
		courseDict["credit"] = self.credit
		courseDict["time"] = self.time
		courseDict["address"] = self.address
		courseDict["maxStudent"] = self.maxStudent
		courseDict["current"] = self.current
		courseDict["available"] = self.available
		courseDict["wList"] = self.wList
		courseDict["percentage"] = self.percentage
		courseDict["weekdays"] = self.weekdays
		if len(self.Labs) != 0:
			courseDict["Labs"] = []
			for eachLab in self.Labs:
				courseDict["Labs"].append(eachLab.toDict())
		else:
			courseDict["Labs"] = []
		return courseDict

class courseSpider:
	def __init__(self):
		self.courses = set()
		self.data = ""
		self.pages = []
		self.gatherTerms()
		self.gatherSubject()
		
	def gatherPages(self, subject = "CSCI", term = "201710"):
		url = "https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=" + term + "&s_subj=" + subject + "&s_numb=&n=1&s_district=All"
		data = self.gatherData(url)
		pattern = re.compile('^(<center>Page\s*<b>1<\/b>\s*)(.*\s*?)*?<\/center>$', re.M)
		result = re.search(pattern, data)
		if result is None:
			self.pages = ["fysktime.P_DisplaySchedule?s_term=201710&s_subj=" + self.subject + "&s_numb=&n=1&s_district=All"]
			return
		else:
			soup = BeautifulSoup(result.group(), "html.parser")
			for each in soup.contents[0].contents:
				try:
					self.pages.append(each.attrs['href'])
				except:
					pass

	def gatherTerms(self, subject = "CSCI", term = "201710"):
		url = "https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=" + term + "&s_subj=" + subject + "&s_numb=&n=1&s_district=All"
		if self.data == "":
			self.data = self.gatherData(url)
		pattern = re.compile('Term-\s*?(.*?\s)*?<\/', re.M)
		result = re.search(pattern, self.data)
		soup = BeautifulSoup(result.group(), "html.parser")
		titles = soup.option.text.split("\n")
		current = soup.option
		values = []
		for _ in range(0, len(titles) - 1):
			values.append(current["value"])
			current = current.option
		self.terms = dict(zip(titles,values))

	def gatherSubject(self, subject = "CSCI", term = "201710"):
		url = "https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=" + term + "&s_subj=" + subject + "&s_numb=&n=1&s_district=All"
		if self.data == "":
			self.data = self.gatherData(url)
		pattern = re.compile('Subject-\s*?(.*?\s)*?<\/', re.M)
		result = re.search(pattern, self.data)
		soup = BeautifulSoup(result.group(), "html.parser")
		titles = soup.option.text.split("\n")
		current = soup.option
		values = []
		for _ in range(0, len(titles) - 1):
			values.append(current["value"])
			current = current.option
		self.subjects = dict(zip(titles,values))

	def gatherData(self, url):
		return urllib.request.urlopen(url).read().decode('UTF-8')

	def spider(self, subject, term):
		self.subject = subject
		self.gatherPages(subject = subject, term = term)
		for page in self.pages:
			url = "https://dalonline.dal.ca/PROD/" + page
			data = self.gatherData(url)
			pattern = re.compile('^<TD.*?COLSPAN="15" CLASS="detthdr">\s*?(.*\s?)*?<tr.*valign=', re.M)
			courseSource = re.finditer(pattern, data)
			for each in courseSource:
				course = self.informationParse(each)
				self.courses.add(course)

	def informationParse(self, each):
		soup = BeautifulSoup(each.group(),"html.parser")
		course = DalCourse()
		course.title = soup.b.string
		if "-" in soup.span.text:
			date = soup.span.text.split("\n")
			course.date = date[0] + date[2]
		else:
			date = soup.contents[2].span.text.split("\n")
			course.date = date[0] + date[2]
		course.link = soup.a['href']
		course.registerID = int(soup.tr.contents[3].string)
		course.courseType = soup.tr.contents[7].string
		course.credit = float(soup.tr.contents[9].string)
		course.time = soup.tr.contents[23].contents[0]
		course.address = soup.tr.contents[25].contents[0]
		if soup.tr.contents[27].string != "OPEN":
			course.maxStudent = int(soup.tr.contents[27].string)
		else:
			course.maxStudent = 9999
		course.current = int(soup.tr.contents[29].string)
		course.available = int(soup.tr.contents[31].string)
		if soup.tr.contents[33].string != "\xa0":
			course.wList = int(soup.tr.contents[33].string)
		else:
			course.wList = 0
		course.percentage = soup.tr.contents[35].font.string.split('\n')[0]
		try:
			if ("\n" in soup.contents[7].text):
				course.professor = soup.contents[7].text.split('\n')[1]
			else:
				course.professor = "Staff"
		except:
			if ('\n' in soup.tr.contents[37].text):
				course.professor = soup.tr.contents[37].text.split('\n')[1]
			else:
				course.professor = soup.tr.contents[37].text
		for i in range(13,22):
			if soup.tr.contents[i].string != "\xa0" and soup.tr.contents[i] != "\n":
				course.weekdays[int((i - 13)/2)] = True
		labIndex = 9
		while True:
			try:
				course.setLabs(soup.contents[labIndex].contents)
				labIndex += 9
			except IndexError:
				break
			except AttributeError:
				break
		return course

cs = courseSpider()
subject = cs.subjects['Computer Science']
print(subject)
term = cs.terms['2016/2017 Winter']
print(term)
cs.spider(subject = subject, term = term)
course = []
for each in cs.courses:
	course.append(each.toDict())
courses = {"courses":course}
print(json.dumps(courses))
