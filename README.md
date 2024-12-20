# Rahkam - DevOps Task Documentation

## Overview

This document provides a step-by-step guide to completing the assigned DevOps tasks, covering Kubernetes cluster setup, PostgreSQL clustering, NGINX web server deployment, monitoring solutions, and ingress configurations. It ensures a reliable and scalable environment suitable for modern application deployment.

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

Run the following commands to optimize the system:

```bash
sudo sysctl fs.inotify.max_user_watches=524288
sudo sysctl fs.inotify.max_user_instances=512
```

### 1.2 Kubernetes Cluster with Kind

Create a multi-node cluster with Kind:

```bash
kind create cluster --name rahkam --config kind-cluster.yml --retain
kubectl cluster-info --context kind-rahkam
```

**Kind Configuration File**:

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
```

Verify nodes:

```bash
kubectl get nodes
```

---

## 2. PostgreSQL Setup

### 2.1 Configurations

Update `values.yaml`:

```yaml
replicaCount: 3
architecture: replication
```

### 2.2 Cluster Deployment

Create a namespace and deploy PostgreSQL using the Bitnami Helm chart:

```bash
kubectl create namespace postgresql
helm install postgresql-cluster bitnami/postgresql -n postgresql
```

### 2.3 Backup Configuration

Enable daily backups:

```yaml
backup:
  enabled: true
  cronjob:
    schedule: "@daily"
    timeZone: ""
    concurrencyPolicy: Allow
```

---

## 3. NGINX Web Server Deployment

### 3.1 Bitnami Helm Chart Setup

```bash
kubectl create namespace web-server
helm install internal bitnami/nginx -n web-server
```

### 3.2 Stub Status Configuration

Update the `serverBlock` section in `values.yaml`:

```nginx
server {
  listen 0.0.0.0:8080;
  location /stat {
    stub_status on;
  }
}
```

### 3.3 Autoscaling Configuration

Enable autoscaling in `values.yaml`:

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 4
  targetCPU: 200m
  targetMemory: 512Mi
```

---

## 4. Monitoring Setup

### 4.1 Prometheus Deployment

Deploy Prometheus:

```bash
kubectl create namespace monitoring
helm install prometheus prometheus-community/prometheus -n monitoring
```

### 4.2 Grafana Integration

Install Grafana:

```bash
helm install grafana grafana/grafana -n monitoring
```

Retrieve Grafana credentials:

```bash
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

Import dashboards:
- `K8sCluster.json`
- `NodeExporter.json`
- `APIServer.json`

### 4.3 NGINX Exporter

1. Create a Dockerfile for the NGINX exporter.
2. Push the Docker image to a repository.
3. Deploy the Helm chart for the NGINX exporter.

---

## 5. Ingress Configuration

Enable ingress in `values.yaml`:

```yaml
ingress:
  enabled: true
  selfSigned: false
  pathType: ImplementationSpecific
  apiVersion: ""
  hostname: nginx.aminiux.ir
  path: /
```

---

## File Structure

```
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
    ├── templates
    │   ├── prometheusrule.yaml
```

---

## Notes

1. Ensure all Helm charts and Docker images are accessible.
2. Follow the provided structure to maintain consistency.
3. Regularly test backups and autoscaling mechanisms.
