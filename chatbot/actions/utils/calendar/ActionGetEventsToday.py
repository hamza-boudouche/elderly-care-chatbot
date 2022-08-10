import aiohttp
import asyncio

CALENDAR_URL = "http://localhost:3000"


async def actionEventsToday():
    async with aiohttp.ClientSession() as session:
        async with session.get(CALENDAR_URL + "/range") as resp:
            res = await resp.json()
            for event in res:
                event["text"] = f"from {event.get('start').get('dateTime')} to {event.get('end').get('dateTime')} you have {event.get('summary')}"
            return res

# testing
if __name__ == "__main__":
    async def wrapper():
        res = await actionEventsToday()
        print(res)
    asyncio.run(wrapper())
