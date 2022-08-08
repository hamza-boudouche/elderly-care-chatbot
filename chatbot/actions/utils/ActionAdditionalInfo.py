import aiohttp
import asyncio
import xmltodict
import json

CALENDAR_URL = "http://localhost:3000"
WOLFRAM_ALPHA_APP_ID = "J937X3-JAV9UYR7QJ"


def parse_markdown(table):
    if "|" not in table:
        return table
    if table[0] == "|":
        table = "\U00002800" + table
    rows = table.split("\n")
    max_separator = 0
    for row in rows:
        nb_separator = row.count("|")
        if nb_separator > max_separator:
            max_separator = nb_separator
    row_separator = ["|" for i in range(max_separator)]
    row_separator = ":---:" + ":---:".join(row_separator) + ":---:"
    rows.insert(1, row_separator)
    rows = "\n".join(rows)
    return rows


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
                        if title != 'Input interpretation' and title != 'Wikipedia summary':
                            useful_info[title] = text
            for key, value in useful_info.items():
                value = parse_markdown(value)
                messages.append(
                    {
                        "type": "markdown",
                        "text": f"{key}:\n{value}"
                    }
                )
    return messages


# testing
if __name__ == "__main__":
    async def wrapper_test1():
        res = await actionAdditionalInfo("elon musk")
        print(json.dumps(res, indent=4))

    async def wrapper_test2():
        table = "full name | Elon Musk\ndate of birth | Monday, June 28, 1971 (age: 51 years)\nplace of birth | South Africa"
        res = parse_markdown(table)
        print(res)

    async def wrapper_test3():
        table = "full name | Elon Musk"
        res = parse_markdown(table)
        print(res)

    async def wrapper_test4():
        table = "|full name | Elon Musk\ndate of birth | Monday, June 28, 1971 (age: 51 years)\nplace of birth | South Africa"
        res = parse_markdown(table)
        print(res)

    async def wrapper_test5():
        table = "some wikipedia paragraph"
        res = parse_markdown(table)
        print(res)
    asyncio.run(wrapper_test1())
