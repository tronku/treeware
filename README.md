# treeware

Generates a categorized changelog and releases your prod or beta with assets. It uses a drafter file to categorize data into labels.

## List of params
```yaml
inputs:
  drafter_path: 
    description: 'Path to the drafter file'
    required: true
    default: drafter.yml

  prod_branch:
    description: 'Production branch of the repo'
    required: false
    default: default branch of the repo

  should_release:
    description: 'Should release a new version?'
    required: false
    default: 'false'
  
  version_name:
    description: 'Version name of the upcoming release'
    required: false
    default: ''

  is_beta:
    description: 'Is this a beta release?'
    required: false
    default: 'false'

  beta_branch:
    description: 'Beta branch of the repo for release'
    required: false
    default: ''

  assets:
    description: 'Path to the assets, separated by comma'
    required: false
    default: ''

  target_commitish:
    description: 'Specifies the commitish value that determines where the Git tag is created from. Can be any branch or commit SHA.'
    default: ''
    required: false

  is_prerelease:
    description: 'Is this a prerelease?'
    default: 'false'
    required: false
  
  is_draft:
    description: 'Is this just a draft of the release?'
    default: 'false'
    required: false
  
  extra_release_note:
    description: 'Extra note to add in the GitHub release notes'
    default: ''
    required: false

  slack_workspace_id:
    description: 'Slack workspace ID for communication'
    default: ''
    required: false

  slack_channel_id:
    description: 'Slack channel ID for communication'
    default: ''
    required: false

  slack_webhook_id:
    description: 'Slack webhook ID for communication'
    default: ''
    required: false

  title_observer_section:
    description: 'Section that needs to be used for title in changelogs, by default it uses PR title'
    default: ''
    required: false

  ignore_changelogs:
    description: 'To ignore changelogs and only release on Github'
    default: 'false'
    required: false
```

## List of outputs
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
Here's the default drafter:
```yaml
categories:
  - title: '🚀 **Features** '
    labels:
      - 'feature'
      - 'enhancement'
  - title: '🐛 **Bug Fixes** '
    labels:
      - 'fix'
      - 'bugfix'
      - 'bug'
  - title: '🧰 **Maintenance** '
    labels:
      - 'chore'
```

## How to use treeware?
- To get the changelogs only (on default branch and drafter)
```yaml
- name: Changelogs
  uses: tronku/treeware@master
```

- To create a release on GitHub with assets and notes
```yaml
- name: Release
  uses: tronku/treeware@master
  with:
    prod_branch: development
    should_release: true
    drafter_path: drafter.yml
    assets: path_of_asset1, path_of_asset2
    extra_release_note: your_extra_note
    version_name: your_release_version
```

- To create a beta release
```yaml
- name: Release
  uses: tronku/treeware@master
  with:
    beta_branch: development
    is_beta: true
    should_release: true
    drafter_path: drafter.yml
    assets: path_of_asset1, path_of_asset2
    extra_release_note: your_extra_note
    version_name: your_release_version
```