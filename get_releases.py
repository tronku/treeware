import requests
import sys

releaseQuery = """
query($owner: String!, $repoName: String!) {
    repository(name: $repoName, owner: $owner) {
        releases(first: 10, orderBy: {field: CREATED_AT, direction: DESC}) {
            nodes {
                createdAt
                tag {
                    name
                }
            }
        }
    }
}
"""

BASE_URL = "https://api.github.com/graphql"


def getLastRelease(token, repoName, isBeta = False):
    repoInfo = repoName.split('/')
    inputVariables = {
        "owner": repoInfo[0],
        "repoName": repoInfo[1]
    }

    try:
        headers = {"Authorization": "token " + token}
        versionRequest = requests.post(
            BASE_URL, 
            json = {'query': releaseQuery, 'variables': inputVariables},
            headers = headers)

        if versionRequest.status_code == 200:
            return parseResponse(versionRequest.json(), isBeta)
        else:
            raise Exception("Query failed " + versionRequest.status_code)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as err:
        raise Exception("Network Exception " + err.response.text)


def parseResponse(response, isBeta):
    nodes = response["data"]["repository"]["releases"]["nodes"]
    for node in nodes:
        tag = node["tag"]["name"]
        if (isBeta == True):
            return node["createdAt"]
        elif (tag.count('.') == 2):
            return node["createdAt"]
    return None

if __name__ == '__main__':
    token = sys.argv[1]
    repo = sys.argv[2]
    if (sys.argv[3] == 'true'):
        isBeta = True
    else:
        isBeta = False
    
    getLastRelease(token, repo, isBeta)