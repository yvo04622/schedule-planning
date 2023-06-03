import datetime


def parse_time(time_str):
    time_obj = datetime.datetime.strptime(time_str, '%H:%M').time()
    return time_obj


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
    """
    for event in events:
        print(f"Event: {event['name']}")
        print(f"Start Time: {event['start_time']}")
        print(f"End Time: {event['deadline']}")
        print()
    """

    return events


file_path = 'test/output.txt'
events = read_events_from_file(file_path)
# routine = read_events_from_file('daily_routine.txt')


def schedule_events(events):
    print('------scheduling------')
    schedule = []

    # for event in routine:
    #     scheduled_event = {
    #         'name': event['name'],
    #         'start_time': event['start_time'],
    #         'end_time': event['deadline']
    #     }
    #     schedule.append(scheduled_event)

    sorted_events = sorted(events, key=lambda event: event['deadline'])
    for event in sorted_events:
        scheduled_event = {
            'name': event['name'],
            'start_time': event['start_time'],
            'end_time': event['deadline']
        }
        schedule.append(scheduled_event)
    return schedule


schedule = schedule_events(events)
schedule = sorted(schedule, key=lambda event: event['start_time'])

# 輸出結果
for event in schedule:
    print(f"Event: {event['name']}")
    print(f"Start Time: {event['start_time']}")
    print(f"End Time: {event['end_time']}")
    print()
