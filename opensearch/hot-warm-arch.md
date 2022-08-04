# OpenSearch Hot-Warm Architecture & Snapshot
Set up a OpenSearch cluster using [opensearch chart](https://github.com/opensearch-project/helm-charts/tree/opensearch-2.3.0/charts/opensearch) with hot and warm data nodes.
```
data-hot:
  nodeGroup: "data-hot"
  config:
    opensearch.yml: |
      ...
      node.attr.temp: hot
      ...
data-warm:
  nodeGroup: "data-warm"
  config:
    opensearch.yml: |
      ...
      node.attr.temp: warm
      ...
```
After the cluster starts, check nodes' attributes.
```
GET /_cat/nodeattrs
test-cluster-data-warm-0 11.127.5.123  11.127.5.123  temp   warm
test-cluster-data-hot-0  11.127.5.240  11.127.5.240  temp   hot
```
To allocate indices to hot and warm data node, add an allocation action in the LSM policy.
```
"actions": [
  ...
  {
    "allocation": {
      "require": { "temp": "hot" }
    }
  }
]
```
#### References
https://opensearch.org/docs/latest/opensearch/cluster/#advanced-step-7-set-up-a-hot-warm-architecture
https://opensearch.org/docs/latest/opensearch/snapshots/snapshot-restore
https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshots.html
https://aws.amazon.com/opensearch-service/faqs/
https://opster.com/guides/elasticsearch/capacity-planning/elasticsearch-hot-warm-cold-frozen-architecture/
https://github.com/opensearch-project/helm-charts/issues/243

