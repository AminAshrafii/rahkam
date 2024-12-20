import requests


def fetch_stub_status(endpoint):
    """Fetch metrics from Nginx stub_status endpoint."""
    try:
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stub_status metrics: {e}")
        return None


def parse_stub_status(metrics):
    """Parse stub_status metrics into a Prometheus-compatible dictionary."""
    parsed = {}

    lines = metrics.splitlines()
    if len(lines) < 3:
        print("Unexpected stub_status format")
        return parsed

    # Parse active connections
    active_connections = int(lines[0].split(":")[1].strip())
    parsed["nginx_http_connections"] = active_connections

    # Parse requests (accepts, handled, requests)
    _, accepts, handled, requests = lines[2].split()
    parsed["nginx_http_requests_total"] = int(requests)

    # Parse reading, writing, and waiting
    reading, writing, waiting = [int(value.split(":")[1]) for value in lines[3].split()]
    parsed["nginx_http_request_duration_seconds"] = {
        "reading": reading,
        "writing": writing,
        "waiting": waiting,
    }

    return parsed


if __name__ == "__main__":
    # Replace with your Nginx stub_status endpoint
    metrics_endpoint = "http://internal-nginx.web-server.svc.cluster.local:8080/stat"

    raw_metrics = fetch_stub_status(metrics_endpoint)
    if raw_metrics:
        parsed_metrics = parse_stub_status(raw_metrics)

        # Print the parsed metrics
        print("nginx_http_requests_total:", parsed_metrics.get("nginx_http_requests_total"))
        print("nginx_http_connections:", parsed_metrics.get("nginx_http_connections"))
        duration = parsed_metrics.get("nginx_http_request_duration_seconds", {})
        print("nginx_http_request_duration_seconds_reading:", duration.get("reading", 0))
        print("nginx_http_request_duration_seconds_writing:", duration.get("writing", 0))
        print("nginx_http_request_duration_seconds_waiting:", duration.get("waiting", 0))
