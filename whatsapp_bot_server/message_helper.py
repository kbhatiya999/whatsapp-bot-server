import os
from types import SimpleNamespace
import aiohttp
import json
from config import config

class WhatsAppMessenger:
    def __init__(self, recipient):
        self.config = SimpleNamespace()
        self.config.version = os.getenv('', 'v18.0')
        self.config.phone_number_id = os.getenv('', '223345670853370')
        self.config.access_token = os.getenv('','EAACkxeo4HFcBO9TaRBndOSxgrAsxwUPPS73aY6klZAo3yP3KwWwvJ42BWOp6ibayUtatijVbgN5OgmVTLpHK1TABSl1UBScnUAElzHSFValgBAPtwglaXxY9cxA2M5WuoTyo0tcFGFRwZAvvThDEq9fgWYjFn1TBNUe3GZCVxSZAQORwCjj7tZC1JZA337FLNUtzlR5Ox4npIKZBChiDaAZDs')
        self.base_url = 'https://graph.facebook.com'
        self.headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self.config.access_token}"
        }
        self.recipient = recipient

    def send_message(self, data):
        url = f"{self.base_url}/{self.config.version}/{self.config.phone_number_id}/messages"
        try:
            response = requests.post(url, data=data, headers=self.headers)
            if response.status_code == 200:
                print("Status:", response.status_code)
                print("Content-type:", response.headers['content-type'])
                print("Body:", response.text)
            else:
                print(response.status_code)
                print(response.text)
        except requests.ConnectionError as e:
            print('Connection Error', str(e))
    
    def send_message_to_whatsapp(self, data, thread_ts=None, error_type=None, document_record=None, attachments=[]):
        url = f"{self.base_url}/{self.config.version}/{self.config.phone_number_id}/messages"
        try:
            response = requests.post(url, data=data, headers=self.headers)
            if response.status_code == 200:
                logger.info("Status: %s", response.status_code)
                logger.info("Content-type: %s", response.headers['content-type'])
                logger.info("Body: %s", response.text)
                # Assuming document_record has a similar structure to the Slack version
                document_record_keys = None
                if document_record:
                    document_record_keys = {
                        "context_record_PK": document_record.get("PK"),
                        "context_record_SK": document_record.get("SK"),
                    }
                current_time = time_utils.get_current_timestamp()
                current_day = current_time.split("T")[0]
                current_time_in_day = current_time.split("T")[1]
                PK = f"whatsappStream#{current_day}"
                SK = f"time#{current_time_in_day}#{self.config.phone_number_id}"
                whatsapp_document_stream_record = {
                    "PK": PK,
                    "SK": SK,
                    "error_message_type": error_type,
                    "document_record_keys": document_record_keys,
                    "email_response": response,
                }
                immutable_table_name = os.getenv("IMMUTABLE_DDB_TABLE_NAME")
                ddb.put_item(immutable_table_name, whatsapp_document_stream_record)

                return {"status": "success"}
            else:
                logger.error("Status: %s", response.status_code)
                logger.error("Body: %s", response.text)
                return {"status": "error", "reason": "Failed to send WhatsApp message"}
        except requests.ConnectionError as e:
            logger.error('Connection Error: %s', str(e))
            return {"status": "error", "reason": "Connection error while sending WhatsApp message"}

    def get_text_message_input(self, recipient=None, text='', reply_to=None):
        if not recipient:
            recipient = self.recipient
        
        data = {
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {
                "body": text
            }
        }
        if reply_to:
            data.update({
                "context": {"message_id": reply_to}
            })
        return json.dumps(data)

    def get_templated_message_input(self, recipient, flight):
        return json.dumps({
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "template",
            "template": {
                "name": "my_sample_flight_confirmation",
                "language": {
                    "code": "en_US"
                },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "document",
                                "document": {
                                    "filename": "FlightConfirmation.pdf",
                                    "link": flight['document']
                                }
                            }
                        ]
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": flight['origin']},
                            {"type": "text", "text": flight['destination']},
                            {"type": "text", "text": flight['time']}
                        ]
                    }
                ]
            }
        })

