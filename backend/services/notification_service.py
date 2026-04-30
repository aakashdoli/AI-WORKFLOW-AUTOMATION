import requests
import os
from app.utils.logger import logger

class NotificationService:
    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send_slack_alert(self, message: str, level: str = "INFO"):
        if not self.webhook_url:
            logger.warning("SLACK_WEBHOOK_URL not configured. Skipping notification.")
            return

        color = "#36a64f" if level == "INFO" else "#eb4034"
        payload = {
            "attachments": [
                {
                    "fallback": f"AI Ops Alert: {message}",
                    "color": color,
                    "title": f"AI Ops Alert - {level}",
                    "text": message,
                    "footer": "AI Workflow Automation Platform"
                }
            ]
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            logger.info("Slack notification sent successfully")
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")
