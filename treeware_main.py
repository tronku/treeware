import sys
from get_releases import getLastRelease
from get_pull_requests import getPullRequests
from extract_changelogs import beautifyChangelogs


def init():
    try:
        lastReleaseTimestamp = getLastRelease(token, repoName, isBeta)
        prList = getPullRequests(token, repoName, branch, lastReleaseTimestamp, titleSection=titleSection)
        changelogs = beautifyChangelogs(prList, drafterPath)
        print(changelogs)
    except Exception as err:
        print("Error - {0}".format(err.args))


if __name__ == '__main__':
    token = sys.argv[1]
    repoName = sys.argv[2]
    branch = sys.argv[3]
    if sys.argv[4] == 'true':
        isBeta = True
    else:
        isBeta = False
    drafterPath = sys.argv[5]
    titleSection = sys.argv[6]
    init()
