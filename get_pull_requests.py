import requests
from extract_changelogs import beautifyChangelogs

prQuery = """
query($owner: String!, $repoName: String!, $timestamp: GitTimestamp!, $ref: String!) {
    repository(name: $repoName, owner: $owner) {
        ref(qualifiedName: $ref) {
            target {
              ... on Commit {
                history(first: 50, since: $timestamp) {
                  totalCount
                  pageInfo {
                    hasNextPage
                    endCursor
                  }  
                  nodes {
                    associatedPullRequests(first: 5) {
                      nodes {
                        title
                        number
                        url
                        author {
                          login
                        }
                        labels(first: 10) {
                          nodes {
                            name
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
        }
    }
}
"""

prQueryWithPagination = """
query($owner: String!, $repoName: String!, $timestamp: GitTimestamp!, $ref: String!, $after: String!) {
    repository(name: $repoName, owner: $owner) {
        ref(qualifiedName: $ref) {
            target {
              ... on Commit {
                history(first: 50, since: $timestamp, after: $after) {
                  totalCount
                  pageInfo {
                    hasNextPage
                    endCursor
                  }  
                  nodes {
                    associatedPullRequests(first: 5) {
                      nodes {
                        title
                        number
                        url
                        author {
                          login
                        }
                        labels(first: 10) {
                          nodes {
                            name
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
        }
    }
}
"""

BASE_URL = "https://api.github.com/graphql"
prNumbers = set()

def getPullRequests(token, repoName, timestamp, branch, paging = False, after = ""):
    prList = list()
    repoInfo = repoName.split('/')
    inputVariables = {
        "owner": repoInfo[0],
        "repoName": repoInfo[1],
        "timestamp": timestamp,
        "ref": branch
    }
    
    if (paging == True):
        query = prQueryWithPagination
        inputVariables["after"] = after
    else:
        query = prQuery

    try:
        headers = {"Authorization": "token " + token}
        versionRequest = requests.post(
            BASE_URL, 
            json = {'query': query, 'variables': inputVariables},
            headers = headers)

        if versionRequest.status_code == 200:
            response = versionRequest.json()
            prList += createList(response)
            prList += checkForNextPR(response, token, repoName, timestamp, branch)
            return prList
        else:
            raise Exception("Query failed " + versionRequest.status_code)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as err:
        raise Exception("Network Exception " + err.response.text)

def createList(response):
  prList = list()
  history = response['data']['repository']['ref']['target']['history']
  for commit in history['nodes']:
    for pr in commit['associatedPullRequests']['nodes']:
      if (pr['number'] not in prNumbers):
        labels = getLabels(pr['labels']['nodes'])
        prList.append("- {0} @{1} [(#{2})]({3}) {4}".format(pr['title'], pr['author']['login'], pr['number'], pr['url'], labels).replace('"', "'"))
        prNumbers.add(pr['number'])
  return prList

def checkForNextPR(response, token, repoName, timestamp, branch):
  history = response['data']['repository']['ref']['target']['history']
  if history['pageInfo']['hasNextPage'] == True:
      nextCursor = history['pageInfo']['endCursor']
      return getPullRequests(token, repoName, timestamp, branch, True, nextCursor)
  else:
      return list()

def getLabels(labels):
    labelString = "|||"
    for label in labels:
        labelString += label['name'] + "|||"
    return labelString
