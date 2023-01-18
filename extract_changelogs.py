import yaml
import re

whatsNewKey = '🌟 **Whats new** '

def beautifyChangelogs(prList, drafterPath):
    with open(drafterPath, 'r') as stream:
        try:
            categories = yaml.safe_load(stream)['categories']
            labelMap = dict()
            for category in categories:
                name = category['title']
                for label in category['labels']:
                    labelMap[label] = name
            refinedPRs = categorization(prList, labelMap)
            return mergeCategories(refinedPRs)

        except yaml.YAMLError as exception:
            raise Exception("Drafter file is not valid. Please fix and try again.")

def categorization(prList, labelMap):
    newPrDict = dict()
    for pr in prList:
        prData = pr.split('|||')
        noOfMatchedLabels = 0
        matchedLabelIndex = -1

        for i in range(1, len(prData)):
            if (prData[i] in labelMap and len(prData[i]) != 0):
                if (matchedLabelIndex == -1):
                    matchedLabelIndex = i
                    noOfMatchedLabels = noOfMatchedLabels + 1
                elif (labelMap[prData[matchedLabelIndex]] != labelMap[prData[i]]):
                    noOfMatchedLabels = noOfMatchedLabels + 1
            if (i == len(prData) - 1):
                if (noOfMatchedLabels == 1):
                    addToDict(newPrDict, labelMap[prData[matchedLabelIndex]], cleanedUpString(prData[0]))
                else:
                    addToDict(newPrDict, whatsNewKey, cleanedUpString(prData[0]))

    return newPrDict

def addToDict(dict, key, appendValue):
    if key in dict:
        dict.update({key: dict[key] + "\n" + appendValue})
    else:
        dict[key] = appendValue


def mergeCategories(refinedPRs):
    changelogs = ""
    if (whatsNewKey in refinedPRs):
        changelogs += '## ' + whatsNewKey + "\n" + refinedPRs[whatsNewKey] + "\n\n"
    for key in refinedPRs:
        if (key != whatsNewKey):
            changelogs += "## " + key + "\n" + refinedPRs[key] + "\n\n"
    return changelogs

def cleanedUpString(data):
    updatedData = re.sub('''[\'\"^\`{-~]''', '', data)
    return updatedData