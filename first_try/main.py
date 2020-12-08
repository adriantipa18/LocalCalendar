import icalendar
import sys



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
