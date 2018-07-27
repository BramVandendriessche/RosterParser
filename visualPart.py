from tkinter import *
# from ttk import *


def chooseOpos(opoSet):
    opoDict = {}
    opoList = list(opoSet)
    opoList.sort(key=lambda x: x.name) #sort opo's on name

    root = Tk()
    canvas = Canvas(root, borderwidth=0)
    frame = Frame(canvas,)
    vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4, 4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    i = 0
    for opo in opoList:
        var = IntVar()
        Checkbutton(frame, text=opo.name, variable=var).grid(row=i, sticky=W)

        opoDict[opo] = var

        i+=1

    Button(frame, text='Generate ics file!', command=root.quit).grid(row=i+1)

    mainloop()
    remainingSet = set()
    for k in opoSet:

        if opoDict.get(k).get() == 1:
            remainingSet.add(k)

    return remainingSet


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))
