import aiohttp
import asyncio

CALENDAR_URL = "http://localhost:4000"


async def actionDeleteEvent(humanIndex, events, event):
    id = ""
    messages = []
    index = 0
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
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{CALENDAR_URL}/{id}") as resp:
            res = await resp.json()
            messages.append(res.get("message"))
    if event is None:
        events.pop(index)
        return messages, events
    return messages, events

# testing
if __name__ == "__main__":
    async def wrapper_test1():
        res = await actionDeleteEvent(1, [{'text': 'from 2022-08-02T16:24:00+01:00 to 2022-08-02T16:35:00+01:00 you have summary', 'id': 'k0a6s6dch604bcth6vdhe6leus'}, {'text': 'from 2022-08-02T18:00:00+01:00 to 2022-08-02T19:00:00+01:00 you have some title', 'id': '0nnb9uu6f4na6bsbmmqj524jnn'}], None)
        print(res)

    async def wrapper_test2():
        res = await actionDeleteEvent(None, [{'text': 'from 2022-08-02T18:00:00+01:00 to 2022-08-02T19:00:00+01:00 you have some title', 'id': '0nnb9uu6f4na6bsbmmqj524jnn'}], {'text': 'from 2022-08-02T18:00:00+01:00 to 2022-08-02T19:00:00+01:00 you have some title', 'id': '6ib77l0poc96hkuiknjiggjc1k'})
        print(res)
    asyncio.run(wrapper_test2())
