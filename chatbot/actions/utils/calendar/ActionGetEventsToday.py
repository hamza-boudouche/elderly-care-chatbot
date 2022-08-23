import json
import aiohttp
import asyncio
from actions.utils.calendar.helper_functions import parseDescription


CALENDAR_URL = "http://calendar:4000"


async def actionEventsToday():
    async with aiohttp.ClientSession() as session:
        async with session.get(CALENDAR_URL + "/range") as resp:
            res = await resp.json()
            for event in res:
                info = parseDescription(event.get("description"))
                #print(info)
                event.update(**info)
                event["text"] = f"Vous avez : {event.get('summary')} ,De {event.get('start').get('dateTime')} à {event.get('end').get('dateTime')}"
            return res

# testing
if __name__ == "__main__":
    async def wrapper():
        res = await actionEventsToday()
        print(json.dumps(res, indent=4))
    asyncio.run(wrapper())
