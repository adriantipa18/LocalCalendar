import icalendar
import sys
import time
import winsound
from datetime import datetime, timedelta
import tkinter as tk
import json


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
def add_years(event):
    another_date = event[3].split('/')
    if len(another_date[2]) < 4:
        another_date = datetime(int('20' + another_date[2]), int(another_date[0]), int(another_date[1]))
    else:
        another_date = datetime(int(another_date[2]), int(another_date[0]), int(another_date[1]))
    curr_date = datetime.now()

    while curr_date.year > another_date.year and curr_date.month > another_date.day and curr_date.day > another_date.day:
        if check_leap_year(another_date.year):
            another_date += timedelta(366)
        else:
            another_date += timedelta(365)

    if curr_date.year == another_date.year:
        if curr_date.month > another_date.day:
            if check_leap_year(another_date.year):
                another_date += timedelta(366)
            else:
                another_date += timedelta(365)
        elif curr_date.month == another_date.month:
            if curr_date.day > another_date.day:
                if check_leap_year(another_date.year):
                    another_date += timedelta(366)
                else:
                    another_date += timedelta(365)

    return another_date.strftime("%m/%d/%Y")


# add months to a date, returns the next set alarm
def add_months(event):
    another_date = event[3].split('/')
    if len(another_date[2]) < 4:
        another_date = datetime(int('20' + another_date[2]), int(another_date[0]), int(another_date[1]))
    else:
        another_date = datetime(int(another_date[2]), int(another_date[0]), int(another_date[1]))
    curr_date = datetime.now()

    while curr_date.year != another_date.year:
        if check_leap_year(another_date.year):
            another_date += timedelta(366)
        else:
            another_date += timedelta(365)

    while curr_date.month > another_date.month:
        if another_date.month == 1 or another_date.month == 3 or another_date.month == 5 or another_date.month == 7 or another_date.month == 8 or another_date.month == 10 or another_date.month == 12:
            another_date += timedelta(31)
        elif another_date.month == 2:
            if check_leap_year(another_date.year):
                another_date += timedelta(29)
            else:
                another_date += timedelta(28)
        else:
            another_date += timedelta(30)

    if curr_date.day > another_date.day:
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


def add_weeks(event):
    another_date = event[3].split('/')
    if len(another_date[2]) < 4:
        another_date = datetime(int('20' + another_date[2]), int(another_date[0]), int(another_date[1]))
    else:
        another_date = datetime(int(another_date[2]), int(another_date[0]), int(another_date[1]))
    curr_date = datetime.now()
    split_time = event[4].split(':')
    split_time[0] = int(split_time[0])
    split_time[1] = int(split_time[1])

    while curr_date.month > another_date.month:
        another_date += timedelta(7)

    while curr_date.day > another_date.day:
        another_date += timedelta(7)

    if curr_date.day == another_date.day:
        if curr_date.hour > int(split_time[0]):
            another_date += timedelta(7)
        elif int(split_time[0]) == curr_date.hour:
            if curr_date.minute >= int(split_time[1]):
                another_date += timedelta(7)

    return another_date.strftime("%m/%d/%Y")


# add days to a date, returns the next set alarm
def add_days(event):
    another_date = event[3].split('/')
    if len(another_date[2]) < 4:
        another_date = datetime(int('20' + another_date[2]), int(another_date[0]), int(another_date[1]))
    else:
        another_date = datetime(int(another_date[2]), int(another_date[0]), int(another_date[1]))
    curr_date = datetime.now()
    split_time = event[4].split(':')
    split_time[0] = int(split_time[0])
    split_time[1] = int(split_time[1])

    while curr_date.day > another_date.day:
        another_date += timedelta(1)

    if curr_date.hour > int(split_time[0]):
        another_date += timedelta(1)
    elif int(split_time[0]) == curr_date.hour:
        if curr_date.minute >= int(split_time[1]):
            another_date += timedelta(1)

    return another_date.strftime("%m/%d/%Y")


# sort the alarm list by date and time
def sort_by_date_time(events_list):
    for i in range(0, len(events_list) - 1):
        split_date1 = events_list[i][3].split('/')
        split_time1 = events_list[i][4].split(':')
        if len(split_date1[2]) < 4:
            d1 = datetime(int('20' + split_date1[2]), int(split_date1[0]), int(split_date1[1]), int(split_time1[0]),
                          int(split_time1[1]))
        else:
            d1 = datetime(int(split_date1[2]), int(split_date1[0]), int(split_date1[1]), int(split_time1[0]),
                          int(split_time1[1]))

        for j in range(i + 1, len(events_list)):
            split_date2 = events_list[j][3].split('/')
            split_time2 = events_list[j][4].split(':')
            if len(split_date2[2]) < 4:
                d2 = datetime(int('20' + split_date2[2]), int(split_date2[0]), int(split_date2[1]), int(split_time2[0]),
                              int(split_time2[1]))
            else:
                d2 = datetime(int(split_date2[2]), int(split_date2[0]), int(split_date2[1]), int(split_time2[0]),
                              int(split_time2[1]))
            if d1 > d2:
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


def error_pop_up(err_message):
    window = tk.Tk()

    label_error = tk.Label(
        text=err_message,
        fg="black",
        height=5,
    )

    label_error.pack()

    window.mainloop()


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
        curr_date = current_time.strftime("%m/%d/%Y")
        # check date and time to be the same *error TO DELETE
        # print(f"comparam timpul curent: {curr_time} cu {event[4]} si data curenta {curr_date} cu {event[3]}")
        if curr_time == event[4] and curr_date == event[3]:
            winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
            alarm_pop_up(event)
            break


# validates the input
def verify_iput():
    if ".ics" in sys.argv[1]:
        print("\nOpened a ics file!")
        return "ics"
    elif ".json" in sys.argv[1]:
        print("\nOpened a custom json file!")
        return "json"
    else:
        print("\nNot a ics or a json file!")
        sys.exit(1)


# opens and reads the content of a ics file
def get_ics_content():
    temp_list = []
    try:
        file_handler = open(sys.argv[1], 'rb')
        file_cal = icalendar.Calendar.from_ical(file_handler.read())
    except:
        error_pop_up("An error ocured opening the file!\n Check the file an try again!")
        sys.exit(-1)
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

    temp_list = sort_by_date_time(temp_list)
    file_handler.close()
    return temp_list


# opens and reads the content of a json file
def get_json_content():
    temp_list = []
    try:
        with open(sys.argv[1]) as file_handler:
            content = json.load(file_handler)
    except:
        error_pop_up("An error ocured opening the file!\n Check the file an try again!")
        sys.exit(-1)
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

    temp_list = sort_by_date_time(temp_list)

    file_handler.close()
    return temp_list


# validates the alarms, regarding date and time in relation to the current date and time
def validate_date_time(events):
    current_time = datetime.now()
    curr_time = current_time.strftime("%H:%M")
    validated_events = []
    for event in events:
        split_date = event[3].split('/')
        if len(split_date[2]) < 4:
            date = datetime(int('20' + split_date[2]), int(split_date[0]), int(split_date[1]))
        else:
            date = datetime(int(split_date[2]), int(split_date[0]), int(split_date[1]))
        if date.year == datetime.now().year and date.month == datetime.now().month and date.day >= datetime.now().day:
            if date == datetime.now() and event[4] >= curr_time:
                validated_events.append(event)
            else:
                print("validated ", event)
                validated_events.append(event)
    return validated_events


if __name__ == "__main__":
    # date = datetime.now()
    # print(date.hour)
    # temp_event = [0, 0, 0, "12/10/2020", "12:00", "14:58", 0]
    # print(add_years(temp_event))
    # print(add_months(temp_event))
    # print(add_days(temp_event))
    # print(add_weeks(temp_event))
    events_list = []
    file_type = verify_iput()
    if file_type == "ics":
        events_list = get_ics_content()
    else:
        events_list = get_json_content()

    # print(events_list)
    events_list = validate_date_time(events_list)

    if not events_list:
        error_pop_up("There is not a valid alarm to be set.")
        sys.exit(0)
    alarms_pop_up(events_list)

    for event in events_list:
        alarm(event)
        print("end of event\n")
    # TO DO
    # logs for succes or failure
    # validate logistics, regarding start_date < end_date and start_time < end_time
    # exceptions for when the input is corrupted
