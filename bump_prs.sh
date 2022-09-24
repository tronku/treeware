bump_file_path=$1
version=$2
changelogs=$3
token=$4
base_branch=$5

repoString=$(yq eval '.repos' $bump_file_path | tr -d '-' | tr -d "'" | tr -d ' ')
repoArr=($(echo "$repoString" | tr ' ' '\n'))
identifier=$(yq eval '.lib_identifier' $bump_file_path)

function createBumpPR() {
  repo=$1
  link="https://${token}@github.com/${repo}.git"

  git clone $link
  bumpBranch="bump_${identifier}_${version}"
  git checkout -b $bumpBranch

  folderName=$(echo $repo | cut -d '/' -f 2)
  cd "$folderName"
  
  gradleFiles=$(find . -type f -name "*.gradle")
  
  for file in ${gradleFiles[@]}
  do
    LIB_IDENTIFIER="$identifier = "
    LIB_IDENTIFIER_VALUE="    ${LIB_IDENTIFIER} = \"${version}\""

    libIdentifierLine=$(gawk "/$LIB_IDENTIFIER/ {print NR}" $file | head -n 1)
    echo "Last occurrence at $libIdentifierLine"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' -e "${libIdentifierLine}s/.*${LIB_IDENTIFIER}.*/${LIB_IDENTIFIER_VALUE}/" "$file"
    else
        sed -i -e "${libIdentifierLine}s/.*${LIB_IDENTIFIER}.*/${LIB_IDENTIFIER_VALUE}/" "$file"
    fi

    git add $file
  done

  title="Bump ${identifier} to ${version}"
  git commit -m "${title}"
  git push origin $bumpBranch

  pr_allow_empty="true"
  bash /createpr.sh "$token" "$bumpBranch" "$base_branch" "$pr_allow_empty" "$title" "$changelogs"

  cd ..
}

for repo in ${repoArr[@]}
do
  createBumpPR $repo
done