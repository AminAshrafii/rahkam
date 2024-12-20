# rahkam
about interview
## 1. Creating Cluster 

### 1.1. The Linux Hardening 
sudo sysctl fs.inotify.max_user_watches=524288
sudo sysctl fs.inotify.max_user_instances=512


### 1.2. Create Cluster with kind 
 kind create cluster --name rahkam --config kind-cluster.yml --retain
 kubectl cluster-info --context kind-rahkam

````
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: control-plane
  - role: control-plane
  - role: worker
  - role: worker
  - role: worker
````



=======================================================================
  kubectl get node -->
     NAME                    STATUS   ROLES           AGE     VERSION
rahkam-control-plane    Ready    control-plane   2m49s   v1.27.3
rahkam-control-plane2   Ready    control-plane   2m18s   v1.27.3
rahkam-control-plane3   Ready    control-plane   68s     v1.27.3
rahkam-worker           Ready    <none>          54s     v1.27.3
rahkam-worker2          Ready    <none>          54s     v1.27.3
rahkam-worker3          Ready    <none>          54s     v1.27.3
=======================================================================
## 2.1. Postgresql Clustering and desired changes 
NOTE: We are using bitnami helm chart to make our work faster and made changes and thinhgs.

````
# 1. change the replica count
 replicaCount: 3
 #########
# 2. change the architucture to replication
 architecture: replication

````

### 2.1. Create Cluster and intall postgresql
kubectl create namespace postgresql
helm install postgresql-cluster . -n postgresql




kubectl create namespace web-server
helm install internal . -n web-server


kubectl create namespace monitoring
helm install prometheus . -n monitoring



=======================================================================
kubectl get pods -n monitoring
NAME                                                 READY   STATUS              RESTARTS   AGE
prometheus-alertmanager-0                            0/1     ContainerCreating   0          5s
prometheus-kube-state-metrics-6d56575bc9-trhhs       0/1     ContainerCreating   0          5s
prometheus-prometheus-node-exporter-7b7mf            0/1     Pending             0          5s
prometheus-prometheus-node-exporter-gcfks            0/1     Pending             0          5s
prometheus-prometheus-node-exporter-lmr2t            0/1     Pending             0          5s
prometheus-prometheus-node-exporter-ln2kd            0/1     Pending             0          5s
prometheus-prometheus-node-exporter-rwb6w            0/1     Pending             0          5s
prometheus-prometheus-node-exporter-rx289            0/1     Pending             0          5s
prometheus-prometheus-pushgateway-7c4665864b-mgx6f   0/1     ContainerCreating   0          5s
prometheus-server-7b496c8d6-jdxd8                    0/2     ContainerCreating   0          5s
=======================================================================





=======================================================================
GRAFANA
helm install grafana . -n monitoring 
1. Get your 'admin' user password by running:

   kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo


2. The Grafana server can be accessed via port 80 on the following DNS name from within your cluster:

   grafana.monitoring.svc.cluster.local

   Get the Grafana URL to visit by running these commands in the same shell:
     export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
     kubectl --namespace monitoring port-forward $POD_NAME 3000

3. Login with the password from step 1 and the username: admin
password: eYAJfQKvQrInJxXlCeQtdF46YBYUWHBTDlLLKs38
=======================================================================



Nginx monitoring

1- create Dockerfile to make image
2- push the image in my docker hub
(its nesseccery for the valus.yaml, cause of kuber just pull image from repository)
3- create helm chart by command:
                               helm create nginxexporter
4- config the values.yaml 
======================================================================= 
Nginx

1- helm pull bitnami/nginx ;)
2- config 
         replicacount : 2
         add this in values.yaml
            serverBlock: |-
   server {
     listen 0.0.0.0:8080;
     location /stat {

                             stub_status on;
     }

Auto scalling config in values.yaml
autoscaling:
  enabled: true
  minReplicas: "2"
  maxReplicas: "4"
  targetCPU: "200Mi"
  targetMemory: ""



