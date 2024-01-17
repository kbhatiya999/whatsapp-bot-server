import os
from types import SimpleNamespace
import requests
import json
from config import config


class WhatsAppMessenger:
    def __init__(self, recipient=None):
        self.config = SimpleNamespace()
        self.config.version = os.getenv("", "v18.0")
        self.config.phone_number_id = os.getenv("", "223345670853370")
        self.config.access_token = os.getenv(
            "",
            "EAACkxeo4HFcBO5vJP7GMzQ59alG0sJtfBNmci3UF4WGlNvk69uE6ygZClcoIfTcZA3IlWKR3bgt85q14oUuIFN0VFz9pN2Bmh9gl0qjIhnc0OQLu7YQDzs27yCIAzX6LJZCZALpAf7IAhvhFrhJgYndPJ3lUwnQINHS7TqZCP6JqQShgTE0UrNEXpZCV7NSZAhYBGnkYSGv6ekJJFqy9d50",
        )
        self.base_url = "https://graph.facebook.com"
        self.headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self.config.access_token}",
        }
        self.recipient = recipient

    def send_message(self, data):
        url = f"{self.base_url}/{self.config.version}/{self.config.phone_number_id}/messages"
        try:
            response = requests.post(url, data=data, headers=self.headers)
            if response.status_code == 200:
                print("Status:", response.status_code)
                print("Content-type:", response.headers["content-type"])
                print("Body:", response.text)
            else:
                print(response.status_code)
                print(response.text)
        except requests.ConnectionError as e:
            print("Connection Error", str(e))

    def get_text_message_input(self, recipient=None, text="", reply_to=None):
        if not recipient:
            recipient = self.recipient

        data = {
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"body": text},
        }
        if reply_to:
            data.update({"context": {"message_id": reply_to}})
        return json.dumps(data)

    def get_image_message_input(self, recipient, image_link, reply_to=None):
        if not recipient:
            recipient = self.recipient
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "image",
            "image": {"link": image_link},
        }
        if reply_to:
            data.update({"context": {"message_id": reply_to}})
        return json.dumps(data)

    def get_templated_message_input(self, recipient, flight):
        return json.dumps(
            {
                "messaging_product": "whatsapp",
                "to": recipient,
                "type": "template",
                "template": {
                    "name": "my_sample_flight_confirmation",
                    "language": {"code": "en_US"},
                    "components": [
                        {
                            "type": "header",
                            "parameters": [
                                {
                                    "type": "document",
                                    "document": {
                                        "filename": "FlightConfirmation.pdf",
                                        "link": flight["document"],
                                    },
                                }
                            ],
                        },
                        {
                            "type": "body",
                            "parameters": [
                                {"type": "text", "text": flight["origin"]},
                                {"type": "text", "text": flight["destination"]},
                                {"type": "text", "text": flight["time"]},
                            ],
                        },
                    ],
                },
            }
        )

    def get_media_download_url(self, media_id):
        url = f"{self.base_url}/{self.config.version}/{media_id}?phone_number_id={self.config.phone_number_id}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                download_url = response.json().get("url")
                return download_url
            else:
                print("Error getting download URL:", response.status_code)
                return None
        except requests.ConnectionError as e:
            print("Connection Error", str(e))
            return None

    def download_media_content(self, download_url):
        try:
            response = requests.get(download_url, headers=self.headers)
            if response.status_code == 200:
                return response.content
            else:
                print("Error downloading media:", response.status_code)
                return None
        except requests.ConnectionError as e:
            print("Connection Error", str(e))
            return None
        
    def get_and_download_media(self, media_id):
        # Retrieve the download URL using the media ID
        download_url = self.get_media_download_url(media_id)
        if download_url:
            # Download the media content using the download URL
            media_content = self.download_media_content(download_url)
            if media_content:
                return media_content
            else:
                print("Failed to download media content")
                return None
        else:
            print("Failed to get media download URL")
            return None
