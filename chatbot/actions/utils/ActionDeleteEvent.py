from cgitb import text
import aiohttp
import asyncio

CALENDAR_URL = "http://localhost:3000"


async def actionDeleteEvent(humanIndex, events):
    index = humanIndex - 1
    messages = []
    if index >= len(events):
        messages.append(
            {
                "text": "there is no such event"
            }
        )
        return messages, events
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{CALENDAR_URL}/{events[index].get('id')}") as resp:
            res = await resp.json()
            messages.append(res.get("message"))
    events.pop(index)
    return messages, events

# testing
if __name__ == "__main__":
    async def wrapper():
        res = await actionDeleteEvent(1, [{'text': 'from 2022-08-01T20:00:00+01:00 to 2022-08-01T22:00:00+01:00 you have testing', 'id': '7tnnt3q0gb1l5e2qknvimg771d'}])
        print(res)
    asyncio.run(wrapper())
