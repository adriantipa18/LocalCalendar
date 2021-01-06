import icalendar
import time
import winsound
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import *
import json
import logging

logging.basicConfig(level=logging.DEBUG)


# creates a datetime based on start_date and start_time of a certain event
def create_datetime(start_date, start_time):
    try:
        another_date = start_date.split('/')
    except ValueError:
        logging.error("Corrupt data! Review the dates in the current file!")
        sys.exit(-1)
    try:
        split_time = start_time.split(':')

    except ValueError:
        logging.error("Corrupt data! Review the timestamps in the current file!")
        sys.exit(-1)

    try:
        if len(another_date[2]) < 4:
            alarm_time = datetime(int('20' + another_date[2]), int(another_date[0]), int(another_date[1]), int(split_time[0]), int(split_time[1]))
        else:
            alarm_time = datetime(int(another_date[2]), int(another_date[0]), int(another_date[1]), int(split_time[0]), int(split_time[1]))
    except ValueError:
        logging.error("Corrupt data! Review the dates/timestamps in the current file!")
        sys.exit(-1)
    return alarm_time


# checks if a year is a leap year
def check_leap_year(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


# add years to a date, returns the next set alarm
def add_years(start_date, start_hour):
    another_date = create_datetime(start_date, start_hour)
    curr_date = datetime.now()

    while curr_date >= another_date:
        if check_leap_year(another_date.year):
            another_date += timedelta(366)
        else:
            another_date += timedelta(365)

    return another_date.strftime("%m/%d/%Y")


# add months to a date, returns the next set alarm
def add_months(start_date, start_time):
    another_date = create_datetime(start_date, start_time)
    curr_date = datetime.now()

    while curr_date >= another_date:
        if another_date.month == 1 or another_date.month == 3 or another_date.month == 5 or another_date.month == 7 or another_date.month == 8 or another_date.month == 10 or another_date.month == 12:
            another_date += timedelta(31)
        elif another_date.month == 2:
            if check_leap_year(another_date.year):
                another_date += timedelta(29)
            else:
                another_date += timedelta(28)
        else:
            another_date += timedelta(30)

    return another_date.strftime("%m/%d/%Y")


def add_weeks(start_date, start_time):
    another_date = create_datetime(start_date, start_time)
    curr_date = datetime.now()

    while curr_date.month != another_date.month:
        another_date += timedelta(7)

    while curr_date.day > another_date.day:
        another_date += timedelta(7)

    if curr_date.day == another_date.day:
        if curr_date.hour > another_date.hour:
            another_date += timedelta(7)
        elif another_date.hour == curr_date.hour:
            if curr_date.minute >= another_date.minute:
                another_date += timedelta(7)

    return another_date.strftime("%m/%d/%Y")


# add days to a date, returns the next set alarm
def add_days(start_date, start_time):
    curr_date = datetime.now()
    another_date = create_datetime(start_date, start_time)

    while curr_date.day > another_date.day:
        another_date += timedelta(1)

    if curr_date.hour > another_date.hour:
        another_date += timedelta(1)
    elif another_date.hour == curr_date.hour:
        if curr_date.minute >= another_date.minute:
            another_date += timedelta(1)

    return another_date.strftime("%m/%d/%Y")


# sort the alarm list by date and time
def sort_by_date_time(events_list):
    for i in range(0, len(events_list) - 1):
        first_alarm_date = create_datetime(events_list[i][3], events_list[i][4])
        for j in range(i + 1, len(events_list)):
            second_alarm_date = create_datetime(events_list[j][3], events_list[j][4])
            if first_alarm_date > second_alarm_date:
                temp_list = events_list[i]
                events_list[i] = events_list[j]
                events_list[j] = temp_list

    return events_list


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
    scrollbar = Scrollbar(window)
    scrollbar.pack(side=RIGHT, fill=Y)
    upcoming_events = tk.Listbox(window, width=40, yscrollcommand=scrollbar.set)
    for each_event in events_list:
        upcoming_events.insert(END, f"Alarm for {each_event[0]}")
        upcoming_events.insert(END, f"Alarm for {each_event[1]}")
        if each_event[2]:
            upcoming_events.insert(END, f"Locul:  {each_event[2]}")
        upcoming_events.insert(END, f"La data {each_event[3]}")
        upcoming_events.insert(END, f"De la  {each_event[4]} pana la {each_event[6]}")
        upcoming_events.insert(END, "")

    upcoming_events.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=upcoming_events.yview)
    window.mainloop()


# keps running till the alarm goes off
def alarm(event):
    while True:
        time.sleep(1)
        current_time = datetime.now()
        alarm_time = create_datetime(event[3], event[4])
        logging.info(f'current time {current_time} <> alarm set off time {alarm_time}')
        alarm_time -= timedelta(minutes=30)
        if current_time >= alarm_time:
            winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
            alarm_pop_up(event)
            break


# validates the input
def verify_iput():
    if ".ics" in sys.argv[1]:
        logging.info("Opened a ics file!")
        return "ics"
    elif ".json" in sys.argv[1]:
        logging.info("Opened a custom json file!")
        return "json"
    else:
        logging.error("Not a ics or a json file!")
        sys.exit(-1)


# opens and reads the content of a ics file
def get_ics_content():
    temp_list = []
    try:
        file_handler = open(sys.argv[1], 'rb')
        file_cal = icalendar.Calendar.from_ical(file_handler.read())
    except ValueError:
        logging.error("An error occurred opening the file! Check the file an try again!")
        sys.exit(-1)
    for content in file_cal.walk():
        try:
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
                rrule = content.get('rrule')
                if rrule:
                    freq = rrule.__getitem__('freq')
                else:
                    freq = ""
                temp_list.append([summary, description, location, start_date, start_time, end_date, end_time, freq])
        except ValueError:
            logging.error("An error occurred while reading the content of ics file! Corrupt Data!")

    for each_alarm in temp_list:
        if ' '.join(each_alarm[7]) == 'YEARLY':
            each_alarm[3] = add_years(each_alarm[3], each_alarm[4])
            each_alarm[5] = add_years(each_alarm[5], each_alarm[4])
        elif ' '.join(each_alarm[7]) == 'MONTHLY':
            each_alarm[3] = add_months(each_alarm[3], each_alarm[4])
            each_alarm[5] = add_months(each_alarm[5], each_alarm[4])
        elif ' '.join(each_alarm[7]) == 'WEEKLY':
            each_alarm[3] = add_weeks(each_alarm[3], each_alarm[4])
            each_alarm[5] = add_weeks(each_alarm[5], each_alarm[4])
        elif ' '.join(each_alarm[7]) == 'DAILY':
            each_alarm[3] = add_days(each_alarm[3], each_alarm[4])
            each_alarm[5] = add_days(each_alarm[5], each_alarm[4])

    temp_list = sort_by_date_time(temp_list)
    file_handler.close()
    return temp_list


# opens and reads the content of a json file
def get_json_content():
    temp_list = []
    try:
        with open(sys.argv[1]) as file_handler:
            content = json.load(file_handler)
    except ValueError:
        logging.error("An error occurred opening the file! Check the file an try again!")
        sys.exit(-1)
    events = content.get('events', 0)
    for event in events:
        try:
            summary = event.get('summary')
            description = event.get('description')
            location = event.get('location')
            start_date = event.get('start_date')
            start_time = event.get('start_time')
            end_date = event.get('end_date')
            end_time = event.get('end_time')
            freq = event.get('freq')
            temp_list.append([summary, description, location, start_date, start_time, end_date, end_time, freq])
        except ValueError:
            logging.error("An error occurred while reading the content of json file! Corrupt Data!")

    for each_alarm in temp_list:
        if each_alarm[7] == 'yearly':
            each_alarm[3] = add_years(each_alarm[3], each_alarm[4])
            each_alarm[5] = add_years(each_alarm[5], each_alarm[4])
        elif each_alarm[7] == 'monthly':
            each_alarm[3] = add_months(each_alarm[3], each_alarm[4])
            each_alarm[5] = add_months(each_alarm[5], each_alarm[4])
        elif each_alarm[7] == 'weekly':
            each_alarm[3] = add_weeks(each_alarm[3], each_alarm[4])
            each_alarm[5] = add_weeks(each_alarm[5], each_alarm[4])
        elif each_alarm[7] == 'daily':
            each_alarm[3] = add_days(each_alarm[3], each_alarm[4])
            each_alarm[5] = add_days(each_alarm[5], each_alarm[4])
    temp_list = sort_by_date_time(temp_list)

    file_handler.close()
    return temp_list


# validates the alarms, regarding date and time in relation to the current date and time
def validate_date_time(events):
    current_time = datetime.now()
    tomorrow = current_time + timedelta(1)
    validated_events = []
    for event in events:
        alarm_date = create_datetime(event[3], event[4])
        if current_time <= alarm_date:
             validated_events.append(event)
        # if current_time <= alarm_date <= tomorrow:
        #     validated_events.append(event)

    return validated_events


if __name__ == "__main__":
    events_list = []
    file_type = verify_iput()
    if file_type == "ics":
        events_list = get_ics_content()
    else:
        events_list = get_json_content()

    events_list = validate_date_time(events_list)
    if not events_list:
        logging.error("There is no valid alarm to be set.")
        sys.exit(0)
    alarms_pop_up(events_list)

    for event in events_list:
        alarm(event)
        logging.info("Alarm closed!\n")

