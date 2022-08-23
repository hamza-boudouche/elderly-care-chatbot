import json

# description is formated as follows:
# meeting:
# {"url": "https://us04web.zoom.us/j/74574059810?pwd=fTwxjgGfDQxa95CigvooBgG5rCl_UH.1", "password": "au4FiM"}
# this is the actual description


def parseDescription(description: str):
    if description == "" or description is None:
        return {
            "description": ""
        }
    lines = description.split("\n")
    if lines[0] == "meeting:":  # means that it contains a meeting
        if len(lines) < 2:  # needs the "meeting:" line and the json line at a minimum
            return {
                "description": description
            }
        meeting_data = json.loads(lines[1])
        return {
            "url": meeting_data.get("url"),
            "password": meeting_data.get("password"),
            "description": "\n".join(lines[2:])
        }
    return {
        "description": description
    }


if __name__ == "__main__":
    def test_wrapper():
        test_description = 'meeting:\n{"url": "https://us04web.zoom.us/j/74574059810?pwd=fTwxjgGfDQxa95CigvooBgG5rCl_UH.1", "password": "au4FiM"}\ndescription'
        res = parseDescription(test_description)
        print(json.dumps(res, indent=4))
    test_wrapper()
