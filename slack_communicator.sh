workspaceId=$1
channelId=$2
webhookId=$3
version_name=$4
changelogs=$5

payload=`python3 /get_slack_message.py $version_name "$changelogs"`
echo $payload

url=https://hooks.slack.com/services/$workspaceId/$channelId/$webhookId

curl -X POST \
  "$url" \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  --data "$payload"