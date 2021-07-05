#!/bin/sh

set -eou pipefail

token=$1
prod_branch=$2
drafter_path=$3
should_release=$4
is_beta=$5

branch=$prod_branch
if [ "$is_beta" = true ] ; then
  branch=$8
fi
changelogs=`python3 /treeware_main.py "$token" "$GITHUB_REPOSITORY" "$branch" "$is_beta" "$drafter_path"`
echo "$changelogs"

if [[ $changelogs == Error* ]] ; then
  echo "Something went wrong. Please check the logs - $changelogs"
  exit 1
else
  content="${changelogs//'%'/'%25'}"
  content="${content//$'\n'/'%0A'}"
  content="${content//$'\r'/'%0D'}"
  echo "::set-output name=changelogs::$content"

  if [ "$should_release" = true ] ; then
    version_name=$6
    assets=$7
    target_commitish=$9
    prerelease=${10}
    is_draft=${11}
    extra_release_note=${12}
    bash /release.sh "$token" "$version_name" "$changelogs" "$assets" "$target_commitish" "$prerelease" "$is_draft" "$extra_release_note"
  fi
fi