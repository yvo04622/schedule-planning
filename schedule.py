def schedule_events(events):
    sorted_events = sorted(events, key=lambda x: int(x.get("start_time", 0)))
    scheduled_events = []

    current_event = sorted_events[0]
    scheduled_events.append(current_event)

    for event in sorted_events[1:]:
        if event["start_time"] >= current_event["end_time"]:
            scheduled_events.append(event)
            current_event = event

    return scheduled_events


# Example usage
event1 = {"title": "Meeting 1", "start_time": 9, "end_time": 10}
event2 = {"title": "Meeting 2", "start_time": 10, "end_time": 11}
event3 = {"title": "Meeting 3", "start_time": 11, "end_time": 12}

events = [event2, event3, event1]  # List of event dictionaries

scheduled_events = schedule_events(events)
for event in scheduled_events:
    print(event)
