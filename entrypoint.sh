#!/bin/sh

set -eou pipefail

prod_branch=$1
drafter_path=$2
should_release=$3
is_beta=$4
beta_branch=$5
version_name=$6
assets=$7
target_commitish=$8
is_prerelease=$9
is_draft=${10}
extra_release_note=${11}
slack_workspace_id=${12}
slack_channel_id=${13}
slack_webhook_id=${14}
title_observer_section=${15}

token=$GITHUB_TOKEN
repo_name=$GITHUB_REPOSITORY

if [ ${#prod_branch} = 0 ]; then
  prod_branch=$(curl -L -H "Authorization: Bearer $token" \
            https://api.github.com/repos/$repo_name \
            | jq .default_branch | tr -d '"')
fi

branch=$prod_branch
if [ "$is_beta" = true ] ; then
  branch=$beta_branch
fi

changelogs=$(python3 /treeware_main.py "$token" "$repo_name" "$branch" "$is_beta" "$drafter_path" "$title_observer_section")
echo "$changelogs"

isSuccess=$(echo "$changelogs" | cut -d " " -f1)

if [[ "$isSuccess" == "Error" ]] ; then
  echo "Something went wrong. Please check the logs - $changelogs"
  exit 1
else
  # in order to push that in the outputs, needs some string manipulations
  content="${changelogs//'%'/'%25'}"
  content="${content//$'\n'/'%0A'}"
  content="${content//$'\r'/'%0D'}"
  echo "::set-output name=changelogs::$content"

  if [ "$should_release" = true ] ; then
    # creates a release on GitHub with the version name as tag
    bash /release.sh "$token" "$version_name" "$changelogs" "$assets" "$target_commitish" "$is_prerelease" "$is_draft" "$extra_release_note" "$is_beta"

    # communicate the changelog to the specified slack webhook
    if [[ ${#slack_workspace_id} != 0 && ${#slack_channel_id} != 0 && ${#slack_webhook_id} != 0 ]]; then
      echo "Sending message to Slack"
      bash /slack_communicator.sh "$slack_workspace_id" "$slack_channel_id" "$slack_webhook_id" "$version_name" "$title_observer_section"
    fi
  fi
fi