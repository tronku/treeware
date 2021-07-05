#!/bin/bash

token=$1
version_name=$2
changelogs=$3
assets=$4
target_commitish=$5
prerelease=$6
is_draft=$7
extra_release_note=$8

command="hub release create --message \"Release $version_name\" --message \"$changelogs\""

# Adding extra note
if [ ${#extra_release_note} != 0 ]; then
  command="$command --message \"> $extra_release_note\""
fi

echo "target - $target_commitish"
# Creating a release on default branch with tag and body
if [ ${#target_commitish} = 0 ] ; then
  target_commitish=$(curl -L -H "Authorization: Bearer $token" \
            https://api.github.com/repos/$GITHUB_REPOSITORY \
            | jq .default_branch)
  
fi
command="$command -t $target_commitish"

# if it's a draft
if [ "$is_draft" = true ] ; then
  command="$command -d"
fi

# it it's a prerelease
if [ "$prerelease" = true ] ; then
  command="$command -p"
fi

# Adding assets, if present
if [ ${#assets} != 0 ] ; then
  assets_path=""
  assets_arr=($(echo "$assets" | tr -d " " | tr "," "\n"))
  for asset in "${assets_arr[@]}"
  do
    assets_path="$assets_path -a \"$asset\""
  done
  command="$command $assets_path"
fi

echo "$command"
release_url=$(sh -c "$command $version_name")

## To extract release info like upload and release URL
upload_url=$(hub release show -f '%uA' "$version_name")
echo "::set-output name=upload_url::$upload_url"
echo "::set-output name=release_url::$release_url"