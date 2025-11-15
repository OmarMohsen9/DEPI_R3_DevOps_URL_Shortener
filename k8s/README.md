**URL Shortener App – Kubernetes Deployment (with Monitoring Stack)**

---

## 🧬 1. Project Overview

**Goal:** Deploy a URL shortener app (FastAPI + SQLite) on Kubernetes, with Prometheus and Grafana for monitoring.
**Image used:** `ahmedanas04/url-shortener:latest`
**Namespace:** `url-shortener`
**Storage:** Persistent Volume + Persistent Volume Claim (hostPath-based)

---

## ⚙️ 2. Components

| Component           | Description              | Port                        | Type          |
| ------------------- | ------------------------ | --------------------------- | ------------- |
| `url-shortener-app` | FastAPI app using SQLite | 9000 (app) → NodePort 30090 | App           |
| `prometheus`        | Metrics collection       | 9090 → NodePort 30091       | Monitoring    |
| `grafana`           | Dashboards & alerts      | 3000 → NodePort 30092       | Visualization |

---

## 📁 3. Kubernetes Structure

```
k8s/
├── app-deployment.yaml
├── app-service.yaml
├── pvc.yaml
├── prometheus-deployment.yaml
├── prometheus-service.yaml
├── grafana-deployment.yaml
├── grafana-service.yaml
├── prometheus-config.yaml
└── namespace.yaml
```

---

## 🚀 4. Deployment Steps

### Step 1: Create namespace

```bash
kubectl apply -f namespace.yaml
```

### Step 2: Create Persistent Volume & PVC

```bash
kubectl apply -f pvc.yaml
```

### Step 3: Deploy the app

```bash
kubectl apply -f app-deployment.yaml
kubectl apply -f app-service.yaml
```

### Step 4: Deploy Prometheus

```bash
kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f prometheus-service.yaml
```

### Step 5: Deploy Grafana

```bash
kubectl apply -f grafana-deployment.yaml
kubectl apply -f grafana-service.yaml
```

### Step 6: Verify all components

```bash
kubectl get pods -n url-shortener
kubectl get svc -n url-shortener
kubectl get pvc -n url-shortener
```

✅ Expected:

* All pods are in `Running` state
* PVC status = `Bound`
* Services expose NodePorts:

  * App → `30090`
  * Prometheus → `30091`
  * Grafana → `30092`

---

## 🌐 5. Access Points

| Service    | URL Example              |
| ---------- | ------------------------ |
| App        | `http://<NODE_IP>:30090` |
| Prometheus | `http://<NODE_IP>:30091` |
| Grafana    | `http://<NODE_IP>:30092` |

---

## 💾 6. Persistent Storage Notes

* SQLite DB path inside container: `/app/data/urls.db`
* Mounted volume (hostPath): `/data/url-shortener` on node
* PVC ensures data persists after pod restarts
