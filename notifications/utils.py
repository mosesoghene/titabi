import requests
from .models import FCMDevice

FCM_SERVER_KEY = 'your-firebase-server-key'  # Move to env later

def send_push_notification(user, title, body, data=None):
    device = FCMDevice.objects.filter(user=user).first()
    if not device:
        return False

    payload = {
        "to": device.token,
        "notification": {
            "title": title,
            "body": body
        },
        "data": data or {}
    }

    headers = {
        "Authorization": f"key={FCM_SERVER_KEY}",
        "Content-Type": "application/json"
    }

    res = requests.post("https://fcm.googleapis.com/fcm/send", json=payload, headers=headers)
    return res.ok