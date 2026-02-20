# 📊 Observability Setup

For this project, we use the **kube-prometheus-stack** via Helm. This is the industry standard for monitoring Kubernetes.

## 📥 Installation Steps

1. **Add Helm Repo:**
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

2. **Install Prometheus & Grafana:**
   ```bash
   helm install prometheus prometheus-community/kube-prometheus-stack \
     --namespace monitoring \
     --create-namespace
   ```

## 📈 What we are monitoring:
- **Cluster Health:** CPU/Memory usage of nodes and pods.
- **Application Metrics:** Our Flask app exposes custom metrics at `/metrics`.
    - `app_requests_total`: Tracks traffic volume.
    - `app_request_latency_seconds`: Tracks performance.

## 🖼️ Grafana Dashboards
Once installed, you can access Grafana:
```bash
kubectl port-forward deployment/prometheus-grafana 3000:3000 -n monitoring
```
- **Login:** admin / prom-operator
- Use the **Kubernetes / Compute Resources / Cluster** dashboard for general health.
- Create a custom dashboard to track `app_requests_total`.
