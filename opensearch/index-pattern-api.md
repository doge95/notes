# Create Index Pattern API
```
curl -k -X POST http://kibanaserver:<password>@<endpoint>/api/saved_objects/index-pattern/logs-* -H "osd-xsrf:true" -H "content-type:application/json" -d '
{
  "attributes": {
    "title": "logs-*",
    "timeFieldName": "@timestamp"
   }
}'
```
It seems only the default `kibanaserver` user has the access to create index pattern in OpenSearch Dashboards. `admin` user does not have this access.