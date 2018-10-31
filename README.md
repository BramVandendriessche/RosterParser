# RosterParser
Generate a .ics file of the Master Computer Science roster of academic year 2018-2019 at KU Leuven ([semester 1](https://people.cs.kuleuven.be/~btw/roosters1819/cws_semester_1.html), [semester 2](https://people.cs.kuleuven.be/~btw/roosters1819/cws_semester_2.html)).

## Requirements
* [python](https://www.python.org/getit/) (tested using version 3.4+)
* [Tkinter](https://wiki.python.org/moin/TkInter)
* [ics](https://pypi.org/project/ics/)
* [pendulum](https://pendulum.eustace.io/)
<!-- wget is not required anymore, since the html files should now be manually saved
* [wget](https://pypi.org/project/wget/) -->

## Disclaimers
* This script might save you some time or waste a lot of it.
* It might also burn your house down, set your cat on fire or cause nightmares.
* There's a lot of "calendar" in this description.


## Usage
Run *mainProgram.py*
```
python mainProgram.py
```
or
```
python3 mainProgram.py
```
or
...

Choose the courses to be included in your calendar. Mousewheel / two-finger scrolling is not supported in the course selection window; move the scrollbar instead. After closing the window, a file *calendar.ics* is generated, which can be imported in Outlook, Google Calendar, iCalendar etc.

## Undoing an import
Importing the file to a calendar, creates events in that calendar (or at least this is the case for Google Calendar). Therefore it is strongly recommended to create a **new** calendar to import the events of *calendar.ics* to. In this way, the entire calendar can just be removed or replaced, without having to remove events one by one.

In case you want to remove the imported events from a calendar without actually removing the calendar itself, try modifying *calendar.ics* by adding the following line to every event:
```
STATUS:CANCELLED
```
Next, import your *"cancelendar"* again, wich should undo the original import. This worked for me in Google Calendar, but it might not for other applications. Some will mark the events as "Cancelled" without actually removing them, for others this won't affect the imported events at all.
