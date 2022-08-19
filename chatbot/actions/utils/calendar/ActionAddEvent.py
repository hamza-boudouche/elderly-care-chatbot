from cgitb import text
from datetime import datetime
import json
import math
import aiohttp
import asyncio
from dateutil import parser

CALENDAR_URL = "http://localhost:4000"
ZOOM_URL = "http://localhost:8000"


async def actionAddEvent(summary, description, start, end, withMeeting):
    messages = []
    newEvent = {}
    async with aiohttp.ClientSession() as session:
        payload = {
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
        }
        if withMeeting:
            zoom_resp = await session.post(url=f"{ZOOM_URL}/meeting/", json={
                "time": start,
                "duration": math.floor((parser.parse(end) - parser.parse(start)).total_seconds() / 60),
                "title": summary
            })
            zoom_res = await zoom_resp.json()
            payload["description"] = "meeting: " + json.dumps({
                "url": zoom_res.get("url"),
                "password": zoom_res.get("password")
            }) + "\n" + description
        async with session.post(url=f"{CALENDAR_URL}/", json=payload) as resp:
            res = await resp.json()
            newEvent = {
                "text": f"from {start} to {end} you have {description}",
                "id": res.get("id")
            }
    return messages, newEvent

# testing
if __name__ == "__main__":
    async def wrapper():
        res = await actionAddEvent("summary", "description", "2022-08-19T15:39:59.000Z", "2022-08-19T15:50:59.000Z", True)
        print(res)
    asyncio.run(wrapper())
