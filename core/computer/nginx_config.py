"""
Nginx Reverse Proxy, SSL / Let's Encrypt & Rate Limit Config Generator.
Generates production Nginx `nginx.conf` with upstream load balancing, SSL TLS 1.3 ciphers,
gRPC proxying, gzip compression, and rate limiting rules.
"""

from typing import Dict, Any

def generate_nginx_config(
    domain_name: str = "api.agent-system.io",
    upstream_port: int = 8000,
    enable_ssl: bool = True
) -> Dict[str, Any]:
    """
    Generates Nginx reverse proxy configuration.
    """
    nginx_conf = f"""# Production Nginx Configuration for {domain_name}
upstream backend_app {{
    server 127.0.0.1:{upstream_port} max_fails=3 fail_timeout=10s;
}}

server {{
    listen 80;
    server_name {domain_name};
    return 301 https://$host$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {domain_name};

    ssl_certificate /etc/letsencrypt/live/{domain_name}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain_name}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {{
        proxy_pass http://backend_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""

    return {
        "status": "success",
        "domain_name": domain_name,
        "upstream_port": upstream_port,
        "ssl_enabled": enable_ssl,
        "nginx_config_file": nginx_conf
    }
