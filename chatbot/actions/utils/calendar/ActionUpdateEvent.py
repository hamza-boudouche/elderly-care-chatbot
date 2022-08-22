import json
import aiohttp
import asyncio

CALENDAR_URL = "http://calendar:4000"


async def actionUpdateEvent(humanIndex, events, event):
    id = ""
    messages = []
    if event is not None:
        id = event.get("id")
    else:
        index = humanIndex - 1
        if index >= len(events):
            messages.append(
                {
                    "text": "there is no such event"
                }
            )
            return messages, events
        else:
            id = events[index].get('id')
            event = events[index]
    async with aiohttp.ClientSession() as session:
        async with session.put(f"{CALENDAR_URL}/{id}", json=event) as resp:
            res = await resp.json()
            messages.append(
                {
                    "text": f"the event {id} was updated"
                }
            )
    if events is None:
        return messages, event
    return messages, events

# testing
if __name__ == "__main__":
    async def wrapper_test1():
        res = await actionUpdateEvent(1, [{'kind': 'calendar#event', 'etag': '"3318872213238000"', 'id': '2ob6f24i5leoehcsf0c11a5op9', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=Mm9iNmYyNGk1bGVvZWhjc2YwYzExYTVvcDkgYm91ZG91Y2hlaGFtemEyQG0', 'created': '2022-08-02T10:28:26.000Z', 'updated': '2022-08-02T10:28:26.619Z', 'summary': 'title updated 2', 'creator': {'email': 'boudouchehamza2@gmail.com', 'self': True}, 'organizer': {'email': 'boudouchehamza2@gmail.com', 'self': True}, 'start': {'dateTime': '2022-08-02T13:45:00+01:00', 'timeZone': 'Africa/Casablanca'}, 'end': {'dateTime': '2022-08-02T18:00:00+01:00', 'timeZone': 'Africa/Casablanca'}, 'iCalUID': '2ob6f24i5leoehcsf0c11a5op9@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default', 'text': 'from 2022-08-02T13:45:00+01:00 to 2022-08-02T18:00:00+01:00 you have title'}], None)
        print(res)

    async def wrapper_test2():
        res = await actionUpdateEvent(None, [{'kind': 'calendar#event', 'etag': '"3318872765538000"', 'id': '4a5io2bnqj3a05la6v98d99hu3', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=NGE1aW8yYm5xajNhMDVsYTZ2OThkOTlodTMgYm91ZG91Y2hlaGFtemEyQG0', 'created': '2022-08-02T10:33:02.000Z', 'updated': '2022-08-02T10:33:02.769Z', 'summary': 'other updated', 'creator': {'email': 'boudouchehamza2@gmail.com', 'self': True}, 'organizer': {'email': 'boudouchehamza2@gmail.com', 'self': True}, 'start': {'dateTime': '2022-08-02T12:00:00+01:00', 'timeZone': 'Africa/Casablanca'}, 'end': {'dateTime': '2022-08-02T13:00:00+01:00', 'timeZone': 'Africa/Casablanca'}, 'iCalUID': '4a5io2bnqj3a05la6v98d99hu3@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default', 'text': 'from 2022-08-02T12:00:00+01:00 to 2022-08-02T13:00:00+01:00 you have other'}, {'kind': 'calendar#event', 'etag': '"3318872213238000"', 'id': '2ob6f24i5leoehcsf0c11a5op9', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=Mm9iNmYyNGk1bGVvZWhjc2YwYzExYTVvcDkgYm91ZG91Y2hlaGFtemEyQG0', 'created': '2022-08-02T10:28:26.000Z', 'updated': '2022-08-02T10:28:26.619Z', 'summary': 'title', 'creator': {'email': 'boudouchehamza2@gmail.com', 'self': True}, 'organizer': {'email': 'boudouchehamza2@gmail.com', 'self': True}, 'start': {'dateTime': '2022-08-02T13:45:00+01:00', 'timeZone': 'Africa/Casablanca'}, 'end': {'dateTime': '2022-08-02T18:00:00+01:00', 'timeZone': 'Africa/Casablanca'}, 'iCalUID': '2ob6f24i5leoehcsf0c11a5op9@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default', 'text': 'from 2022-08-02T13:45:00+01:00 to 2022-08-02T18:00:00+01:00 you have title'}], {'kind': 'calendar#event', 'etag': '"3318872213238000"', 'id': '2ob6f24i5leoehcsf0c11a5op9', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=Mm9iNmYyNGk1bGVvZWhjc2YwYzExYTVvcDkgYm91ZG91Y2hlaGFtemEyQG0', 'created': '2022-08-02T10:28:26.000Z', 'updated': '2022-08-02T10:28:26.619Z', 'summary': 'title 2', 'creator': {'email': 'boudouchehamza2@gmail.com', 'self': True}, 'organizer': {'email': 'boudouchehamza2@gmail.com', 'self': True}, 'start': {'dateTime': '2022-08-02T13:45:00+01:00', 'timeZone': 'Africa/Casablanca'}, 'end': {'dateTime': '2022-08-02T18:00:00+01:00', 'timeZone': 'Africa/Casablanca'}, 'iCalUID': '2ob6f24i5leoehcsf0c11a5op9@google.com', 'sequence': 0, 'reminders': {'useDefault': True}, 'eventType': 'default', 'text': 'from 2022-08-02T13:45:00+01:00 to 2022-08-02T18:00:00+01:00 you have title'})
        print(res)
    asyncio.run(wrapper_test2())
