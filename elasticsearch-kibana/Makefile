STACK_VERSION := 7.12.1
RELEASE := elasticsearch-kibana
ELASTICSEARCH_IMAGE := docker.elastic.co/elasticsearch/elasticsearch:$(STACK_VERSION)
NAMESPACE := default
# Containerd runtime
# elastic:
# 	rm -f elastic-certificates.p12 elastic-certificate.pem elastic-certificate.crt elastic-stack-ca.p12 || true
# 	ctr image pull docker.io/library/busybox:1.31.1
#	ctr image pull docker.elastic.co/elasticsearch/elasticsearch:7.12.1
#	password=$$([ ! -z "$$ELASTIC_PASSWORD" ] && echo $$ELASTIC_PASSWORD || echo $$(ctr run --rm docker.io/library/busybox:1.31.1 v1 /bin/sh -c "< /dev/urandom tr -cd '[:alnum:]' | head -c20")) && \
# 	ctr run --cwd /app $(ELASTICSEARCH_IMAGE) elastic-helm-charts-certs /bin/sh -c " \
# 			elasticsearch-certutil ca --out /app/elastic-stack-ca.p12 --pass '' && \
# 			elasticsearch-certutil cert --name security-master --dns security-master --ca /app/elastic-stack-ca.p12 --pass '' --ca-pass '' --out /app/elastic-certificates.p12" && \
# 	mkdir /tmp/efkmount && \
# 	sudo ctr snapshot mounts /tmp/efkmount elastic-helm-charts-certs | xargs sudo && \
# 	cp /tmp/efkmount/app/elastic-certificates.p12 $$HOME/efk/  && \
# 	umount /tmp/efkmount && \
# 	rm -rf /tmp/efkmount && \
# 	ctr c rm elastic-helm-charts-certs && \
# 	openssl pkcs12 -nodes -passin pass:'' -in elastic-certificates.p12 -out elastic-certificate.pem && \
# 	openssl x509 -outform der -in elastic-certificate.pem -out elastic-certificate.crt && \
# 	kubectl create secret generic -n $(NAMESPACE) elastic-certificates --from-file=elastic-certificates.p12 && \
# 	kubectl create secret generic -n $(NAMESPACE) elastic-certificate-pem --from-file=elastic-certificate.pem && \
# 	kubectl create secret generic -n $(NAMESPACE) elastic-certificate-crt --from-file=elastic-certificate.crt && \
# 	kubectl create secret generic -n $(NAMESPACE) elastic-credentials  --from-literal=password=$$password --from-literal=username=elastic && \
# 	rm -f elastic-certificates.p12 elastic-certificate.pem elastic-certificate.crt elastic-stack-ca.p12

# kibana:
# 	encryptionkey=$$(ctr run --rm docker.io/library/busybox:1.31.1 v1 /bin/sh -c "< /dev/urandom tr -dc _A-Za-z0-9 | head -c50") && \kubectl create secret generic -n $(NAMESPACE) kibana --from-literal=encryptionkey=$$encryptionkey

# Docker runtime
elastic:
	docker rm -f elastic-helm-charts-certs || true
	rm -f elastic-certificates.p12 elastic-certificate.pem elastic-certificate.crt elastic-stack-ca.p12 || true
	password=$$([ ! -z "$$ELASTIC_PASSWORD" ] && echo $$ELASTIC_PASSWORD || echo $$(docker run --rm busybox:1.31.1 /bin/sh -c "< /dev/urandom tr -cd '[:alnum:]' | head -c20")) && \
	docker run --name elastic-helm-charts-certs -i -w /app \
		$(ELASTICSEARCH_IMAGE) \
		/bin/sh -c " \
			elasticsearch-certutil ca --out /app/elastic-stack-ca.p12 --pass '' && \
			elasticsearch-certutil cert --name security-master --dns security-master --ca /app/elastic-stack-ca.p12 --pass '' --ca-pass '' --out /app/elastic-certificates.p12" && \
	docker cp elastic-helm-charts-certs:/app/elastic-certificates.p12 ./ && \
	docker rm -f elastic-helm-charts-certs && \
	openssl pkcs12 -nodes -passin pass:'' -in elastic-certificates.p12 -out elastic-certificate.pem && \
	openssl x509 -outform der -in elastic-certificate.pem -out elastic-certificate.crt && \
	kubectl create secret generic -n $(NAMESPACE) elastic-certificates --from-file=elastic-certificates.p12 && \
	kubectl create secret generic -n $(NAMESPACE) elastic-certificate-pem --from-file=elastic-certificate.pem && \
	kubectl create secret generic -n $(NAMESPACE) elastic-certificate-crt --from-file=elastic-certificate.crt && \
	kubectl create secret generic -n $(NAMESPACE) elastic-credentials  --from-literal=password=$$password --from-literal=username=elastic && \
	rm -f elastic-certificates.p12 elastic-certificate.pem elastic-certificate.crt elastic-stack-ca.p12

kibana:
	encryptionkey=$$(docker run --rm busybox:1.31.1 /bin/sh -c "< /dev/urandom tr -dc _A-Za-z0-9 | head -c50") && \kubectl create secret generic -n $(NAMESPACE) kibana --from-literal=encryptionkey=$$encryptionkey

all: elastic kibana