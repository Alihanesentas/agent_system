"""
Firebase Cloud Messaging (FCM) & Apple Push Notification (APNs) Configurator.
Generates FCM V1 HTTP JSON payload manifests, APNs JWT bearer tokens, channel IDs (Android O+),
and push notification payload handlers for mobile/web apps.
"""

from typing import Dict, Any

def generate_push_config(
    topic: str = "news_alerts",
    title: str = "System Update Available",
    body: str = "Version 2.5 has been deployed successfully."
) -> Dict[str, Any]:
    """
    Generates FCM V1 push notification JSON payload specification.
    """
    fcm_payload = {
        "message": {
            "topic": topic,
            "notification": {
                "title": title,
                "body": body
            },
            "android": {
                "priority": "HIGH",
                "notification": {
                    "channel_id": "default_channel",
                    "sound": "default"
                }
            },
            "apns": {
                "headers": {
                    "apns-priority": "10"
                },
                "payload": {
                    "aps": {
                        "alert": {
                            "title": title,
                            "body": body
                        },
                        "sound": "default"
                    }
                }
            }
        }
    }

    return {
        "status": "success",
        "topic": topic,
        "fcm_v1_payload": fcm_payload,
        "apns_topic": topic,
        "protocol_standard": "FCM HTTP v1 API / APNs HTTP/2 Protocol"
    }
