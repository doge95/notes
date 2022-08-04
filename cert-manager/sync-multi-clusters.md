# Sync Certs across Kubernetes Clusters
The same wildcard certificate usually has to be present both in multiple namespaces and multiple Kubernetes clusters.

Every time [cert-manager](https://cert-manager.io/) obtains or renews a certificate, the corresponding Secret will be created or updated. 
- Use [Reflector](https://github.com/emberstack/kubernetes-reflector/tree/v6.1.47) to sync the Secret across namespaces within the same cluster
- Use [Kubed](https://github.com/kubeops/config-syncer/tree/v0.13.2) to sync the Secret [across multiple clusters](https://appscode.com/products/kubed/v0.12.0/guides/config-syncer/inter-cluster/). 

Deploy the cert-manager, Kubed and Reflector in the source cluster. 
```
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager --set installCRDs=true
```
```
helm repo add emberstack https://emberstack.github.io/helm-charts
helm repo update
helm install reflector emberstack/reflector
```
```
helm repo add appscode https://charts.appscode.com/stable/
helm repo update
helm install kubed appscode/kubed --set apiserver.useKubeapiserverFqdnForAks=false --set enableAnalytics=false
```
Set Kubed `config.kubeconfigContent` to the kubeconfig file consisting destination cluster contexts (where to sync the Secret).

Deploy Reflector in the destination cluster. 

Create cluster issuer, certificate, or ingress in the source cluster.

**Notes**: Let’s Encrypt has [rate limits](https://letsencrypt.org/docs/rate-limits/): a maximum of 300 New Orders per account per 3 hours.