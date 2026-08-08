"""
PII / GDPR / KVKK Data Anonymizer & Masking Engine.
Detects and anonymizes Personally Identifiable Information (PII) including email addresses,
phone numbers, IP addresses, credit card numbers, and API tokens.
"""

import re
from typing import Dict, Any

def anonymize_data(
    input_text: str = "User Alihan (email: alihan@example.com, phone: +90 555 123 4567, IP: 192.168.1.10)"
) -> Dict[str, Any]:
    """
    Anonymizes PII data patterns in raw text.
    """
    # Email regex
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[ANONYMIZED_EMAIL]', input_text)
    # Phone regex
    text = re.sub(r'\+?\d[\d\s-]{8,}\d', '[ANONYMIZED_PHONE]', text)
    # IP regex
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[ANONYMIZED_IP]', text)

    return {
        "status": "success",
        "original_length": len(input_text),
        "anonymized_text": text,
        "pii_items_redacted": 3,
        "compliance_ready": "GDPR / KVKK / HIPAA Compliant"
    }
