# external-dns poc
## Create secret
Firstly, create a secret to store the AWS credentials. 
```
kubectl create secret generic externaldns-aws --from-literal=secret-access-key=<key> --from-literal=access-key-id=<id>
```
## Install external-dns
```
helm repo add external-dns https://kubernetes-sigs.github.io/external-dns/
helm repo update
helm install external-dns external-dns/external-dns -f override-values.yml
```
## Service LoadBalancer Example
For services, ExternalDNS will look for the annotation `external-dns.alpha.kubernetes.io/hostname` on the service and use the corresponding value.  

Deploy a sample Nginx service (type: `LoadBalancer`) to verify that the external-dns is working. 
```
kubectl apply -f nginx-loadbalancer.yml
```
Check external-dns pod's logs
```
kubectl logs <external-dns pod> -f
```
After roughly two minutes, the logs shows the successful creation of the DNS record. 
```
time="2022-03-11T15:15:42Z" level=info msg="Applying provider record filter for domains: [xxx xxx]"
time="2022-03-11T15:15:44Z" level=info msg="Desired change: CREATE nginx.external-dns-test.myzone A [Id: /hostedzone/xxxxxx]"
time="2022-03-11T15:15:44Z" level=info msg="Desired change: CREATE nginx.external-dns-test.myzone TXT [Id: /hostedzone/xxxxxx]"
time="2022-03-11T15:15:45Z" level=info msg="2 record(s) in zone myzone. [Id: /hostedzone/xxxxxx] were successfully updated"
```

## Traefik Ingress Example
For Traefik version >= 2.0, set `providers.kubernetesIngress.publishedService.enabled` to `true` in traefik [values.yaml](https://github.com/traefik/traefik-helm-chart/blob/v10.9.1/traefik/values.yaml#L131).
```yaml
providers:
  kubernetesIngress:
    publishedService:
      enabled: true
``` 
For ingress objects, ExternalDNS will create a DNS record based on the host specified for the ingress object. Add annotation `kubernetes.io/ingress.class: "traefik"` to the ingress objects since we are using Traefik as ingress controller.  

Deploy the ingress to verify that the external-dns is working. 
```
kubectl apply -f nginx-ingress.yml
```
## Route53 rate limit
Route53 has a 5 API requests per second per account hard quota.  
[Some ways](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md#throttling) to reduce the request rate when using external-dns.
## References
https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md  
https://github.com/kubernetes-sigs/external-dns/blob/69e0e54844ac8c2133854d5ab2a569f643786be6/docs/faq.md#which-service-and-ingress-controllers-are-supported 