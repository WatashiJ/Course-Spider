# Course-Spider

## A better tool is built, visit [course-checker](https://github.com/YaxinCheng/ScriptTools/tree/master/Course-Checker)

## Since: Mar 26, 2016

## Introduction:
This is a python crawler for Dalhousie Academic Table(https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule)<br>
It started from my personal interests, and ended up with a full accessible API<br>
I appreciate the process of doing things fun<br>
This will only be an example of how I learned about Python and Flask<br>

## API:
### Index page: 
https://course-spider.herokuapp.com <br>
It will redirect you here<br>
<br>
### GET all terms:
https://course-spider.herokuapp.com/api/terms <br>
Method: .GET<br>
Parameters: None<br>
Sample response: {"2016/2017 Fall": "201710"}<br>
<br>
### GET all subjects:
https://course-spider.herokuapp.com/api/subjects <br>
Method: .POST<br>
Parameters: term(Required)<br>Sample parameters: {"term": "201710"}<br>
Sample response: {"Computer Science": "CSCI"}<br>
<br>
### GET all courses:
https://course-spider.herokuapp.com/api/courses <br>
Method: .POST<br>
Parameters: term(Required), subject(Required), page(Optional)<br>
Sample parameters: {"term": "201710", "subject": "CSCI"}<br>
Sample response: {"courses":  {"Labs":[],<br>
            "address": "Studley MCCAIN ARTS&SS; AUD-1",<br>
            "available": "11",<br>
            "courseType": "Lec",<br>
            "credit": "3",<br>
            "current": "89",<br>
            "date": "06-SEP-2016 - 06-DEC-2016",<br>
            "link": "http://academiccalendar.dal.ca/Catalog/ViewCatalog.aspx?pageid=viewcatalog&entitytype=CID&entitycode=CSCI+2100",<br>
            "maxStudent": "100",<br>
            "percentage": "WLIST",<br>
            "professor": ""Fleming J. ",<br>
            "registerID": "10701",<br>
            "time": "1635-1725",<br>
            "title": CSCI 2100 Comm Skills: Oral/Written",<br>
            "wList": "15",<br>
            "weekdays": [
                1,
                0,
                1,
                0,
                1
            ]<br>
        }, "totalPages": "3"<br>
    }
<br>
## End:
I was building an iOS app to select course, but since Dal has its own app, this looks kinda superfluous. But I will keep making other things, to optimize myself. Thanks
