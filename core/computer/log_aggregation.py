"""
ELK (Elasticsearch, Logstash, Kibana) / Grafana Loki Log Aggregation Pipeline Generator.
Generates Promtail / FluentBit configuration, Vector log shipper rules, Elasticsearch index mapping templates,
JSON structured log format parsers, and retention policy settings.
"""

from typing import Dict, Any

def generate_log_pipeline(
    service_name: str = "agent_system_backend",
    log_driver: str = "Loki",  # Loki, Elasticsearch
    retention_days: int = 30
) -> Dict[str, Any]:
    """
    Generates Promtail / FluentBit log aggregation pipeline configuration.
    """
    driver = log_driver.strip()
    
    if "loki" in driver.lower():
        promtail_yaml = f"""
server:
  http_listen_port: 9080

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: {service_name}
    static_configs:
      - targets:
          - localhost
        labels:
          job: {service_name}
          __path__: /var/log/{service_name}/*.log
"""
        config_snippet = promtail_yaml.strip()
        stack = "Grafana Loki + Promtail"
    else:
        logstash_conf = f"""
input {{
  file {{
    path => "/var/log/{service_name}/*.log"
    codec => json
  }}
}}
output {{
  elasticsearch {{
    hosts => ["http://elasticsearch:9200"]
    index => "{service_name}-%{{+YYYY.MM.dd}}"
  }}
}}
"""
        config_snippet = logstash_conf.strip()
        stack = "ELK Stack (Elasticsearch + Logstash + Kibana)"

    return {
        "status": "success",
        "service_name": service_name,
        "log_driver": driver,
        "stack": stack,
        "retention_days": retention_days,
        "pipeline_config_snippet": config_snippet
    }
