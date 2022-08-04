# Export/ Migrate Data from Elasticsearch
Use the open-source tool - [elasticsearch-dump](https://github.com/elasticsearch-dump/elasticsearch-dump/tree/v6.87.0) to export or migrate data from Elasticsearch indices. 

### Export Query Results from Elasticsearch Indices
Install the package. 
```
npm install elasticdump -g
elasticdump
```
Get the search query in JSON format and identify the indices to query from. Store the query in query.json file. 
```
{"query": {
    "bool": {
      "must": [],
      "filter": [
        {
          "bool": {
            "should": [
              {
                "match_phrase": {
                  "app": "myapp"
                }
              }
            ],
            "minimum_should_match": 1
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": "2022-07-26T06:44:52.776Z",
              "lte": "2022-07-26T07:14:52.776Z",
              "format": "strict_date_optional_time"
            }
          }
        }
      ],
      "should": [],
      "must_not": []
    }
  }
}
```
Export data from Elasticsearch to a file. 
```
# bypassing self-sign certificate errors
export NODE_TLS_REJECT_UNAUTHORIZED=0
nohup elasticdump --limit=10000 --input=https://elastic:xxxxxx@<elasticsearch-ip>:9200/<index> --output=results.json --searchBody=@query.json >/dev/null 2>&1 &
```
### Migrate Elasticsearch Indices in Kubernetes
Import the index mapping before migrating the index. Specify `--type=mapping`.
```
apiVersion: batch/v1
kind: Job
metadata:
  labels:
    app: elasticdump-mapping
  name: elasticdump-mapping
spec:
  template:
    spec:
      containers:
      - image: elasticdump/elasticsearch-dump
        name: elasticdump
        args:
        - --input=<source-es-cluster>/<index>
        - --output=<destination-es-cluster>/<index>
        - --type=mapping
        env:
        - name: NODE_TLS_REJECT_UNAUTHORIZED
          value: "0"
      restartPolicy: Never
  backoffLimit: 1
```
Migrate the index.
```
apiVersion: batch/v1
kind: Job
metadata:
  labels:
    app: elasticdump-index
  name: elasticdump-index
spec:
  template:
    spec:
      containers:
      - image: elasticdump/elasticsearch-dump
        name: elasticdump
        args:
        - --input=<source-es-cluster>/<index>
        - --output=<destination-es-cluster>/<index>
        - --limit=2000
        env:
        - name: NODE_TLS_REJECT_UNAUTHORIZED
          value: "0"
      restartPolicy: Never
  backoffLimit: 1
```
`--limit=2000` - How many objects to move in batch per operation limit is approximate for file streams (default: 100). 

Increase this setting to speed up the migration. 

However, if getting `error (413) Request Entity Too Large`, decrease this setting or increase the Elasticsearch setting `http.max_content_length` (default 100mb) to remediate. 

Check the index status.
```
# Get the index mapping
GET <index>
# Get all indices
GET _cat/indices
# Get the number of documents in an index
GET _cat/count/<index> 
```