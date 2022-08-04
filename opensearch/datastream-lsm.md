# LSM Policy & Index Template for Data Stream 
Index template for data stream
```
PUT _index_template/logs-template
{
  "index_patterns": [
    "logs-*"
  ],
  "data_stream": {},
  "priority": 100
}
```
LSM policy for auto rollover. It applies to index patterns - `logs-*`. 

Data streams matching this pattern will be rollovered automatically every 1d, and then moved to `warm` state for 14d, and finally be deleted. 
```
PUT _plugins/_ism/policies/logs-policy
{
  "policy": {
    "description": "hot warm delete workflow",
    "default_state": "hot",
    "schema_version": 1,
    "states": [
      {
        "name": "hot",
        "actions": [
          {
            "rollover": {
              "min_index_age": "1d"
            }
          }
        ],
        "transitions": [
          {
            "state_name": "warm"
          }
        ]
      },
      {
        "name": "warm",
        "actions": [
          {
            "replica_count": {
              "number_of_replicas": 1
            }
          }
        ],
        "transitions": [
          {
            "state_name": "delete",
            "conditions": {
              "min_index_age": "14d"
            }
          }
        ]
      },
      {
        "name": "delete",
        "actions": [
          {
            "delete": {}
          }
        ]
      }
    ],
    "ism_template": {
      "index_patterns": ["logs-*"]
    }
  }
}
```