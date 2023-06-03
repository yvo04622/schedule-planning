import datetime


def parse_time(time_str):
    time_obj = datetime.datetime.strptime(time_str, '%H:%M').time()
    return time_obj


# seperate data
def read_events_from_file(file_path):
    events = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        data = line.strip().split(',')
        name = data[0]
        start_time = parse_time(data[1])
        deadline = parse_time(data[2])

        event = {'name': name, 'start_time': start_time, 'deadline': deadline}
        events.append(event)

    return events


# read data
file_path = 'test/output.txt'
events = read_events_from_file(file_path)

# file_path = 'daily_routine.txt'
# routine = read_events_from_file(file_path)


#scheduling
def schedule_events(events):
    schedule = []
    give_up = []
    # #add daily routine to schedule first
    # for event in routine:
    #     scheduled_event = {
    #         'name': event['name'],
    #         'start_time': event['start_time'],
    #         'end_time': event['deadline']
    #     }
    #     schedule.append(scheduled_event)
    # use deadline to sort the events
    sorted_events = sorted(events, key=lambda event: event['deadline'])
    # add events to schedule
    for event in sorted_events:
        #check overlapped
        for scheduled_event in schedule:
            if scheduled_event['start_time'] <= event['start_time'] and scheduled_event[
                    'end_time'] >= event['start_time']:
                event['start_time'] = scheduled_event['end_time']
            elif scheduled_event['start_time'] <= event['deadline'] and scheduled_event[
                    'end_time'] >= event['deadline']:
                event['deadline'] = scheduled_event['start_time']
            elif scheduled_event['start_time'] > event['start_time'] and scheduled_event[
                    'end_time'] < event['deadline']:
                new_scheduled_event = {
                    'name': event['name'],
                    'start_time': event['start_time'],
                    'end_time': scheduled_event['start_time']
                }
                schedule.append(new_scheduled_event)
                event['start_time'] = scheduled_event['end_time']

        if event['start_time'] < event['deadline']:
            new_scheduled_event = {
                'name': event['name'],
                'start_time': event['start_time'],
                'end_time': event['deadline']
            }
            schedule.append(new_scheduled_event)
        else:
            give_up.append(event['name'])
        schedule = sorted(schedule, key=lambda event: event['start_time'])
    return schedule, give_up


schedule, give_up = schedule_events(events)

# Print the schedule in chronological order.
print("Today's schedule:")
schedule = sorted(schedule, key=lambda event: event['start_time'])
for event in schedule:
    print(f"{event['start_time']} - {event['end_time']} {event['name']}")

print()
print("Give up event:")
for event in give_up:
    print(event)