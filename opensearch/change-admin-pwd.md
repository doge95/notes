# Change Default OpenSearch Credentials
1. Deploy the [OpenSearch chart](https://github.com/opensearch-project/helm-charts/tree/opensearch-2.3.0/charts/opensearch) with default values.
2. Exec into the pod and generate the hashed passwords.
```
plugins/opensearch-security/tools/hash.sh -p <password>
```
3. Replace the new hash value in [`internal_users.yml`](https://opensearch.org/docs/latest/security-plugin/configuration/yaml/#internal_usersyml) for `admin`.
4. Create a Secret using the `internal_users.yml` file.
```
kubectl create secret generic opensearch-internal-users --from-file=internal_users.yml
```
5. Deploy a new OpenSearch with this Secret using below values.
```
securityConfig:
  enabled: true
  path: "/usr/share/opensearch/config/opensearch-security"
  internalUsersSecret: opensearch-internal-users
  config:
    dataComplete: false
```