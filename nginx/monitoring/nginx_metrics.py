import requests

def fetch_nginx_metrics(endpoint):
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        metrics = response.text
        return metrics
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metrics: {e}")
        return None

def parse_metrics(metrics):
    parsed = {}
    for line in metrics.splitlines():
        if line.startswith("#"):
            continue  # Skip comments
        try:
            key, value = line.split(" ", 1)
            parsed[key] = value
        except ValueError:
            continue
    return parsed

if __name__ == "__main__":
    # Replace with your Nginx exporter endpoint
    metrics_endpoint = "http://internal-nginx.web-server.svc.cluster.local:9113/metrics"
    
    raw_metrics = fetch_nginx_metrics(metrics_endpoint)
    if raw_metrics:
        parsed_metrics = parse_metrics(raw_metrics)
        
        # Example metrics to print
        keys_of_interest = [
            "nginx_http_requests_total",
            "nginx_http_request_duration_seconds_sum",
            "nginx_http_connections_active"
        ]
        
        for key in keys_of_interest:
            print(f"{key}: {parsed_metrics.get(key, 'Metric not found')}")

