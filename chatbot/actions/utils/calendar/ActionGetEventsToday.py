import json
import aiohttp
import asyncio
from helper import parseDescription

CALENDAR_URL = "http://localhost:4000"


async def actionEventsToday():
    async with aiohttp.ClientSession() as session:
        async with session.get(CALENDAR_URL + "/range") as resp:
            res = await resp.json()
            for event in res:
                info = parseDescription(event["description"])
                print(info)
                event.update(**info)
                event["text"] = f"from {event.get('start').get('dateTime')} to {event.get('end').get('dateTime')} you have {event.get('summary')}"
            return res

# testing
if __name__ == "__main__":
    async def wrapper():
        res = await actionEventsToday()
        print(json.dumps(res, indent=4))
    asyncio.run(wrapper())
