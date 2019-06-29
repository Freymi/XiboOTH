import webuntis
import datetime
from datetime import datetime as dt
import os
import time
import re
import json

wanted_rooms = ['K006', 'K007', 'K139', 'K140', 'K220', 'K222', 'K223']
dir_path = os.path.dirname(os.path.realpath(__file__))


def readfile():
    "Lest Daten zu der aktuellen Belegung aus der Datei"

    freeRooms = []
    takenRooms = []
    # + 2 Stunden, da der Xibo CMS Server die UTC Zeit verwendet
    now = dt.now() + datetime.timedelta(hours=2)
    f = open(dir_path + "/Files/" + today.strftime("%d.%m.%Y") + ".txt", "r")

    lines = f.readlines()

    for line in lines:
        roomSplit = line.split(":")
        room = roomSplit[0]

        if roomSplit[1].strip():

            timeSplit = re.split("[-,]", roomSplit[1].strip())

            for i in range(0, len(timeSplit)):
                if(i == len(timeSplit) - 1):
                    freeRooms.append((room, "frei bis Morgen"))
                    break

                startTime = dt.fromtimestamp(float(timeSplit[i]))
                endTime = dt.fromtimestamp(float(timeSplit[i + 1]))

                #print(room + ": " + str(i) + ", " + startTime.strftime("%H:%M") + ", " + now.strftime("%H:%M") + ", " + endTime.strftime("%H:%M"))

                if(i == 0 and now < startTime):
                    freeRooms.append((room, "frei bis " + startTime.strftime("%H:%M")))
                    break;

                if(startTime <= now <= endTime):
                    if((i % 2) == 0):
                        takenRooms.append((room, "belegt bis " + endTime.strftime("%H:%M")))
                    else:
                        freeRooms.append((room, "frei bis " + endTime.strftime("%H:%M")))
                    break

        else:
            freeRooms.append((room, "frei bis Morgen"))


    jsonArray = []

    for room in wanted_rooms:
        for name, time in freeRooms:
            if name == room:
                jsonArray.append({"name": room, "free": 1, "until": time})
                break
        for name, time in takenRooms:
            if name == room:
                jsonArray.append({"name": room, "free": 0, "until": time})
                break

    print(json.dumps({"rooms": jsonArray}))

    return

today = datetime.date.today()
filename = dir_path +  "/Files/" + today.strftime("%d.%m.%Y") + ".txt";

if(os.path.isfile(filename)):
    readfile()
else:

    #dateien loeschen
    for file in os.listdir(dir_path + "/Files"):
        file_path = os.path.join(dir_path + "/Files", file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    s = webuntis.Session(
        server='kephiso.webuntis.com',
        username='........',
        password='........',
        school='OTH-Regensburg',
        useragent='WebUntis Test'
    )

    s.login()

    roomlist = []

    for room in s.rooms():
        if(room.name in wanted_rooms):
            roomlist.append(room)

    f = open(filename, "w+")

    for room in roomlist:
        f.write(room.name + ":");
        timetable = s.timetable(room=room.id, start=today, end=today)

        timeList = []

        for i in range(len(timetable)):
            startPresent = False
            time = timetable[i].start - datetime.timedelta(minutes=15)
            for j in range(len(timeList)):
                if(timeList[j][0] == time):
                    startPresent = True
                    break
            if(not startPresent):
                timeList.append((time, timetable[i].end))

        timeList.sort()
        timeListClean = []

        i = 0
        while i < len(timeList):

            #Letzter Block einzelne Stunde
            if(i == len(timeList) - 1):
                timeListClean.append((timeList[i][0], timeList[i][1]))

            for j in range(i + 1, len(timeList)):
                if(timeList[j - 1][1] != timeList[j][0]):
                    timeListClean.append((timeList[i][0], timeList[j-1][1]))
                    i = j - 1
                    break
                if(j == len(timeList) - 1):
                    timeListClean.append((timeList[i][0], timeList[j][1]))
                    i = j

            i += 1

        for i in range(len(timeListClean)):
            f.write(str(dt.timestamp(timeListClean[i][0])) + "-" + str(dt.timestamp(timeListClean[i][1])))
            if(i < len(timeListClean) - 1):
                f.write(",")
        f.write("\n");

    f.close()

    s.logout()

    readfile()
