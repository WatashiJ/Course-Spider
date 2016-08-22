import urllib.request
import re
from bs4 import BeautifulSoup
import json
from DalCourse import DalCourse

class courseSpider:
	data = ""
	def __init__(self):
		self.courses = set()
		self.pages = []
		
	def gatherPages(self, subject = "CSCI", term = "201710"):
		url = "https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=" + term + "&s_subj=" + subject + "&s_numb=&n=1&s_district=All"
		courseSpider.data = self.gatherData(url)
		pattern = re.compile('^(<center>Page\s*<b>1<\/b>\s*)(.*\s*?)*?<\/center>$', re.M)
		result = re.search(pattern, courseSpider.data)
		self.pages = ["fysktime.P_DisplaySchedule?s_term="+ term + "&s_subj=" + subject + "&s_numb=&n=1&s_district=All"]
		if result is None:
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
		courseSpider.data = self.gatherData(url)
		pattern = re.compile('Term-\s*?(.*?\s)*?<\/', re.M)
		result = re.search(pattern, courseSpider.data)
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
		courseSpider.data = self.gatherData(url)
		pattern = re.compile('Subject-\s*?(.*?\s)*?<\/', re.M)
		result = re.search(pattern, courseSpider.data)
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

	def spider(self, subject, term, pageNumber = -1):
		self.subject = subject
		self.gatherPages(subject = subject, term = term)
		self.totalPage = len(self.pages)
		if not(pageNumber == -1):
			if pageNumber < len(self.pages):
				self.separateCourses(self.pages[pageNumber])
		else:
			for page in self.pages:
				self.separateCourses(page = page)

	def separateCourses(self, page):
		url = "https://dalonline.dal.ca/PROD/" + page
		data = self.gatherData(url)
		pattern = re.compile('^<TD.*?COLSPAN="15" CLASS="detthdr">\s*?(.*\s?)*?<tr.*valign=', re.M)
		courseSource = re.finditer(pattern, data)
		for each in courseSource:
			courses = self.informationParse(each)
			self.courses = self.courses | courses

	def informationParse(self, each):
		soup = BeautifulSoup(each.group(),"html.parser")
		course = DalCourse()
		course.title = soup.b.string
		if "-" in soup.span.text:
			course.date = soup.span.text.split(": ")[1]
		else:
			course.date = soup.contents[2].span.text.split(": ")[1]
		course.link = soup.a['href']
		course.registerID = soup.tr.contents[3].string
		course.courseType = soup.tr.contents[7].string
		course.credit = float(soup.tr.contents[9].string)
		if soup.tr.contents[13].string == "C/D":
			course.time = "C/D"
			course.address = ""
			course.maxStudent = soup.tr.contents[15].text
			course.current = soup.tr.contents[17].text
			course.available = soup.tr.contents[19].text
			if soup.tr.contents[21].string != "\xa0":
				course.wList = soup.tr.contents[33].text
			else:
				course.wList = 0
			course.percentage = soup.tr.contents[23].font.string.split('\n')[0].replace(" ", "")
			course.professor = "Staff"
			return course
		course.time = soup.tr.contents[23].contents[0]
		course.address = soup.tr.contents[25].contents[0].strip()
		if soup.tr.contents[27].text != "OPEN":
			course.maxStudent = soup.tr.contents[27].text
		else:
			course.maxStudent = "9999"
		course.current = soup.tr.contents[29].text# Problem occur when there're multiple lines in Commerce
		course.available = soup.tr.contents[31].text
		if soup.tr.contents[33].string != "\xa0":
			course.wList = soup.tr.contents[33].text
		else:
			course.wList = 0
		course.percentage = soup.tr.contents[35].font.string.split('\n')[0].replace(" ", "")
		try:
			if ('\n' in soup.tr.contents[37].text):
				course.professor = soup.tr.contents[37].text.split('\n')[1]
			elif ("\n" in soup.contents[7].text):
				course.professor = soup.contents[7].text.split('\n')[1]
			else:
				course.professor = soup.contents[7].text
		except:
			course.professor = "Staff"
		for i in range(13,22):
			if soup.tr.contents[i].string != "\xa0" and soup.tr.contents[i] != "\n":
				course.weekdays[int((i - 13)/2)] = True
		labIndex = 9
		multipleCourse = set()
		multipleCourse.add(course)
		for index in range(8, len(soup.contents)):
			info = soup.contents[index]
			try:
				courseType = info.contents[7].string
				if courseType == "Lec":
					newCourse = self.multiLec(info = soup.contents, index = index, originalCourse = course)
					multipleCourse.add(newCourse)
				elif courseType == "Lab" or courseType == "Tut":
					print(course.title)
					for each in multipleCourse:
						each.setLabs(info.contents)			
			except IndexError:
				continue
			except AttributeError:
				continue
		return multipleCourse

	def multiLec(self, info, index, originalCourse):
		course = DalCourse()
		course.title = originalCourse.title
		course.date = originalCourse.date
		course.link = originalCourse.link
		course.courseType = info[index].contents[7].string
		course.registerID = info[index].contents[3].string
		course.credit = originalCourse.credit
		course.time = info[index].contents[23].string
		course.Labs = []
		course.address = info[index].contents[25].string.strip()
		course.maxStudent = info[index].contents[27].text
		course.current = info[index].contents[29].text
		course.available = info[index].contents[31].text
		if info[index].contents[33].string != '\xa0':
			course.wList = info[index].contents[33].string
		else:
			course.wList = 0
		course.percentage = info[index].contents[35].font.string.split('\n')[0].replace(" ", "")
		course.professor = info[index + 2].contents[0].strip("\n").strip()
		for i in range(13,22):
			if info[index].contents[i].string != "\xa0" and info[index].contents[i].string != "\n":
				course.weekdays[int((i - 13)/2)] = True
		return course
