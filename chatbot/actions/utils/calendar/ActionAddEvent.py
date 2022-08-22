from cgitb import text
import aiohttp
import asyncio

CALENDAR_URL = "http://calendar:4000"


async def actionAddEvent(summary, description, start, end):
    messages = []
    newEvent = {}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{CALENDAR_URL}/", json={
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start,
                "timeZone": "Africa/Casablanca"
            },
            "end": {
                "dateTime": end,
                "timeZone": "Africa/Casablanca"
            }
        }) as resp:
            res = await resp.json()
            newEvent = {
                "text": f"from {start} to {end} you have {description}",
                "id": res.get("id")
            }
    return messages, newEvent

# testing
if __name__ == "__main__":
    async def wrapper():
        res = await actionAddEvent("summary", "description", "2022-08-01T15:39:59.000Z", "2022-08-01T15:50:59.000Z")
        print(res)
    asyncio.run(wrapper())
