import sys
import json


# For JSON related to Release workflow
def getReleaseJson():
    version_name = sys.argv[1]
    changelogs = sys.argv[2]
    changelogs = getRefinedChangelogs(changelogs)

    content_dict = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Published a new " + getReleaseType(version_name)
                }
            },
            getDivider()
        ]
    }

    for log in changelogs:
        content_dict["blocks"].append(log)

    print(json.dumps(content_dict))


def getDivider():
    return {"type": "divider"}


def getTitleDict(title, subtitle="", list=""):
    title_dict = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title
                }
            }
        ]
    }

    if len(subtitle) != 0:
        title_dict['blocks'].append(newSection(subtitle.strip()))
    if len(list) != 0:
        title_dict['blocks'].append(getDivider())
        title_dict['blocks'].append(listToBulletPoints(list))
    return title_dict


# To check if prod or beta release
def getReleaseType(versionName):
    if versionName.count('.') == 2:
        return "release - " + versionName
    else:
        return "beta - " + versionName


# To format changelogs
def getRefinedChangelogs(changelogs):
    relevantLogs = list()
    headingSections = changelogs.strip().split("##")

    for section in headingSections:
        if len(section.strip()) == 0:
            continue
        heading = section.strip().split("\n", 1)
        if len(heading[0]) != 0 and len(heading[1]) != 0:
            headingText = newSection(heading[0].strip().replace("*", ""), True)
            formattedText = listToBulletPoints(heading[1].strip())
            relevantLogs.append(headingText)
            relevantLogs.append(formattedText)
    return relevantLogs


def listToBulletPoints(dataList):
    formattedDataList = list()
    for data in dataList.split("\n"):
        data = data.strip()
        if data.startswith("- "):
            pos = data.rfind("#")
            prLink = data[data.rfind("https://"):len(data) - 1]
            prNum = prLink[prLink.rfind("/") + 1:]
            prInfo = data[2:pos - 2]

            formattedDataList.append(
                {
                    "type": "rich_text_section",
                    "elements": [
                        {
                            "type": "text",
                            "text": prInfo
                        },
                        {
                            "type": "link",
                            "text": "(#{0})".format(prNum),
                            "url": prLink
                        }
                    ]
                })

    return getBullets(formattedDataList)


def getBullets(dataList):
    bullets = {
        "type": "rich_text",
        "elements": [
            {
                "type": "rich_text_list",
                "elements": dataList,
                "style": "bullet",
                "indent": 1
            }
        ]
    }
    return bullets


def newSection(text, isBold=False, isItalics=False):
    if isBold:
        text = "*{0}*".format(text)

    if isItalics:
        text = "_{0}_".format(text)

    section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "{0}".format(text)
        }
    }
    return section


if __name__ == '__main__':
    getReleaseJson()
