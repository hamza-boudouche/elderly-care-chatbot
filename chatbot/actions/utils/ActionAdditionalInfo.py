import aiohttp
import asyncio
import xmltodict
import json

CALENDAR_URL = "http://localhost:3000"
WOLFRAM_ALPHA_APP_ID = "J937X3-JAV9UYR7QJ"


async def actionAdditionalInfo(search_query):
    messages = []
    if(search_query is None):
        return messages
    URL = f"https://api.wolframalpha.com/v2/query?input={search_query}&appid={WOLFRAM_ALPHA_APP_ID}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            res = await resp.text()
            pods = xmltodict.parse(res).get("queryresult").get("pod")
            useful_info = {}
            for pod in pods:
                subpods = pod.get("subpod")
                if type(subpods) != list:
                    subpods = [subpods]
                for subpod in subpods:
                    text = subpod.get("plaintext")
                    if text:
                        title = subpod.get("@title")
                        if title == "":
                            title = pod.get("@title")
                        if title != 'Input interpretation':
                            useful_info[title] = text
            messages = useful_info
    return messages


def parse_markdown(table):
    pass


# testing
if __name__ == "__main__":
    async def wrapper_test1():
        res = await actionAdditionalInfo("elon musk")
        print(json.dumps(res, indent=4))

    async def wrapper_test2():
        table = "full name | Elon Musk\ndate of birth | Monday, June 28, 1971 (age: 51 years)\nplace of birth | South Africa"
        res = parse_markdown(table)
        print(res)
    asyncio.run(wrapper_test2())
