# treeware

Generates a categorized changelog and releases your prod or beta. It uses a drafter file to categorize data into labels.

## Params required
```yaml
inputs:
  token:
    description: 'GitHub token to access your repo'
    required: true

  prod_branch:
    description: 'Production branch of the repo'
    required: true
    default: 'development'
    
  drafter_path: 
    description: 'Path to the drafter file'
    required: true

  should_release:
    description: 'Should release a new version?'
    required: false
    default: 'false'
  
  version_name:
    description: 'Version name of the upcoming release'
    required: false

  has_beta:
    description: 'Do you have a beta release to handle?'
    required: false
    default: 'false'

  beta_branch:
    description: 'Beta branch of the repo for release'
    required: false

  assets:
    description: 'Path to the assets, separated by comma'
    required: false
    default: ''

  target_commitish:
    description: 'Specifies the commitish value that determines where the Git tag is created from. Can be any branch or commit SHA.'
    default: default branch of the repo

  prerelease:
    description: 'Is this a prerelease?'
    default: false
  
  is_draft:
    description: 'Is this just a draft of the release?'
    default: false

  extra_release_note:
    description: 'Extra note to add in the GitHub release notes'
    default: ''
    required: false
```

## Outputs generated
```yaml
outputs:
  changelogs:
    description: 'Categorized changelogs based on labels'
  
  upload_url:
    description: 'The upload URL to the GitHub release'

  release_url:
    description: 'The URL to the GitHub release' 
```

## Format of drafter.yml
```yaml
categories:
  - title: '🚀 **Features** '
    labels:
      - 'feature'
      - 'enhancement'
  - title: '🐛 **Bug Fixes** '
    labels:
      - 'Bug'
      - 'fix'
```

## How to use
```yaml
- name: Changelogs
  uses: tronku/treeware@master
  with:
    token: ${{ env.GITHUB_TOKEN }}
    prod_branch: development
    drafter_path: drafter.yml
```