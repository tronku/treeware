# treeware

Generates a categorized changelog and releases your prod or beta. It uses a drafter file to categorize data into labels.

## Params required
```yaml
inputs:
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

  is_beta:
    description: 'Is this a beta release?'
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

  is_prerelease:
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
You can add any title or labels for the changelogs. Your drafter must follow the same format though.
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
    prod_branch: development
    drafter_path: drafter.yml
```