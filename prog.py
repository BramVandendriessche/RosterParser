import re
import os
from ics import Calendar, Event
import visualPart
import pendulum
import wget

# testline = '<tr><td bgcolor="FFDEAD">Vrijdag</td><td bgcolor="FFDEAD">08:30-10:30</td><td bgcolor="FFDEAD">200<i>XXX</i></td><td bgcolor="FFDEAD">H03F7A</td><td bgcolor="FFDEAD">H03F7a</td><td bgcolor="FFDEAD">Wavelets with Applications in Signal and Image Processing: Lecture</td><td bgcolor="lightgreen"></td><td bgcolor="lightgreen"></td><td bgcolor="lightgreen"></td><td bgcolor="lightgreen"></td><td bgcolor="lightgreen"></td><td></td><td bgcolor="lightgreen"></td><td bgcolor="lightgreen"></td><td bgcolor="lightgreen"></td><td bgcolor="lightgreen"></td><td bgcolor="lightgreen"></td><td bgcolor="lightgreen"></td><td></td></tr>''

# '(<td bgcolor="([A-Z0-9]*)">([A-Za-z0-9\-\:\s\.]*)</td>){6}(<(td|td bgcolor="[A-Z0-9a-z]*")></td>){13}</tr>'
def parseLine(line):
    # dag : tijdsslot : lokaal : OPO : OLA : Naam : Weken (39,40,41,42,43,44,45,46,47,48,49,50,51)

    #                color       day/hour/location/opo/ola/naam                    color --> x'th column --> nth week if has color

    line = re.sub('<td bgcolor="[A-Za-z0-9]+"></td>', '<td>yes</td>', line)

    tempresBeforeWeeks = re.split('<td bgcolor="[A-Z0-9]+">', line)
    tempresBeforeWeeks.remove('<tr>')
    tempresOPONameandWeeks = re.split('</td>', (tempresBeforeWeeks[len(tempresBeforeWeeks) - 1]))
    tempresBeforeWeeks.pop()  # remove the opo concatenated to the weeks
    tempresOPONameandWeeks.remove('</tr>')
    # remove </td> from tempresBeforeWeeks
    for i in range(len(tempresBeforeWeeks)):
        el = tempresBeforeWeeks[i]
        tempresBeforeWeeks[i] = el[:len(el) - 5]

    # remove <td> from tempresOPONameandWeeks (except for the first)
    for i in range(1, len(tempresOPONameandWeeks)):
        el = tempresOPONameandWeeks[i]
        tempresOPONameandWeeks[i] = el[4:]

    return tempresBeforeWeeks + tempresOPONameandWeeks


def main():
    # get file

    response = wget.download("https://people.cs.kuleuven.be/~btw/roosters1819/cws_semester_1.html",  "file.html")
    # os.system('wget "https://people.cs.kuleuven.be/~btw/roosters1819/cws_semester_1.html" -O file.html')

    # read file
    file = open("file.html", "r")
    # file = open("cws_semester_1.html")

    cellSet = []

    for line in file:
        line = line.rstrip()
        std = '''<tr>(<td bgcolor="([A-Z0-9]*)">([A-Za-z0-9\-\:\s\.\<\>\/&,]*)</td>){6}(<(td|td bgcolor="[A-Z0-9a-z]*")></td>){13}</tr>'''
        if (re.match(std, line)):
            cells = parseLine(line)
            cellSet.append(cells)
            # print(cells)
        else:
            print(line)
            pass

    # close file:
    file.close()

    # remove file
    os.system("rm file.html")

    # TODO: handle cells
    Opos = handleCells(cellSet)

    chosenOpos = visualPart.chooseOpos(Opos)

    calendar = createCalendar(chosenOpos)

    with open("calendar.ics", 'w') as calendarFile:
        calendarFile.writelines(calendar)



def createCalendar(opos):
    c = Calendar()
    for opo in opos:
        c.events.update(opo.events)

    return c


def handleCells(cellSet):
    # dag : tijdsslot : lokaal : OPO : OLA : Naam : Weken (39,40,41,42,43,44,45,46,47,48,49,50,51)

    Opos = {}
    # TODO: semester setten
    semester = 1

    for cells in cellSet:
        day, timeSlot, location, opoCode, olaCode, olaName = [str(el) for el in cells[:6]]
        nameOfOPO = olaName.split(":")[0]
        if "Capita Selecta" in nameOfOPO:
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
            d = None
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

    return Opos.values()


def getDayNumber(day):
    return ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag"].index(day)


class Opo:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.events = set()

    # set of events


# list all OPO's, let user choose which to take
# create ICS with events of the selected opo's


if __name__ == "__main__":
    main()
