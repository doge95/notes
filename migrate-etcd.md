# Migrate ETCD
### Add a new member
```
ETCD_INITIAL_CLUSTER_STATE: "existing"
```
Exec into any existing ETCD container; Run below commands to add a new ETCD member.
```
(etcd)[etcd@server-1 /]$ export ETCDCTL_API=3
(etcd)[etcd@server-1 /]$ export endpoints="<server-1-ip>:2383,<server-2-ip>:2383,<server-3-ip>:2383"
(etcd)[etcd@server-1 /]$ etcdctl member list --endpoints $endpoints -wtable
+------------------+---------+---------------------------+---------------------------+---------------------------+
|        ID        | STATUS  |           NAME            |        PEER ADDRS         |       CLIENT ADDRS        |
+------------------+---------+---------------------------+---------------------------+---------------------------+
| 3aa526941a9cadfb | started | server-2                  | http://<server-2-ip>:2383 | http://<server-2-ip>:2382 |
| 4419311d90ebec75 | started | server-1                  | http://<server-1-ip>:2383 | http://<server-1-ip>:2382 |
| fc8d81dba83ac0bd | started | server-3                  | http://<server-3-ip>:2383 | http://<server-3-ip>:2382 |
+------------------+---------+---------------------------+---------------------------+---------------------------+
(etcd)[etcd@server-1 /]$ etcdctl --endpoints $endpoints member add server-4 --peer-urls=http://<server-4-ip>:2383
Member 46adcd3e339c9926 added to cluster 53a5401a06848a73

ETCD_NAME="server-4"
ETCD_INITIAL_CLUSTER="server-2=http://<server-2-ip>:2383,server-1=http://<server-1-ip>:2383,server-4=http://<server-4-ip>:2383,server-3=http://<server-3-ip>:2383"
ETCD_INITIAL_CLUSTER_STATE="existing"
(etcd)[etcd@server-1 /]$ etcdctl member list --endpoints $endpoints -wtable
+------------------+-----------+---------------------------+---------------------------+---------------------------+
|        ID        |  STATUS   |           NAME            |        PEER ADDRS         |       CLIENT ADDRS        |
+------------------+-----------+---------------------------+---------------------------+---------------------------+
| 3aa526941a9cadfb |   started | server-2                  | http://<server-2-ip>:2383 | http://<server-2-ip>:2382 |
| 4419311d90ebec75 |   started | server-1                  | http://<server-1-ip>:2383 | http://<server-1-ip>:2382 |
| 46adcd3e339c9926 | unstarted |                           | http://<server-4-ip>:2383 |                           |
| fc8d81dba83ac0bd |   started | server-3                  | http://<server-3-ip>:2383 | http://<server-3-ip>:2382 |
+------------------+-----------+---------------------------+---------------------------+---------------------------+
```
New ETCD member has to be added one by one.
### Remove a member
Exec into any ETCD container; Run below commands to remove the ETCD member running on `server-3` using its **ID** - `fc8d81dba83ac0bd`.
```
(etcd)[etcd@server-1 /]$ export endpoints="<server-1-ip>:2383"
(etcd)[etcd@server-1 /]$ export ETCDCTL_API=3
(etcd)[etcd@server-1 /]$ etcdctl member list --endpoints $endpoints -wtable
+------------------+---------+---------------------------+---------------------------+---------------------------+
|        ID        | STATUS  |           NAME            |        PEER ADDRS         |       CLIENT ADDRS        |
+------------------+---------+---------------------------+---------------------------+---------------------------+
| 3aa526941a9cadfb | started | server-2                  | http://<server-2-ip>:2383 | http://<server-2-ip>:2382 |
| 4419311d90ebec75 | started | server-1                  | http://<server-1-ip>:2383 | http://<server-1-ip>:2382 |
| 46adcd3e339c9926 | started | server-4                  | http://<server-4-ip>:2383 | http://<server-4-ip>:2382 |
| fc8d81dba83ac0bd | started | server-3                  | http://<server-3-ip>:2383 | http://<server-3-ip>:2382 |
+------------------+---------+---------------------------+---------------------------+---------------------------+
(etcd)[etcd@server-1 /]$ etcdctl --endpoints $endpoints member remove fc8d81dba83ac0bd
Member fc8d81dba83ac0bd removed from cluster 53a5401a06848a73
(etcd)[etcd@server-1 /]$ etcdctl member list --endpoints $endpoints -wtable
+------------------+---------+---------------------------+---------------------------+---------------------------+
|        ID        | STATUS  |           NAME            |        PEER ADDRS         |       CLIENT ADDRS        |
+------------------+---------+---------------------------+---------------------------+---------------------------+
| 3aa526941a9cadfb | started | server-2                  | http://<server-2-ip>:2383 | http://<server-2-ip>:2382 |
| 4419311d90ebec75 | started | server-1                  | http://<server-1-ip>:2383 | http://<server-1-ip>:2382 |
| 46adcd3e339c9926 | started | server-4                  | http://<server-4-ip>:2383 | http://<server-4-ip>:2382 |
+------------------+---------+---------------------------+---------------------------+---------------------------+
```
### Useful commands to check cluster status
```
# Check current members
etcdctl member list --endpoints $endpoints -wtable
 
# Check endpoints' status
etcdctl endpoint status --endpoints $endpoints -wtable
 
# Check endpoints' health
etcdctl endpoint status --endpoints $endpoints -wtable
```