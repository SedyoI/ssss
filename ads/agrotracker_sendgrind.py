import requests
from flask import current_app

def send_notification_email(to_email, subject, message, is_html=False):
    # Отримуємо ключ API та адресу відправника з середовищних змінних
    sendgrid_api_key = current_app.config['SENDGRID_API_KEY']
    mail_default_sender = current_app.config['MAIL_DEFAULT_SENDER']
    
    # Перевіряємо наявність ключа API
    if not sendgrid_api_key:
        raise ValueError("SENDGRID_API_KEY is not set in environment variables")
    
    # Визначаємо тип контенту (HTML або Plain Text)
    content_type = "text/html" if is_html else "text/plain"
    
    # Формуємо запит для SendGrid API
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {sendgrid_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": subject
            }
        ],
        "from": {"email": mail_default_sender},
        "content": [
            {
                "type": content_type,
                "value": message
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 202:
        raise Exception(f"SendGrid API Error: {response.status_code}, {response.text}")
    
    return response
