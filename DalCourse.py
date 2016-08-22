class DalCourse:
	__Weekdays = ["M","T","W","R","F"]

	def __init__(self):
		self.title = "title"
		self.date = "date"
		self.link = "web"
		self.registerID = "0"
		self.courseType = "Lec"
		self.credit = 0
		self.time = "NONE"
		self.address = "DALHOUSIE"
		self.maxStudent = "0"
		self.current = "0"
		self.available = "0"
		self.wList = "0"
		self.percentage = "%0"
		self.professor = ""
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
		lab = DalCourse()
		lab.title = self.title + " " + info[5].string
		lab.date = self.date
		lab.link = ""
		lab.registerID = info[3].string
		lab.courseType = info[7].string
		lab.credit = 0
		lab.time = info[23].string
		lab.address = info[25].string.strip()
		lab.maxStudent = info[27].text
		lab.current = info[29].text
		lab.available = info[31].text
		if info[33].string != '\xa0':
			lab.wList = info[33].string
		else:
			lab.wList = 0
		lab.percentage = info[35].font.string.split('\n')[0].replace(" ", "")
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
		courseDict["professor"] = self.professor
		if len(self.Labs) != 0:
			courseDict["Labs"] = []
			for eachLab in self.Labs:
				courseDict["Labs"].append(eachLab.toDict())
		else:
			courseDict["Labs"] = []
		return courseDict