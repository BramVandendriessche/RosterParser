# RosterParser
Generate a .ics file of the Master Computer Science roster of academic year 2018-2019.

## Requirements
* [python](https://www.python.org/getit/) (tested using version 3.4+)
* [ics](https://pypi.org/project/ics/)
* [pendulum](https://tkdocs.com/tutorial/install.html)
* [wget](https://pypi.org/project/wget/)
* [Tkinter](https://tkdocs.com/tutorial/install.html)


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

Choose the courses to be included in your calendar.

A file *calendar.ics* is generated, which can be imported in Outlook, Google Calendar etc.

## Undoing an import
In case you want to remove the imported classes from your calendar, modify *calendar.ics* by adding the following line to every event:
```
STATUS:CANCELLED
```
