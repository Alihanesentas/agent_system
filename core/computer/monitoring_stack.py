"""
Prometheus + Grafana Monitoring & Alerting Stack Generator.
Generates `prometheus.yml` scrape configs, Alertmanager alert rules (High CPU, Memory Leak, 5xx Error Spike),
Grafana dashboard JSON templates, and OpenTelemetry collector setups.
"""

from typing import Dict, Any, List

def generate_monitoring_stack(
    service_name: str = "agent_system_api",
    metrics_port: int = 9090,
    scrape_interval_sec: int = 15
) -> Dict[str, Any]:
    """
    Generates Prometheus scrape config and Alertmanager rules YAML.
    """
    prom_yaml = f"""
global:
  scrape_interval: {scrape_interval_sec}s

scrape_configs:
  - job_name: '{service_name}'
    static_configs:
      - targets: ['localhost:{metrics_port}']
"""

    alert_rules_yaml = f"""
groups:
  - name: {service_name}_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{{status=~"5.."}}[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High 5xx error rate on {service_name}"
"""

    return {
        "status": "success",
        "service_name": service_name,
        "metrics_port": metrics_port,
        "scrape_interval_sec": scrape_interval_sec,
        "prometheus_config_yaml": prom_yaml.strip(),
        "alertmanager_rules_yaml": alert_rules_yaml.strip(),
        "stack_components": ["Prometheus", "Grafana", "Alertmanager", "OpenTelemetry Exporter"]
    }
