import icalendar
import sys
import time
import winsound
from datetime import datetime, timedelta, timezone
import tkinter as tk
import json


# sort the alarm list by date
def sort_by_date(events_list):

    for i in range(0, len(events_list)-1):
        split_date1 = events_list[i][3].split('/')
        if len(split_date1[2]) < 4:
            d1 = datetime(int('20' + split_date1[2]), int(split_date1[0]), int(split_date1[1]))
        else:
            d1 = datetime(int(split_date1[2]), int(split_date1[0]), int(split_date1[1]))

        for j in range(i+1, len(events_list)):
            split_date2 = events_list[j][3].split('/')
            if len(split_date2[2]) < 4:
                d2 = datetime(int('20' + split_date2[2]), int(split_date2[0]), int(split_date2[1]))
            else:
                d2 = datetime(int(split_date2[2]), int(split_date2[0]), int(split_date2[1]))
            if d1 > d2:
                tem_list = events_list[i]
                events_list[i] = events_list[j]
                events_list[j] = tem_list

    return events_list


# sort the alarm list by time
def sort_by_time(atribute):
    return atribute[4]


# creates new label with a certain message text
def new_label(message):
    return tk.Label(
        text=message,
        fg="black",
        height=1,
    )


# creates a pop-up window with an alert, printing a certain description of the alarm
def alarm_pop_up(event):
    window = tk.Tk()

    label_alarm = new_label("Alarm for " + event[0])
    label_description = new_label(event[1])
    label_local = new_label("Locul: " + event[2])
    label_startdt = new_label("La data " + event[3])
    label_starttm = new_label("De la " + event[4] + " pana la " + event[6])
    label_alarm.pack()
    label_description.pack()
    label_local.pack()
    label_startdt.pack()
    label_starttm.pack()

    window.mainloop()


# # creates a pop-up window with all alerts, printing all information about the alarm
def alarms_pop_up(events_list):
    window = tk.Tk()

    for each_event in events_list:
        label_alarm = new_label("Alarm for " + each_event[0])
        label_description = new_label(each_event[1])
        label_local = new_label("Locul: " + each_event[2])
        label_startdt = new_label("La data " + each_event[3])
        label_starttm = new_label("De la " + each_event[4] + " pana la " + each_event[6])
        label_empty = new_label(" ")
        label_alarm.pack()
        label_description.pack()
        label_local.pack()
        label_startdt.pack()
        label_starttm.pack()
        label_empty.pack()


    window.mainloop()


# keps running till the alarm goes off
def alarm(event):
    while True:
        time.sleep(1)
        current_time = datetime.now()
        curr_time = current_time.strftime("%H:%M")
        curr_date = current_time.strftime("%d/%m/%Y")
        if curr_time >= event[4] and curr_date == event[3]:
            winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
            alarm_pop_up(event)
            break


# validates the input
def verify_iput():
    if ".ics" in sys.argv[1]:
        print("\nOpened a ics file!\n")
        return "ics"
    elif ".json" in sys.argv[1]:
        print("Opened a custom json file!")
        return "json"
    else:
        print("Not a ics or a json file!")
        sys.exit(1)


def get_ics_content():
    temp_list = []
    file_handler = open(sys.argv[1], 'rb')
    file_cal = icalendar.Calendar.from_ical(file_handler.read())
    for content in file_cal.walk():
        if content.name == "VEVENT":
            summary = content.get('summary')
            description = content.get('description')
            location = content.get('location')
            startdt = content.get('dtstart').dt
            enddt = content.get('dtend').dt
            start_date = startdt.strftime('%D')
            start_time = startdt.strftime('%H:%M')
            end_date = enddt.strftime('%D')
            end_time = enddt.strftime('%H:%M')
            temp_list.append([summary, description, location, start_date, start_time, end_date, end_time])

    temp_list.sort(reverse=True, key=sort_by_time)
    temp_list = sort_by_date(temp_list)
    file_handler.close()
    return temp_list


def get_json_content():
    temp_list = []
    with open(sys.argv[1]) as file_handler:
        content = json.load(file_handler)
    events = content.get('events', 0)
    for event in events:
        summary = event.get('summary')
        description = event.get('description')
        location = event.get('location')
        start_date = event.get('start_date')
        start_time = event.get('start_time')
        end_date = event.get('end_date')
        end_time = event.get('end_time')
        temp_list.append([summary, description, location, start_date, start_time, end_date, end_time])

    temp_list.sort(reverse=True, key=sort_by_time)
    temp_list = sort_by_date(temp_list)
    file_handler.close()
    return temp_list


if __name__ == "__main__":
    events_list = []
    file_type = verify_iput()
    if file_type == "ics":
        events_list = get_ics_content()
    else:
        events_list = get_json_content()

    alarms_pop_up(events_list)

    for event in events_list:
        alarm(event)
        print("end of event\n")


