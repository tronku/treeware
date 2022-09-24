bump_file_path=$1
version=$2
changelogs=$3
token=$4

repoString=$(yq eval '.repos' $bump_file_path | tr -d '-' | tr -d "'" | tr -d ' ')
repoArr=($(echo "$repoString" | tr ' ' '\n'))
identifier=$(yq eval '.lib_identifier' $bump_file_path)

function createBumpPR() {
  repoInfo=$1
  repo=$(echo $repoInfo | gawk '{split($0,a,"=>"); print a[1]}')
  branch=$(echo $repoInfo | gawk '{split($0,a,"=>"); print a[2]}')

  link="https://${token}@github.com/${repo}.git"

  git clone $link
  git config --global user.name ${GITHUB_ACTOR}
  git config --global user.email ${GITHUB_ACTOR}@gmail.com

  folderName=$(echo $repo | cut -d '/' -f 2)
  cd "$folderName"

  bumpBranch="bump_${identifier}_${version}"
  git remote set-url origin "https://$GITHUB_ACTOR:$token@github.com/$repo"

  git fetch origin '+refs/heads/*:refs/heads/*' --update-head-ok

  git checkout $branch
  git checkout -b $bumpBranch
  
  gradleFiles=$(find . -type f -name "*.gradle")
  
  for file in ${gradleFiles[@]}
  do
    LIB_IDENTIFIER="$identifier ="
    version_value=$(echo $version | tr -d "[:alpha:]")
    LIB_IDENTIFIER_VALUE="    ${LIB_IDENTIFIER} '${version_value}'"

    libIdentifierLine=$(gawk "/$LIB_IDENTIFIER/ {print NR}" $file | head -n 1)

    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' -e "${libIdentifierLine}s/.*${LIB_IDENTIFIER}.*/${LIB_IDENTIFIER_VALUE}/" "$file"
    else
        sed -i -e "${libIdentifierLine}s/.*${LIB_IDENTIFIER}.*/${LIB_IDENTIFIER_VALUE}/" "$file"
    fi

    git add $file
  done

  title="Bump ${identifier} to ${version}"
  git commit -m "${title}"
  git push origin "HEAD:$bumpBranch"

  PR_ARG="$title"
  if [[ ! -z "$PR_ARG" ]]; then
    PR_ARG="-m \"$PR_ARG\""

    if [[ ! -z "$changelogs" ]]; then
      PR_ARG="$PR_ARG -m \"$changelogs\""
    fi
  fi

  export GITHUB_USER="$GITHUB_ACTOR"
  COMMAND="hub pull-request \
    -b $branch \
    -h $bumpBranch \
    $PR_ARG \
    --no-edit --push \
    || true"

  echo "$COMMAND"

  PR_URL=$(sh -c "$COMMAND")
  if [[ "$?" != "0" ]]; then
    exit 1
  fi
  cd ..
}

for repo in ${repoArr[@]}
do
  createBumpPR $repo
done