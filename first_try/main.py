import icalendar
import sys
import time
import winsound
from datetime import datetime, timedelta, timezone
import tkinter as tk


# creates new label with a certain message text
def new_label(message):
    return tk.Label(
        text=message,
        fg="black",
        height=3,
        )


# creates a pop-up window with an alert, printing a certain description of the alarm
def create_window(description):
    window = tk.Tk()

    label_alarm = new_label("Alarm")
    label_description = new_label(description)
    label_start = new_label("Incepe in 30 minute")
    label_alarm.pack()
    label_description.pack()
    label_start.pack()

    window.mainloop()


# keps running till the alarm goes off
def alarm(set_alarm_timer, set_alarm_date):
    while True:
        time.sleep(1)
        current_time = datetime.now()
        curr_time = current_time.strftime("%H:%M:%S")
        curr_date = current_time.strftime("%d/%m/%Y")
        if curr_time == set_alarm_timer and curr_date == set_alarm_date:
            print("Time to Wake up")
            winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
            break


# sets the date and time for the alarm then calles the alarm
def actual_time(year_time, month_time, day_time, hour_time, min_time, sec_time):
    set_alarm_timer = f"{hour_time}:{min_time}:{sec_time}"
    set_alarm_date = f"{day_time}/{month_time}/{year_time}"
    alarm(set_alarm_timer, set_alarm_date)


# validates the input
def verify_iput():
    if ".ics" in sys.argv[1]:
        print("\nOpened a ics file!\n")
        temp_handler = open(sys.argv[1], 'rb')
    elif ".json" in sys.argv[1]:
        print("Opened a custom json file!")
        temp_handler = open(sys.argv[1])
    else:
        print("Not a ics or a json file!")
        sys.exit(1)
    return temp_handler


file_habdler = verify_iput()
file_cal = icalendar.Calendar.from_ical(file_habdler.read())

for component in file_cal.walk():
    if component.name == "VEVENT":
        summary = component.get('summary')
        description = component.get('description')
        location = component.get('location')
        startdt = component.get('dtstart').dt
        enddt = component.get('dtend').dt
        exdate = component.get('exdate')
        print(f"{summary}-{description}-{location}-{startdt}-{enddt}-{exdate}")
        # if component.get('rrule'):
        #     print("An alarm should be set for this events!\n")
        #     reoccur = component.get('rrule').to_ical().decode('utf-8')
        #     for item in parse_recurrences(reoccur, startdt, exdate):
        #         print(f'{item} {summary}: {description} - {location}\n')
        # else:
        #     print("There won't be an alarm for this events!\n")
        #     start_date = startdt.strftime('%D %H:%M UTC')
        #     end_date = enddt.strftime('%D %H:%M UTC')
        #     print(f'{start_date}-{end_date} {summary}: {description} - {location}\n')
file_habdler.close()
