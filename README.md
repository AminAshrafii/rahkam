# Rahkam - DevOps Task Documentation  

## Overview  

This document provides a step-by-step guide to completing the assigned DevOps tasks, focusing on Kubernetes cluster setup, PostgreSQL clustering, NGINX web server deployment, monitoring solutions, and ingress configurations. The goal is to establish a secure, scalable, and reliable environment for modern application deployment.  

---

## Table of Contents  

1. [Cluster Creation](#1-cluster-creation)  
   - [1.1 Linux Hardening](#11-linux-hardening)  
   - [1.2 Kubernetes Cluster with Kind](#12-kubernetes-cluster-with-kind)  
2. [PostgreSQL Setup](#2-postgresql-setup)  
   - [2.1 Configurations](#21-configurations)  
   - [2.2 Cluster Deployment](#22-cluster-deployment)  
   - [2.3 Backup Configuration](#23-backup-configuration)  
3. [NGINX Web Server Deployment](#3-nginx-web-server-deployment)  
   - [3.1 Bitnami Helm Chart Setup](#31-bitnami-helm-chart-setup)  
   - [3.2 Stub Status Configuration](#32-stub-status-configuration)  
   - [3.3 Autoscaling Configuration](#33-autoscaling-configuration)  
4. [Monitoring Setup](#4-monitoring-setup)  
   - [4.1 Prometheus Deployment](#41-prometheus-deployment)  
   - [4.2 Grafana Integration](#42-grafana-integration)  
   - [4.3 NGINX Exporter](#43-nginx-exporter)  
5. [Ingress Configuration](#5-ingress-configuration)  

---

## 1. Cluster Creation  

### 1.1 Linux Hardening  

Harden the Linux environment for security and performance:  

```bash  
# Update the system  
sudo apt update && sudo apt upgrade -y  

# Set system limits for Kubernetes  
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf  
echo "fs.inotify.max_user_instances=512" | sudo tee -a /etc/sysctl.conf  
sudo sysctl -p  

# Disable swap (required for Kubernetes)  
sudo swapoff -a  
sudo sed -i '/swap/d' /etc/fstab  

# Ensure correct kernel modules are loaded  
sudo modprobe overlay  
sudo modprobe br_netfilter  

# Add required kernel settings  
cat <<EOF | sudo tee /etc/sysctl.d/kubernetes.conf  
net.bridge.bridge-nf-call-ip6tables = 1  
net.bridge.bridge-nf-call-iptables = 1  
net.ipv4.ip_forward = 1  
EOF  
sudo sysctl --system  

# Set up firewall rules  
sudo ufw allow ssh  
sudo ufw enable  
```  

### 1.2 Kubernetes Cluster with Kind  

Create a Kubernetes cluster using Kind:  

```bash  
# Install Kind if not already installed  
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64  
chmod +x ./kind  
sudo mv ./kind /usr/local/bin/kind  

# Create a multi-node Kind cluster  
kind create cluster --name rahkam --config kind-cluster.yml --retain  

# Verify cluster is running  
kubectl cluster-info --context kind-rahkam  
kubectl get nodes  
kubectl get pods -A  
```  

**Kind Cluster Configuration File**:  

```yaml  
kind: Cluster  
apiVersion: kind.x-k8s.io/v1alpha4  
nodes:  
  - role: control-plane  
  - role: control-plane  
  - role: control-plane  
  - role: worker  
  - role: worker  
  - role: worker  
networking:  
  disableDefaultCNI: false  
```  

---

## 2. PostgreSQL Setup  

### 2.1 Configurations  

Update the Helm chart configuration (`values.yaml`):  

```yaml  
replicaCount: 3  
architecture: replication  
persistence:  
  enabled: true  
  size: 10Gi  
resources:  
  requests:  
    memory: 256Mi  
    cpu: 100m  
```  

### 2.2 Cluster Deployment  

Deploy the PostgreSQL cluster:  

```bash  
# Add the Bitnami Helm repository  
helm repo add bitnami https://charts.bitnami.com/bitnami  
helm repo update  

# Create a namespace and deploy PostgreSQL  
kubectl create namespace postgresql  
helm install postgresql-cluster bitnami/postgresql -n postgresql  

# Verify deployment  
kubectl get pods -n postgresql  
kubectl get svc -n postgresql  
```  

### 2.3 Backup Configuration  

Enable daily backups using CronJobs:  

```yaml  
backup:  
  enabled: true  
  cronjob:  
    schedule: "0 3 * * *"  
    concurrencyPolicy: Replace  
  volumes:  
    - name: backup-storage  
      persistentVolumeClaim:  
        claimName: backup-pvc  
```  

---

## 3. NGINX Web Server Deployment  

### 3.1 Bitnami Helm Chart Setup  

```bash  
# Create namespace and deploy NGINX  
kubectl create namespace web-server  
helm install nginx-server bitnami/nginx -n web-server  

# Verify deployment  
kubectl get pods -n web-server  
kubectl get svc -n web-server  
```  

### 3.2 Stub Status Configuration  

Update the `values.yaml`:  

```yaml  
serverBlock: |  
  server {  
    listen 8080;  
    location /status {  
      stub_status on;  
      allow 127.0.0.1;  
      deny all;  
    }  
  }  
```  

Deploy changes:  

```bash  
helm upgrade nginx-server bitnami/nginx -n web-server -f values.yaml  
```  

### 3.3 Autoscaling Configuration  

```yaml  
autoscaling:  
  enabled: true  
  minReplicas: 2  
  maxReplicas: 5  
  targetCPU: 75  
  targetMemory: 500Mi  
```  

---

## 4. Monitoring Setup  

### 4.1 Prometheus Deployment  

```bash  
# Deploy Prometheus  
kubectl create namespace monitoring  
helm install prometheus prometheus-community/prometheus -n monitoring  

# Verify deployment  
kubectl get pods -n monitoring  
kubectl get svc -n monitoring  
```  

### 4.2 Grafana Integration  

```bash  
# Install Grafana  
helm install grafana grafana/grafana -n monitoring  

# Retrieve Grafana admin password  
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode  
```  

Import the following dashboards:  
- Kubernetes Cluster  
- Node Exporter  
- API Server  

### 4.3 NGINX Exporter  

1. Build and push the Docker image:  

```bash  
docker build -t your-repo/nginx-exporter .  
docker push your-repo/nginx-exporter  
```  

2. Deploy the exporter:  

```bash  
helm install nginx-exporter ./nginx_exporter -n monitoring  
```  

---

## 5. Ingress Configuration  

Enable ingress for NGINX:  

```yaml  
ingress:  
  enabled: true  
  hostname: nginx.rahkam.local  
  path: /  
  tls:  
    enabled: true  
    certManager: true  
```  

Deploy the ingress:  

```bash  
kubectl apply -f ingress.yaml  
```  

---

## File Structure  

```plaintext  
.  
├── CLUSTER_SETTING  
│   └── kind-cluster.yml  
├── README.md  
├── grafana  
│   ├── dashboards  
│   │   ├── K8sCluster.json  
│   │   ├── NodeExporter.json  
│   │   ├── APIServer.json  
├── nginx  
│   ├── monitoring  
│   │   ├── Dockerfile  
│   │   └── nginx_exporter  
│   │       ├── Chart.yaml  
│   │       └── values.yaml  
├── postgresql  
│   └── postgresql  
│       ├── templates  
│       │   ├── backup  
│       │   │   └── cronjob.yaml  
├── prometheus  
│   ├── templates  
│   │   ├── prometheusrule.yaml  
```  

---

## Notes  

1. Always validate configuration files before deployment.  
2. Periodically test backup restoration and autoscaling configurations.  
3. Enable role-based access control (RBAC) for added security.  

