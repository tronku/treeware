import requests
import sys

prQuery = """
query($owner: String!, $repoName: String!, $timestamp: GitTimestamp!, $ref: String!) {
    repository(name: $repoName, owner: $owner) {
        ref(qualifiedName: $ref) {
            target {
              ... on Commit {
                history(first: 100, since: $timestamp) {
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
                        body
                        author {
                          ... on User {
                            name
                          }
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
                history(first: 100, since: $timestamp, after: $after) {
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
                        body
                        author {
                          ... on User {
                            name
                          }
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

prQueryForFirstRelease = """
query($owner: String!, $repoName: String!, $ref: String!) {
    repository(name: $repoName, owner: $owner) {
        ref(qualifiedName: $ref) {
            target {
              ... on Commit {
                history(first: 100) {
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
                        body
                        author {
                          ... on User {
                            name
                          }
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

prQueryWithPaginationForFirstRelease = """
query($owner: String!, $repoName: String!, $ref: String!, $after: String!) {
    repository(name: $repoName, owner: $owner) {
        ref(qualifiedName: $ref) {
            target {
              ... on Commit {
                history(first: 100, after: $after) {
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
                        body
                        author {
                          ... on User {
                            name
                          }
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
titleObservableSection = ''


def getPullRequests(token, repoName, branch, timestamp=None, paging=False, after="", titleSection=""):
    global titleObservableSection
    if len(titleObservableSection) == 0:
        titleObservableSection = titleSection

    prList = list()
    repoInfo = repoName.split('/')
    inputVariables = {
        "owner": repoInfo[0],
        "repoName": repoInfo[1],
        "ref": branch
    }

    if timestamp is not None:
        inputVariables["timestamp"] = timestamp
        if not paging:
            query = prQuery
        else:
            query = prQueryWithPagination
            inputVariables["after"] = after
    else:
        # for the first time releases
        if not paging:
            query = prQueryForFirstRelease
        else:
            query = prQueryWithPaginationForFirstRelease
            inputVariables["after"] = after

    try:
        headers = {"Authorization": "token " + token}
        versionRequest = requests.post(
            BASE_URL,
            json={'query': query, 'variables': inputVariables},
            headers=headers)

        if versionRequest.status_code == 200:
            response = versionRequest.json()
            prList += createList(response, titleSection)
            prList += checkForNextPR(response, token, repoName, branch, timestamp)
            return prList
        else:
            raise Exception("Query failed " + versionRequest.status_code)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as err:
        raise Exception("Network Exception " + err.response.text)


def createList(response, titleSection):
    prList = list()
    history = response['data']['repository']['ref']['target']['history']
    for commit in history['nodes']:
        for pr in commit['associatedPullRequests']['nodes']:
            if pr['number'] not in prNumbers:
                labels = getLabels(pr['labels']['nodes'])
                prList.append("- {0} @{1} [(#{2})]({3}) {4}".format(getTitle(pr, titleSection), pr['author']['name'],
                                                                    pr['number'], pr['url'], labels).replace('"', "'"))
                prNumbers.add(pr['number'])
    return prList


def getTitle(prData, titleSection):
    if len(titleSection.strip()) == 0:
        print("TITLE IS EMPTY!!!!")
        return prData['title']
    else:
        return getPullRequestSection(prData, titleSection)


def getPullRequestSection(prData, titleSection):
    body = prData['body']
    # if prData['number'] == 10400:
    #     print("\n\nPR BODY === " + str(prData['number']) + " == " + body)
    titleData = ''
    foundGivenSection = False
    for line in body.split('\n'):
        if len(line.strip()) == 0:
            continue
        if titleSection in line:
            foundGivenSection = True
        elif foundGivenSection and not line.startswith("#"):
            titleData = line.strip().replace('- ', '', 1)
            break

    if len(titleData) == 0:
        titleData = prData['title']
    return titleData


def checkForNextPR(response, token, repoName, branch, timestamp):
    history = response['data']['repository']['ref']['target']['history']
    if history['pageInfo']['hasNextPage']:
        nextCursor = history['pageInfo']['endCursor']
        return getPullRequests(token, repoName, branch, timestamp, paging=True, after=nextCursor, titleSection=titleObservableSection)
    else:
        return list()


def getLabels(labels):
    labelString = "|||"
    for label in labels:
        labelString += label['name'] + "|||"
    return labelString


if __name__ == '__main__':
    token = sys.argv[1]
    repo = sys.argv[2]
    branch = sys.argv[3]
    timestamp = sys.argv[4]

    getPullRequests(token, repo, branch, timestamp)