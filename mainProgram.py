import re
import os
from ics import Calendar, Event
import visualPart
import pendulum
import wget


def parseLine(line):

    # remove row tags
    line = line[4:len(line)-5]
    # split in multiple cells
    cells = line.split("</td>")

    #clean up cell content; catch ValueError (if regex not in string)
    try:
        cells[:6] = [re.sub('<td bgcolor="[A-Za-z0-9]+">|', '', i) for i in cells[:6]]
        cells[:6] = [re.sub('<i>', '', i) for i in cells[:6]]
        cells[:6] = [re.sub('</i>', '', i) for i in cells[:6]]
        #if the week's cell has a color, there's class that week
        cells[6:] = [re.sub('<td bgcolor="[A-Za-z0-9]+">', 'yes', i) for i in cells[6:]]
        cells = [re.sub('<td>', '', i) for i in cells]

    except ValueError:
        pass

    return cells


def createCalendar(opos):
    c = Calendar()
    for opo in opos:
        c.events.update(opo.events)

    return c


def handleCells(cellSet, semester):

    Opos = {}

    for cells in cellSet:
        day, timeSlot, location, opoCode, olaCode, olaName = [str(el) for el in cells[:6]]
        nameOfOPO = olaName.split(":")[0]
        if "Capita Selecta" in nameOfOPO:
            nameOfOPO = olaName
        if "Studium" in nameOfOPO:
            nameOfOPO = olaName

        begintime, endtime = timeSlot.split("-")
        beginHour, beginMinutes = [int(i) for i in begintime.split(":")]
        endHour, endMinutes = [int(el) for el in endtime.split(":")]

        if opoCode not in Opos:
            opo = Opo(nameOfOPO, opoCode)
            Opos[opoCode] = opo
        else:
            opo = Opos[opoCode]

        if semester == 1:
            d = pendulum.datetime(2018, 9, 24, 0, 0, 0, tz=pendulum.timezone('Europe/Brussels'))
            weekStart = 39
        elif semester == 2:
            d = pendulum.datetime(2019, 2, 11, 0, 0, 0, tz=pendulum.timezone('Europe/Brussels'))
        else:
            raise ValueError("invalid semester!")

        weekCount = 0
        for weekActivity in cells[6:]:
            if weekActivity != "":
                e = Event()
                e.begin = d.add(weeks=weekCount, days=getDayNumber(day), hours=beginHour, minutes=beginMinutes)
                e.end = d.add(weeks=weekCount, days=getDayNumber(day), hours=endHour, minutes=endMinutes)
                e.name = olaName
                e.location = location

                opo.events.add(e)

            weekCount += 1

    return Opos


def getDayNumber(day):
    return ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag"].index(day)

def parseFile(semester):
    # get file

    # response = wget.download("https://people.cs.kuleuven.be/~btw/roosters1819/cws_semester_"+str(semester)+".html",  "file.html")
    # os.system('wget "https://people.cs.kuleuven.be/~btw/roosters1819/cws_semester_1.html" -O file.html')

    # read file
    # file = open("file.html", "r")
    file = open("cws_semester_"+str(semester)+".html")

    cellSet = []

    for line in file:
        line = line.rstrip()
        std = '''<tr>(<td bgcolor="([A-Z0-9]*)">([A-Za-z0-9\-\:\s\.\<\>\/&,]*)</td>){6}(<(td|td bgcolor="[A-Z0-9a-z]*")></td>){13,15}</tr>'''
        if (re.match(std, line)):
            cells = parseLine(line)
            cellSet.append(cells)
        else:
            # print(line)    # enable this if if the parser might have missed a row of the table
            pass

    # close file:
    file.close()

    # remove file
    # os.system("rm file.html")
    return cellSet

def concatenateClassesAcrossYear(cellSetSem1, cellSetSem2):
    cellSetSem1 = cellSetSem1.copy()
    res = cellSetSem1
    for opoCode,opo in cellSetSem2.items():
        if opoCode not in cellSetSem1:
            res[opoCode]=opo
        else:
            res[opoCode].events.update(opo.events)

    return res.values()




def main():

    cellSetSem1 = parseFile(1)
    cellSetSem2 = parseFile(2)

    Opos = concatenateClassesAcrossYear(handleCells(cellSetSem1, 1), handleCells(cellSetSem2, 2))

    chosenOpos = visualPart.chooseOpos(Opos)

    calendar = createCalendar(chosenOpos)

    with open("calendar.ics", 'w') as calendarFile:
        calendarFile.writelines(calendar)

    print("\n\nCalendar sucessfully exported to 'calendar.ics'")
    print("The following courses were selected:")
    for chosenOpo in chosenOpos:
        print(chosenOpo.name)


class Opo:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.events = set()

if __name__ == "__main__":
    main()
