import aiohttp
import asyncio

CALENDAR_URL = "http://localhost:3000"


async def actionEventsRange(start, end):
    events = []
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{CALENDAR_URL}/range/{start}/{end}") as resp:
            res = await resp.json()
            for event in res:
                events.append(
                    {
                        "text": f"from {event.get('start').get('dateTime')} to {event.get('end').get('dateTime')} you have {event.get('summary')}",
                        "id": event.get('id')
                    }
                )
    return events

# testing
if __name__ == "__main__":
    async def wrapper():
        res = await actionEventsRange("2022-08-01T10:00:00+01:00", "2022-08-02T10:00:00+01:00")
        print(res)
    asyncio.run(wrapper())
