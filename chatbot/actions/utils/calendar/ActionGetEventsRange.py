from datetime import datetime
import aiohttp
import asyncio

CALENDAR_URL = "http://calendar:4000"


async def actionEventsRange(start, end):
    if start is None:
        start = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{CALENDAR_URL}/range/{start}/{end}") as resp:
            res = await resp.json()
            for event in res:
                event["text"] = f"from {event.get('start').get('dateTime')} to {event.get('end').get('dateTime')} you have {event.get('summary')}"
            return res

# testing
if __name__ == "__main__":
    async def wrapper_test1():
        res = await actionEventsRange("2022-08-01T10:00:00+01:00", "2022-08-02T10:00:00+01:00")
        print(res)

    async def wrapper_test2():
        res = await actionEventsRange(None, "2022-08-02T21:00:00+01:00")
        print(res)
    asyncio.run(wrapper_test2())
